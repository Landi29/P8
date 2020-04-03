class TET:

    def __init__(self, root=None, freevars=None, children=None):
        self._root = root
        self._freevars = freevars
        self._children = children

    def copytet(self, TET):
        self._root = TET._root
        self._freevars = TET._freevars
        self._children = TET._children

    def addchild(self, child):
        if self._children==None:
            self._children = [child]
        else:
            self._children.append(child)

    def tostring(self):
        string = "[" + self._root
        for child in self._children:
            string += "," + child.tostring()
        string += "]"
        return string

    def isroot(self,user):
        if user == self._root:
            return True
        return False


class TETChild:
    def __init__(self, root, free=None, children=None):
        self._root = root
        if isinstance(children, list): 
            self._children = children
        elif children != None:
            self._children = [children]
        else:
            self._children = children

    def tostring(self):
        #if self._children = []:
        #    return "["+self._root+"]"
        
        string = "[" + self._root
        if self._children != None:
            for child in self._children:
                string += "," + child.tostring()
        string += "]"
        return string

tet = TET()


