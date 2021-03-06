__author__ = 'jwely'
__all__ = ["_extract_HDF_datatype"]

from _extract_HDF_layer_data import *
from _gdal_dataset_to_tif import *

from dnppy import core
import os


def _extract_HDF_datatype(hdf, layer_indexs, outdir = None, datatype = None,
                             force_custom = False, nodata_value = None):
    """
    This function wraps "_extract_HDF_layer_data" and "_gdal_dataset_to_tif"
    It only works for datatypes listed in the datatype_library.csv

    :param hdf:             a single hdf filepath
    :param layer_indexs:    list of int index values of layers to extract
    :param outdir:          filepath to output directory to place tifs. If left
                            as "None" output geotiffs will be placed right next to
                            input HDF.
    :param datatype:        a dnppy.convert.datatype object created from an
                            entry in the datatype_library.csv
    :param force_custom:    if True, this will force the data to take on the
                            projection and geotransform attributes from
                            the datatype object, even if valid projection
                            and geotransform info can be pulled from the gdal
                            dataset. Should almost never be True.
    :param nodata_value:    the value to set to Nodata

    :return:                list of filepaths to output files
    """

    output_filelist = []

    if outdir is None:
        outdir = os.path.dirname(hdf)

    data = _extract_HDF_layer_data(hdf, layer_indexs)
    layer_indexs = core.enf_list(layer_indexs)
    for layer_index in layer_indexs:

        dataset = data[layer_index]
        outpath = core.create_outname(outdir, hdf, str(layer_index), "tif")

        print("creating dataset at {0}".format(outpath))

        _gdal_dataset_to_tif(dataset, outpath,
                            cust_projection = datatype.projectionTXT,
                            cust_geotransform = datatype.geotransform,
                            force_custom = force_custom,
                            nodata_value = nodata_value)

        output_filelist.append(outpath)

    return output_filelist

