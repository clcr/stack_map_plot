import gdal
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def test_stack_map_plot():
    in_raster = "some_raster.tif"
    stack_map_plot("some_raster.tif", labels)


def stack_map_plot(in_raster_path, label_spec, colormap_spec=None):
    raster_array  = gdal.Open(in_raster_path).ReadAsArray()
    axis = plt.figure().gca(projection="3d")
    for band in raster_array[:,...]:
        axis.add(band)
        axis.setcolormap(colormp)
        axis.setlabel(label)
