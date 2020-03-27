import pathlib
import networkx as nx

"""SimRank can return the similarity of two nodes in the graph by running the SimRank algorithm
For more detail on SimRank please read http://ilpubs.stanford.edu:8090/508/1/2001-41.pdf"""


class SimRank:
    # Graph.csv path
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'

    """Loads graph.csv and creates a sub graph of the given users
    
    Parameters:
    u1 (String): User ID of user 1
    u2 (String): User ID of user 2
    path (String): Path to the graph.csv file
    
    Returns:
    NetworkX Graph Object"""
    @staticmethod
    def load_graph_users(u1, u2, path):
        if int(u1) >= int(u2):
            maximal = int(u1)
        else:
            maximal = int(u2)
        with open(path) as file:
            next(file)
            graph = nx.Graph()
            for lines in file:
                splitlines = lines.split(",")
                if splitlines[1] == u1:
                    graph.add_edge(u1, "M"+splitlines[0], weight=splitlines[2])
                elif splitlines[1] == u2:
                    graph.add_edge(u2, "M"+splitlines[0], weight=splitlines[2])
                else:
                    if maximal < int(splitlines[1]):
                        break
                    continue
            return graph

    """Given 2 users returns the similarity of them using NetworkX SimRank
    
    Parameters:
    user1 (String): User ID of user 1
    user2 (String): User ID of user 2
    
    Returns:
    int: Similarity of user 1 and user 2"""
    def similarity(self, user1, user2):
        graph = self.load_graph_users(user1, user2, self.GRAPH_DATA_PATH)
        similarity = nx.algorithms.similarity.simrank_similarity(graph, user1, user2)
        return similarity
