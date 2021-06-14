from random import choice
from typing import Tuple, List, Dict, AnyStr

def checkFinished(path_state, end_node):
    # print("path: ",path_state)
    # print("end: ",end_node)
    if path_state == end_node:
        return True
    else:
        return False


def value_out(node):
    if (node.finished):
        return 1
    else:
        return 0


class TreeNode:
    def __init__(self, gstate: Tuple[AnyStr, Dict[int, int]],
                 valid_move_list: List, end_node, parent_node=None,
                 last_move=None):
        self.value: int = 0
        self.gstate_: Tuple = gstate
        self.valid_move_list_ = valid_move_list
        self.finished = checkFinished(self.gstate_, end_node)
        self.parent_node_: TreeNode = parent_node
        self.children_ = []
        self.last_move_: int = last_move

    def best_move(self):
        self.value = value_out(self)
        best_value = self.value
        for ch in self.children_:
            ch.value = value_out(ch)
            if ch.value is best_value:
                return ch.last_move_
        return None  # als het geen children heeft

    def __repr__(self):
        for key, item in schoolLayout.items():
            if self.gstate_[1] == item[1]:
                return f"{key}: {self.gstate_}"

    def valid_moves(self, state):
        moves = []
        for key in state[1]:
            if self.parent_node_ is not None:
                if key not in self.parent_node_.gstate_[1]:  # [1] are the neighbouring keys.
                    moves.append(key)
            else:
                moves.append(key)
        return moves


def make_state(tree_node: TreeNode, move, schoolLayout):
    valid_moves = tree_node.valid_move_list_
    if move in valid_moves:
        return schoolLayout[move]  # lijst van mogelijke zetten en lengtes


def expandAllByOne(tree_node, valid_moves, schoolLayout, end_node):
    for move in valid_moves:
        new_state = make_state(tree_node, move, schoolLayout)
        tree_node.children_.append(TreeNode(new_state, end_node, parent_node=tree_node, last_move=move))
    return True


def tree2String(tree_node, prefix=""):
    result = ""
    if (tree_node is not None):
        result += prefix + str(int(len(prefix) / 2)) + ": " + str(tree_node.gstate_) + "\n"
        result += prefix + "{\n"
        if (tree_node.value != None):
            result += prefix + str(tree_node.value)
        cprefix = (prefix + "  ")
        for child in tree_node.children_:
            result += tree2String(child, cprefix)
        result += prefix + "}\n"
    return result


def expandTreeRec(tree_node: TreeNode, end: int, school_layout: Dict[int, Tuple[AnyStr, Dict[int, int]]]):
    """
    Expand the tree recursively
    :param school_layout: The dict with the weighted graph.
    :param tree_node: The initial root node
    :param end: Int: ke of the end node in school_layout
    :return: the leaf node.
    """
    if len(tree_node.valid_move_list_) == 0:
        valid_move_list = tree_node.valid_moves(tree_node.gstate_)
        if tree_node.gstate_ == end:
            print("REE")
            return False
    for i in range(len(tree_node.valid_move_list_)):
        try_this_move = choice(tree_node.valid_move_list_)
        if not tree_node.last_move_ == try_this_move:
            new_state = make_state(tree_node, try_this_move, school_layout)
            new_moves = tree_node.valid_moves(new_state)
            tree_node.children_.append(
                TreeNode(gstate=new_state, valid_move_list=new_moves, end_node=end, parent_node=tree_node,
                         last_move=try_this_move))
            tree_node.valid_move_list_.remove(try_this_move)
        else:
            continue
        expandTreeRec(tree_node.children_[i], end=end, school_layout=school_layout)
    return tree_node


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

    start_state = schoolLayout[start][1]
    start_moves = list(schoolLayout[start][1].keys())

    root = TreeNode(gstate=start_state, valid_move_list=start_moves, end_node=end, parent_node=None, last_move=None)

    # moves = valid_moves(node=root, state=root._gstate)
    root = expandTreeRec(tree_node=root, end=end, school_layout=schoolLayout)

    print(root.best_move())
    print(tree2String(root))

    # expandAllByOne(root, moves, schoolLayout, end)
    # print(tree2String(root))
