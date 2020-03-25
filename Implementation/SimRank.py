import pathlib
import networkx as nx

# SimRank class
class SimRank:
    # Graph.csv path
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'

    # Loads graph.csv and finds users
    # Input:
    # u1 (User ID of user 1)
    # u2 (User ID of user 2)
    # path (Path to graph.csv)
    # Output:
    # Graph (Sub graph containing User1 and User2)
    def load_graph_users(self, u1, u2, path):
        if int(u1) >= int(u2):
            maxi = int(u1)
        else:
            maxi = int(u2)
        with open(path) as file:
            next(file)
            l = []
            graph = nx.Graph()
            for lines in file:
                l = lines.split(",")
                if l[1] == u1:
                    graph.add_edge(u1, "M"+l[0], weight=l[2])
                elif l[1] == u2:
                    graph.add_edge(u2, "M"+l[0], weight=l[2])
                else:
                    if maxi < int(l[1]):
                        break
                    continue
            return graph

    # Input:
    # user1 (Node ID of user 1)
    # user2 (Node ID of user 2)
    # Output:
    # Returns similarity between user 1 and 2
    def Similarity(self, user1, user2):
        graph = self.load_graph_users(user1, user2, self.GRAPH_DATA_PATH)
        f = nx.algorithms.similarity.simrank_similarity(graph, user1, user2)
        return(f)
