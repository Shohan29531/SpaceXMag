import concurrent.futures
import enum
from hashlib import new
import itertools
import json
import logging
import math
from pathlib import Path
from typing import final
import time

import cv2 
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
from PIL import Image, ImageOps, ImageDraw
import pickle

import os
import glob

import json
from operator import index, inv
import collections

start_time = time.time()

# def crop_circular_section(img_file, fisheye_radius, fisheye_center):
#     img=Image.open(img_file)
#     # img.show()
#     h, w = img.size

#     lum_img = Image.new('L', [h, w], 0)

#     draw = ImageDraw.Draw(lum_img)
#     draw.pieslice([(fisheye_center[0] - fisheye_radius, fisheye_center[1] -fisheye_radius), (fisheye_center[0]+ fisheye_radius, fisheye_center[1] + fisheye_radius)], 0, 360, 
#                 fill = 255, outline = "white")
    
#     img_arr =np.array(img)
#     lum_img_arr =np.array(lum_img)
    
#     # Image.fromarray(lum_img_arr).show()
    
#     final_img_arr = np.dstack((img_arr,lum_img_arr))  
#     final_img = Image.fromarray(final_img_arr)
#     # final_img.save('fisheye_focus.png')
#     # final_img.resize((fisheye_radius, fisheye_radius))
#     # final_img.show()
    
#     # final_img.save('fisheye_focus.jpg')
#     print(final_img.size)
    




# crop_circular_section("fisheye_output.jpg", 250, (540, 960))


def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )




def gaussian_drop_off(dist, MM, fisheye_rad):
    
    drop_off = 1 - 0.2 * ( math.sin( (dist/(fisheye_rad*MM)) * (3.1416/2) ) )
    
    # drop_off = drop_off * ( MM - 1) + 1
    
    # print(drop_off)
    
    return drop_off


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

    min_x = 9999
    max_x = 0
    
    min_y = 9999 
    max_y = 0
    
    new_img = img.copy()
    

    for x in range(dim_x):
        for y in range(dim_y):

            current_pixel = img_pixels[ x, y ]
            # print(current_pixel)

            distance_from_center = get_euclidean_distance( x_c, y_c, x, y )

            if( distance_from_center <= inner_fisheye_radius):
                
                # new_img.putpixel( ( x, y ), (0, 0, 0) ) 
                
                # new_position = [ x_c + (( x - x_c ) * MM), 
                #                  y_c + (( y - y_c ) * MM)  ]

                # transformed = [ round( new_position[0] ), round( new_position[1] ) ]       

                # # print( [x, y] ,"   ", transformed)     

                # if ( str( transformed ) in new_to_old_map.keys() ):
                #             new_to_old_map[ str( transformed ) ].append([ x, y ])
                # else:
                #      new_to_old_map[ str( transformed ) ] = [ [ x, y ] ]  
                
                         
                new_img.putpixel( ( x, y ), (0, 0, 0) )  
            
                
                # print( mag_range_high, mag_range_low)
 
                drop_off = gaussian_drop_off( abs(distance_from_center), MM, outer_fisheye_radius )  
                # print(drop_off)  
                
                new_position = [ x_c + ( x - x_c ) * drop_off  , 
                                 y_c + ( y - y_c ) * drop_off  ]

                transformed = [ round( new_position[0] ), round( new_position[1] ) ]       

                # print( [x, y] ,"   ", transformed)     

                if ( str( transformed ) in new_to_old_map.keys() ):
                            new_to_old_map[ str( transformed ) ].append([ x, y ])
                else:
                     new_to_old_map[ str( transformed ) ] = [ [ x, y ] ]     
                
                
                      
            
            elif( distance_from_center > inner_fisheye_radius and distance_from_center < outer_fisheye_radius ):
                
                new_img.putpixel( ( x, y ), (0, 0, 0) )  
            
                
                # print( mag_range_high, mag_range_low)
 
                drop_off = gaussian_drop_off( abs(distance_from_center), MM, outer_fisheye_radius )  
                # print(drop_off)  
                
                new_position = [ x_c + ( x - x_c ) * drop_off  , 
                                 y_c + ( y - y_c ) * drop_off  ]

                transformed = [ round( new_position[0] ), round( new_position[1] ) ]       

                # print( [x, y] ,"   ", transformed)     

                if ( str( transformed ) in new_to_old_map.keys() ):
                            new_to_old_map[ str( transformed ) ].append([ x, y ])
                else:
                     new_to_old_map[ str( transformed ) ] = [ [ x, y ] ]     
                     
                   



    for key in new_to_old_map.keys():
        new_coordinate = json.loads(key)

        old_coordinate_list = new_to_old_map[key]

        old_coordinate_bitmaps = []

        for item in old_coordinate_list:
            old_coordinate_bitmaps.append( img_pixels[ item[0], item[1] ] )


        r = 0
        g = 0
        b = 0

        for item in old_coordinate_bitmaps:
            r += item[0]
            g += item[1]
            b += item[2]

        r = round ( r / len( old_coordinate_bitmaps ) )
        g = round ( g / len( old_coordinate_bitmaps ) )  
        b = round ( b / len( old_coordinate_bitmaps ) )    
        
        # print(new_coordinate)

        new_img.putpixel( (new_coordinate[0], new_coordinate[1] ), (r, g, b) )


    new_img.save('fisheye_output.jpg')





apply_fisheye("Output.jpg", (540, 960), 100, 250, 1.5)

print("--- %s seconds ---" % (time.time() - start_time))