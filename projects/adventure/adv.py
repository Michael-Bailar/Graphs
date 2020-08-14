from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def get_random_unvisited_direction(room_number, graph):
    
    possible_moves = []
    for key, value in graph[room_number].items():
        if value == '?':
                possible_moves.append(key)
    if len(possible_moves) == 0:
        return None
    else:
        return random.choice(possible_moves)

def null_unneeded_directions(room_number, graph):
    unneeded_moves = []
    for key, value in graph[room_number].items():
        if value == '?':
            test = world.rooms[room_number].get_room_in_direction(key)
            if test == None:
                unneeded_moves.append(key)
    print("unneeded", unneeded_moves)
    print(graph[room_number])
    for item in unneeded_moves:
        del graph[room_number][item]
    print(graph[room_number])
    print(" ")
    return graph


def get_unvisited_direction_bfs(room_number, graph):
    possible_moves = []
    for item in graph[room_number].items():
        possible_moves.append(item[1])
    return possible_moves


def get_opposite_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'w':
        return 'e'
    if direction == 'e':
        return 'w'

def follow_branch_dft(graph, location):
    dft_direction_commands = []
    current_location = location
    cleaned_graph = null_unneeded_directions(location, graph)
    next_direction = get_random_unvisited_direction(current_location, cleaned_graph)

    while next_direction != None:
        player.travel(next_direction)
        new_location = player.current_room.id
        
        if new_location == current_location:
            
            del cleaned_graph[current_location][next_direction]
            next_direction = get_random_unvisited_direction(current_location, cleaned_graph)
        else:
            if new_location not in cleaned_graph:
                cleaned_graph[new_location] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
            dft_direction_commands.append(next_direction)
            cleaned_graph[current_location][next_direction] = new_location
            cleaned_graph[new_location][get_opposite_direction(next_direction)] = current_location

            current_location = player.current_room.id
            next_direction = get_random_unvisited_direction(current_location, cleaned_graph)
    return(dft_direction_commands, cleaned_graph, current_location)


def move_to_nearest_unvisited_bfs(graph, starting_location):
    bfs_direction_commands = []
    shortest_path = []
    q = Queue()
    q.enqueue([starting_location])
    visited = set()
    stop_boolean = False

    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if v == '?':
                shortest_path.append(path[:-1])
            else:
                visited.add(v)  
                for next_location in get_unvisited_direction_bfs(v, graph):
                    if next_location not in visited:
                        new_path = path.copy()
                        new_path.append(next_location)
                        q.enqueue(new_path)


    if len(shortest_path) == 0:
        stop_boolean = True
    else:
        for location in min(shortest_path, key=len):
            for key, value in graph[player.current_room.id].items():
                if value == location:
                    bfs_direction_commands.append(key)
                    player.travel(key)
        if player.current_room.id == starting_location:
            bfs_direction_commands = []

    return bfs_direction_commands, player.current_room.id, stop_boolean

def create_traversal_path():
    direction_commands = []
    traversal_graph = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}
    current_location = world.rooms[0].id
    visited = set()
    visited.add(0)
    stop = False

    while stop == False:
        dft_direction_commands, cleaned_graph, current_location = follow_branch_dft(traversal_graph, current_location)
        direction_commands = direction_commands + dft_direction_commands
        traversal_graph = cleaned_graph

        bfs_direction_commands, current_location, stop_boolean = move_to_nearest_unvisited_bfs(cleaned_graph, current_location)
        if stop_boolean == True:
            stop = True
        else:
            direction_commands = direction_commands +  bfs_direction_commands



    return direction_commands

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = create_traversal_path()
print(traversal_path)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
