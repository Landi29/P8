import networkx as nx
import matplotlib.pyplot as plt
import csv
import pathlib
import sys


MOVIE_NODES_PATH = pathlib.Path.cwd() /'Implementation' / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() /'Implementation'/ 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() /'Implementation'/ 'Movielens_data' / 'graph.csv'
newpath = "Movielens_data\\graph.csv"


gr = nx.Graph()


string = 5645

a = sys.getsizeof(string)
print(a)
#with open(GRAPH_DATA_PATH, "r") as fp:
    #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
#    for edge in csv.reader(fp):
#        gr.add_edge(edge[0], edge[1], weight = edge[2])


#    non = gr.number_of_nodes()
#    noe = gr.number_of_edges()
#    print("success:"+ str(non) +" "+ str(noe))
