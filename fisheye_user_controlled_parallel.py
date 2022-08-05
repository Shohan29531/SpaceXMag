import cv2

import custom_fisheye_parallel as F

def render_new_image(img, x, y, lens_shape = 'circular'):

    if ( lens_shape == 'circular'):
        new_img = F.apply_fisheye_effect_circular_parallel( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )

    # elif ( lens_shape == 'elliptical'):
    #     new_img = F.apply_fisheye_effect_elliptical( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )   

    # else:
    #     new_img = F.apply_fisheye_effect_rectangular( img_file = img, fisheye_focus = (x, y), fisheye_radius = int( current_fisheye_radius * scale_factor_computation ), d = d[ d_index ] )    
    
    cv2.imshow( 'image', new_img )  



def mouse_events( event, x, y, flags, param ):  

    global current_fisheye_radius, d_index, xw_index, lens_shapes_index, pos_x, pos_y

    pos_x = x
    pos_y = y


    ## Left button click
    ## zoom in
    if( event == cv2.EVENT_LBUTTONDOWN ):

        print("zoom in")
        
        current_fisheye_radius += step_size

        if ( current_fisheye_radius >= max_fisheye_radius ):
            current_fisheye_radius = max_fisheye_radius

        d_index = d_index + 1

        if( d_index == len(d) ):
            d_index = d_index -1

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] ) 
    
    ## Right button click    
    ## zoom out
    elif( event == cv2.EVENT_RBUTTONDOWN ):
        
        print("zoom out")

        current_fisheye_radius -= step_size

        if ( current_fisheye_radius < min_fisheye_radius ):
            current_fisheye_radius = min_fisheye_radius

        d_index = d_index - 1

        if( d_index == -1 ):
            d_index = 0

        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )  

                
    ## Mouse cursor hover    
    elif( event == cv2.EVENT_MOUSEMOVE ):
        render_new_image( img = img, x = x, y = y, lens_shape = lens_shapes[ lens_shapes_index ] )   

     

if __name__ == "__main__":
    scale_factor_display = 0.4
    scale_factor_computation = 0.5
    current_fisheye_radius = 152


    min_fisheye_radius = 152
    max_fisheye_radius = 500
    step_size = int( ( max_fisheye_radius - min_fisheye_radius) / 4 )


    d = [ 1.5, 2, 2.5, 3.0]
    xw = [0.6, 0.4, 0.2, 0]
    lens_shapes = ['circular', 'elliptical', 'rectangular']

    d_index = 0
    xw_index = 0
    lens_shapes_index = 0

    img = cv2.imread('Output.jpg')
    dim_x, dim_y = img.shape[1], img.shape[0]


    cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)

    img = cv2.resize( img, ( int( dim_x * scale_factor_computation ), int( dim_y * scale_factor_computation ) ) )
    cv2.imshow( 'image', img )
    cv2.resizeWindow('image', ( int( dim_x * scale_factor_display ), int( dim_y * scale_factor_display ) ))

    pos_x = 0
    pos_y = 0

    cv2.setMouseCallback( 'image', mouse_events )


    while True:
        k = cv2.waitKey(10)
        
        ## if esc is pressed, exit the program
        if k == 27:
            print("exit")
            break
        ## if space is presssed, change the shape
        elif k == 32:
            print("shape change")
            lens_shapes_index += 1
            lens_shapes_index = lens_shapes_index % len( lens_shapes )

            render_new_image( img = img, x = pos_x, y = pos_y, lens_shape = lens_shapes[ lens_shapes_index ] )   


    cv2.destroyAllWindows( )
