import math


def heuristic(current_node, target_node):
    nodeCords = {
        1: (0, 17), 2: (9, 17), 3: (9, 6), 4: (10.5, 19), 5: (10.5, 24), 6: (15.5, 19), 7: (15.5, 25), 8: (17.5, 6),
        9: (17.5, 0), 10: (19.5, 6), 11: (19.5, 19), 12: (25.5, 6), 13: (25.5, 19), 14: (25.5, 25), 15: (42.5, 6),
        16: (42, 19), 17: (10.5, 17), 18: (45.5, 19), 19: (72, 15.5), 20: (48, 19), 21: (56, 19), 22: (56, 25),
        23: (62, 6), 24: (62, 19), 25: (64, 0), 26: (64, 6), 27: (66, 19), 28: (66, 25), 29: (72, 0),
        30: (72, 6), 31: (72, 19), 32: (74.5, 15.5), 33: (74.5, 19)
    }
    cordsX = (nodeCords[current_node][0] - nodeCords[target_node][0])
    cordsY = (nodeCords[current_node][1] - nodeCords[target_node][1])
    return math.sqrt((cordsX * cordsX) + (cordsY * cordsY))


def get_minimum_f(unvisited):
    minimum_key = list(unvisited.keys())[0]
    for key in unvisited.keys():
        if unvisited[key][1] < unvisited[minimum_key][1]:
            minimum_key = key

    return minimum_key


def a_star(graph, start_node, target_node):
    visited = {}
    unvisited = {}
    distance = 0

    for key in graph.keys():
        unvisited[key] = [float('inf'), float('inf'), None]  # G, F, PREV

    h_score = heuristic(start_node, target_node)
    unvisited[start_node] = [0, h_score, None]

    finished = False
    while not finished:
        if len(unvisited) == 0:
            finished = True
        else:
            current_node = get_minimum_f(unvisited)
            distance = unvisited[current_node][0]
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
                del unvisited[current_node]

    node = target_node
    route = [node]
    while node != start_node:
        node = visited[node][2]
        route.insert(0, node)

    return distance, route


schoolLayout = {1: ("", {2: 9}),
                2: ("", {1: 9, 3: 11, 17: 1.5}),
                3: ("", {2: 11, 8: 8.5}),
                4: ("", {5: 6, 6: 5, 17: 2}),
                5: ("", {4: 6}),
                6: ("", {4: 5, 7: 6, 11: 4}),
                7: ("", {6: 6, 14: 10}),
                8: ("", {3: 8.5, 9: 6, 10: 2}),
                9: ("", {8: 6}),
                10: ("", {8: 2, 11: 13, 12: 6}),
                11: ("", {6: 4, 10: 13, 13: 6}),
                12: ("", {10: 6, 15: 17}),
                13: ("", {11: 6, 14: 6, 16: 16.5}),
                14: ("", {7: 10, 13: 6}),
                15: ("", {12: 17, 20: 13.5, 23: 19.5}),
                16: ("", {13: 16.5, 18: 3.5}),
                17: ("", {2: 1.5, 4: 2}),
                18: ("", {16: 3.5, 20: 2.5}),
                19: ("", {30: 9.5, 31: 3.5}),
                20: ("", {15: 13.5, 18: 2.5, 21: 8}),
                21: ("", {20: 8, 22: 6, 24: 6}),
                22: ("", {21: 6, 28: 10}),
                23: ("", {15: 19.5, 24: 13, 26: 2}),
                24: ("", {21: 6, 23: 13, 27: 4}),
                25: ("", {26: 6}),
                26: ("", {23: 2, 25: 6, 30: 8}),
                27: ("", {24: 4, 28: 6, 31: 6}),
                28: ("", {22: 10, 27: 6}),
                29: ("", {30: 6}),
                30: ("", {26: 8, 29: 6, 19: 9.5}),
                31: ("", {19: 3.5, 27: 6}),
                }

print(a_star(schoolLayout, 15, 31))
