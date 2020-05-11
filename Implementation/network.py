"""Module for creating a graph using networkx
and training a node2vec model given a networkx graph"""
import csv
from datetime import datetime
import pickle
import node2vec as n2v
import networkx as nx
import Paths
import random

#Link for article about node2vec and graph2vec with useful links https://maelfabien.github.io/machinelearning/graph_5/#
# https://github.com/eliorc/node2vec Node2vec implementation
# https://arxiv.org/pdf/1607.00653.pdf Node2vec article
# https://github.com/benedekrozemberczki/graph2vec Graph2vec implementation

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
    print("Saving graph as edgelist, started: "+ str(now))

    nx.write_weighted_edgelist(graph, save_path, comments='#', delimiter=',', encoding='utf-8')

    now = datetime.now()
    print("Saved graph as edgelist, finished: "+ str(now))


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

    graph = nx.read_weighted_edgelist(path, comments='#', delimiter=',',
                                      create_using=None, nodetype=None, encoding='utf-8')

    return graph


#Runs the node2vec package on a given NetworkX graph
def run_node2vec(graph, save_path):
    """
    Runs the node2vec method from Node2Vec on a given graph, saves it as a pickle

    Parameters:
    graph (Networkx graph): NetworkX graph objects
    save_path (filepath): Filepath for where to save the pickled model
    """

    #Parameter p is the propability of revisitting a node you have just seen,
    #a high value means we are less likely to backtract to it
    #Parameter q makes the random walk more biased towards nodes close to our starting node,
    # a high value makes it stay close to out start node
    graphn2v = n2v.Node2Vec(graph, dimensions=50, walk_length=40, num_walks=50, p=1, q=2, workers=1)

    n2vmodel = graphn2v.fit(window=10, min_count=5)

    pickle.dump(n2vmodel, open(save_path, "wb"))

#Loads a pickled node2vec model
def get_model(model_path):
    """
    Loads and unpickles a pickled node2vec model

    Parameters:
    model_path (filepath): filepath to a pickled node2vec model
    """

    model = pickle.load(open(model_path, "rb"))
    return model

def get_key_vectors(w2v_model):
    """
    Given a word2vec model loads the keys and their vector embedding into a dictionary

    Parameters:
    model (word2vec.model): trained word2vec model
    """

    keydict = {}

    for key in w2v_model.wv.vocab:
        keydict[key] = w2v_model.wv[key]

    return keydict

def create_dict_graph(inputpath):
    """
    Loads a .csv edgelist of a graph into a dictionary representation of the graph

    Parameters:
    inputpath (filepath): filepath to read from
    """

    #Create a dictionary containing all nodes and their neighbours
    graphdict = {}
    with open(inputpath, "r") as fp:
        reader = csv.reader(fp)

        for edge in reader:
            temp = graphdict.get(edge[0], [])
            temp2 = graphdict.get(edge[1], [])
            temp.append((edge[1], edge[2]))
            temp2.append((edge[0], edge[2]))
            graphdict[edge[0]] = temp
            graphdict[edge[1]] = temp2

    return graphdict


def create_subgraphs(inputpath, max_number_of_nodes):
    """
    Not implemented!

    Creates subgraphs from a graph, where number of nodes in the graph is at most
    equal to a threshold given

    Parameters:
    inputpath (filepath): filepath to a .csv edgelist representaiton of a graph
    max_number_of_nodes (int): Maximum number of nodes a subgraph can have
    """

    #get out dictionary representation of the full graph
    graphdict = create_dict_graph(inputpath)

    #Shuffle the dictionary and pick a random node not already in a subgraph
    shuffle_nodes = list(graphdict.keys())
    random.shuffle(shuffle_nodes)

    #Construct a new dictionary with that node,
    #expand it with neighboars until nodecount is = threshold
    #Also keep a list of nodes already in a subgraph
    subgraph_dict = {}
    users_in_a_graph = []

    #Iterate through all nodes
    for source in shuffle_nodes:

        #Check if they're not already in a graph
        if source not in users_in_a_graph:
            #add the source node to dictionary
            #add immediate neighbours
            temp = subgraph_dict.get(source, [])
            neighbours = list(graphdict[source])
            temp.append(neighbours)
            subgraph_dict[source] = temp

            #Add the neighbour nodes to our graph
            #Add the original node as their neighbour
            for n in neighbours:
                #n is a tuple of (ID, Rating)
                temp = subgraph_dict.get(n[0], [])
                temp.append((source, n[1]))
                subgraph_dict[n[0]] = temp

            #while len(subgraph_dict) < max_number_of_nodes:
            #    print("Hello") #placeholder fordi at pylint fucking tuder
                #while number of nodes is below threshold
                #find next node to expand
                #expand it and add to dictionary


        #Save this dictionary as our subgraph
        #Keep list of users in subgraph updated

    #Continue construction of new subgraphs/dictionaries until all users are in a subgraph


if __name__ == "__main__":
    #create_graph(Paths.GRAPH_DATA_PATH_100K, Paths.NETWORKX_GRAPH_100K)

    #graph = load_graph(Paths.NETWORKX_GRAPH_100K)

    #run_node2vec(graph,"n2v_100k_model.p")
    model = get_model("n2v_100k_model.p")

    similar = model.wv.most_similar("U:1")
