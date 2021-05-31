
def getState(node, schoolLayout):
    stateList = []
    for n in schoolLayout[node]:
        stateList.append(n);

    return stateList

def checkFinished(path_state, end_node):
    #print("path: ",path_state)
    #print("end: ",end_node)
    if path_state == end_node:
        return True
    else:
        return False

def value_out(node):
    if(node.finished):
        return 1
    else:
        return 0


class PathTreeNode:
    def __init__(self, gstate, end_node, parentNode=None, last_move=None):
        self.value = None
        self.state = gstate
        self.finished = checkFinished(self.state, end_node)
        self.parent = parentNode
        self.children = []
        self.previous_move = last_move

    def printNode(self):
        # print("Node:\n")
        print("  has_parent: " + str(self.parent is not None))
        print("  no. of children: " + str(len(self.children)))
        print("  path state:")
        print(state)


class pathTreeNode2:
    def __init__(self, gstate, end_node, parentNode=None, last_move=None):
        self.value = None
        self.state = gstate
        self.finished = checkFinished(self.state, end_node)
        self.parent = parentNode
        self.children = []
        self.move = last_move

    def best_move(self):
        self.value = value_out(self)
        best_value = self.value
        for ch in self.children:
            ch.value = value_out(ch)
            if ch.value is best_value:
                return ch.move
        return None  #als het geen children heeft

def validMoves(state):
    moves = []
    for key in state[1]:
        moves.append(key)
    return moves

def makeMove(tree_node, move, schoolLayout):
    return schoolLayout[move] #lijst van mogelijke zetten en lengtes

def expandAllByOne(tree_node, valid_moves, schoolLayout, end_node):
    for move in valid_moves:
        new_state = makeMove(tree_node, move, schoolLayout)
        tree_node.children.append(PathTreeNode(new_state, end_node, parentNode=tree_node, last_move=move))
    return True

def tree2String(tree_node, prefix=""):
    result=""
    if(tree_node is not None):
        result+=prefix+str(int(len(prefix)/2))+": "+str(tree_node.state)+"\n"
        result+=prefix+"{\n"
        if(tree_node.value != None):
            result+=prefix+ str(tree_node.value)
        cprefix=(prefix+"  ")
        for child in tree_node.children:
            result+=tree2String(child,cprefix)
        result+=prefix+"}\n"
    return result

def expandTreeRec(tree_node, valid_moves, schoolLayout, end_node):
    if(len(valid_moves)==0):
        valid_moves = validMoves(tree_node.state)
        if tree_node == end_node:
            print("REE")
            return False
    for i in range(len(valid_moves)):
        new_state = makeMove(tree_node.state, valid_moves[-1], schoolLayout)
        tree_node.children.append(pathTreeNode2(new_state, end_node, parentNode=tree_node, last_move=valid_moves[-1]))
        valid_moves.remove(valid_moves[-1])

        expandTreeRec(tree_node.children[i], [], schoolLayout, end_node)
    return tree_node



schoolLayout = {1: ("", {2:9}),
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

start = 15
end = 31

validMovesEnd = tuple(getState(end,schoolLayout)) #Dit wordt gebruikt om te checken bij finished
state = getState(start,schoolLayout)

root = PathTreeNode(state, validMovesEnd, parentNode=None, last_move=None)
testroot = pathTreeNode2(state, validMovesEnd, parentNode=None, last_move=None)


moves = validMoves(state)
testmoves = validMoves(testroot.state)

testroot = expandTreeRec(testroot, testmoves, schoolLayout, validMovesEnd)

print(testroot.best_move())
print(tree2String(testroot))

#expandAllByOne(root, moves, schoolLayout, end)
#print(tree2String(root))
