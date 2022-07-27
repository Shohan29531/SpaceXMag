import concurrent.futures
import enum
import itertools
import json
import logging
import math
from pathlib import Path

import cv2 
import hydra
import numpy as np
import scipy.interpolate
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

    for x in range(dim_x):
        for y in range(dim_y):

            current_pixel = img_pixels[ x, y ]

            distance_from_center = get_euclidean_distance( x_c, y_c, x, y )

            if( distance_from_center <= inner_fisheye_radius):
                # print( distance_from_center, " -> inside the focus" )
                new_position = [ x_c + ( x - x_c ) / MM, 
                                 y_c + ( y - y_c ) / MM  ]

                print( [x, y] ,"   ", new_position)                 



            elif( distance_from_center > inner_fisheye_radius and distance_from_center < outer_fisheye_radius ):
                # print( distance_from_center, " -> distortion region" )
                continue

            elif( distance_from_center >= outer_fisheye_radius ):
                # print( "no change region (context region)" )   
                continue




apply_fisheye("Output.jpg", (540, 960), 80, 100, 3)


