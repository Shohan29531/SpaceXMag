import read_json


maps = read_json.get_maps('0.json')

parent_to_child = maps[0]
child_to_parent = maps[1]

index_to_coordinates = maps[2]
coordinates_to_index = maps[3]


print( index_to_coordinates.keys() )