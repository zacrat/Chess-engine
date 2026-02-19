import Engine

class TreeNode:
    def __init__(self,content,parent=None):
        self.content = content
        self.parent = parent
        self.children = []
        self.checkmate = False
        self.next = None
        self.passed = 0

    def addChild(self,child):
        self.children.append(TreeNode(child, self))
    def getParent(self):
        return self.parent
    def getContent(self):
        return self.content
    def getLevel(self):
        level = 0
        cur = self
        while cur.parent is not None:
            cur = cur.parent
            level += 1
        return level
class Tree():
    def __init__(self, root):
        self.root = root
    def search(self, node, root = None):
        print("Searching tree...")
        found = None
        curr = self.root if root is None else root
        str_curr = Engine.ChessEngine.get_str_pos(None, curr.getContent())
        if str_curr == node:
            print("Found node!")
            return curr
        for child in curr.children:
            found = self.search(node,child)
            if found is not None:
                return found
        return found


        

