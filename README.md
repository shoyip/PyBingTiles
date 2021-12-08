# PyBingTiles

This is a small toolkit in order to deal with Bing Tiles, used i.e. by Facebook
for their Data for Good datasets.

## Install

Clone this repository, then issue the following command:

```
python setup.py install
```

## Use

### Generate a Shapefile from a bounding box

If you run
```
python pybingtiles/mkshp.py
```
you will be asked to enter the latitudes and the longitudes of the upper left
and bottom right corners of the bounding box inside of which you would like to
define the Bing Tile grid. You will also be asked to insert a *level of
definition*, an integer between 1 and 23 depending on the coarseness of the
tile.

You can also have an image produced of the geographic area that you are going to
crop in order to be sure of the operation. The script then produces an ESRI
Shapefile with the grid squares as Polygons in the area previously defined.

### Use conversion functions

You can also import
```
from pybingtiles.convert import *
```
and get the conversion functions between Bing Maps Pixels XY coordinates, Bing
Maps Tiles XY coordinates, WGS 84 latitudes and longitudes and QuadKeys. 

Five functions are available:
- `lat_long_to_pixel`
- `lat_long_to_tile`
- `pixel_to_lat_long`
- `tile_to_lat_long`
- `tile_to_quadkey`

Check docstrings for more details.

## References

- [Bing Maps Tile System](https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system) - Microsoft
