'''
Module for embedding the movielens dataset with 1 million ratings
using node2vec.
'''
import pickle
from datetime import datetime
import networkx
from tqdm import tqdm
from node2vec import Node2Vec
import Paths
import pathlib
import csv


def create_graph_dat(data_path):
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
        graph.add_edge(int("1" + rating_data[1]), int("2" + rating_data[0]),
                       weight=float(rating_data[2]))
    return graph

def create_graph_csv(data_path):
    graph = networkx.Graph()
    with open(data_path, "r") as data:
        csvreader = csv.reader(data)
        for edge in csvreader:
            graph.add_edge(int("1"+ edge[0]), int("2" + edge[1]), weight=float(edge[2]))
    return graph

def print_graph_information(number_of_nodes, number_of_edges):
    '''
    Description
    -----------
    A collection of print statemements for a graph.
    This is to increase the readability of the code and execution of it.

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

    filename = input("Please specify the name of the file to read from: ")
    filepath = Paths.SMALL_GRAPH_FOLDER_PATH / filename
    print("Start at: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    filetype = filename.split(".")[1]
    SAVE_PATH = None

    if filetype == "dat":
        print("Reading the file: ")
        GRAPH = create_graph_dat(filepath)
        print_graph_information(GRAPH.number_of_nodes(), GRAPH.number_of_edges())
        SAVE_PATH = Paths.SMALL_N2V_MODEL_PATH_DATFILE

    elif filetype == "csv":
        fileversion = input("Is the graph with 1 or 2 million ratings?: ")
        if fileversion == "1": 
            SAVE_PATH = Paths.SMALL_N2V_MODEL_PATH_1M
        elif fileversion == "2":
            SAVE_PATH = Paths.SMALL_N2V_MODEL_PATH_2M
        else: 
            print("You did not specify a valid value.")
        print("Reading the file: ")
        GRAPH = create_graph_csv(filepath)
        print_graph_information(GRAPH.number_of_nodes(), GRAPH.number_of_edges())
        

    # Generate walks
    print("Generate walks:")
    #node2vec = Node2Vec(graph, dimensions=20, walk_length=16, num_walks=100)

    GRAPH_N2V = Node2Vec(GRAPH, dimensions=20, walk_length=20, num_walks=50, p=1, q=2)

    # Learn embeddings
    print("Learning embeddings:")
    N2V_MODEL = GRAPH_N2V.fit(window=10, min_count=1)
    print("nv2model is written to disc")
    with open(SAVE_PATH, "wb") as disc_file:
        pickle.dump(N2V_MODEL, disc_file)
    print("Finished at: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
