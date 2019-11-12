import gdal
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import pdb

def test_stack_map_plot():
    data_dir = Path("./data")
    raster_list = [str(x) for x in data_dir.glob("*.tif")]
    stack_map_plot(raster_list)


def stack_map_plot(raster_path_list, label_spec = None, colormap_spec=None):
    fig = plt.figure()
    axis = fig.gca(projection='3d')
    for ii, raster_path in enumerate(raster_path_list[0:2]):
        band = gdal.Open(raster_path)
        band_array = band.ReadAsArray()
        nodata = band_array.min()
        band_array[band_array == nodata] = np.median(band_array)
        gt = band.GetGeoTransform()
        X = np.arange(gt[0], gt[0] + gt[1]*band.RasterXSize, gt[1])
        Y = np.arange(gt[3], gt[3] + gt[5]*band.RasterYSize*-1, gt[5]*-1)   # Geotransforms.
        X, Y = np.meshgrid(X, Y)
        Z = band_array * ii
        axis.plot_surface(X, Y, Z)
    plt.show()   
