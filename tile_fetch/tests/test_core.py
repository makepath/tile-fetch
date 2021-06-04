import os
import pytest

from os import path
from tile_fetch import (
    get_tile, save_tile,
    render_tiles_by_extent,
    save_tile_by_extent
)


TEMPLATE = ('https://c.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png')

here = path.abspath(path.join(path.dirname(__file__)))
OUTPUT_PATH = path.join(here, 'tiles-directory')


def get_tiles_in_dir(dir_name, traversed = set(), results = set()):
    dirs = os.listdir(dir_name)
    if dirs:
        for f in dirs:
            new_dir = dir_name + '/' + f
            if os.path.isdir(new_dir) and new_dir not in traversed:
                traversed.add(new_dir)
                get_tiles_in_dir(new_dir, traversed, results)
            else:
                results.add(new_dir)
    return results


@pytest.fixture
def remove_files():
    yield
    files = get_tiles_in_dir(OUTPUT_PATH, traversed=set())
    for file in files:
        os.remove(file)


def test_get_tile():
    lng = -90.283741
    lat = 29.890626
    level = 7
    tile = get_tile(lng, lat, level, template=TEMPLATE)
    assert isinstance(tile, str)


def test_save_tile():
    output_path = path.join(here, 'test_save_tile.png')
    lng = -90.283741
    lat = 29.890626
    tile = None
    tile = save_tile(output_path, lng=lng, lat=lat)
    assert isinstance(tile, str)
    assert path.exists(tile)

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
    assert len(tile_list) == 6


def test_save_tile_by_extent(remove_files):
    xmin = -90.283741
    ymin = 29.890626
    xmax = -89.912952
    ymax = 30.057766
    level = 11
    tiles = None
    tiles = save_tile_by_extent(output_path=OUTPUT_PATH, xmin=xmin, ymin=ymin, xmax=xmax,
                                ymax=ymax, level=level, template=TEMPLATE)
    assert isinstance(tiles, str)
    assert path.exists(tiles)
    file_list = get_tiles_in_dir(tiles + f'/{level}', traversed=set())
    assert len(file_list) == 6
