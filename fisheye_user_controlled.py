import cv2
from cv2 import EVENT_MOUSEMOVE

import custom_fisheye_effect_opencv as F

scale_factor = 0.5
current_fisheye_radius = 150
d = [ 1.5, 2, 2.5, 3.0]
xw = [0.6, 0.4, 0.2, 0]

d_index = 0
xw_index = 0


img = cv2.imread('Output.jpg')



dim_x, dim_y = img.shape[1], img.shape[0]

print( dim_x, dim_y)

img = cv2.resize( img, ( int( dim_x * scale_factor ), int( dim_y * scale_factor ) ) )
cv2.imshow( 'image', img )


def mouse_events( event, x, y, flags, param ):  
    ## Left button click
    if( event == cv2.EVENT_LBUTTONDOWN ):
        
        # font = cv2.FONT_HERSHEY_TRIPLEX
        # LB = 'Left Button'
        # cv2.putText( img, LB, (x, y), font, 1, (255, 255, 0), 2 )
        

        ## zoom in
        global current_fisheye_radius, d_index, xw_index
        current_fisheye_radius += 25

        if ( current_fisheye_radius >= 250 ):
            current_fisheye_radius = 250

        d_index = d_index + 1

        if( d_index == len(d) ):
            d_index = d_index -1

        new_img = F.apply_fisheye_effect( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor ), d = d[ d_index ] )
        new_img = cv2.resize( new_img, ( int( dim_x * scale_factor ), int( dim_y * scale_factor ) ) )
        cv2.imshow( 'image', new_img )  
    
    ## Right button click    
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        # global current_fisheye_radius, d_index, xw_index
        current_fisheye_radius -= 25

        if ( current_fisheye_radius < 150 ):
            current_fisheye_radius = 150

        d_index = d_index - 1

        if( d_index == -1 ):
            d_index = 0

        new_img = F.apply_fisheye_effect( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor ), d = d[ d_index ] )
        new_img = cv2.resize( new_img, ( int( dim_x * scale_factor ), int( dim_y * scale_factor ) ) )
        cv2.imshow( 'image', new_img )  

    
    ## Scroll button up    
    elif( event == cv2.EVENT_MBUTTONUP ):
        return
    
    ## Scroll button down
    elif( event == cv2.EVENT_MBUTTONDOWN ):
        return

              
    ## Mouse cursor hover    
    elif( event == EVENT_MOUSEMOVE ):
        new_img = F.apply_fisheye_effect( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor ) )
        new_img = cv2.resize( new_img, ( int( dim_x * scale_factor ), int( dim_y * scale_factor ) ) )
        cv2.imshow( 'image', new_img )  



cv2.setMouseCallback( 'image', mouse_events )
cv2.waitKey( 0 )
cv2.destroyAllWindows( )
