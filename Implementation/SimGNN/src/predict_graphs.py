import pickle
import math

def predictGraph(user1, user2, graphs):
    """
    This function loads in our trained neural networks and uses it to predict how similar two
    graphs are.
    Parameter: user1 and user2 are the two graphs we would like to find similarity on.
    graphs is all the graphs
    Return: A similarity score on how similar user1 and user 2 is.
    """
    trainer = pickle.load(open("simGNN.p", "rb"))
    graphDict = create_simgnn_file(user1, user2, graphs)
    result = trainer.predictionScore(graphDict)
    print(-math.log(result))


def create_simgnn_file(user1, user2, graphs):
    user1_graph = graphs[user1]
    user2_graph = graphs[user2]
    return_dict = {}
    interm_graph, interm_labels = create_SimGNN_graph(user1, user1_graph)
    return_dict["graph_1"] = interm_graph
    return_dict["labels_1"] = interm_labels
    interm_graph, interm_labels = create_SimGNN_graph(user1, user2_graph)
    return_dict["graph_2"] = interm_graph
    return_dict["labels_2"] = interm_labels
    return_dict["ged"] = 0
    return return_dict


def create_SimGNN_graph(user, user_graph):
    labels = []
    graph = []
    labels.append(user)
    labels.append("High")
    labels.append("Medium")
    labels.append("Low")
    graph.append([0, 1])
    graph.append([0, 2])
    graph.append([0, 3])
    for edges in user_graph:
        edge, labels = get_new_graph(edges, labels)
        graph.append(edge[0])
    return graph, labels


def get_new_graph(graph, labels):
    edgelist = []
    value = float(graph[2].strip())
    labels.append(graph[0])
    position = labels.index(graph[0])
    if value > 3.5:
        edgelist.append([1, position])
    elif value > 2.5:
        edgelist.append([2, position])
    else:
        edgelist.append([3, position])
    return edgelist, labels