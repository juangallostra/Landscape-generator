
# coding: utf-8

# Landscape Generation with Midpoint displacement algorithm
# author : Juan Gallostra
# date : 12/05/2016
# version : 0.1.0

import sys, os

import random
from PIL import Image, ImageDraw
import bisect

# non recursive midpoint vertical displacement
def midp_disp(init,end,roughness,disp=None,iterations=16):
    # number of points = (2^iterations)+1
    if disp == None:
        disp = (init[1]+end[1])/2
    points = [init,end]
    for i in range(iterations):
        t_points = tuple(points)
        for z in range(len(t_points)-1):
            midpoint = list(map(lambda x: (t_points[z][x]+t_points[z+1][x])/2,[0,1]))   # calculate midpoint
            midpoint[1]+=random.choice([-disp,disp])                                    # diplace midpoint y-coordinate
            bisect.insort(points,midpoint)
        disp = disp*(2**(-roughness))                                                   #reduce displacement range
    #print(points)
    return points
        
    
def fill_horizons_overlap(data_sets,horizons,width,height,theme=None):
    # color palette
    color_dict={'0':(240,203,163),'1':(195,157,224),'2':(158,98,204),'3':(130,79,138),'4':(68,28,99),'5':(49,7,82),
                '6':(23,3,38)}
    
    landscape = Image.new('RGBA',(width,height),color_dict[str(0)])
    landscape_draw = ImageDraw.Draw(landscape)
    
    # draw the sun 
    landscape_draw.ellipse((50,25,100,75), fill=(255,255,255,255))
    
    # sampling all x in image for every data set
    data=[]
    new_data_set=[]
    for data_set in data_sets:
        for x in range(len(data_set)-1):
            new_data_set+=[data_set[x]]
            if data_set[x+1][0]-data_set[x][0] > 1: # if difference is greater than 1
                # linearly sample x-values
                m = float(data_set[x+1][1]-data_set[x][1])/(data_set[x+1][0]-data_set[x][0])
                n = data_set[x][1]-m*data_set[x][0]
                r=lambda x: m*x+n # straight line
                for i in range(data_set[x][0]+1,data_set[x+1][0]): # for all missing x
                    new_data_set+=[[i,r(i)]] # sample points
        data+=[new_data_set]
        new_data_set=[]
        
    # drawing landscape 
    for data_set in data:
        for x in range(len(data_set)-1):
            landscape_draw.line((data_set[x][0],height-data_set[x][1],data_set[x][0],height), color_dict[str(data.index(data_set)+2)]) 

    return landscape

def main():
    WIDTH = 1000
    HEIGHT = 500
    # Compute different layers of the landscape
    test2 = midp_disp([0,270],[WIDTH,190],1,120,9)
    test = midp_disp([0,20],[500,0],1,7,12)
    test3 = midp_disp([0,180],[WIDTH,80],1,30,12)
    test4 = midp_disp([0,350],[WIDTH,320],0.9,250,8)
    test5 = midp_disp([250,0],[WIDTH,200],1,20,12)
    landscape=fill_horizons_overlap([test4,test2,test3,test5],4,WIDTH,HEIGHT) #[test4,test2,test3,test5,test]
    landscape.save(os.getcwd()+'\\testing.png')





    
if __name__ == "__main__":
    main()




