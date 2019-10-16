# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:59:31 2018

@author: u18343
"""
import gdal
import os

def array_to_geotiff(fname, data, geo_transform, projection,
                     nodata_val=0, dtype=gdal.GDT_Float32):
    """
    Create a single band GeoTIFF file with data from an array. 
    
    Because this works with simple arrays rather than xarray datasets from DEA, it requires
    geotransform info ("(upleft_x, x_size, x_rotation, upleft_y, y_rotation, y_size)") and 
    projection data (in "WKT" format) for the output raster. These are typically obtained from 
    an existing raster using the following GDAL calls:
    
    # import gdal
    # gdal_dataset = gdal.Open(raster_path)
    # geotrans = gdal_dataset.GetGeoTransform()
    # prj = gdal_dataset.GetProjection()
    
    ...or alternatively, directly from an xarray dataset:
    
    # geotrans = xarraydataset.geobox.transform.to_gdal()
    # prj = xarraydataset.geobox.crs.wkt
    
    Last modified: March 2018
    Author: Robbi Bishop-Taylor
    
    :attr fname: output file path
    :attr data: input array
    :attr geo_transform: geotransform for output raster; 
    			 e.g. "(upleft_x, x_size, x_rotation, upleft_y, y_rotation, y_size)"
    :attr projection: projection for output raster (in "WKT" format)
    :attr nodata_val: value to convert to nodata in output raster; default 0
    :attr dtype: value to convert to nodata in output raster; default gdal.GDT_Float32
    """

    # Set up driver
    driver = gdal.GetDriverByName('GTiff')

    # Create raster of given size and projection
    rows, cols = data.shape
    dataset = driver.Create(fname, cols, rows, 1, dtype)
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)

    # Write data to array and set nodata values
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    band.SetNoDataValue(nodata_val)

    # Close file
    dataset = None
    