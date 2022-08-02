from bdb import effective
from cv2 import rectangle
import numpy as np
import math
import time
import cv2
from PIL import Image

from fisheye import fisheye


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # return np.asarray(img)


def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )


def apply_fisheye_effect( 
    img_file, 
    fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.0,
    model = 'Sarkar', 
    boundary_circle_width = 10, 
    boundary_circle_color = ( 0, 255, 0 ), 
    output_file_name = 'fisheye_applied.jpg' 
    ):

    start = time.time()

    img = convert_from_cv2_to_image( img_file )
    dim_x, dim_y = img.size
    
    img_pixels = img.load()

    new_img = img.copy()

    fisheye_coordinates = []


    rectangle_length = int( fisheye_radius ) 
    rectangle_width = int( fisheye_radius * 0.6)

    
    effective_rectangle_length = rectangle_length + boundary_circle_width
    effective_rectangle_width = rectangle_width + boundary_circle_width
    
    # effective_fisheye_radius = ( fisheye_radius + boundary_circle_width )

    for i in range( fisheye_focus[0] - effective_rectangle_length, 
                   fisheye_focus[0] + effective_rectangle_length ):
        for j in range( fisheye_focus[1] - effective_rectangle_width, 
                   fisheye_focus[1] + effective_rectangle_width ):
        
            if( i >= dim_x or i < 0 ):
                continue
            if( j >= dim_y or j < 0 ):
                continue

            dist_x = abs( fisheye_focus[0] - i )
            dist_y = abs( fisheye_focus[1] - j )
        
            # dist = get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j )
            
            if ( dist_x >= rectangle_length  and dist_x <= effective_rectangle_length ) or ( dist_y >= rectangle_width  and dist_y <= effective_rectangle_width ):
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
    
    print("--- %s seconds ---" % (time.time() - start))

    return convert_from_image_to_cv2( new_img )


# img = cv2.imread( 'Output.jpg' )

# apply_fisheye_effect(img_file = img, fisheye_focus = (540, 960), fisheye_radius = 200 )
        

