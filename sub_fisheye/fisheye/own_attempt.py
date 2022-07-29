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




img = Image.open("Output.jpg")
dim_x, dim_y = img.size
# img.show()

print(dim_x, dim_y)

img_pixels = img.load()


original = []
fisheye_focus = [540, 960]
fisheye_radius = 150


def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )

for i in range(0, dim_x):
    for j in range(0, dim_y):
        if get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j) >= fisheye_radius:
            continue
        original.append([i, j]) 




      

F = fisheye( R = fisheye_radius, d = 3 )
F.set_focus( fisheye_focus )

F.set_mode('Sarkar')
transformed = F.radial_2D(original) 



    
img_pixels = img.load()
new_img = img.copy()

for i in range(0, dim_x):
    for j in range(0, dim_y):
        new_img.putpixel( ( i, j ), (0, 0, 0) )

   
        
for i in range(len(original)):
    
    old = [ original[i][0], original[i][1] ] 
    new = [ transformed[i][0], transformed[i][1] ] 
    
    current_pixel  = img_pixels[ old[0], old[1]]
      
    new_img.putpixel( ( new[0], new[1] ), current_pixel )
              
# new_img.show()

new_img.save("fisheye_applied.jpg")



print("--- %s seconds ---" % (time.time() - start_time))
        

