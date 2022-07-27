import concurrent.futures
import enum
from hashlib import new
import itertools
import json
import logging
import math
from pathlib import Path

import cv2 
import hydra
import numpy as np
import scipy.interpolate
from sklearn import neighbors
import tifffile
from omegaconf import OmegaConf, DictConfig
from tqdm import tqdm

from operator import index
from textwrap import indent
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
from urllib3 import Retry
from PIL import Image, ImageOps
import pickle

import os
import glob

import json
from operator import index, inv
import collections



def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )



def apply_fisheye(imgfile, fisheye_center, inner_fisheye_radius, outer_fisheye_radius, MM):

    img = Image.open(imgfile)
    dim_x, dim_y = img.size

    img_pixels = img.load()

    x_c, y_c = fisheye_center[0], fisheye_center[1]

    ## loop through all the pixels
    ## each pixel gets one of the three possible transformations
    ## i) pixels in the focus get magnified
    ## ii) pixels outside the focus, i.e., in the context do not change
    ## iii) pixels in the transition gets noisy and distorted

    new_to_old_map = {}

    max_x = 0
    max_y = 0

    min_x = 9999
    min_y = 9999

    for x in range(dim_x):
        for y in range(dim_y):

            current_pixel = img_pixels[ x, y ]
            # print(current_pixel)

            distance_from_center = get_euclidean_distance( x_c, y_c, x, y )

            if( distance_from_center <= inner_fisheye_radius):
                # print( distance_from_center, " -> inside the focus" )
                new_position = [ x_c + ( x - x_c ) / MM, 
                                 y_c + ( y - y_c ) / MM  ]

                transformed = [ round( new_position[0] ), round( new_position[1] ) ]       

                if( round( new_position[0] ) > max_x ):
                    max_x = round( new_position[0] ) 

                if( round( new_position[1] ) > max_y ):
                    max_y = round( new_position[1] )      

                
                if( round( new_position[0] ) < min_x ):
                    min_x = round( new_position[0] ) 

                if( round( new_position[1] ) < min_y ):
                    min_y = round( new_position[1] )             

                # print( [x, y] ,"   ", transformed)     

                if ( str( transformed ) in new_to_old_map.keys() ):
                            new_to_old_map[ str( transformed ) ].append([ x, y ])
                else:
                     new_to_old_map[ str( transformed ) ] = [ [ x, y ] ]           



            elif( distance_from_center > inner_fisheye_radius and distance_from_center < outer_fisheye_radius ):
                # print( distance_from_center, " -> distortion region" )
                continue

            elif( distance_from_center >= outer_fisheye_radius ):
                # print( "no change region (context region)" )      
                continue

    # print(new_to_old_map)

    new_img = img.copy()

    for i in range(dim_x):
        for j in range(dim_y):
            new_img.putpixel( (i, j), (0, 0, 0))

    ## if MM > 1:

    # for key in new_to_old_map.keys():
    #     new_coordinate = json.loads(key)

    #     old_coordinate_list = new_to_old_map[key]

    #     old_coordinate_bitmaps = []

    #     for item in old_coordinate_list:
    #         old_coordinate_bitmaps.append( img_pixels[ item[0], item[1] ] )


    #     r = 0
    #     g = 0
    #     b = 0

    #     for item in old_coordinate_bitmaps:
    #         r += item[0]
    #         g += item[1]
    #         b += item[2]

    #     r = round ( r / len( old_coordinate_bitmaps ) )
    #     g = round ( g / len( old_coordinate_bitmaps ) )  
    #     b = round ( b / len( old_coordinate_bitmaps ) )    

     #     new_img.putpixel( (new_coordinate[0], new_coordinate[1] ), (r, g, b) )


    ## if MM < 1   


    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):

            if (str([i, j]) in new_to_old_map.keys()):

                old = new_to_old_map[ str([i, j]) ][0]
                current_pixel_bitmap = img_pixels[ old[0], old[1] ]
                new_img.putpixel( (i, j), (current_pixel_bitmap[0], current_pixel_bitmap[1], current_pixel_bitmap[2]))

    

    new_img_pixels = new_img.load()

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):

            if (str([i, j]) not in new_to_old_map.keys()):

                neighbors = []    


                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if(k==l):
                            continue
                        neighbors.append([k, l])


                neighbor_bitmaps = []

                for neighbor in neighbors:

                    neighbor_bitmaps.append(new_img_pixels[ neighbor[0], neighbor[1] ])
                    # print(new_img_pixels[ neighbor[0], neighbor[1] ])
            

                r = 0
                g = 0
                b = 0

                for item in neighbor_bitmaps:
                    r += item[0]
                    g += item[1]
                    b += item[2]

                r = round( r/len(neighbor_bitmaps) )        
                g = round( g/len(neighbor_bitmaps) )    
                b = round( b/len(neighbor_bitmaps) )    


                new_img.putpixel( (i, j), (r, g, b))   

    
    print(min_x, min_y)
    print(max_x, max_y)





    new_img.save('fisheye_output.jpg')





apply_fisheye("output.jpg", (540, 960), 200, 120, .5)


# print(json.loads('[2, 3]'))