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

    # methods to get the parent, content, and level of the node in the tree
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
        # Searches the tree for a node with the given content and returns it if found, otherwise returns None
        found = None
        curr = self.root if root is None else root
        str_curr = Engine.ChessEngine.get_str_pos(None, curr.getContent()) # Convert the current node's content to a string representation of the chess position
        if str_curr == node:
            # If the current node's content matches the search node, print a message and return the current node
            print("Found node!")
            return curr
        for child in curr.children:
            # Recursively search the tree for the node and return it if found
            found = self.search(node,child)
            if found is not None:
                return found
        return found


        

