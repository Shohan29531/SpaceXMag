import threading
import numpy as np
import math
import time
import cv2
from PIL import Image

from fisheye import fisheye
import joblib
from joblib import delayed, Parallel


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # return np.asarray(img)


def get_euclidean_distance( x0, y0, x1, y1 ):
    return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )


def get_elliptical_distance( p, q, a, b, x, y):

    dist = b**2 * ( x - p )**2 + a**2 * ( y - q )**2
    dist = math.sqrt( dist )

    return dist


def apply_fisheye_effect_circular_parallel( 
    img_file, 
    fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.0,
    model = 'Sarkar', 
    boundary_circle_width = 5, 
    boundary_circle_color = ( 0, 255, 0 )
    ):

    start = time.time()

    img = convert_from_cv2_to_image( img_file )
    dim_x, dim_y = img.size
    
    img_pixels = img.load()

    new_img = img.copy()
    
    effective_fisheye_radius = ( fisheye_radius + boundary_circle_width )

    list_i = [ i for i in range( fisheye_focus[0] - effective_fisheye_radius, 
                   fisheye_focus[0] + effective_fisheye_radius ) ]

    list_j = [ j for j in range( fisheye_focus[1] - effective_fisheye_radius, 
                   fisheye_focus[1] + effective_fisheye_radius ) ]  

    all_points = []

    for i in list_i:
        for j in list_j:
            all_points.append([i, j])               

    F = fisheye( R = fisheye_radius, d = d, xw = xw )
    F.set_focus( fisheye_focus )
    F.set_mode( model )                     

    delayed_funcs = [ delayed( parallel_task )( point, fisheye_focus, fisheye_radius, effective_fisheye_radius, dim_x, dim_y, boundary_circle_color, new_img, img_pixels, F ) for point in all_points ]

    # print(delayed_funcs)

    parallel_pool = Parallel( n_jobs = joblib.cpu_count(), prefer='threads' )

    parallel_pool(delayed_funcs)
   
    print("--- %s seconds ---" % (time.time() - start))

    return convert_from_image_to_cv2( new_img )






def parallel_task( 
    point,
    fisheye_focus, 
    fisheye_radius, 
    effective_fisheye_radius, 
    dim_x,
    dim_y,
    boundary_circle_color,
    new_img,
    img_pixels, 
    F
    ):

    i = point[0]
    j = point[1]
        
    if( i >= dim_x or i < 0 ):
        return
    if( j >= dim_y or j < 0 ):
        return
        
    dist = get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j )
            
    if dist > effective_fisheye_radius:
        return
    elif dist >= fisheye_radius  and dist <= effective_fisheye_radius:
        new_img.putpixel( ( i, j ), boundary_circle_color )
        return

    original_coordinates = F.inverse_radial_2D( [i,j] )

    new = [ i, j ] 
    old = [ original_coordinates[0], original_coordinates[1] ] 

    current_pixel  = img_pixels[ old[0], old[1] ]
        
    new_img.putpixel( ( new[0], new[1] ), current_pixel )

    