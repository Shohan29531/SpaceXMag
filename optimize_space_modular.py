import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO


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

# the the object coordinates from file
with open("coords.txt") as file:
    lines = file.readlines()

children = []

is_root = True
for line in lines:
  coordinates = line.split(",")
  temp = []
  for coordinate in coordinates:
    temp.append(int(coordinate))
  print(temp)
  new_node = Node(temp[0], temp[1], temp[2], temp[3])
  if( is_root == True ):
    root = new_node
    is_root = False
  else:
    children.append(new_node)

################################################################################

def optimize_space(root_id):




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



