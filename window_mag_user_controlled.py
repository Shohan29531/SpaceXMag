import cv2
import os
import json
import time

import zoom_and_fisheye_tools as tools



def uniquify( path ):
    filename, extension = os.path.splitext(path)
    counter = 0

    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1

    return path



def render_new_image(img, x, y):

    img = cv2.resize( img, ( int( dim_x * scale_factor_computation ), int( dim_y * scale_factor_computation ) ) )

    new_img = tools.apply_basic_magnification( 
        img_file = img,
        zoom_center = ( x, y ),
        rectangle_length = int( current_rect_length * scale_factor_computation ) ,
        rectangle_width = int( current_rect_length * scale_factor_computation * 0.5 ),
        magnification_level = current_magnification
    )  

    cv2.imshow( 'image', new_img )  



def mouse_events( event, x, y, flags, param ):  

    global pos_x, pos_y, scale_factor_computation, current_rect_length, current_magnification

    pos_x = x
    pos_y = y

    print(x, y)


    ## Left button click
    ## zoom in
    if( event == cv2.EVENT_LBUTTONDOWN ):

        print("zoom in")
        
        # current_rect_length += step_size

        # if ( current_rect_length >= max_rect_length ):
        #     current_rect_length = max_rect_length

        scale_factor_computation -= comp_step_size

        if( scale_factor_computation <= scale_factor_computation_min ):
            scale_factor_computation = scale_factor_computation_min 

        print(scale_factor_computation)    

        current_magnification += step_size_mag

        if( current_magnification >= max_magnification ):  
            current_magnification = max_magnification


        render_new_image( img = img, x = x, y = y ) 

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "LEFT_BUTTON", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
                current_rectangle_length = current_rect_length,
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )
    
    ## Right button click    
    ## zoom out
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        print("zoom out")

        # current_rect_length -= step_size

        # if ( current_rect_length < min_rect_length ):
        #     current_rect_length = min_rect_length


        scale_factor_computation += comp_step_size

        if( scale_factor_computation >= scale_factor_computation_max ):
            scale_factor_computation = scale_factor_computation_max 

        print(scale_factor_computation)   

        current_magnification -= step_size_mag

        if( current_magnification < min_magnification ):  
            current_magnification = min_magnification

        render_new_image( img = img, x = x, y = y )  

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "RIGHT_BUTTON", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
                current_rectangle_length = current_rect_length,
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )

                
    ## Mouse cursor hover    
    elif( event == cv2.EVENT_MOUSEMOVE ):
        render_new_image( img = img, x = x, y = y)  

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "CURSOR_MOVED", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
                current_rectangle_length = current_rect_length,
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )


def record_event(
    username,
    event_device,
    event_type,
    x,
    y,
    time,
    img_id,
    scale_factor_computation,
    current_magnification,
    current_rectangle_length,
    dim_x,
    dim_y,

):
    global event_list

    event = {}

    event[ "img_id" ] = img_id
    event[ "dim_x" ] = dim_x
    event[ "dim_y" ] = dim_y

    event[ "scale_factor_computation" ] = scale_factor_computation

    event[ "current_magnification" ] = current_magnification
    event[ "current_rectangle_length" ] = current_rectangle_length
    event[ "current_rectangle_width" ] = int( current_rectangle_length * 0.5 )

    event[ "username" ] = username
    event[ "event_device" ] = event_device
    event[ "event_type" ] = event_type
    event[ "x" ] = x
    event[ "y" ] = y
    event[ "time" ] = time - start

    events = event_list[ "events" ]
    events.append( event )
    event_list[ "events" ] = events

    with open( username_unique, "w") as outfile:
        json.dump(event_list, outfile)

if __name__ == "__main__":

    start = time.time()

    username = "test"
    username_unique = uniquify( username + ".json" )

    file_id = 12419

    # input_file_name = str(file_id) + ".jpg"
    input_file_name = str(file_id) + "_output.jpg"

    img = cv2.imread(input_file_name)
    dim_x, dim_y = img.shape[1], img.shape[0]


    scale_factor_computation_max = 0.5
    scale_factor_computation_min = 0.3

    comp_step_size = ( scale_factor_computation_max - scale_factor_computation_min ) / 4
    scale_factor_computation = scale_factor_computation_max


    scale_factor_display = 0.5


    min_rect_length = dim_x * 0.2
    max_rect_length = dim_x * 0.45
    step_size = int( ( max_rect_length - min_rect_length) / 4 )

    current_rect_length = int( min_rect_length )

    

    min_magnification = 1
    max_magnification = 4

    step_size_mag = ( max_magnification - min_magnification ) / 4

    current_magnification = min_magnification

    cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
    img = cv2.resize( img, ( int( dim_x * scale_factor_computation ), int( dim_y * scale_factor_computation ) ) )

    cv2.imshow( 'image', img )
    cv2.resizeWindow('image', ( int( dim_x * scale_factor_display ), int( dim_y * scale_factor_display ) ))

    pos_x = 0
    pos_y = 0

    event_list = {}
    event_list[ "events" ] = []

    cv2.setMouseCallback( 'image', mouse_events )

    while True:
        k = cv2.waitKey(10)
        
        ## if esc is pressed, exit the program
        if k == 27:
            print("exit")

            record_event(
                username = username,
                event_device = "keyboard", 
                event_type = "ESC", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
                current_rectangle_length = current_rect_length,
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )

            break

        elif k == 32:
            print("rectnagle size change")

            current_rect_length += step_size

            if ( current_rect_length >= max_rect_length ):
                current_rect_length = min_rect_length        

            record_event(
                username = username,
                event_device = "keyboard", 
                event_type = "SPACE", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
                current_rectangle_length = current_rect_length,
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )

    with open( username_unique + "window_mag" , "w") as outfile:
        json.dump(event_list, outfile)
    cv2.destroyAllWindows( )
