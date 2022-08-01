import cv2
from cv2 import EVENT_MOUSEMOVE

import custom_fisheye_effect

img = cv2.imread('Output.jpg')
img = cv2.resize( img, (540, 960) )
cv2.imshow('image', img)


def mouse_events( event, x, y, flags, param ):
    
    ## Left button click
    if( event == cv2.EVENT_LBUTTONDOWN ):
        font = cv2.FONT_HERSHEY_TRIPLEX
        LB = 'Left Button'
        cv2.putText( img, LB, (x, y), font, 1, (255, 255, 0), 2 )
        cv2.imshow( 'image', img )
    
    ## Right button click    
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        RB = 'Right Button'
        cv2.putText( img, RB, (x, y), font, 1, (0, 255, 255), 2 )
        cv2.imshow( 'image', img )
    
    ## Scroll button up    
    elif( event == cv2.EVENT_MBUTTONUP ):
        print( "Zoom in here" )    
    
    ## Scroll button down
    elif( event == cv2.EVENT_MBUTTONDOWN ):
        print( "Zoom out here" )        
    
    ## Mouse cursor hover    
    elif( event == EVENT_MOUSEMOVE ):
        print( "(", x, y, ")" )

 
        


cv2.setMouseCallback( 'image', mouse_events )
cv2.waitKey( 0 )
cv2.destroyAllWindows( )
