class TET:
    '''
    a TET is a tree structure that represent substructures in graphs
    '''
    def __init__(self, root=None, freevars=None, children=None):
        self._root = root
        self._freevars = freevars
        self._children = children

    def getroot(self):
        '''
        get the protected root of the tree
        '''
        return self._root

    def isroot(self, user):
        '''
        checks if an user is the root of this tree
        '''
        if user == self._root:
            return True
        return False

    def isleaf(self):
        return self._children is None
    
    def isoverleaf(self):
        return self._children[0].isleaf()

    def getchildren(self):
        '''
        gets a list of children to the root
        '''
        return self._children
    
    def getchildrenwithkey(self,key):
        for child in self._children:
            if child.tostring() == key:
                return child

    def addchild(self, child):
        '''
        adds a child to the root
        '''
        if self._children is None:
            self._children = [child]
        else:
            self._children.append(child)

    def tostring(self):
        '''
        converts the tree to a string
        '''
        stringchildren = {}
        string = "[" + self._root
        if self._children is not None:
            for child in self._children:
                count = stringchildren.get(child.tostring(), 0)
                stringchildren[child.tostring()] = count + 1
            string += ',[' + list(stringchildren)[0] + ':'\
                + str(stringchildren[list(stringchildren)[0]])
            for child in list(stringchildren)[1:]:
                string += "," + child + ':' + str(stringchildren[child])
            string += ']'
        string += ']'
        return string

    def count_children(self):
        '''
        counts the amount of each subtet returning a dictionary
        where the key is the subtree containing an integer
        '''
        stringchildren = {}
        if self._children is not None:
            for child in self._children:
                if stringchildren.get(child.tostring(), 0) == 0:
                    stringchildren[child.tostring()] = 1
                else:
                    stringchildren[child.tostring()] = stringchildren[child.tostring()] + 1
        return stringchildren

    def histogram(self):
        '''
        represents the countchildren as a histogram by converting the values to persentile values
        '''
        stringchildren = self.count_children()
        total = 0
        for string in stringchildren:
            total += stringchildren[string]
        for string in stringchildren:
            stringchildren[string] = stringchildren[string]/total
        return stringchildren

    def find_most_with_rating(self, rating):
        '''
        this funktion finds the most frequent substructure with a specific trade or rating
        '''
        stringchildren = self.count_children()
        best = None
        for string in stringchildren:
            if rating in string:
                if best is None:
                    best = [[string, stringchildren[string]]]
                elif best[0][1] < stringchildren[string]:
                    best = [[string, stringchildren[string]]]
                elif best[0][1] == stringchildren[string]:
                    best.append([string, stringchildren[string]])
        if best is None:
            return [['['+ rating + ',[[no' + rating + ']]]', 0]]
        return best

class TETChild(TET):
    '''
    tetchild is a class that can most of what a tet can but when
    writing to string it does not need the number of the children
    '''
    def __init__(self, root, free=None, children=None):
        self._root = root
        self._freevars = free
        if children is not None and not isinstance(children, list):
            children = [children]
        super().__init__(root, free, children)

    def tostring(self):
        string = "[" + self._root
        if self._children is not None:
            string += ',[' + self._children[0].tostring()
            for child in self._children[1:]:
                string += "," + child.tostring()
            string += "]"
        string += "]"
        return string
