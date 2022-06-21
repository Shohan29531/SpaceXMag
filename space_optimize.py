from operator import index
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
from urllib3 import Retry
from PIL import Image


import os
import glob

import json
from operator import index, inv

object_separation = 0
current_index = 0

parent_to_child = {}
child_to_parent = {}

index_to_coordinates = {}
coordinates_to_index = {}

node_valididty_map = {}

given_dim_x = 1440
given_dim_y = 2560

input_img_dim_x = 0
input_img_dim_y = 0

traversal_order = []

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

    for invalid_node in invalid_nodes:
        index_to_coordinates.pop(invalid_node, None)                   


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


def main(filename, imagename):
    with open(filename) as d:
        dictData = json.load(d)

    img = Image.open(imagename)
    dim_x, dim_y = img.size

    global input_img_dim_x 
    input_img_dim_x = dim_x

    global input_img_dim_y 
    input_img_dim_y = dim_y

    x_ratio = dim_x * 1.0 / given_dim_x
    y_ratio = dim_y * 1.0 / given_dim_y

    root = dictData['activity']['root']

    assign_id(root)
    build_maps(root, x_ratio, y_ratio)
    assign_children_to_parents(root)
    assign_parent_to_children()
    for i in range(50):
        remove_duplications()
    for i in range(10):
        remove_invalid_nodes()    



################################################################################

class Node:
  def __init__(self, x1, x2, y1, y2):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2



def get_rectangle_coordinates(x1, x2, y1, y2):
  return [ x1, x2, x2, x1, x1 ], [ y1, y1, y2, y2, y1 ]



################################################################################

## Find the order in which the nodes will be optimized (post order traversal)

def postorder_traversal( id ):

  if( id in parent_to_child.keys() ):
    children = parent_to_child[id]

    for child in children:
      postorder_traversal( child )

    traversal_order.append( id ) 

  else:
    traversal_order.append( id ) 


################################################################################

## optimize function

def optimize_space( root_id ):

  print("Currently Optimizing: ", root_id)  

  root_coordinates = index_to_coordinates[root_id]

  root = Node( root_coordinates[0], root_coordinates[2], root_coordinates[1], root_coordinates[3] )

  children = []
  children_ids = []
  if root_id in parent_to_child.keys():
    children_ids = parent_to_child[root_id]
  else:
    return  

  for children_id in children_ids:
    child_coordinates = index_to_coordinates[children_id]
    child = Node( child_coordinates[0], child_coordinates[2], child_coordinates[1], child_coordinates[3] )
    children.append( child )

  dummy_root_area = abs( root_coordinates[0] -root_coordinates[2] ) * abs(root_coordinates[1] -root_coordinates[3] )

  dummy_children_area = 0

  for children_id in children_ids:
    child_coordinates = index_to_coordinates[children_id]
    child_area = abs(child_coordinates[0]- child_coordinates[2]) *  abs( child_coordinates[1] - child_coordinates[3] )
    dummy_children_area += child_area

  if (dummy_root_area == dummy_children_area):
    return  
  
  print(index_to_coordinates)

  # initialize the GEKKO model (non-linear optimizer)
  m = GEKKO(remote=False)

  ################################################################################

  # initialize the variables

  X = m.Array( m.Var, ( len( children ) + 1 ) * 2, lb=root.x1, ub=root.x2 )
  Y = m.Array( m.Var, ( len( children ) + 1 ) * 2, lb=root.y1, ub=root.y2 )

  for i in range(0, len(children) + 1):

    if ( i == 0 ):
      # handle root here
      j = i * 2
      X[j].value = root.x1
      X[j+1].value = root.x2

      Y[j].value = root.y1
      Y[j+1].value = root.y2

    else:
      # handle all the other nodes
      child = children[i-1]
      j = i * 2

      X[j].value = child.x1
      X[j+1].value = child.x2

      Y[j].value = child.y1
      Y[j+1].value = child.y2

  ################################################################################

  ## constraints

  # sum of children area must be lower than the parent's area

  root_area = abs( X[0] - X[1] ) * abs( Y[0] - Y[1] )

  children_area = 0

  for i in range(1, len(children) + 1):
    j = i * 2
    child = children[i-1]

    child_area = abs( X[j+1] - X[j] ) * abs( Y[j+1] - Y[j] )
    children_area += child_area

  m.Equation( root_area >= children_area)

  #######################################

  # Not changing the sizes and shapes of the children

  for i in range(1, len(children) + 1):
    j = i * 2
    child = children[i-1]

    m.Equation ( X[j+1] - X[j] == child.x2 - child.x1)
    m.Equation ( Y[j+1] - Y[j] == child.y2 - child.y1)


  #######################################

  # Boundary within the root

  for i in range(1, len(children) + 1):
    j = i * 2

    m.Equation( X[j] >= X[0] + object_separation )
    m.Equation( Y[j] >= Y[0] + object_separation )

    m.Equation( X[1] >= X[j+1] + object_separation )
    m.Equation( Y[1] >= Y[j+1] + object_separation )

  # max coordinate is bigger than the min coordinate

    # m.Equation( X[j+1] >= X[j] )
    # m.Equation( Y[j+1] >= Y[j] )

  #######################################

  # Relative positions of the children

  relative_position_matrix = [['N' for x in range(len(children) +1)] 
                              for y in range(len(children) +1)] 

  # print("RELATIVE POSITION MATRIX")

  # for row in relative_position_matrix:
  #   print(row)

  for i in range(1, len(children) + 1):
    first_child = children[i-1]
    for k in range(i+1, len(children) + 1):
      second_child = children[k-1]

      ## Left check
      if ( first_child.x2 <= second_child.x1 ):
        relative_position_matrix[i][k] = 'L'
        relative_position_matrix[k][i] = 'R'

    ## Right check
      if ( second_child.x2 <= first_child.x1 ):
        relative_position_matrix[i][k] = 'R'
        relative_position_matrix[k][i] = 'L'   


    ## Top check   
      if ( second_child.y1 >= first_child.y2 ):
        relative_position_matrix[i][k] = 'T'
        relative_position_matrix[k][i] = 'B' 

    ## Bottom check   
      if ( first_child.y1 >= second_child.y2 ):
        relative_position_matrix[i][k] = 'B'
        relative_position_matrix[k][i] = 'T'       


  for i in range(1, len(children) + 1):
    j = i * 2
    for k in range(i+1, len(children) + 1):
      l = k * 2

      code = relative_position_matrix[i][k]

      if ( code == 'L' ):
        m.Equation( X[j+1] + object_separation <= X[l] )
      elif ( code == 'R' ):
        m.Equation( X[l+1] + object_separation <= X[j])  

      if ( code == 'T' ):
        m.Equation( Y[l] >= Y[j+1] + object_separation)
      elif( code == 'B' ):
        m.Equation ( Y[j] >= Y[l+1] + object_separation) 

    # print("Pos: ")
    # for row in relative_position_matrix:
    #     print(row)         

  #######################################

  # Relative positions within rows and columns

  relative_row_col_matrix = [['N' for x in range(len(children) +1)] 
                              for y in range(len(children) +1)] 



  for i in range(1, len(children) + 1):
    first_child = children[i-1]
    for k in range(i+1, len(children) + 1):
      second_child = children[k-1]

      ## same row check
      if ( first_child.y2 == second_child.y2 and first_child.y1 == second_child.y1 ):
        relative_row_col_matrix[i][k] = 'SR'
        relative_row_col_matrix[k][i] = 'SR'

    ## same col check
      if ( first_child.x2 == second_child.x2 and first_child.x1 == second_child.x1 ):
        relative_row_col_matrix[i][k] = 'SC'
        relative_row_col_matrix[k][i] = 'SC'  


  for i in range(1, len(children) + 1):
    j = i * 2
    for k in range(i+1, len(children) + 1):
      l = k * 2

      code = relative_row_col_matrix[i][k]

      if ( code == 'SR' ):
        m.Equation( Y[j] == Y[l] )
        m.Equation( Y[j+1] == Y[l+1] )

      elif ( code == 'SC' ):
        m.Equation( X[j] == X[l] )
        m.Equation( X[j+1] == X[l+1] )


  ################################################################################
  # objective function

  m.Minimize( root_area - children_area )
#   m.options.IMODE=4
  m.solve(disp=False)

  ################################################################################
  # optimization finished, update the index_to_coordinates and coordinates_to_index maps
  
  # update root coordinates
  root_coordinates = [ round( X[0].value[0] ), round( Y[0].value[0] ), round( X[1].value[0] ),  round( Y[1].value[0] ) ]
  index_to_coordinates[ root_id ] = root_coordinates
  # coordinates_to_index[ str( root_coordinates ) ] = root_id

  # update children coordinates

  for i in range( 1, 1 + len( children ) ):
    j = i * 2

    child_coordinates = [ round( X[j].value[0] ), round( Y[j].value[0] ),  round( X[j+1].value[0] ), round( Y[j+1].value[0] ) ] 

    relevant_child_id = children_ids[i-1]

    child_old_coordinates = index_to_coordinates[relevant_child_id]

    index_to_coordinates[relevant_child_id] = child_coordinates

    if relevant_child_id in parent_to_child.keys():
        difference_in_coordinates = [ child_coordinates[0] - child_old_coordinates[0], child_coordinates[1] - child_old_coordinates[1], child_coordinates[2] - child_old_coordinates[2], child_coordinates[3] - child_old_coordinates[3] ]

        update_subtree_coordinates( relevant_child_id, difference_in_coordinates )
        # print("difference:\n ", difference_in_coordinates)


    # coordinates_to_index[ str( child_coordinates ) ] = relevant_child_id


def update_subtree_coordinates(local_root_id, difference):

    if local_root_id not in parent_to_child.keys():
        return

    children = parent_to_child[local_root_id]
    for child in children:
        child_old_coords = index_to_coordinates[child]
        child_new_coords = [ child_old_coords[0] + difference[0], child_old_coords[1] + difference[1], child_old_coords[2] + difference[2], child_old_coords[3] + difference[3]]

        index_to_coordinates[child] = child_new_coords

        update_subtree_coordinates(child, difference)


def save_image_segments(image_file):

    img = Image.open( image_file )
    for key in index_to_coordinates.keys():
        if( node_valididty_map[ key ] == False):
            continue
        coordinate = index_to_coordinates[key]

        img2 = img.crop( ( coordinate[0], coordinate[1], coordinate[2], coordinate[3] ) )
        img2.save( "image_segments/" + str(key) + ".jpg" )   




################################################################################

## Read the input json file and build the maps

image_id = 9700

jsonfile = str(image_id) + '.json'
image_file = str(image_id) + '.jpg'


main(jsonfile, image_file)
save_image_segments(image_file)

old_index_to_coordinates = index_to_coordinates.copy()
print(old_index_to_coordinates)
print(parent_to_child)

postorder_traversal(0)

print(traversal_order)

for current_id in traversal_order:
    optimize_space(current_id)

# print(old_index_to_coordinates)
print(parent_to_child)
print(index_to_coordinates)


all_valid_nodes = []

for node in node_valididty_map.keys():
    if( node_valididty_map[node] == True):
        all_valid_nodes.append(node)

print(all_valid_nodes)        

parents = [key for key in parent_to_child.keys()]

for parent in parents:
    if parent in all_valid_nodes:
        all_valid_nodes.remove(parent)
all_valid_leaves = all_valid_nodes  


### render the final image

final_output = Image.new('RGB', (input_img_dim_x, input_img_dim_y))

for im_id in all_valid_leaves:
  im =  Image.open( "image_segments/" + str(im_id) + '.jpg' ) 
  leaf_coordinates = index_to_coordinates[im_id]
  final_output.paste(im, (leaf_coordinates[0], leaf_coordinates[1]))

final_output.save('Output.jpg')

files = glob.glob('image_segments/*')
for f in files:
    os.remove(f)


