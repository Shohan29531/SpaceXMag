from email.policy import default
from json import tool
import cv2
import os
import json
import time
import sys

import zoom_and_fisheye_tools as tools



def uniquify( path ):
    filename, extension = os.path.splitext(path)
    counter = 0

    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1

    return path




def render_new_image(img, x, y):

    new_img = tools.zoom_at_point(
        img = img,
        zoom = current_magnification,
        cursor_position = (x, y), 
        reverse_horizontal_scrolling = reverse_horizontal_scrolling,
        zoom_center = None,
    )

    cv2.imshow( input_file_name, new_img )  



def mouse_events( event, x, y, flags, param ):  

    global pos_x, pos_y, current_magnification, mouse_moved

    pos_x = x
    pos_y = y

    

    ## Left button click
    ## zoom in
    if( event == cv2.EVENT_LBUTTONDOWN ):

        print("zoom in")

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
                dim_x = dim_x, 
                dim_y = dim_y
                )
    
    ## Right button click    
    ## zoom out
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        print("zoom out")

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
                dim_x = dim_x, 
                dim_y = dim_y
                )

                
    ## Mouse cursor hover    
    elif( event == cv2.EVENT_MOUSEMOVE ):
        mouse_moved = mouse_moved + 1

        if( mouse_moved == int ( 5 * current_magnification ) ):
            render_new_image( img = img, x = x, y = y )  
            mouse_moved = 0

        record_event(
                username = username,
                event_device = "Mouse", 
                event_type = "CURSOR_MOVED", 
                x = pos_x, 
                y = pos_y, 
                time = time.time(), 
                img_id = file_id, 
                current_magnification = current_magnification,
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
    current_magnification,
    dim_x,
    dim_y,

):
    global event_list

    event = {}

    event[ "img_id" ] = img_id
    event[ "dim_x" ] = dim_x
    event[ "dim_y" ] = dim_y

    event[ "current_magnification" ] = current_magnification
    event[ "base_magnification" ] = base_magnification

    event[ "username" ] = username
    event[ "event_device" ] = event_device
    event[ "event_type" ] = event_type
    event[ "x" ] = x
    event[ "y" ] = y
    event[ "time" ] = time - start

    events = event_list[ "events" ]
    events.append( event )
    event_list[ "events" ] = events

    with open( "temp_logs/" + username_unique, "w") as outfile:
        json.dump(event_list, outfile)





if __name__ == "__main__":

    start = time.time()

    original = True
    space_optimized = False

    org_T1 = [2535, 169, 2084]
    spc_T1 = [2778, 327, 1530]

    org_T2 = [3800, 1517, 366]
    spc_T2 = [835, 1002, 300]

    org_T3 = [17]
    spc_T3 = [86]


    target_array = []
    task = 1
    ## argv[1] is for original or space_optimized
    ## true for space optimized, false for original
    if sys.argv[1] == 'False':
        space_optimized = True
        original = False

    ## argv[2] is the id of the task (one of 1, 2, or 3)    
    task = int( sys.argv[2] )  
 
  
    if task == 1 and original == True:
        target_array = org_T1
    elif task == 2 and original == True:
        target_array = org_T2    
    elif task == 3 and original == True:
        target_array = org_T3  

    elif task == 1 and original == False:
        target_array = spc_T1  
    elif task == 2 and original == False:
        target_array = spc_T2 
    elif task == 3 and original == False:
        target_array = spc_T3 

    print(target_array)     



    for file_id in target_array:

        user_data = []
        with open('user_data.txt') as f:
            user_data = [line.rstrip() for line in f]

        reverse_horizontal_scrolling = 'False'    

        username = user_data[0]
        screen_size = float( user_data[1] )
        reverse_horizontal_scrolling = user_data[2]


        if original:
            input_file_name = str(file_id) + ".jpg"
            username_unique = uniquify( username + "_Task" + str( task ) + "_fullscreen_" + str( file_id ) + "_org.json" )
        if space_optimized:
            input_file_name = str(file_id) + "_output.jpg"
            username_unique = uniquify( username + "_Task" + str( task ) + "_fullscreen_" + str( file_id ) + "_spc.json" )
 


        img = cv2.imread(input_file_name)
        dim_x, dim_y = img.shape[1], img.shape[0]

        min_magnification = 1
        max_magnification = 10

        step_size_mag = ( max_magnification - min_magnification ) / 8

        current_magnification = 1
        base_magnification = tools.get_screen_height( screen_size ) / tools.get_screen_height( 13 )

        cv2.namedWindow(input_file_name, cv2.WINDOW_GUI_NORMAL)
        
        cv2.resizeWindow(input_file_name, 640, 1140 )
        cv2.imshow( input_file_name, img )

        pos_x = 0
        pos_y = 0

        event_list = {}
        event_list[ "events" ] = []

        mouse_moved = 0

        cv2.setMouseCallback( input_file_name, mouse_events )

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
                    dim_x = dim_x, 
                    dim_y = dim_y
                    )

                break

        with open( "logs/" + username_unique , "w") as outfile:
            json.dump(event_list, outfile)
        cv2.destroyAllWindows( )
