import json
from PIL import Image


current_index = 0

parent_to_child = {}
child_to_parent = {}

index_to_coordinates = {}
coordinates_to_index = {}

node_valididty_map = {}

given_dim_x = 1440
given_dim_y = 2560

def assign_id(node):
    
    global current_index
    node['id'] = current_index
    # print(current_index)
    current_index += 1
    

    if ( 'children' in node.keys() ):
        children_of_current_node = node['children']

        for child in children_of_current_node:
            assign_id(child)


def build_maps(node, x_ratio, y_ratio):

    temp_coordinates = node['bounds']

    temp_coordinates[0] = round( temp_coordinates[0] * x_ratio )
    temp_coordinates[2] = round( temp_coordinates[2] * x_ratio )

    temp_coordinates[1] = round( temp_coordinates[1] * y_ratio )
    temp_coordinates[3] = round( temp_coordinates[3] * y_ratio )
    
    index_to_coordinates[ node['id'] ] = temp_coordinates  
    coordinates_to_index[ str( temp_coordinates ) ] = node['id']

    area = abs ( temp_coordinates[0] - temp_coordinates[2] ) * abs ( temp_coordinates[1] - temp_coordinates[3] ) 

    if( area == 0 ):
        node_valididty_map[ node['id'] ] = False
    elif( node['visibility'] == 'invisible' ):
      node_valididty_map[ node['id'] ] = False  
    else:
        node_valididty_map[ node['id'] ] = True    
    
    if ( 'children' in node.keys() ):
        children_of_current_node = node['children']

        for child in children_of_current_node:
            build_maps(child, x_ratio, y_ratio)


def assign_children_to_parents(node):

    if ( 'children' in node.keys() ):
        children_of_current_node = node['children']
        temp = []
        for child in children_of_current_node:
            assign_children_to_parents(child)
            temp.append( child['id'] )
        parent_to_child[ node['id'] ] = temp
             


def assign_parent_to_children():
    for item in parent_to_child.keys():
        parent = item
        children = parent_to_child[ parent ]

        for child in children:
            child_to_parent[ child ] = parent



def main(filename, imagename):
    with open(filename) as d:
        dictData = json.load(d)

    img = Image.open(imagename)
    dim_x, dim_y = img.size

    x_ratio = dim_x * 1.0 / given_dim_x
    y_ratio = dim_y * 1.0 / given_dim_y

    root = dictData['activity']['root']

    assign_id(root)
    build_maps(root, x_ratio, y_ratio)
    assign_children_to_parents(root)
    assign_parent_to_children()



def get_maps(filename, imagename):

    main( filename, imagename )

    return [ parent_to_child, child_to_parent, index_to_coordinates, coordinates_to_index, node_valididty_map ]



maps = get_maps( '100.json', '100.jpg' )

print(maps)

img = Image.open( '100.jpg' )
for key in index_to_coordinates.keys():
    if( node_valididty_map[ key ] == False):
        continue
    coordinate = index_to_coordinates[key]

    img2 = img.crop( ( coordinate[0], coordinate[1], coordinate[2], coordinate[3] ) )
    img2.save( "image_segments/" + str(key) + ".png" )   