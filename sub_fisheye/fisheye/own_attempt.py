from traceback import print_tb
import numpy as np
import matplotlib.pyplot as pl

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
from sklearn.metrics import euclidean_distances
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

from fisheye import fisheye

start_time = time.time()


boundary_circle_width = 20
boundary_circle_color = (0, 255, 0)


img = Image.open("Output.jpg")
dim_x, dim_y = img.size
# img.show()

print(dim_x, dim_y)

img_pixels = img.load()

new_img = img.copy()

fisheye_coordinates = []
fisheye_focus = [960, 960]
fisheye_radius = 200


def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )

for i in range(0, dim_x):
    for j in range(0, dim_y):
        
        dist = get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j)
        
        if dist > ( fisheye_radius + boundary_circle_width ):
            continue
        elif dist >= fisheye_radius  and dist <= (fisheye_radius + boundary_circle_width):
            new_img.putpixel( ( i, j ), boundary_circle_color )
            continue
        
        fisheye_coordinates.append([i, j]) 
   

F = fisheye( R = fisheye_radius, d = 1.5, xw = 0.4 )
F.set_focus( fisheye_focus )

F.set_mode('Sarkar')
original_coordinates = F.inverse_radial_2D(fisheye_coordinates) 
        
      
for i in range(len(fisheye_coordinates)):
    
    new = [ fisheye_coordinates[i][0], fisheye_coordinates[i][1] ] 
    old = [ original_coordinates[i][0], original_coordinates[i][1] ] 
    
    current_pixel  = img_pixels[ old[0], old[1] ]
      
    new_img.putpixel( ( new[0], new[1] ), current_pixel )

new_img.save("fisheye_applied.jpg")



print("--- %s seconds ---" % (time.time() - start_time))
        

