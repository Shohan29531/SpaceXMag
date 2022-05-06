from operator import index
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
import read_json


################################################################################

class Node:
  def __init__(self, x1, x2, y1, y2):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2

object_separation = 10

def get_rectangle_coordinates(x1, x2, y1, y2):
  return [ x1, x2, x2, x1, x1 ], [ y1, y1, y2, y2, y1 ]

################################################################################

## Read the input json file and build the maps

filename = '0.json'

maps = read_json.get_maps(filename)

parent_to_child = maps[0]
child_to_parent = maps[1]

index_to_coordinates = maps[2]
coordinates_to_index = maps[3]


################################################################################

## initialize the flags notifying that none of the nodes are optimized yet

max_id = max( index_to_coordinates.keys() )

is_optimized_flag_map = {}

for i in range( max_id + 1 ):
  is_optimized_flag_map[i] = False


for xx in range( max_id ):
  print(xx, "--> ", index_to_coordinates[xx][0], ",", index_to_coordinates[xx][2], ",", index_to_coordinates[xx][1], ",", index_to_coordinates[xx][3] )
################################################################################

## Find the order in which the nodes will be optimized (post order traversal)

traversal_order = []

def postorder_traversal( id ):

  if( id in parent_to_child.keys() ):
    children = parent_to_child[id]

    for child in children:
      postorder_traversal( child )

    traversal_order.append( id ) 

  else:
    traversal_order.append( id ) 

postorder_traversal(0)

################################################################################

## optimize function

def optimize_space( root_id ):


  root_coordinates = index_to_coordinates[root_id]

  root = Node(root_coordinates[0], root_coordinates[2], root_coordinates[1], root_coordinates[3])

  children = []
  children_ids = parent_to_child[root_id]

  for children_id in children_ids:
    child_coordinates = index_to_coordinates[children_id]
    child = Node(child_coordinates[0], child_coordinates[2], child_coordinates[1], child_coordinates[3])
    children.append(child)

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

    m.Equation( X[j] > X[0] + object_separation )
    m.Equation( Y[j] > Y[0] + object_separation )

    m.Equation( X[1] > X[j+1] + object_separation )
    m.Equation( Y[1] > Y[j+1] + object_separation )


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
        m.Equation( X[j+1] + object_separation < X[l] )
      elif ( code == 'R' ):
        m.Equation( X[l+1] + object_separation < X[j])  

      if ( code == 'T' ):
        m.Equation( Y[l] > Y[j+1] + object_separation)
      elif( code == 'B' ):
        m.Equation ( Y[j] > Y[l+1] + object_separation)    

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


  for row in relative_row_col_matrix:
    print(row)

  ################################################################################
  # objective function
  m.Minimize( root_area - children_area )

  m.solve(disp=False)



