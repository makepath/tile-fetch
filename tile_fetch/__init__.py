from __future__ import print_function, absolute_import

from tile_fetch.core import get_tile, render_tiles_by_extent, save_tile, save_tile_by_extent

from .test import test  # NOQA

from ._version import get_versions
__version__ = get_versions()['version']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
