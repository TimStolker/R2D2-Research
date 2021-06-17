from matplotlib import pyplot as plt
import numpy as np
import time
import statistics as stats

from Research.AStar import a_star
from Research.Dijkstra import DPath
from Research.TreeSearch import MCTS

if __name__ == '__main__':
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

    mean_d_path = []
    stdev_d_path = []
    mean_a_star = []
    stdev_a_star = []
    mean_tree_search = []
    stdev_tree_search = []
    meetpunten = list(range(1, 32, 1))
    for i in meetpunten:
        d_path = []
        astar = []
        tree_search = []
        for j in meetpunten:
            t1 = time.time()
            res = DPath(schoolLayout, i, j)
            t2 = time.time()
            d_path.append(t2 - t1)
            t1 = time.time()
            res = a_star(schoolLayout, i, j)
            t2 = time.time()
            astar.append(t2 - t1)
            t1 = time.time()
            res = MCTS(schoolLayout, i, j)
            t2 = time.time()
            tree_search.append(t2 - t1)
        mean_d_path.append(stats.mean(d_path))
        stdev_d_path.append(stats.stdev(d_path))
        mean_a_star.append(stats.mean(astar))
        stdev_a_star.append(stats.stdev(astar))
        mean_tree_search.append(stats.mean(tree_search))
        stdev_tree_search.append(stats.stdev(tree_search))

    plt.plot(meetpunten, mean_d_path, 'b-')
    plt.fill_between(meetpunten, np.array(mean_d_path) - np.array(stdev_d_path),
                     np.array(mean_d_path) + np.array(stdev_d_path), color='b', alpha=0.3)
    plt.plot(meetpunten, mean_a_star, 'r-')
    plt.fill_between(meetpunten, np.array(mean_a_star) - np.array(stdev_a_star),
                     np.array(mean_a_star) + np.array(stdev_a_star), color='r', alpha=0.3)
    plt.plot(meetpunten, mean_tree_search, 'g-')
    plt.fill_between(meetpunten, np.array(mean_tree_search) - np.array(stdev_tree_search),
                     np.array(mean_tree_search) + np.array(stdev_tree_search), color='g', alpha=0.3)
    plt.xlabel("Start node")
    plt.ylabel("time (seconds)")
    plt.legend(["Dijksta", "A-Star", "Tree-Search"], loc='upper left')
    plt.show()

    mean_d_path = []
    stdev_d_path = []
    mean_a_star = []
    stdev_a_star = []
    mean_tree_search = []
    stdev_tree_search = []
    meetpunten = list(range(1, 32, 1))
    for i in meetpunten:
        d_path = []
        astar = []
        tree_search = []
        for j in meetpunten:
            res = DPath(schoolLayout, i, j)
            d_path.append(res[0])
            res = a_star(schoolLayout, i, j)
            astar.append(res[0])
            res = MCTS(schoolLayout, i, j)
            if res[0] != 0:
                tree_search.append(res[0])
        mean_d_path.append(stats.mean(d_path))
        stdev_d_path.append(stats.stdev(d_path))
        mean_a_star.append(stats.mean(astar))
        stdev_a_star.append(stats.stdev(astar))
        mean_tree_search.append(stats.mean(tree_search))
        stdev_tree_search.append(stats.stdev(tree_search))

    plt.plot(meetpunten, mean_d_path, 'b-')
    plt.fill_between(meetpunten, np.array(mean_d_path) - np.array(stdev_d_path),
                     np.array(mean_d_path) + np.array(stdev_d_path), color='b', alpha=0.3)
    plt.plot(meetpunten, mean_a_star, 'r-')
    plt.fill_between(meetpunten, np.array(mean_a_star) - np.array(stdev_a_star),
                     np.array(mean_a_star) + np.array(stdev_a_star), color='r', alpha=0.3)
    plt.plot(meetpunten, mean_tree_search, 'g-')
    plt.fill_between(meetpunten, np.array(mean_tree_search) - np.array(stdev_tree_search),
                     np.array(mean_tree_search) + np.array(stdev_tree_search), color='g', alpha=0.3)
    plt.xlabel("Start node")
    plt.ylabel("length")
    plt.legend(["Dijksta", "A-Star", "Tree-Search"], loc='upper left')
    plt.show()
