'''
Module for embedding the movielens dataset with 1 million ratings
using node2vec.
'''
import json
import pickle
from datetime import datetime
import networkx
from tqdm import tqdm
from node2vec import Node2Vec
import Paths
import pathlib
import csv
from folds_training import get_fold_indexes


def create_graph_csv(data_path):
    '''
    Description
    -----------
    Create a graph based on the csv files. 

    Parameters
    ----------
    `data_path`: File path to the graph data.
    '''
    graph = networkx.Graph()
    with open(data_path, "r") as data:
        csvreader = csv.reader(data)
        for edge in csvreader:
            graph.add_edge(int(edge[0].replace("M:","1")), 
                           int(edge[1].replace("U:","2")), weight=float(edge[2]))
    return graph


def create_graph_from_folds(data_path, list_of_folds):
    graph = networkx.Graph()
    with open(data_path, "r") as read_file:
        graph_data = json.load(read_file)
    # For each of the folds    
    for fold in list_of_folds:
        for edge in graph_data[fold]:
            graph.add_edge(int(edge[0].replace("M:","1")), 
                           int(edge[1].replace("U:","2")), weight=float(edge[2]))
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

    FILENAME = "Folds_100k.json"
    filepath = Paths.EXPERIMENT_DATA_PATH / FILENAME
    file_data = FILENAME.split(".")
    #filetype = file_data[1]

    # if filetype == "csv":
    #     print("Start at: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    #     print("Reading the file: ")
    #     GRAPH = create_graph_csv(filepath)
    #     print_graph_information(GRAPH.number_of_nodes(), GRAPH.number_of_edges())

    
    fold_keys = get_fold_indexes()
    iteration = 1
    for list_of_folds in fold_keys:
        print("Iteration {} start at: {}".format(str(iteration),
                                                 datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n"))

        OUTPUT_PATH = Paths.EXPERIMENT_DATA_OUTPUT_PATH / (file_data[0] + '_' + str(iteration)
                    + '.pkl')
        GRAPH = create_graph_from_folds(filepath, list_of_folds)
        print_graph_information(GRAPH.number_of_nodes(), GRAPH.number_of_edges())

        # Generate walks
        print("Generate walks:")
        GRAPH_N2V = Node2Vec(GRAPH, dimensions=20, walk_length=20, num_walks=50, p=1, q=2)

        # Learn embeddings
        print("Learning embeddings:")
        N2V_MODEL = GRAPH_N2V.fit(window=10, min_count=1)

        with open(OUTPUT_PATH, "wb") as disc_file:
            pickle.dump(N2V_MODEL, disc_file)
        print("nv2model is written to disc")
        print("Iteration {} finished at: {}".format(iteration, 
                                                    datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n"))
        iteration += 1