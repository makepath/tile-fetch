import os
from os import path
from tile_fetch import (
    get_tile, save_tile,
    render_tiles_by_extent,
    save_tile_by_extent
)


TEMPLATE = ('https://c.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png')

here = path.abspath(path.join(path.dirname(__file__)))


def test_get_tile():
    lng = -90.283741
    lat = 29.890626
    level = 7
    tile = get_tile(lng, lat, level, template=TEMPLATE)
    print(tile)
    assert isinstance(tile, str)


def test_save_tile():
    output_path = path.join(here, 'test_save_tile.png')
    lng = -90.283741
    lat = 29.890626
    tile = None
    try:
        tile = save_tile(output_path, lng=lng, lat=lat)
        assert isinstance(tile, str)
        assert path.exists(tile)
    finally:
        if tile and path.exists(tile):
            os.remove(tile)


def test_render_tiles_by_extent():
    xmin = -90.283741
    ymin = 29.890626
    xmax = -89.912952
    ymax = 30.057766
    level = 11
    tiles = render_tiles_by_extent(xmin, ymin, xmax,
                                   ymax, level, template=TEMPLATE)
    tile_list = list(tiles)
    print(tile_list)
    assert len(tile_list) == 6


def test_save_tile_by_extent():
    output_path = path.join(here, 'tiles-directory')
    xmin = -90.283741
    ymin = 29.890626
    xmax = -89.912952
    ymax = 30.057766
    level = 11
    tiles = None
    try:
        tiles = save_tile_by_extent(output_path=output_path, xmin=xmin, ymin=ymin, xmax=xmax,
                                   ymax=ymax, level=level, template=TEMPLATE)
        assert isinstance(tiles, str)
        assert path.exists(tiles)
        assert len(os.listdir(tiles)) == 6
    finally:
        if tiles and path.exists(tiles):
            os.rmdir(tiles)
