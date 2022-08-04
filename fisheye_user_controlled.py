import cv2
from cv2 import EVENT_MOUSEMOVE
from cv2 import EVENT_FLAG_CTRLKEY

import custom_fisheye_effect_opencv as F


scale_factor = 0.5
current_fisheye_radius = 150
d = [ 1.5, 2, 2.5, 3.0]
xw = [0.6, 0.4, 0.2, 0]
lens_shapes = ['circular', 'elliptical', 'rectangular']

d_index = 0
xw_index = 0
lens_shapes_index = 0

img = cv2.imread('Output.jpg')
dim_x, dim_y = img.shape[1], img.shape[0]


cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow( 'image', img )
cv2.resizeWindow('image', ( int( dim_x * scale_factor ), int( dim_y * scale_factor ) ))



def render_new_image(img, x, y, lens_shape = 'circular'):

    if ( lens_shape == 'circular'):
        new_img = F.apply_fisheye_effect_circular( img_file = img, fisheye_focus = (x, y), fisheye_radius = current_fisheye_radius, d = d[ d_index ] )

    elif ( lens_shape == 'elliptical'):
        new_img = F.apply_fisheye_effect_elliptical( img_file = img, fisheye_focus = (x, y), fisheye_radius = current_fisheye_radius, d = d[ d_index ] )   

    else:
        new_img = F.apply_fisheye_effect_rectangular( img_file = img, fisheye_focus = (x, y), fisheye_radius = current_fisheye_radius, d = d[ d_index ] )    
    
    cv2.imshow( 'image', new_img )  


def mouse_events( event, x, y, flags, param ):  

    global current_fisheye_radius, d_index, xw_index, lens_shapes_index

    if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_LBUTTONDOWN:

        print("shape change")

        lens_shapes_index += 1
        lens_shapes_index = lens_shapes_index % len( lens_shapes )

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] ) 


    ## Left button click
    elif( event == cv2.EVENT_LBUTTONDOWN ):

        print("zoom in")
        
        current_fisheye_radius += 25

        if ( current_fisheye_radius >= 250 ):
            current_fisheye_radius = 250

        d_index = d_index + 1

        if( d_index == len(d) ):
            d_index = d_index -1

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] ) 
    
    ## Right button click    
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        print("zoom out")

        current_fisheye_radius -= 25

        if ( current_fisheye_radius < 150 ):
            current_fisheye_radius = 150

        d_index = d_index - 1

        if( d_index == -1 ):
            d_index = 0

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )  

    elif event == cv2.EVENT_MBUTTONDOWN:

        print("shape change")
        lens_shapes_index += 1
        lens_shapes_index = lens_shapes_index % len( lens_shapes )

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )     

              
    ## Mouse cursor hover    
    elif( event == cv2.EVENT_MOUSEMOVE ):
        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )   

     

cv2.setMouseCallback( 'image', mouse_events )
cv2.waitKey( 0 )
cv2.destroyAllWindows( )
