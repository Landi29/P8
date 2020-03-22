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
            self._children=[child]
        self._children.append(child)


class TETChild:
    def __init__(self, movie, rating, genres):
        self._rating = rating
        self._movie = movie
        self._children = genres

tet = TET()


