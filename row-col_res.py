  #######################################

  # Relative positions within rows and columns

#   relative_row_col_matrix = [['N' for x in range(len(children) +1)] 
#                               for y in range(len(children) +1)] 



#   for i in range(1, len(children) + 1):
#     first_child = children[i-1]
#     for k in range(i+1, len(children) + 1):
#       second_child = children[k-1]

#       ## same row check
#       if ( first_child.y2 == second_child.y2 and first_child.y1 == second_child.y1 ):
#         relative_row_col_matrix[i][k] = 'SR'
#         relative_row_col_matrix[k][i] = 'SR'

#     ## same col check
#       if ( first_child.x2 == second_child.x2 and first_child.x1 == second_child.x1 ):
#         relative_row_col_matrix[i][k] = 'SC'
#         relative_row_col_matrix[k][i] = 'SC'  


#   for i in range(1, len(children) + 1):
#     j = i * 2
#     for k in range(i+1, len(children) + 1):
#       l = k * 2

#       code = relative_row_col_matrix[i][k]

#       if ( code == 'SR' ):
#         m.Equation( Y[j] == Y[l] )
#         m.Equation( Y[j+1] == Y[l+1] )

#       elif ( code == 'SC' ):
#         m.Equation( X[j] == X[l] )
#         m.Equation( X[j+1] == X[l+1] )


  ################################################################################