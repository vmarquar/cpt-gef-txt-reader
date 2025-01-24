import gef_reader.gef_parser as gef_reader

from gef_reader.utils.pytess_main import pytess_triangulate, pytess_voronoi # original code from pytess, see https://github.com/karimbahgat/Pytess


from .gef_parser import read_gef_file, read_alt_gef_file