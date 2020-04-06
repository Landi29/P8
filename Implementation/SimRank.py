import pathlib
import networkx as nx

"""SimRank can return the similarity of two nodes in the graph by running the SimRank algorithm
For more detail on SimRank please read http://ilpubs.stanford.edu:8090/508/1/2001-41.pdf"""


class SimRank:
    # Graph.csv path
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'

    @staticmethod
    def load_graph_users(u1, u2, path):
        """Loads graph.csv and creates a sub graph of the given users

        Parameters:
        u1 (Integer): User ID of user 1
        u2 (Integer): User ID of user 2
        path (String): Path to the graph.csv file

        Returns:
        NetworkX Graph Object"""
        u1_string = "U:" + str(u1)
        u2_string = "U:" + str(u2)
        if u1 >= u2:
            max_val = u1
        else:
            max_val = u2
        with open(path) as file:
            next(file)
            graph = nx.Graph()
            for lines in file:
                file_line_split = lines.split(",")
                if file_line_split[1] == u1_string:
                    graph.add_edge(u1_string, file_line_split[0], weight=file_line_split[2])
                elif file_line_split[1] == u2_string:
                    graph.add_edge(u2_string, file_line_split[0], weight=file_line_split[2])
                else:
                    if max_val < int(file_line_split[1].split(":")[1]):
                        break
                    continue
            return graph

    def similarity(self, user1, user2):
        """Given 2 users returns the similarity of them using NetworkX SimRank

        Parameters:
        user1 (String): User ID of user 1
        user2 (String): User ID of user 2

        Returns:
        int: Similarity of user 1 and user 2"""
        graph = self.load_graph_users(user1, user2, self.GRAPH_DATA_PATH)
        similarity = nx.algorithms.similarity.simrank_similarity(graph, "U:"+str(user1), "U:"+str(user2))
        return similarity

f = SimRank()
f.similarity(1, 2)
