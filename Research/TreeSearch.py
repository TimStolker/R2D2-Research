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
        self.value = value_out(self)
        best_value = self.value
        for ch in self.children:
            ch.value = value_out(ch)
            if ch.value is best_value:
                return ch.last_move
        return None  # als het geen children heeft

    def __repr__(self):
        return f"{self.id}: {self.gstate}"

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
        child = self.children[0]
        chld: TreeNode
        for chld in self.children:
            val = self.uct()
            if val > value:
                value = val
                child = chld
        return child


def valid_moves(id: int, gstate: List[int]):
    moves = list()
    for key in schoolLayout[id][1].keys():
        if key in gstate:
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
    for node in gstate:
        if node == end_node:
            return True
    return False


def backup_value(node: TreeNode, val):
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
        result += prefix + str(int(len(prefix) / 2)) + ": " + str(tree_node.gstate) + "\n"
        result += prefix + "{\n"
        cprefix = (prefix + "  ")
        for child in tree_node.children:
            result += tree2String(child, cprefix)
        result += prefix + "}\n"
    return result


def expandTreeRec(tree_node: TreeNode, start: int, end: int, school_layout: Dict[int, Tuple[AnyStr, Dict[int, int]]]):
    """
    Expand the tree recursively
    :param school_layout: The dict with the weighted graph.
    :param tree_node: The initial root node
    :param end: Int: ke of the end node in school_layout
    :return: the leaf node.
    """
    tree_node.finished = check_finished(tree_node.gstate, end)
    if tree_node.finished or len(tree_node.valid_move_list) == 0:
        return tree_node
    elif tree_node.last_move is not None and check_finished(tree_node.gstate, end):
        return tree_node
    elif len(tree_node.valid_move_list) > len(tree_node.children):
        new_moves = tree_node.valid_move_list
        try_this_move = choice(new_moves)
        new_moves.remove(try_this_move)
        new_state = deepcopy(tree_node.gstate)
        new_state.append(try_this_move)
        leaf = TreeNode(try_this_move, start, end, new_state, new_moves, school_layout, tree_node, try_this_move)
        tree_node.children.append(leaf)
        return leaf
    return expandTreeRec(tree_node.best_child(), start, end, school_layout)

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
        while (True):
            leaf.last_move = choice(valid_moves(leaf.id, leaf.gstate))
            x, finished, new_state = move(leaf.id, leaf.gstate, leaf.last_move)
            leaf.valid_move_list = valid_moves(leaf.id, leaf.gstate)
            if check_finished(leaf.gstate, end) or len(leaf.valid_move_list) == 0:
                break
    else:
        return None

    if check_finished(leaf.gstate, end):
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

    start = 15
    end = 31

    start_state = [15]
    start_moves = list(schoolLayout[start][1].keys())

    root = TreeNode(15, 15, 31, gstate=start_state, valid_move_list=start_moves, school_layout=schoolLayout, parent_node=None, last_move=None)
    for i in range(10):
        leaf = expandTreeRec(tree_node=root, start=start, end=end, school_layout=schoolLayout)
        leaf_val = rollout(leaf)
        backup_value(leaf, leaf_val)
    print(root.best_move())
    print(tree2String(root))

    # expandAllByOne(root, moves, schoolLayout, end)
    # print(tree2String(root))
