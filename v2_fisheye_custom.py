from cmath import sin
import concurrent.futures
import enum
from hashlib import new
import itertools
import json
import logging
import math
from pathlib import Path

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
from PIL import Image, ImageOps
import pickle

import os
import glob

import json
from operator import index, inv
import collections


D = 1.46

def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )



def G(x):
    # print(x)
    num = (D+1)*x
    denom = D*x + 1
    
    return num*1.0/denom


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


    for x in range(dim_x):
        for y in range(dim_y):
            
            d_norm_x = x - x_c
            d_norm_y = y - y_c
            
            d_max_x = x_c
            d_max_y = y_c
            
            transformed = [G( d_norm_x/d_max_x ) * d_max_x + x_c,
                           G( d_norm_y/d_max_y ) * d_max_y + y_c]
            
            # print("   ",[x, y], "   ", transformed)


    new_img = img.copy()

    for i in range(dim_x):
        for j in range(dim_y):
            new_img.putpixel( (i, j), (0, 0, 0))

    ## if MM > 1:

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

        new_img.putpixel( (new_coordinate[0], new_coordinate[1] ), (r, g, b) )


    new_img.save('fisheye_output.jpg')





apply_fisheye("Output.jpg", (540, 960), 250, 350, 2)


# print(json.loads('[2, 3]'))