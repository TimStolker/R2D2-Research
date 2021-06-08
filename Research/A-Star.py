
def heuristic(current_node, target_node):
    pathsToLandmark = {1: 67.0, 2: 58.0, 3: 47.0, 4: 37.5, 5: 43.5, 6: 32.5, 7: 38.5, 8: 38.5, 9: 44.5, 10: 36.5, 11: 28.5, 12: 30.5,
            13: 22.5, 14: 28.5, 15: 13.5, 16: 6.0, 17: 6.5, 18: 2.5, 19: 4.5, 20: 0, 21: 8, 22: 14, 23: 33.0, 24: 14, 25: 41.0,
            26: 35.0, 27: 18, 28: 24, 29: 49.0, 30: 43.0, 31: 24, 32: 28.5, 33: 26.5}


    if current_node > 19:
        print(pathsToLandmark[target_node], "-", pathsToLandmark[current_node], "=")
        return abs(pathsToLandmark[target_node] - pathsToLandmark[current_node])
    print(pathsToLandmark[target_node], "+", pathsToLandmark[current_node], "=")
    return pathsToLandmark[target_node] + pathsToLandmark[current_node]


def get_minimum_f(graph):
    print("------")
    print(graph)
    minimum_key = list(graph.keys())[0]
    for key in graph.keys():
        if graph[key][1] < graph[minimum_key][1]:
            minimum_key = key
    return minimum_key


def a_star(graph, start_node, target_node):
    route = []
    visited = {}
    unvisited = {}
    distance = 0

    for key in graph.keys():
        unvisited[key] = [float('inf'), float('inf'), None] # G, F, PREV

    h_score = heuristic(start_node, target_node)
    unvisited[start_node] = [0, h_score, None]

    finished = False
    current_node = get_minimum_f(unvisited)
    while not finished:
        if len(unvisited) == 0:
            finished = True
        else:
            if current_node == target_node:
                finished = True
                visited[current_node] = unvisited[current_node]
            else:
                for neighbour in graph[current_node][1].keys():
                    if neighbour not in visited:
                        new_g_score = unvisited[current_node][0] + graph[current_node][1][neighbour]
                        if new_g_score < unvisited[neighbour][0]:
                            unvisited[neighbour][0] = new_g_score
                            unvisited[neighbour][1] = new_g_score + heuristic(neighbour, target_node)
                            unvisited[neighbour][2] = current_node
                visited[current_node] = unvisited[current_node]
                route.append(current_node)
                print(route)
                del unvisited[current_node]

            neighbours = {}
            for neighbour_key in graph[current_node][1].keys():
                if neighbour_key in unvisited:
                    neighbours[neighbour_key] = unvisited[neighbour_key]
            if target_node in neighbours:
                current_node = target_node
            else:
                current_node = get_minimum_f(neighbours)
            if unvisited[current_node][0] != float('inf'):
                distance = unvisited[current_node][0]
    route.append(target_node)
    return distance, route


gr2 = {1: ("", {2:9} ),
       2: ("", {1:9, 3:11}),
       3: ("", {2:11, 8:8.5}),
       4: ("", {5:6, 6:5}),
       5: ("", {4:6}),
       6: ("", {4:5, 7:6, 11:4}),
       7: ("", {6:6, 14:10}),
       8: ("", {3:8.5, 9:6, 10:2}),
       9: ("", {8:6}),
       10: ("", {8:2, 11:13, 12:6}),
       11: ("", {6:4, 10:13, 13:6}),
       12: ("", {10:6, 15:17}),
       13: ("", {11:6, 14:6, 16:16.5}),
       14: ("", {7:10, 13:6}),
       15: ("", {12:17, 20:13.5, 23:19.5}),
       16: ("", {13:16.5, 17:2, 18:3.5, 19:4}),
       17: ("", {16:2, 18:4, 19:3.5}),
       18: ("", {16:3.5, 17:4, 19:2, 20:2.5}),
       19: ("", {16:4, 17:3.5, 18:2}),
       20: ("", {15:13.5, 18:2.5, 21:8}),
       21: ("", {20:8, 22:6, 24:6}),
       22: ("", {21:6, 28:10}),
       23: ("", {15:19.5, 24:13, 26:2}),
       24: ("", {21:6, 23:13, 27:4}),
       25: ("", {26:6}),
       26: ("", {23:2, 25:6, 30:8}),
       27: ("", {24:4, 28:6, 31:6}),
       28: ("", {22:10, 27:6}),
       29: ("", {30:6}),
       30: ("", {26:8, 29:6, 31:13}),
       31: ("", {27:6, 30:13, 32:4.5, 33:2.5}),
       32: ("", {31:4.5, 33:3.5}),
       33: ("", {31:2.5, 32:3.5})
      }

print(a_star(gr2, 1, 31))
