import gdal
import os
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
    zlabel = []
    zpos = []
    for ii, raster_path in enumerate(raster_path_list):
        # Get and filter raster values
        band = gdal.Open(raster_path)
        band_array = band.ReadAsArray()
        nodata = band_array.min()
        band_array[band_array == nodata] = np.nan
        
        # Calulate x and y axis from geotransforms: top-left corner and stride from GT, number
        # of strides from RasterX/Ysize
        gt = band.GetGeoTransform()
        X = np.arange(gt[0], gt[0] + gt[1]*band.RasterXSize, gt[1])
        Y = np.arange(gt[3], gt[3] + gt[5]*band.RasterYSize*-1, gt[5]*-1)   # Geotransforms are a pain..
        
        # Set Z to offsets and build colormap
        Z = np.ones(band_array.shape)
        Z = Z+(ii*10)
        Z[band_array == nodata] = np.nan
        nan_colorscale = [[0,'grey'],
                          [0.01, 'rgba(0,0,0,1)'],
                          [0.01, 'darkgoldenrod'],
                          [1, 'mistyrose']]   
        data.append(go.Surface(x=X, y= Y, z=Z, surfacecolor=band_array, connectgaps = False,
            colorscale=nan_colorscale, cmin = band_array.min(), cmax = band_array.max()))
        
        # Setting labels and positions
        zlabel.append(os.path.basename(raster_path))
        zpos.append(1+(ii*10))
        if ii > 0:
            data[ii].showscale=False
    
    #Creating figure and setting 
    fig = go.Figure(data=data)
    fig.update_layout(scene = {
        "zaxis": {
            "ticktext":zlabel,
            "tickvals":zpos
            },
        "xaxis_title": "lon",
        "yaxis_title": "lat"
        })
    fig.show()
