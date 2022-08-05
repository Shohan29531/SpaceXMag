

list_i = [i for i in range(10)]
list_j = [j for j in range(10)]


tuples =[]

for i in list_i:
    for j in list_j:
        tuples.append( [i, j] )




for item in tuples:
    print(item)