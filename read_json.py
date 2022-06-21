import json
from operator import index, inv
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
    elif( node['visibility'] != 'visible' ):
      node_valididty_map[ node['id'] ] = False 
    elif( node['visible-to-user'] != True ):
      node_valididty_map[ node['id'] ] = False  

    elif temp_coordinates[0] < 0 or temp_coordinates[1] < 0 or temp_coordinates[2] < 0 or temp_coordinates[3] < 0:
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
    for i in range(50):
        remove_duplications()
    remove_invalid_nodes()    
    print(parent_to_child)


def remove_invalid_nodes():
    invalid_nodes = []

    for key in node_valididty_map.keys():
        if(node_valididty_map[key] == False):
            invalid_nodes.append(key)

    parents = sorted(parent_to_child.keys())

    for parent in parents:
        if parent in parent_to_child.keys():
            if node_valididty_map[parent] == False:
                parent_to_child.pop(parent, None)
                continue
             
            children_of_current_parent = parent_to_child[parent] 
            for child in children_of_current_parent:
                if child in children_of_current_parent:
                    if node_valididty_map[child] == False:
                        children_of_current_parent.remove(child)

                        parent_to_child[parent] = children_of_current_parent




def remove_duplications():

    parents = sorted(parent_to_child.keys())

    for parent in parents:
        if parent in parent_to_child.keys():
            children_of_current_parent = parent_to_child[parent]
            for child in children_of_current_parent:
                if index_to_coordinates[child] == index_to_coordinates[parent]:
                    handle_duplication(parent, child)




def handle_duplication(parent, child):
    children_of_child = []
    if child in parent_to_child.keys():
        children_of_child = parent_to_child[child]

    children_of_parent = parent_to_child[parent]

    ## update the chain 
    children_of_parent.remove(child)
    
    for item in children_of_child:
        children_of_parent.append(item) 

    parent_to_child[parent] = children_of_parent 

    ## remove the duplicate node from chain
    parent_to_child.pop(child, None)

    ## update the child_to_parent map

    ## make the duplicate child invalid
    node_valididty_map[child] = False





def get_maps(filename, imagename):

    main( filename, imagename )

    return [ parent_to_child, child_to_parent, index_to_coordinates, coordinates_to_index, node_valididty_map ]



maps = get_maps( '10000.json', '10000.jpg' )

print(maps)

img = Image.open( '10000.jpg' )
for key in index_to_coordinates.keys():
    if( node_valididty_map[ key ] == False):
        continue
    coordinate = index_to_coordinates[key]

    img2 = img.crop( ( coordinate[0], coordinate[1], coordinate[2], coordinate[3] ) )
    img2.save( "image_segments/" + str(key) + ".png" )   



# for key in sorted(parent_to_child.keys()):
#     print(key, parent_to_child[ key ])   

# for key in index_to_coordinates.keys():
#     if( node_valididty_map[ key ] == False):
#         continue
#     print(key, index_to_coordinates[ key ])    

