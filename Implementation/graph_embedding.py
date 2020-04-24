from node2vec import Node2Vec
import networkx
import Paths



def create_graph(data_path):
    with open(data_path, "r") as data:
        ratings = data.readlines()
    graph = networkx.Graph()

    return graph





if __name__ == "__main__":
    graph = create_graph(Paths.SMALL_GRAPH_RATINGS_PATH)
    # Generate walks
    node2vec = Node2Vec(graph, dimensions=20, walk_length=16, num_walks=100)

    # Learn embeddings 
    model = node2vec.fit(window=10, min_count=1)