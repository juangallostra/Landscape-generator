# coding: utf-8

# Landscape Generation with Midpoint displacement algorithm
# author : Juan Gallostra
# date : 10/12/2016
# version : 0.1.0


import os                             # path resolving and image saving
import random                         # midpoint displacement
from PIL import Image, ImageDraw      # image creation and drawing
import bisect                         # working with the sorted list of points
import colourlovers_api as clapi


# Iterative midpoint vertical displacement
def midpoint_displacement(start, end, roughness, vertical_displacement=None,
                          num_of_iterations=16):
    """
    Given a straight line segment specified by a starting point and an endpoint
    in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
    a roughness value > 0, an initial vertical displacement and a number of
    iterations > 0 applies the  midpoint algorithm to the specified segment and
    returns the obtained list of points in the form
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    """
    # Final number of points = (2^iterations)+1
    if vertical_displacement is None:
        # if no initial displacement is specified set displacement to:
        #  (y_start+y_end)/2
        vertical_displacement = (start[1]+end[1])/2
    # Data structure that stores the points is a list of lists where
    # each sublist represents a point and holds its x and y coordinates:
    # points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    #              |          |              |
    #           point 0    point 1        point n
    # The points list is always kept sorted from smallest to biggest x-value
    points = [start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        # Since the list of points will be dynamically updated with the new computed
        # points after each midpoint displacement it is necessary to create a copy
        # of the state at the beginning of the iteration so we can iterate over
        # the original sequence.
        # Tuple type is used for security reasons since they are immutable in Python.
        points_tup = tuple(points)
        for i in range(len(points_tup)-1):
            # Calculate x and y midpoint coordinates:
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2,
                                [0, 1]))
            # Displace midpoint y-coordinate
            midpoint[1] += random.choice([-vertical_displacement,
                                          vertical_displacement])
            # Insert the displaced midpoint in the current list of points         
            bisect.insort(points, midpoint)
            # bisect allows to insert an element in a list so that its order
            # is preserved.
            # By default the maintained order is from smallest to biggest list first
            # element which is what we want.
        # Reduce displacement range
        vertical_displacement *= 2 ** (-roughness)
        # update number of iterations
        iteration += 1
    return points
        
    
def draw_layers(layers, width, height, color_dict=None):
    # Default color palette
    if color_dict is None:
        color_dict = {'0': (195, 157, 224), '1': (158, 98, 204),
                      '2': (130, 79, 138), '3': (68, 28, 99), '4': (49, 7, 82),
                      '5': (23, 3, 38), '6': (240, 203, 163)}
    else:
        # len(color_dict) should be at least: # of layers +1 (background color)
        if len(color_dict) < len(layers)+1:
            raise ValueError("Num of colors should be bigger than the num of layers")

    # Create image into which the terrain will be drawn
    landscape = Image.new('RGBA', (width, height), color_dict[str(len(color_dict)-1)])
    landscape_draw = ImageDraw.Draw(landscape)
    # Draw the sun
    landscape_draw.ellipse((50, 25, 100, 75), fill=(255, 255, 255, 255))
    # Sample the y values of all x in image
    final_layers = []
    for layer in layers:
        sampled_layer = []
        for i in range(len(layer)-1):
            sampled_layer += [layer[i]]
            # If x difference is greater than 1
            if layer[i+1][0]-layer[i][0] > 1:
                # Linearly sample the y values in the range x_[i+1]-x_[i]
                # This is done by obtaining the equation of the straight
                # line (in the form of y=m*x+n) that connects two consecutive
                # points
                m = float(layer[i+1][1]-layer[i][1])/(layer[i+1][0]-layer[i][0])
                n = layer[i][1]-m*layer[i][0]
                r = lambda x: m*x+n  # straight line
                for j in range(int(layer[i][0]+1), int(layer[i+1][0])):  # for all missing x
                    sampled_layer += [[j, r(j)]]  # Sample points
        final_layers += [sampled_layer]

    final_layers_enum = enumerate(final_layers)
    for final_layer in final_layers_enum:
        # traverse all x values in the layer
        for x in range(len(final_layer[1])-1):
            # for each x value draw a line from its y value to the bottom
            landscape_draw.line((final_layer[1][x][0], height-final_layer[1][x][1],
                                 final_layer[1][x][0], height),
                                 color_dict[str(final_layer[0])])

    return landscape


def main():
    width = 1000  # Terrain width
    height = 500  # Terrain height
    # Compute different layers of the landscape
    layer_1 = midpoint_displacement([250, 0], [width, 200], 1.4, 20, 12)
    layer_2 = midpoint_displacement([0, 180], [width, 80], 1.2, 30, 12)
    layer_3 = midpoint_displacement([0, 270], [width, 190], 1, 120, 9)
    layer_4 = midpoint_displacement([0, 350], [width, 320], 0.9, 250, 8)

    landscape = draw_layers([layer_4, layer_3, layer_2, layer_1], width, height)

    landscape.save(os.getcwd()+'\\testing.png')


if __name__ == "__main__":
    main()
