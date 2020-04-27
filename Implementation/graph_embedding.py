from node2vec import Node2Vec
import networkx
import Paths
from tqdm import tqdm
import pickle
from datetime import datetime

def create_graph(data_path):
    '''
    Description
    -----------
    Create a networkx graph based on the data of the form: userid::movieid::rating

    Parameters
    ----------
    `data_path`: File path to the graph data. 
    '''
    graph = networkx.Graph()
    with open(data_path, "r") as data:
        ratings = data.readlines()
    
    for rating in tqdm(ratings):
        rating_data = rating.split("::")
        graph.add_edge(int("1" + rating_data[0]), int("2" + rating_data[1]), weight = float(rating_data[2]))
    return graph

def print_graph_information(number_of_nodes, number_of_edges):
    '''
    Description
    -----------
    A collection of print statemements for a graph. This is to increase the readability of the code and execution of it.

    Parameters
    ----------
    number_of_nodes: The number of nodes in the graph.
    number_of_edges: The number of edges in the graph.
    '''
    print("Graph created.")
    print("Graph information:")
    print("Number of nodes: {}".format(number_of_nodes))
    print("Number of edges: {}".format(number_of_edges))

if __name__ == "__main__":

    print("Start at: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    print("Reading the file: ")
    graph = create_graph(Paths.SMALL_GRAPH_RATINGS_PATH)
    print_graph_information(graph.number_of_nodes(), graph.number_of_edges())
    
    # Generate walks
    print("Generate walks:")
    #node2vec = Node2Vec(graph, dimensions=20, walk_length=16, num_walks=100)

    graphn2v = Node2Vec(graph, dimensions= 20, walk_length=20, num_walks=50, p=1, q=2)

    # Learn embeddings 
    print("Learning embeddings:")
    nv2model = graphn2v.fit(window=10, min_count=1)
    print("nv2model is written to disc")
    with open(Paths.SMALL_N2V_MODEL_PATH_2, "wb") as disc_file:
        pickle.dump(nv2model, disc_file) 
    print("Finished at: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
