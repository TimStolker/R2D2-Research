from math import inf
from copy import deepcopy
from random import choice
from typing import Tuple, List, Dict, AnyStr


def value_out(node):
    if (node.finished):
        return 1
    else:
        return 0


class TreeNode:
    def __init__(self, node_id: int, start_node: int, end_node: int, gstate: List,
                 valid_move_list: List, school_layout: Dict[int, Tuple[AnyStr, Dict[int, int]]], parent_node=None,
                 last_move=None):
        self.value = 0
        self.id = node_id
        self.gstate: List = gstate
        self.start_node = start_node
        self.end_node = end_node
        self.valid_move_list = valid_move_list
        self.finished = check_finished(self.gstate, end_node)
        self.parent_node: TreeNode = parent_node
        self.children = []
        self.N = 0
        self.Q = 0
        self.last_move: int = last_move

    def best_move(self):
        highest_value = self.children[0].Q / self.children[0].N
        best_child = self.children[0]
        for child in self.children:
            if child.Q / child.N > highest_value:
                highestVal = child.Q / child.N
                best_child = child
        return best_child.id

    def __repr__(self):
        return f"{self.id}: {self.gstate}"

    def __eq__(self, other):
        if isinstance(other, TreeNode):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other

    def uct(self):
        """
        Calculate node value
        :return: int: value
        """
        return self.Q / self.N

    def best_child(self):
        """
        Find the best child in the tree
        Runtime-complexity of O(n) because you only loop though all children once.
        :return: the child with highest value.
        """
        value = 0
        chosen_child = choice(self.children)
        child: TreeNode
        for child in self.children:
            val = child.uct()
            if val < value:
                chosen_child = child
            elif child.N > chosen_child.N:
                chosen_child = child
            elif child.value < chosen_child.value:
                chosen_child = child
        return chosen_child


def valid_moves(id: int, gstate: List[int]):
    moves = []
    for key in schoolLayout[id][1].keys():
        if key in gstate:
            continue
        else:
            if key == id:
                continue
            else:
                moves.append(key)
    return moves


def check_finished(gstate: List[int], end_node: int):
    """
    Checks is the goal node has been reached
    :param gstate: list of traversed nodes.
    :param end_node: the key of the end node.
    :return: boolean
    """
    node: int
    if end_node in gstate:
            return True
    return False


def backup_value(node: TreeNode, val: int):
    """
    Calculates the value of a node, according to the value of it's children.
    complexity of O(d), where d stands for the depth of the tree.
    :param node:
    :param val:
    :return:
    """
    if (node.parent_node is not None):
        while (node is not None):
            node.N += 1
            node.Q = node.Q - val

            node = node.parent_node


def make_state(tree_node: TreeNode, move, schoolLayout):
    valid_moves = tree_node.valid_move_list
    if move in valid_moves:
        return schoolLayout[move]  # lijst van mogelijke zetten en lengtes


def tree2String(tree_node, prefix=""):
    result = ""
    if (tree_node is not None):
        result += f"{prefix + str(tree_node.id)}: {str(tree_node.gstate)}\n"
        result += prefix + "{\n"
        cprefix = (prefix + "  ")
        for child in tree_node.children:
            result += tree2String(child, cprefix)
        result += prefix + "}\n"
    return result


def findSpot(tree_node, school_layout):
    if len(tree_node.valid_move_list) == 0:
        tree_node.value += 100
        return tree_node
    elif len(tree_node.valid_move_list) > len(tree_node.children):
        return expand(tree_node, tree_node.valid_move_list[len(tree_node.children)], school_layout)
    return findSpot(tree_node.best_child(), school_layout)

def expand(tree_node, move, school_layout):
    new_valid_moves = list(school_layout[move][1].keys())
    new_valid_moves.remove(tree_node.id) # remove parent_node where we came from

    new_state = deepcopy(tree_node.gstate)
    new_state.append(move)

    leaf = TreeNode(move, start, end, new_state, new_valid_moves, school_layout, tree_node, move)
    tree_node.children.append(leaf)
    return leaf


def move(id: int, gstate: List[int], move: int):
    test_state = gstate
    valids = valid_moves(id, test_state)
    if move not in valids:
        return False, check_finished(test_state, end), test_state
    else:
        test_state.append(move)
        return True, check_finished(test_state, end), test_state


def rollout(leaf: TreeNode):
    if leaf.parent_node is not None:
        new_state = deepcopy(leaf.gstate)
        if len(valid_moves(leaf.id, leaf.gstate)) != 0:
            while (True):
                #print(leaf.id, new_state)
                #print("moves:",valid_moves(leaf.id, new_state))
                try_this_move = choice(valid_moves(leaf.id, new_state))
                leaf.last_move = try_this_move
                is_valid_move, finished, new_state = move(leaf.id, new_state, leaf.last_move)
                # leaf.valid_move_list = valid_moves(leaf.id, leaf.gstate)
                if check_finished(new_state, end) or len(valid_moves(leaf.id, new_state)) == 0:
                    break
    else:
        return None

    if check_finished(new_state, end):
        return 1
    else:
        return 0


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
    start = 9
    end = 7

    start_state = [start]
    start_moves = list(schoolLayout[start][1].keys())

    root = TreeNode(start, start, end, gstate=start_state, valid_move_list=start_moves, school_layout=schoolLayout, parent_node=None, last_move=None)
    root.valid_move_list = valid_moves(root.id, start_state)
    for i in range(50):
        leaf = findSpot(root, schoolLayout)
        leaf_reward = rollout(leaf)
        backup_value(leaf, leaf_reward)
    #print(root.best_move())
    print(tree2String(root))

    # expandAllByOne(root, moves, schoolLayout, end)
    # print(tree2String(root
