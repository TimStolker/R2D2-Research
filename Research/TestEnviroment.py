import copy
import math
from matplotlib import pyplot as plt
import numpy as np
import time
import statistics as stats

def findNeighbours(n, graph):
    neighbours = set()
    for group in graph.E:
        if (group.v1 == n) or (group.v2 == n):
            if group.v1 != n:
                neighbours.add(group.v1)
            elif group.v2 != n:
                neighbours.add(group.v2)
    return neighbours


def minDist(N):
    minValue = float('inf')
    minDict = {}
    for i in N:
        if N[i][1]["dist"] < minValue:
            minValue = N[i][1]["dist"]
            minDict[i] = N[i]
    return minDict


def findNeighboursD(n, graph, n_key):
    neighbours = {}
    keys = n[n_key][1].keys()
    for key in keys:
        if key != "dist" and key != "prev" and key != "solved":
            neighbours[key] = graph[key]

    return neighbours


def getPath(node, start, path):
    key = list(node.keys())[0]
    path.append(key)

    if key == start:
        return path

    getPath(node[key][1]["prev"], start, path)


def DPath(schoolLayout, start, finish):
    graph = copy.deepcopy(schoolLayout)
    for n in graph:
        graph[n][1]["dist"] = float('inf')
        graph[n][1]["prev"] = None
        graph[n][1]["solved"] = False

    graph[start][1]["dist"] = 0
    S = {}
    N = {start: graph[start]}

    while len(N) != 0:
        n = minDist(N)
        n_key = list(n.keys())[0]
        n[n_key][1]["solved"] = True

        S.update(n)
        del N[n_key]

        if n_key == finish:
            break

        neighbours = findNeighboursD(n, graph, n_key)
        for m in neighbours:
            if not neighbours[m][1]["solved"]:
                if m not in N:
                    N[m] = graph[m]
                altDistance = n[n_key][1]["dist"] + n[n_key][1][m]
                if neighbours[m][1]["dist"] > altDistance:
                    neighbours[m][1]["dist"] = altDistance
                    neighbours[m][1]["prev"] = n

    node = {finish: graph[finish]}
    path = []
    getPath(node, start, path)
    path.reverse()
    return node[finish][1]["dist"], path

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


def get_minimum_f(unvisited, graph, target):
    minimum_key = list(unvisited.keys())[0]
    i = 0
    for key in unvisited.keys():
        if(len(graph[key][1])) > 1:
            minimum_key = list(unvisited.keys())[i]
        i += 1
    for key in unvisited.keys():
        if target in graph[key][1]:
            minimum_key = key
        elif unvisited[key][1] < unvisited[minimum_key][1] and len(graph[key][1]) > 1:
            minimum_key = key

    return minimum_key


def a_star(graph, start_node, target_node):
    route = []
    visited = {}
    unvisited = {}
    distance = 0

    for key in graph.keys():
        unvisited[key] = [float('inf'), float('inf'), None]  # G, F, PREV

    h_score = heuristic(start_node, target_node)
    unvisited[start_node] = [0, h_score, None]

    finished = False
    current_node = start_node
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
                        unvisited[neighbour][0] = new_g_score
                        unvisited[neighbour][1] = new_g_score + heuristic(neighbour, target_node)
                        unvisited[neighbour][2] = current_node
                visited[current_node] = unvisited[current_node]
                route.append(current_node)
                del unvisited[current_node]

            neighbours = {}
            for neighbour_key in graph[current_node][1].keys():
                if neighbour_key in unvisited:
                    neighbours[neighbour_key] = unvisited[neighbour_key]
            if target_node in neighbours:
                current_node = target_node
            else:
                if current_node != target_node:
                    current_node = get_minimum_f(neighbours, graph, target_node)
                else:
                    finished = True
            if unvisited[current_node][0] != float('inf'):
                distance = unvisited[current_node][0]
    route.append(target_node)
    return distance, route

schoolLayout = {1: ("", {2:9}),
       2: ("", {1:9, 3:11, 17:1.5}),
       3: ("", {2:11, 8:8.5}),
       4: ("", {5:6, 6:5, 17:2}),
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
       16: ("", {13:16.5, 18:3.5}),
       17: ("", {2:1.5, 4:2}),
       18: ("", {16:3.5, 20:2.5}),
       19: ("", {30:9.5, 31:3.5, 32:2.5, 33:4.5}),
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
       30: ("", {26:8, 29:6, 19:9.5}),
       31: ("", {27:6, 32:4.5, 33:2.5, 19:3.5}),
       32: ("", {31:4.5, 33:3.5, 19:2.5}),
       33: ("", {31:2.5, 32:3.5, 19:4.5}),
      }

a_star(schoolLayout, 31, 23)

mean_std_max = []
stdev_std_max = []
mean_my_max = []
stdev_my_max = []
meetpunten = list(range(1, 32, 1))
print(meetpunten)
for i in meetpunten:
    std = []
    my = []
    for j in meetpunten:
        t1 = time.time()
        res = DPath(schoolLayout, i, j)
        t2 = time.time()
        std.append(t2 - t1)
        t1 = time.time()
        res = a_star(schoolLayout, i, j)
        t2 = time.time()
        my.append(t2 - t1)
    mean_std_max.append(stats.mean(std))
    stdev_std_max.append(stats.stdev(std))
    mean_my_max.append(stats.mean(my))
    stdev_my_max.append(stats.stdev(my))

plt.plot(meetpunten, mean_std_max, 'b-')
plt.fill_between(meetpunten, np.array(mean_std_max) - np.array(stdev_std_max),
                 np.array(mean_std_max) + np.array(stdev_std_max), color='b', alpha=0.3)
plt.plot(meetpunten, mean_my_max, 'r-')
plt.fill_between(meetpunten, np.array(mean_my_max) - np.array(stdev_my_max),
                 np.array(mean_my_max) + np.array(stdev_my_max), color='r', alpha=0.3)
plt.xlabel("number of array elements")
plt.ylabel("time (seconds)")
plt.legend(["Dijksta", "A-Start"], loc='upper left')
plt.show()
