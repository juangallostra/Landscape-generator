"""
test suite for the colourlovers API wrapper
This test unit is intended only for testing and not for anything else
@Author: Juan Gallostra
@Date: 09-03-2017

UNDER DEVELOPMENT
"""
import colourlovers_wrapper as cl_wrapper


if __name__=="__main__":

    cl = cl_wrapper.ColourLovers()

    # Method test
    # Unique request tests
    colors_r = cl.search_colors(request="random")
    colors_n = cl.search_colors(request="new")
    colors_t = cl.search_colors(request="top")

    color = cl.search_color()
    palettes = cl.search_palettes()
    palette = cl.search_palette()
    patterns = cl.search_patterns()
    pattern = cl.search_pattern()
    pattern = cl.search_lovers()
    lover = cl.search_lover()
    stats = cl.search_stats()
