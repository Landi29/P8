import pickle
import math

class predictGraph:
    
    def __init__(self, graph):
        self.trainer = pickle.load(open("simGNN.p", "rb"))
        self.graph = graph
    
    def predictGraph(self, user1, user2):
        """
        This function uses our trained neural network (trainer) to predict how similar two
        graphs are.
        Parameter: user1 and user2 are the two graphs we would like to find similarity on.
        graphs is all the graphs
        Return: A similarity score on how similar user1 and user 2 is.
        """
        graphDict = self.create_simgnn_file(user1, user2, self.graph)
        result = self.trainer.predictionScore(graphDict)
        print(-math.log(result))


    def create_simgnn_file(self, user1, user2):
        user1_graph = self.graph[user1]
        user2_graph = self.graph[user2]
        graph_pair = {}
        interm_graph, interm_labels = self.create_SimGNN_graph(user1, user1_graph)
        graph_pair["graph_1"] = interm_graph
        graph_pair["labels_1"] = interm_labels
        interm_graph, interm_labels = self.create_SimGNN_graph(user1, user2_graph)
        graph_pair["graph_2"] = interm_graph
        graph_pair["labels_2"] = interm_labels
        graph_pair["ged"] = 0
        return graph_pair


    def create_SimGNN_graph(self, user, user_graph):
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
            edge, labels = self.get_new_graph(edges, labels)
            graph.append(edge[0])
        return graph, labels


    def get_new_graph(self, graph, labels):
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
        return edgelist