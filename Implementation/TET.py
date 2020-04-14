class TET:

    def __init__(self, root=None, freevars=None, children=None):
        self._root = root
        self._freevars = freevars
        self._children = children
    
    def getroot(self):
        return self._root   
    
    def isroot(self,user):
        if user == self._root:
            return True
        return False

    def getchildren(self):
        return self._children
    
    def addchild(self, child):
        if self._children==None:
            self._children = [child]
        else:
            self._children.append(child)

    def tostring(self):
        stringchildren = {}
        string = "[" + self._root
        if self._children != None:
            for child in self._children:
                count = stringchildren.get(child.tostring(), 0)
                stringchildren[child.tostring()] = count + 1
            string += ',[' + list(stringchildren)[0] + ':' + str(stringchildren[list(stringchildren)[0]])
            for child in list(stringchildren)[1:]:
                string += "," + child + ':' + str(stringchildren[child])
            string += ']'
        string += ']'
        return string
    
    def count_children(self):
        stringchildren = {}
        if self._children != None:
            for child in self._children:
                if stringchildren.get(child.tostring(), 0) == 0:
                    stringchildren[child.tostring()] = 1
                else:
                    stringchildren[child.tostring()] = stringchildren[child.tostring()] + 1
        return stringchildren
    
    def histogram(self):
        stringchildren = self.count_children()
        total = 0
        for string in stringchildren:
            total += stringchildren[string]
        for string in stringchildren:
            stringchildren[string] = stringchildren[string]/total
        return stringchildren

    def find_most_with_rating(self, rating):
        stringchildren = self.count_children()
        best = None
        for string in stringchildren:
            if rating in string:
                if best == None or best[0][1] < stringchildren[string]:
                    best = [[string, stringchildren[string]]]
                elif best[0][1] == stringchildren[string]:
                    best.append([string, stringchildren[string]])
                else:
                    continue
        if best == None:
            return [['['+ rating + ',[[no' + rating + ']]]', 0]]
        return best

class TETChild(TET):
    def __init__(self, root, free=None, children=None):
        self._root = root
        if isinstance(children, list): 
            self._children = children
        elif children != None:
            self._children = [children]
        else:
            self._children = children

    def tostring(self):
        string = "[" + self._root
        if self._children != None:
            string += ',[' + self._children[0].tostring()
            for child in self._children[1:]:
                string += "," + child.tostring()
            string += "]"
        string += "]"
        return string


