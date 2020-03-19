import networkx as nx
import matplotlib.pyplot as plt
import csv
import pathlib
import sys
import node2vec
from datetime import datetime

#Link for article about node2vec and graph2vec with useful links https://maelfabien.github.io/machinelearning/graph_5/#
# https://github.com/eliorc/node2vec Node2vec implementation
# https://arxiv.org/pdf/1607.00653.pdf Node2vec article
# https://github.com/benedekrozemberczki/graph2vec Graph2vec implementation


MOVIE_NODES_PATH = pathlib.Path.cwd() /'Implementation' / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() /'Implementation'/ 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() /'Implementation'/ 'Movielens_data' / 'graph.csv'
NETWORKX_GRAPH = pathlib.Path.cwd() /'Implementation'/ 'Movielens_data' / 'movielens.edgelist'

#method to create a netwrokx graph using the graph.csv file from movielens and saves it as an .edgelist file
def create_graph(path):

    graph = nx.Graph()

    with open(GRAPH_DATA_PATH, "r") as fp:
        #edge is an array of the form [MovieId,UserID,Rating]
        csvreader = csv.reader(fp)
        next(csvreader)
        for edge in csvreader:
                graph.add_edge(edge[0], edge[1], weight = edge[2])

        non = graph.number_of_nodes()
        noe = graph.number_of_edges()
        now = datetime.now()
        print(now)
        print("success:"+" nodes:"+ str(non) +" Edges:"+str(noe))

        nx.write_weighted_edgelist(graph, path, comments='#', delimiter=',', encoding='utf-8')
        now = datetime.now()
        print(now)
        print("Writing done")




#Method to load the graph from an .edgelist file
def load_graph(path):
    
    graph = nx.read_weighted_edgelist(path, comments='#', delimiter=',',create_using=None, nodetype=None, encoding='utf-8')

    return graph


def node2vec(graph):

    return

#create_graph(NETWORKX_GRAPH)

#graph = load_graph(NETWORKX_GRAPH)