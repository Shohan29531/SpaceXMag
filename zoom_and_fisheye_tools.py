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


def get_elliptical_distance( p, q, a, b, x, y):

    dist = b**2 * ( x - p )**2 + a**2 * ( y - q )**2
    dist = math.sqrt( dist )

    return dist


def apply_fisheye_effect_circular( 
    img_file, 
    fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.0,
    model = 'Sarkar', 
    boundary_circle_width = 5, 
    boundary_circle_color = ( 0, 255, 0 ), 
    output_file_name = 'fisheye_applied.jpg' 
    ):

    start = time.time()

    img = convert_from_cv2_to_image( img_file )
    dim_x, dim_y = img.size
    
    img_pixels = img.load()

    new_img = img.copy()

    fisheye_coordinates = []
    
    effective_fisheye_radius = ( fisheye_radius + boundary_circle_width )

    for i in range( fisheye_focus[0] - effective_fisheye_radius, 
                   fisheye_focus[0] + effective_fisheye_radius ):
        for j in range( fisheye_focus[1] - effective_fisheye_radius, 
                   fisheye_focus[1] + effective_fisheye_radius ):
        
            if( i >= dim_x or i < 0 ):
                continue
            if( j >= dim_y or j < 0 ):
                continue
        
            dist = get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j )
            
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
    
    print("--- %s seconds ---" % (time.time() - start))

    return convert_from_image_to_cv2( new_img )


def apply_fisheye_effect_elliptical( 
    img_file, 
    fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.0,
    model = 'Sarkar', 
    boundary_circle_width = 5, 
    boundary_circle_color = ( 0, 255, 0 ), 
    output_file_name = 'fisheye_applied.jpg' 
    ):

    start = time.time()

    img = convert_from_cv2_to_image( img_file )
    dim_x, dim_y = img.size
    
    img_pixels = img.load()

    new_img = img.copy()

    fisheye_coordinates = []


    primary_axis = fisheye_radius
    secondary_axis = int( fisheye_radius * 0.6 )

    effective_primary_axis = primary_axis + boundary_circle_width
    effective_secondary_axis = secondary_axis + boundary_circle_width

    # effective_fisheye_radius = ( fisheye_radius + boundary_circle_width )

    for i in range( fisheye_focus[0] - effective_primary_axis, 
                   fisheye_focus[0] + effective_primary_axis ):
        for j in range( fisheye_focus[1] - effective_secondary_axis, 
                   fisheye_focus[1] + effective_secondary_axis ):
        
            if( i >= dim_x or i < 0 ):
                continue
            if( j >= dim_y or j < 0 ):
                continue
        
            dist = get_elliptical_distance( fisheye_focus[0], fisheye_focus[1], primary_axis, secondary_axis, i, j )

            effective_dist = get_elliptical_distance( fisheye_focus[0], fisheye_focus[1], effective_primary_axis, effective_secondary_axis, i, j )
            
            if effective_dist > ( effective_primary_axis * effective_secondary_axis ):
                continue
            elif dist >= ( primary_axis * secondary_axis)  and effective_dist < ( effective_primary_axis * effective_secondary_axis ):
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


def apply_fisheye_effect_rectangular( 
    img_file, 
    fisheye_focus, 
    fisheye_radius, 
    d = 1.5, 
    xw = 0.0,
    model = 'Sarkar', 
    boundary_circle_width = 5, 
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



def apply_basic_magnification( 
    img_file,
    zoom_center,
    rectangle_length,
    rectangle_width, 
    magnification_level,
    boundary_width = 2,
    boundary_circle_color = ( 0, 255, 0 ),
    ):

    start = time.time()

    img = convert_from_cv2_to_image( img_file )
    dim_x, dim_y = img.size
    
    img_pixels = img.load()

    new_img = img.copy()

    magnified_coordinates = []

    effective_rectangle_length = rectangle_length + boundary_width
    effective_rectangle_width = rectangle_width + boundary_width
    
    # effective_fisheye_radius = ( fisheye_radius + boundary_circle_width )

    for i in range( zoom_center[0] - effective_rectangle_length, 
                   zoom_center[0] + effective_rectangle_length ):
        for j in range( zoom_center[1] - effective_rectangle_width, 
                   zoom_center[1] + effective_rectangle_width ):
        
            if( i >= dim_x or i < 0 ):
                continue
            if( j >= dim_y or j < 0 ):
                continue

            dist_x = abs( zoom_center[0] - i )
            dist_y = abs( zoom_center[1] - j )
        
            # dist = get_euclidean_distance( fisheye_focus[0], fisheye_focus[1], i, j )
            
            if ( dist_x >= rectangle_length  and dist_x <= effective_rectangle_length ) or ( dist_y >= rectangle_width  and dist_y <= effective_rectangle_width ):
                new_img.putpixel( ( i, j ), boundary_circle_color )
                continue
        
            magnified_coordinates.append( [i, j] ) 


    for i in range(len(magnified_coordinates)):
    
        new = [ magnified_coordinates[i][0], magnified_coordinates[i][1] ] 

        dist_x = new[0] - zoom_center[0] 
        dist_y = new[1] - zoom_center[1]

        int( zoom_center[0] + ( dist_x / magnification_level ) )


        old = [ int( zoom_center[0] + ( dist_x / magnification_level ) ),
                int( zoom_center[1] + ( dist_y / magnification_level ) ) ] 
        
        current_pixel  = img_pixels[ old[0], old[1] ]
        
        new_img.putpixel( ( new[0], new[1] ), current_pixel )
    
    print("--- %s seconds ---" % (time.time() - start))

    return convert_from_image_to_cv2( new_img )


def zoom_at_point(img, cursor_position, zoom = 1, reverse_horizontal_scrolling = False, zoom_center = None):


    org_height, org_width, _ = [i for i in img.shape]

    zoomed_height, zoomed_width, _ = [ zoom * i for i in img.shape ]
    
    
    if zoom_center is None:
         cx, cy = org_width/2, org_height/2
    else:
         cx, cy = [ c for c in zoom_center ]



    if reverse_horizontal_scrolling:
        deviation_from_center = ( 
            cursor_position[1] - cy, 
        -( cursor_position[0] - cx )
        ) 
    else:
        deviation_from_center = ( 
            cursor_position[1] - cy, 
            cursor_position[0] - cx
        )             

        

    ## adjust the deviation based on zoom

    dim_diff = [ zoomed_height - org_height, zoomed_width - org_width]

    deviation_from_center = [ 
        int( dim_diff[0] * ( deviation_from_center[0] / (org_height/2) ) ), 
        int( dim_diff[1] * ( deviation_from_center[1] / (org_width/2) ) )
    ]  
    
    img = cv2.resize( img, (0, 0), fx = zoom, fy = zoom)

    y1 = int( round(cy - zoomed_height/zoom * .5) + deviation_from_center[0] ) 
    y2 = int( round(cy + zoomed_height/zoom * .5) + deviation_from_center[0] )

    x1 = int( round(cx - zoomed_width/zoom * .5) + deviation_from_center[1] ) 
    x2 = int( round(cx + zoomed_width/zoom * .5) + deviation_from_center[1] )


    if y1 < 0:
        y1 = 0
        y2 = y1 + org_height
    elif y2 > int( zoomed_height ):
        y2 = int( zoomed_height )
        y1 = y2 - org_height    

    if x1 < 0:
        x1 = 0
        x2 = x1 + org_width
    elif x2 > int( zoomed_width ):
        x2 = int( zoomed_width )  
        x1 = x2 - org_width
      
    
    img = img[ y1 : y2, x1 : x2 ]
    
    return img


