from random import choice
from typing import Tuple, AnyStr, Dict, List, Union


def get_state(node, schoolLayout):
    stateList = []
    for n in schoolLayout[node]:
        stateList.append(n)

    return stateList


def valid_moves(node) -> list:
    state = school_layout[node.id]
    moves = []
    for key in state[1]:
        if key is not node.last_move:
            moves.append(key)
    return moves



class TreeNode:
    def __init__(self, nb: Tuple[AnyStr, Dict], gstate=None, parentNode=None, last_move: Union[None, int] = None):
        if gstate is None:
            gstate = list()
        for key, value in school_layout.items():
            if nb == value:
                self.id = key
                self.nb = school_layout[self.id][1]
                break
        self.value = None
        self.state = gstate
        self.last_move = last_move
        self.valid_moves = valid_moves(self)
        self.finished = check_finished(self.state, end)
        self.parent = parentNode
        self.children = []
        self.N = 0
        self.Q = 0

    def best_child(self):
        value = 0
        child = self.children[0]
        for chld in self.children:
            val = chld.uct()
            if val > value:
                value = val
                child = chld
        return child

    def best_move(self) -> Union[None, ]:
        self.value = self.rollout()
        best_value = self.value

        ch: TreeNode
        for ch in self.children:
            ch.value = self.rollout()
            if ch.value is best_value:
                return ch.last_move
        return None  # als het geen children heeft


    def rollout(self):
        if (self.parent is not None):
            while (True):
                self.last_move = choice(valid_moves(self))
                make_move(self, self.last_move)
                self.valid_moves = valid_moves(self)
                if check_finished(self.state, end) or len(valid_moves(self)) == 0:
                    break
        else:
            return None

        return 1 if check_finished(self.state, end) else 0

    def __repr__(self):
        for key, item in school_layout.items():
            if self.state[1] == item[1]:
                return f"{key}: {self.state}"



def check_finished(path_state: List, end_node: int):
    """
    Checks whether the targetnode is reached
    :param path_state: the past nodes in your path
    :param end_node: node id according to the school_layout
    :return: bool true if end is reached.
    """
    if path_state == end_node:
        return True
    else:
        return False


def make_move(tree_node, move):
    if not move in tree_node.parent.gstate_:
        tree_node.gstate_.append(move)
        return tree_node.gstate_
    else:
        # this shouldn't happen
        return None


def backup_value(node: TreeNode, val):
    if (node.parent is not None):
        while (node is not None):
            node.N += 1
            node.Q = node.Q - val

        node = node.parent


def expand_tree_rec(tree_node):
    tree_node.finished = check_finished(tree_node.gstate_, end)
    if tree_node.finished or len(tree_node.valid_moves) == 0:
        return tree_node
    elif root.last_move is not None and check_finished(root.state, end):
        return tree_node
    elif len(tree_node.valid_moves) > len(tree_node.children_):
        new_moves = tree_node.valid_moves
        try_this_move = choice(new_moves)
        new_state = make_move(tree_node, try_this_move)
        new_moves.remove(try_this_move)
        leaf = TreeNode(school_layout[try_this_move], new_state, tree_node, tree_node.id)
        tree_node.children_.append(leaf)
        return leaf
    return expand_tree_rec(tree_node.best_child())


if __name__ == '__main__':
    school_layout = {1: ("", {2:9}),
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

    start = 15
    end = 31

    validMovesEnd = tuple(get_state(end, school_layout))  # Dit wordt gebruikt om te checken bij finished
    # state = get_state(start, school_layout)
    for i in range(10):
        root = TreeNode(school_layout[15], parentNode=None, last_move=None)
        leaf = expand_tree_rec(root)
        leaf_value = leaf.rollout()
        backup_value(leaf, leaf.value)

    print(root.best_move())
    # print(tree2String(root))
