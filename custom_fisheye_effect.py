import numpy as np
import math
import time
from PIL import Image

from fisheye import fisheye

def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )


def apply_fisheye_effect( 
    img_file, fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.4,
    model = 'Sarkar', 
    boundary_circle_width = 20, 
    boundary_circle_color = ( 0, 255, 0 ), 
    output_file_name = 'fisheye_applied.jpg' 
    ):

    img = Image.open(img_file)
    dim_x, dim_y = img.size
    img_pixels = img.load()

    new_img = img.copy()

    fisheye_coordinates = []

    for i in range(0, dim_x):
        for j in range(0, dim_y):
        
            dist = get_euclidean_distance( fisheye_focus[0], 
            fisheye_focus[1], i, j )
            
            if dist > ( fisheye_radius + boundary_circle_width ):
                continue
            elif dist >= fisheye_radius  and dist <= ( fisheye_radius + boundary_circle_width ):
                new_img.putpixel( ( i, j ), boundary_circle_color )
                continue
        
            fisheye_coordinates.append( [i, j] ) 

    F = fisheye( R = fisheye_radius, d = d, xw = xw )
    F.set_focus( fisheye_focus )

    F.set_mode( model )
    original_coordinates = F.inverse_radial_2D(fisheye_coordinates)

    for i in range(len(fisheye_coordinates)):
    
        new = [ fisheye_coordinates[i][0], fisheye_coordinates[i][1] ] 
        old = [ original_coordinates[i][0], original_coordinates[i][1] ] 
        
        current_pixel  = img_pixels[ old[0], old[1] ]
        
        new_img.putpixel( ( new[0], new[1] ), current_pixel )

    new_img.save(output_file_name) 


start_time = time.time()

apply_fisheye_effect(img_file = 'Output.jpg', fisheye_focus = (540, 960), fisheye_radius = 300 )

print("--- %s seconds ---" % (time.time() - start_time))
        

