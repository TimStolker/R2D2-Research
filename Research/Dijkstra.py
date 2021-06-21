import copy


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
       19: ("", {30:9.5, 31:3.5}),
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
       31: ("", { 19:3.5, 27:6}),
      }

print(DPath(schoolLayout, 1, 30))
