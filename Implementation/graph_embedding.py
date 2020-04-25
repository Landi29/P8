from node2vec import Node2Vec
import networkx
import Paths
from tqdm import tqdm
import pickle
def create_graph(data_path):
    graph = networkx.Graph()
    #with open(data_path, "r") as data:
        #ratings = [next(data) for x in range(100000)]
    with open(data_path, "r") as data:
        ratings = data.readlines()
    
    for rating in tqdm(ratings):
        rating_data = rating.split("::")
        graph.add_edge(int("1" + rating_data[0]), int("2" + rating_data[1]), weight = float(rating_data[2]))
    return graph

def print_graph_information(number_of_nodes, number_of_edges):
    print("Graph created.")
    print("Graph information:")
    print("Number of nodes: {}".format(number_of_nodes))
    print("Number of edges: {}".format(number_of_edges))

if __name__ == "__main__":
    print("Reading the file: ")
    graph = create_graph(Paths.SMALL_GRAPH_RATINGS_PATH)
    print_graph_information(graph.number_of_nodes(), graph.number_of_edges())
    
    # Generate walks
    print("Generate walks:")
    node2vec = Node2Vec(graph, dimensions=20, walk_length=16, num_walks=100)
    #graphn2v = Node2Vec(graph, dimensions= 20, walk_length=20, num_walks=50, p=1, q=2, workers=4)

    # Learn embeddings 
    print("Learning embeddings:")
    nv2model = node2vec.fit(window=10, min_count=1)
    print("nv2model is written to disc")
    with open(Paths.SMALL_NV2_MODEL_PATH, "wb") as disc_file:
        pickle.dump(nv2model, disc_file) 