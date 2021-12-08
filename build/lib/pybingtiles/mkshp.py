"""make_shapefile.py
This script generates a shapefile if the WGS 84 coordinates of a bounding box are inserted.
The code is based off the informations contained in the following web page:
https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system.
"""

from convert import *
import warnings
from shapely.geometry import Polygon
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import geopandas as gpd

def bbox_to_gdf(bbox, level):
    """This function generates a GeoPandas GeoDataFrame with the shapes of the
    desired grid, composed of squares associated to their own QuadKey, given the
    WGS 84 coordinates of the upper left corner and the bottom right corner of
    the bounding box.
    
    :param bbox: A dictionary with four values, the latitude of the upper left corner
        `y1`, the longitude of the upper left corner `x1`, the latitude of the bottom
        right corner `y2`, the longitude of the bottom right corner `x2`
    :param level: The level of detail of the Bing Map
    :return: A GeoDataFrame with the polygons that compose the grid
    """
    tile_x1_0, tile_y1_0 = lat_long_to_tile(bbox['y1'], bbox['x1'], level)
    tile_x2_0, tile_y2_0 = lat_long_to_tile(bbox['y2'], bbox['x2'], level)
    tile_x1 = min(tile_x1_0, tile_x2_0)
    tile_x2 = max(tile_x1_0, tile_x2_0)
    tile_y1 = min(tile_y1_0, tile_y2_0)
    tile_y2 = max(tile_y1_0, tile_y2_0)
    lat_ul_l, lat_ur_l, lat_bl_l, lat_br_l = [], [], [], []
    long_ul_l, long_ur_l, long_bl_l, long_br_l = [], [], [], []
    tile_x_l = []
    tile_y_l = []
    quadkey_l = []
    total_count = (tile_x2+1-tile_x1)*(tile_y2+1-tile_y1)
    count = 0
    print("Defining grid...")
    for i in range(tile_x1, tile_x2 + 1):
        for j in range(tile_y1, tile_y2 + 1):
            tile_x_l.append(i)
            tile_y_l.append(j)
            lat_ul, long_ul = tile_to_lat_long(i, j, level)
            lat_ur, long_ur = tile_to_lat_long(i+1, j, level)
            lat_bl, long_bl = tile_to_lat_long(i, j+1, level)
            lat_br, long_br = tile_to_lat_long(i+1, j+1, level)
            lat_ul_l.append(lat_ul)
            lat_ur_l.append(lat_ur)
            lat_bl_l.append(lat_bl)
            lat_br_l.append(lat_br)
            long_ul_l.append(long_ul)
            long_ur_l.append(long_ur)
            long_bl_l.append(long_bl)
            long_br_l.append(long_br)
            quadkey_l.append(tile_to_quadkey(i, j, level))
            count += 1
    df = pd.DataFrame(zip(quadkey_l, tile_x_l, tile_y_l, lat_ul_l, lat_ur_l, lat_bl_l, lat_br_l, long_ul_l, long_ur_l, long_bl_l, long_br_l), columns = ['quadkey', 'tile_x', 'tile_y', 'lat_ul', 'lat_ur', 'lat_bl', 'lat_br', 'long_ul', 'long_ur', 'long_bl', 'long_br'])
    df['geometry'] = df.apply(lambda row: Polygon([[row[f'long_{v}'], row[f'lat_{v}']] for v in ['ul', 'ur', 'br', 'bl']]), axis = 1)
    print("Creating GeoDataFrame...")
    gdf = gpd.GeoDataFrame(df, geometry=df.geometry).set_crs("EPSG:4326")
    return gdf

def export_grid(gdf, file):
    """This function produces a shapefile with the shapes contained in the specified
    GeoDataFrame
    
    :param gdf: A GeoDataFrame with the polygons of the grid
    :param file: The filename or path where the shapefile should be saved (including the `.shp` extension)
    """
    print("Exporting shapefile...")
    gdf.to_file(file)

if __name__ == "__main__":
    bbox = {}
    bbox['y1'] = float(input("Enter latitude for the upper left corner of the bounding box (WGS 84): "))
    bbox['x1'] = float(input("Enter longitude for the upper left corner of the bounding box (WGS 84): "))
    bbox['y2'] = float(input("Enter latitude for the bottom right corner of the bounding box (WGS 84): "))
    bbox['x2'] = float(input("Enter longitude for the bottom right corner of the bounding box (WGS 84): "))
    level = int(input("Enter Bing Tiles level of detail of interest (1-23): "))
    conf_viz = bool(input("Do you want to see a confirmation of the area you selected? (True/False): "))
    if (conf_viz==True):
        poly = Polygon([[bbox['x1'], bbox['y1']], [bbox['x2'], bbox['y1']], [bbox['x2'], bbox['y2']], [bbox['x1'], bbox['y2']]])
        fig, ax = plt.subplots()
        plt.plot(*poly.exterior.xy, color='red')
        cx.add_basemap(ax, crs='EPSG:4326')
        fig.savefig("bbox_map.png")
        print("Check the bbox_map.png file in the current folder.")
    file = str(input("Enter the filename of the shapefile you want to output your grid to (.shp): "))
    
    grid_gdf = bbox_to_gdf(bbox, level)
    export_grid(grid_gdf, file)
