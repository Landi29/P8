import csv
from datetime import datetime
import pickle
import node2vec as n2v
import networkx as nx
import Paths
import random

def create_graph(data_path):
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

    return graph

print("Creating the graph: ")
graph = create_graph(Paths.GRAPH_DATA_PATH)

print ("Summing the neighbors of nodes")
sum_of_neighbors = 0
for node in graph.nodes():
    neighbors = 0
    for neighbor in graph.neighbors(node):
        neighbors += 1
    sum_of_neighbors += neighbors

value = str(sum_of_neighbors/graph.number_of_nodes)
print("The average number of neighbors for a node is: {}".format(value))