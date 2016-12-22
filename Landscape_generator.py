# coding: utf-8

# Landscape Generation with Midpoint displacement algorithm
# author : Juan Gallostra
# date : 10/12/2016
# version : 0.1.0


import os                             # path resolving and image saving
import random                         # midpoint displacement
from PIL import Image, ImageDraw      # image creation and drawing
import bisect                         # working with the sorted list of points


# Iterative midpoint vertical displacement
def midpoint_displacement(start, end, roughness, vertical_displacement=None, num_of_iterations=16):
    """
    Given a straight line segment specified by a starting point and an endpoint in the form of 
    [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y], a roughness value > 0, 
    an initial vertical displacement and a number of iterations > 0 applies the  midpoint algorithm
    to the specified segment and returns the obtained list of points in the form 
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    """
    # Final number of points = (2^iterations)+1
    if vertical_displacement is None:
        # if no initial displacement is specified set displacement to: (y_start+y_end)/2
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
        # Since the list of points will be dynamically updated with the new computed points
        # after each midpoint displacement it is necessary to create a copy of the
        # state at the beginning of the iteration so we can iterate over the original sequence.
        # The tuple type is used for security reasons since they are immutable in Python.
        points_tup = tuple(points)
        for i in range(len(points_tup)-1):
            # Calculate x and y midpoint coordinates: [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2, [0, 1]))
            # Displace midpoint y-coordinate 
            # midpoint[1]+=random.choice(range(-int(vertical_displacement)-1,int(vertical_displacement)+1))
            midpoint[1] += random.choice([-vertical_displacement, vertical_displacement])
            # Insert the displaced midpoint in the current list of points         
            bisect.insort(points, midpoint)
            # bisect allows to insert an element in a list so that its order is preserved.
            # By default the maintained order is from smallest to biggest list first element
            # which is what we want.
        # Reduce displacement range
        vertical_displacement *= 2 ** (-roughness)
        # update number of iterations
        iteration += 1
    return points
        
    
def fill_horizons_overlap(data_sets, width, height, color_dict=None):
    # color palette
    if color_dict is None:
        color_dict = {'0': (240, 203, 163), '1': (195, 157, 224), '2': (158, 98, 204), '3': (130, 79, 138),
                          '4': (68, 28, 99), '5': (49, 7, 82), '6': (23, 3, 38)}

    else:
        if len(color_dict)<len(data_sets):
            raise ValueError("Number of colors should be bigger than the amount of terrain layers")

    landscape = Image.new('RGBA', (width, height), color_dict[str(0)])
    landscape_draw = ImageDraw.Draw(landscape)
    
    # draw the sun 
    landscape_draw.ellipse((50, 25, 100, 75), fill=(255, 255, 255, 255))
    
    # sampling all x in image for every data set
    data = []
    new_data_set = []
    for data_set in data_sets:
        for i in range(len(data_set)-1):
            new_data_set += [data_set[i]]
            if data_set[i+1][0]-data_set[i][0] > 1:  # if difference is greater than 1
                # linearly sample x-values
                m = float(data_set[i+1][1]-data_set[i][1])/(data_set[i+1][0]-data_set[i][0])
                n = data_set[i][1]-m*data_set[i][0]
                r = lambda x: m*x+n  # straight line
                for j in range(data_set[i][0]+1, data_set[i+1][0]):  # for all missing x
                    new_data_set += [[j, r(j)]]  # sample points
        data += [new_data_set]
        new_data_set = []
        
    # drawing landscape 
    for data_set in data:
        for x in range(len(data_set)-1):
            # TODO enumerate(data_sets) so as to access color_dict by data_set enumerate index
            landscape_draw.line((data_set[x][0], height-data_set[x][1], data_set[x][0], height),
                                color_dict[str(data.index(data_set)+2)])

    return landscape


def main():
    width = 1000
    height = 500
    # Compute different layers of the landscape
    test2 = midpoint_displacement([0, 270], [width, 190], 1, 120, 9)
    test = midpoint_displacement([0, 20], [500, 0], 1, 7, 12)
    test3 = midpoint_displacement([0, 180], [width, 80], 1.2, 30, 12)
    test4 = midpoint_displacement([0, 350], [width, 320], 0.9, 250, 8)
    test5 = midpoint_displacement([250, 0], [width, 200], 1.4, 20, 12)
    landscape = fill_horizons_overlap([test4, test2, test3, test5], width, height)  # [test4,test2,test3,test5,test]
    # landscape=fill_horizons_overlap([test2],1,WIDTH,HEIGHT) #[test4,test2,test3,test5,test]
    landscape.save(os.getcwd()+'\\testing.png')


if __name__ == "__main__":
    main()
