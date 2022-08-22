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



def render_new_image(img, x, y, lens_shape = 'circular'):

    img = cv2.resize( img, ( int( dim_x * scale_factor_computation ), int( dim_y * scale_factor_computation ) ) )

    if ( lens_shape == 'circular'):
        new_img = tools.apply_fisheye_effect_circular( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )

    elif ( lens_shape == 'elliptical'):
        new_img = tools.apply_fisheye_effect_elliptical( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )   

    else:
        new_img = tools.apply_fisheye_effect_rectangular( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )   

    cv2.imshow( 'image', new_img )  



def mouse_events( event, x, y, flags, param ):  

    global current_fisheye_radius, d_index, xw_index, lens_shapes_index, pos_x, pos_y, scale_factor_computation

    pos_x = x
    pos_y = y


    ## Left button click
    ## zoom in
    if( event == cv2.EVENT_LBUTTONDOWN ):

        print("zoom in")
        
        current_fisheye_radius += step_size

        if ( current_fisheye_radius >= max_fisheye_radius ):
            current_fisheye_radius = max_fisheye_radius

        scale_factor_computation -= comp_step_size

        if( scale_factor_computation <= scale_factor_computation_min ):
            scale_factor_computation = scale_factor_computation_min 

        print(scale_factor_computation)      

        d_index = d_index + 1

        if( d_index == len(d) ):
            d_index = d_index -1

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] ) 

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "LEFT_BUTTON", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                fisheye_radius = current_fisheye_radius, fisheye_focus_shape = lens_shapes[ lens_shapes_index ], 
                d = d[ d_index ], 
                xw = xw[ xw_index ], 
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )
    
    ## Right button click    
    ## zoom out
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        print("zoom out")

        current_fisheye_radius -= step_size

        if ( current_fisheye_radius < min_fisheye_radius ):
            current_fisheye_radius = min_fisheye_radius


        scale_factor_computation += comp_step_size

        if( scale_factor_computation >= scale_factor_computation_max ):
            scale_factor_computation = scale_factor_computation_max 

        print(scale_factor_computation)   

        d_index = d_index - 1

        if( d_index == -1 ):
            d_index = 0

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )  

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "RIGHT_BUTTON", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                fisheye_radius = current_fisheye_radius, fisheye_focus_shape = lens_shapes[ lens_shapes_index ], 
                d = d[ d_index ], 
                xw = xw[ xw_index ], 
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )

                
    ## Mouse cursor hover    
    elif( event == cv2.EVENT_MOUSEMOVE ):
        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )  

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "CURSOR_MOVED", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                fisheye_radius = current_fisheye_radius, fisheye_focus_shape = lens_shapes[ lens_shapes_index ], 
                d = d[ d_index ], 
                xw = xw[ xw_index ], 
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
    fisheye_radius,
    fisheye_focus_shape,
    d,
    xw,
    scale_factor_computation,
    dim_x,
    dim_y,

):
    # global event_list

    # event = {}

    # event[ "img_id" ] = img_id
    # event[ "dim_x" ] = dim_x
    # event[ "dim_y" ] = dim_y

    # event[ "scale_factor_computation" ] = scale_factor_computation

    # event[ "fisheye_radius" ] = fisheye_radius
    # event[ "fisheye_focus_shape" ] = fisheye_focus_shape
    # event[ "d" ] = d
    # event[ "xw" ] = xw

    # event[ "username" ] = username
    # event[ "event_device" ] = event_device
    # event[ "event_type" ] = event_type
    # event[ "x" ] = x
    # event[ "y" ] = y
    # event[ "time" ] = time - start

    # events = event_list[ "events" ]
    # events.append( event )
    # event_list[ "events" ] = events

    # with open( username_unique, "w") as outfile:
    #     json.dump(event_list, outfile)
    return 

if __name__ == "__main__":

    start = time.time()

    user_data = []
    with open('user_data.txt') as f:
        user_data = [line.rstrip() for line in f]

    username = user_data[0]
    screen_size = user_data[1]
    username_unique = uniquify( username + "_fisheye_mag" + ".json" )

    file_id = 'training_4959'

    # input_file_name = str(file_id) + ".jpg"
    input_file_name = str(file_id) + "_output.jpg"

    img = cv2.imread(input_file_name)
    dim_x, dim_y = img.shape[1], img.shape[0]

    scale_factor_computation_max =  ( 540 / dim_x ) 
    scale_factor_computation_min = ( 324 / dim_x ) 

    comp_step_size = ( scale_factor_computation_max - scale_factor_computation_min ) / 4
    scale_factor_computation = scale_factor_computation_max

    screen_length = 12


    min_fisheye_radius = dim_x * 0.15
    max_fisheye_radius = dim_x * 0.45
    step_size = int( ( max_fisheye_radius - min_fisheye_radius) / 4 )

    current_fisheye_radius = min_fisheye_radius



    d = [ 1.5, 2, 2.5, 3.0]
    xw = [0.6, 0.4, 0.2, 0]
    lens_shapes = ['circular', 'elliptical', 'rectangular']

    d_index = 0
    xw_index = 0
    lens_shapes_index = 0


    cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
    img = cv2.resize( img, ( int( dim_x * scale_factor_computation ), int( dim_y * scale_factor_computation ) ) )

    cv2.resizeWindow('image', 640, 1140 )
    cv2.imshow( 'image', img )

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
                fisheye_radius = current_fisheye_radius, fisheye_focus_shape = lens_shapes[ lens_shapes_index ], 
                d = d[ d_index ], 
                xw = xw[ xw_index ], 
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                )

            break
        ## if space is presssed, change the shape
        elif k == 32:
            print("shape change")
            lens_shapes_index += 1
            lens_shapes_index = lens_shapes_index % len( lens_shapes )

            render_new_image( img = img, x = pos_x, y = pos_y, lens_shape = lens_shapes[ lens_shapes_index ] )  

            record_event(
                username = username,
                event_device = "keyboard", 
                event_type = "SPACE", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                fisheye_radius = current_fisheye_radius, fisheye_focus_shape = lens_shapes[ lens_shapes_index ], 
                d = d[ d_index ], 
                xw = xw[ xw_index ], 
                scale_factor_computation = scale_factor_computation, 
                dim_x = dim_x, 
                dim_y = dim_y
                ) 

    # with open( username_unique, "w") as outfile:
    #     json.dump(event_list, outfile)
    cv2.destroyAllWindows( )
