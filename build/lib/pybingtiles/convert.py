"""convert.py
This module contains the functions to operate conversions between
WGS 84 latitude and longitude, Bing Map pixels, Bing Map tiles and
Bing Map QuadKeys.
"""

import math as mt
import numpy as np

# define constants

earth_radius = 6378137
min_lat = -85.05112878
max_lat = 85.05112878
min_long = -180
max_long = 180

# define converting functions between latlong, pixels, tiles, quadkey

def lat_long_to_pixel(lat, long, level):
    """This is a function that converts WGS 84 latitude and longitude to
    the pixel coordinates of a Bing Map at a certain level of detail.
    
    :param lat: The latitude in degrees unit (WGS 84)
    :param long: The longitude in degrees unit (WGS 84)
    :param level: The level of detail of the Bing Map
    :return: Two float values, `pixel_x` and `pixel_y`
    """
    lat = np.clip(lat, min_lat, max_lat)
    long = np.clip(long, min_long, max_long)
    x = (long + 180) / 360
    sin_lat = np.sin(lat * mt.pi / 180)
    y = 0.5 - np.log((1 + sin_lat) / (1 - sin_lat)) / (4 * mt.pi)
    map_size = 256 << level
    
    pixel_x = int(np.clip(x * map_size + 0.5, 0, map_size - 1))
    pixel_y = int(np.clip(y * map_size + 0.5, 0, map_size - 1))
    
    return pixel_x, pixel_y

def lat_long_to_tile(lat, long, level):
    """This is a function that converts WGS 84 latitude and longitude to
    the tile coordinates of a Bing Map at a certain level of detail.
    
    :param lat: The latitude in degrees unit (WGS 84)
    :param long: The longitude in degrees unit (WGS 84)
    :param level: The level of detail of the Bing Map
    :return: Two integer values, `tile_x` and `tile_y`
    """
    pixel_x, pixel_y = lat_long_to_pixel(lat, long, level)
    tile_x, tile_y = int(pixel_x/256), int(pixel_y/256)
    return tile_x, tile_y

def pixel_to_lat_long(pixel_x, pixel_y, level):
    """This is a function that converts pixel coordinates at a certain
    level of detail of a Bing Map to WGS 84 latitude and longitude.
    
    :param pixel_x: The x axis coordinate of the pixel at `level` level of detail
    :param pixel_y: The y axis coordinate of the pixel at `level` level of detail
    :param level: The level of detail of the Bing Map
    :return: Two floats, `lat` and `long`, expressed in degrees
    """
    map_size = 256 << level
    x = (np.clip(pixel_x, 0, map_size - 1) / map_size) - 0.5
    y = 0.5 - (np.clip(pixel_y, 0, map_size - 1) / map_size)
    
    lat = 90 - 360 * np.arctan(np.exp(-y * 2 * mt.pi)) / mt.pi
    long = 360 * x
    
    return lat, long

def tile_to_lat_long(tile_x, tile_y, level):
    """This is a function that converts tile coordinates at a certain
    level of detail of a Bing Map to WGS 84 latitude and longitude.
    
    :param tile_x: The x axis coordinate of the tile at `level` level of detail
    :param tile_y: The y axis coordinate of the tile at `level` level of detail
    :param level: The level of detail of the Bing Map
    :return: Two floats, `lat` and `long`, expressed in degrees
    """
    pixel_x, pixel_y = int(tile_x * 256), int(tile_y * 256)
    lat, long = pixel_to_lat_long(pixel_x, pixel_y, level)
    return lat, long

def tile_to_quadkey(tile_x, tile_y, level):
    """This is a function that converts tile coordinates at a certain
    level of detail of a Bing Map to a unique string identifier (QuadKey).
    
    :param tile_x: The x axis coordinate of the tile at `level` level of detail
    :param tile_y: The y axis coordinate of the tile at `level` level of detail
    :param level: The level of detail of the Bing Map
    :return: A `quadkey` string of length given by the `level` level of detail
    """
    ql = []
    for i in range(level, 0, -1):
        digit = ord('0')
        mask = 1 << (i-1)
        if ((tile_x & mask) != 0):
            digit+=1
        if ((tile_y & mask) != 0):
            digit+=2
        ql.append(chr(digit))
    quadkey = ''.join(ql)
    return quadkey
