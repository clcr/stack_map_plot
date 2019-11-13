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
    data = []
    for ii, raster_path in enumerate(raster_path_list):
        band = gdal.Open(raster_path)
        band_array = band.ReadAsArray()
        nodata = band_array.min()
        band_array[band_array == nodata] = np.nan
        gt = band.GetGeoTransform()
        X = np.arange(gt[0], gt[0] + gt[1]*band.RasterXSize, gt[1])
        Y = np.arange(gt[3], gt[3] + gt[5]*band.RasterYSize*-1, gt[5]*-1)   # Geotransforms.
        Z = np.ones(band_array.shape)
        Z[band_array == nodata] = np.nan
        Z = Z+(ii*5)
        data.append(go.Surface(x=X, y= Y, z=Z, surfacecolor=band_array))
        if ii > 0:
            data[ii].showscale=False
    fig = go.Figure(data=data)
    fig.show()
