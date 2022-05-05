import json
from multiprocessing.dummy import current_process

current_index = 0

parent_to_child = {}
child_to_parent = {}

index_to_coordinates = {}
coordinates_to_index = {}

def assign_id(node):
    
    global current_index
    node['id'] = current_index
    # print(current_index)
    current_index += 1
    

    if ( 'children' in node.keys() ):
        children_of_current_node = node['children']

        for child in children_of_current_node:
            assign_id(child)


def build_maps(node):
    
    index_to_coordinates[ node['id'] ] =  node['bounds'] 
    coordinates_to_index[ str(node['bounds']) ] = node['id']
    
    if ( 'children' in node.keys() ):
        children_of_current_node = node['children']

        for child in children_of_current_node:
            build_maps(child)


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



def main(filename):
    with open(filename) as d:
        dictData = json.load(d)

    root = dictData['activity']['root']

    assign_id(root)
    build_maps(root)
    assign_children_to_parents(root)
    assign_parent_to_children()



def get_maps(filename):

    main(filename)

    return [ parent_to_child, child_to_parent, index_to_coordinates, coordinates_to_index ]