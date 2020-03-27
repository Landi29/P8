"""Module for creating a graph using networkx
and training a node2vec model given a networkx graph"""

import csv
import pathlib
from datetime import datetime
import pickle
import node2vec as n2v
import networkx as nx

#Link for article about node2vec and graph2vec with useful links https://maelfabien.github.io/machinelearning/graph_5/#
# https://github.com/eliorc/node2vec Node2vec implementation
# https://arxiv.org/pdf/1607.00653.pdf Node2vec article
# https://github.com/benedekrozemberczki/graph2vec Graph2vec implementation


#Different filepaths used for the project, these paths are used for the different methods.
MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
GRAPH_DATA_PATH_1000 = pathlib.Path.cwd() / 'Movielens_data' / 'graphs1000.csv'
NETWORKX_GRAPH = pathlib.Path.cwd() / 'Movielens_data' / 'movielens.edgelist'
NETWORKX_GRAPH_1000 = pathlib.Path.cwd() / 'Movielens_data' / 'movielens1000.edgelist'
NETWORKX_GRAPH_500 =pathlib.Path.cwd() / 'Movielens_data' / 'movielens500.edgelist'
TEMP_FOLDER = pathlib.Path.cwd() / 'temp_folder'

#method to create a NetworkX graph using graph representation data
def create_graph(data_path, save_path):
    """
    Creates a NetworkX graph and saves it as an .edgelist file

    Parameters:
    data_path (filepath): Filepath to input data, should be a csv file
    save_path (filepath): Filepath where to save the data, filename should end on .edgelist
    """


    graph = nx.Graph()

    with open(data_path, "r") as fp:
        csvreader = csv.reader(fp)

        #use this if first line is a header
        #next(csvreader)

        #edge is a list of the form [MovieId,UserID,Rating]
        for edge in csvreader:
            graph.add_edge(edge[0], edge[1], weight=edge[2])

        non = graph.number_of_nodes()
        noe = graph.number_of_edges()

        print("success:"+" nodes:"+ str(non) +" Edges:"+str(noe))

        now = datetime.now()
        print("Saving graph as edgelist, started: "+ now)

        nx.write_weighted_edgelist(graph, save_path, comments='#', delimiter=',', encoding='utf-8')

        now = datetime.now()
        print("Saved graph as edgelist, finished: "+now)


#Method for loading a edgelist into a networkx graph
#takes a filepath to a .edgelist
#returns the NetworkX graph
def load_graph(path):
    """
    Reads a .edgelist graph into a NetworkX graph

    Parameters:
    path (filepath): Filepath for an .edgelist file to read

    Returns:
    graph: returns a NetworkX graph object
    """

    graph = nx.read_weighted_edgelist(path, comments='#', delimiter=',', create_using=None, nodetype=None, encoding='utf-8')

    return graph


#Runs the node2vec package on a given NetworkX graph
def run_node2vec(graph, save_path):
    """
    Runs the node2vec method from Node2Vec on a given graph, saves it as a pickle

    Parameters:
    graph (Networkx graph): NetworkX graph objects
    save_path (filepath): Filepath for where to save the pickled model
    """

    #Parameter p is the propability of revisitting a node you have just seen, a high value means we are less likely to backtract to it
    #Parameter q makes the random walk more biased towards nodes close to our starting node, a high value makes it stay close to out start node
    graphn2v = n2v.Node2Vec(graph, dimensions=50, walk_length=30, num_walks=50, p=2, q=1, workers=1, temp_folder=TEMP_FOLDER)

    n2vmodel = graphn2v.fit(window=10, min_count=5)

    pickle.dump(n2vmodel, open(save_path, "wb"))

#Loads a pickled node2vec model
def get_model(model_path):
    """
    Loads and unpickles a pickled node2vec model

    Parameters:
    model_path (filepath): filepath to pickle node2vec model for unpickled
    """

    model = pickle.load(open(model_path, "rb"))
    return model


if __name__ == "__main__":
    #create_graph(GRAPH_DATA_PATH_1000,NETWORKX_GRAPH_1000)
    #graph = load_graph(NETWORKX_GRAPH)
    #run_node2vec(graph,"n2vfullmodel")
    #mostsimilar("U:900")
    #model = getmodel("n2vmodel2.p")
    print(n2v.__file__)