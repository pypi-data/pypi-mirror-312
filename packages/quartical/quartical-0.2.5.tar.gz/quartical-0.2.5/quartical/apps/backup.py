import argparse
from math import prod, ceil
from quartical.data_handling.selection import filter_xds_list
from daskms import xds_from_storage_ms, xds_to_storage_table
from daskms.experimental.zarr import xds_to_zarr, xds_from_zarr
from daskms.fsspec_store import DaskMSStore
import time
import dask


def backup():
    parser = argparse.ArgumentParser(
        description='Backup any Measurement Set column to zarr. Backups will '
                    'be labelled using a combination of the passed in label '
                    '(defaults to datetime), the Measurement Set name and '
                    'the column name.'
    )

    parser.add_argument(
        'ms_path',
        type=DaskMSStore,
        help='Path to input measurement set, e.g. path/to/dir/foo.MS. Also '
             'accepts valid s3 urls.'
    )
    parser.add_argument(
        'zarr_dir',
        type=DaskMSStore,
        help='Path to desired backup location. Note that this only allows '
             'the user to specify a directory and not the name of the backup '
             'zarr that will be created, e.g. path/to/dir. Also '
             'accepts valid s3 urls.'
    )
    parser.add_argument(
        'column_name',
        type=str,
        help='Name of column to be backed up.'
    )
    parser.add_argument(
        '--label',
        type=str,
        help='An explicit label to include in the backup name. Defaults to '
             'datetime at which the backup was created. Full name will be '
             'given by [label]-[msname]-[column].bkp.qc.'
    )
    parser.add_argument(
        '--nthread',
        type=int,
        default=1,
        help='Number of threads to use.'
    )
    parser.add_argument(
        '--field-id',
        type=int,
        help='Field ID to back up.'
    )

    args = parser.parse_args()

    ms_name = args.ms_path.full_path.rsplit("/", 1)[1]
    column_name = args.column_name

    if args.label:
        label = args.label
    else:
        label = time.strftime("%Y%m%d-%H%M%S")

    # This call exists purely to get the relevant shape and dtype info.
    data_xds_list = xds_from_storage_ms(
        args.ms_path,
        columns=column_name,
        index_cols=("TIME",),
        group_cols=("FIELD_ID", "DATA_DESC_ID", "SCAN_NUMBER"),
    )

    # Use existing functionality. TODO: Improve and expose DDID selection.
    xdso = filter_xds_list(data_xds_list, args.field_id)

    # Compute appropriate chunks (256MB by default) to keep zarr happy.
    chunks = [chunk_by_size(xds[column_name]) for xds in xdso]

    # Repeat of above call but now with correct chunking information.
    data_xds_list = xds_from_storage_ms(
        args.ms_path,
        columns=column_name,
        index_cols=("TIME",),
        group_cols=("FIELD_ID", "DATA_DESC_ID", "SCAN_NUMBER"),
        chunks=chunks
    )

    # Use existing functionality. TODO: Improve and expose DDID selection.
    xdso = filter_xds_list(data_xds_list, args.field_id)

    bkp_xds_list = xds_to_zarr(
        xdso,
        f"{args.zarr_dir.url}::{label}-{ms_name}-{column_name}.bkp.qc",
    )

    dask.compute(bkp_xds_list, num_workers=args.nthread)


def restore():
    parser = argparse.ArgumentParser(
        description='Restore a zarr column backup to a Measurement Set.'
    )

    parser.add_argument(
        'zarr_path',
        type=DaskMSStore,
        help='Path to backup zarr column e.g. '
             'path/to/dir/20211201-154457-foo.MS-FLAG.bkp.qc. '
             'Also accepts valid s3 urls.'
    )
    parser.add_argument(
        'ms_path',
        type=DaskMSStore,
        help='Path to measurement set, e.g. path/to/dir/foo.MS. '
             'Also accepts valid s3 urls.'
    )
    parser.add_argument(
        'column_name',
        type=str,
        help='Name of column to populate using the backup. Note that this '
             'does not have to be the same column as was used to create the '
             'backup.'
    )
    parser.add_argument(
        '--nthread',
        type=int,
        default=1,
        help='Number of threads to use.'
    )

    args = parser.parse_args()

    zarr_root, zarr_name = args.zarr_path.url.rsplit("/", 1)

    zarr_xds_list = xds_from_zarr(f"{zarr_root}::{zarr_name}")
    backup_column_name = list(zarr_xds_list[0].data_vars.keys()).pop()

    # This will fail if the column does not exist but if we allow all columns
    # we need to select out the relevant dims for rechunking below
    ms_xds_list = xds_from_storage_ms(
        args.ms_path,
        columns=(args.column_name,),
        index_cols=("TIME",),
        group_cols=("FIELD_ID", "DATA_DESC_ID", "SCAN_NUMBER"),
    )

    for i, (ds, dsr) in enumerate(zip(ms_xds_list, zarr_xds_list)):
        dsr = dsr.chunk(ds.chunks)
        data_array = getattr(dsr, backup_column_name)
        ms_xds_list[i] = ds.assign(
            {args.column_name: (data_array.dims, data_array.data)}
        )

    restored_xds_list = xds_to_storage_table(
        ms_xds_list,
        args.ms_path,
        columns=(args.column_name,),
        rechunk=True
    )

    dask.compute(restored_xds_list, num_workers=args.nthread)


def chunk_by_size(data_array, nbytes=256*1e6):
    """Compute chunking for a specific chunk size in bytes.

    Args:
        data_array: An xarray.DataArray object.
        nbytes: An interger number of bytes describing the chunk size.

    Returns:
        chunks: A dict containing chunking consistent with nbytes.
    """

    assert data_array.dims[0] == 'row', (
        "chunk_by_size expects first dimension of DataArray to be 'row'."
    )

    dtype = data_array.dtype
    dtype_nbytes = dtype.itemsize
    shape = data_array.shape

    row_nbytes = dtype_nbytes * prod(shape[1:])

    optimal_nrow = ceil(nbytes / row_nbytes)

    chunks = {k: -1 for k in data_array.dims}
    chunks['row'] = optimal_nrow

    return chunks
