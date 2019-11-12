import gdal
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

import pdb

def test_stack_map_plot():
    data_dir = Path("./data")
    raster_list = [str(x) for x in data_dir.glob("*.tif")]
    stack_map_plot(raster_list)


def stack_map_plot(raster_path_list, label_spec = None, colormap_spec=None):
    Z = []
    for ii, raster_path in enumerate(raster_path_list):
        band = gdal.Open(raster_path)
        band_array = band.ReadAsArray()
        nodata = band_array.min()
        band_array[band_array == nodata] = np.nan
        gt = band.GetGeoTransform()
        X = np.arange(gt[0], gt[0] + gt[1]*band.RasterXSize, gt[1])
        Y = np.arange(gt[3], gt[3] + gt[5]*band.RasterYSize*-1, gt[5]*-1)   # Geotransforms.
        X, Y = np.meshgrid(X, Y)
        Z.append(band_array + (ii*10))

    data = [go.Surface(z=z_map) for z_map in Z]
    fig = go.Figure(data=data)
    fig.show()
