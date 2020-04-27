"""Contains functionality for creating the dataset used in SimGNN"""
import pathlib
from tqdm import tqdm
import json
import simgnn.main_SimGNN as SimGNN

class SimGNNDatasetCreator:
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
    GRAPHLIST_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graphlists.edgelist'
    JSON_FILE = pathlib.Path.cwd() / 'Movielens_data' / 'training.pkl'
    graph = "C:/Users/FiercePC/Documents/SimGNN-master/dataset/graph.csv"

    def make_dataset(self):
        """
        Will from the graph.csv file which contains an edgelist create every user graph
        It will then use these values to create the dataset used for SimGNN.
        Currently the amount of data entries per user is set to 5
        """
        with open(self.GRAPH_DATA_PATH, "r") as file:
            next(file)
            labels = {}
            allgraphs = {}
            amount_of_graphs = 0
            label_amount = 0
            label_list = []
            label_list.append("High")
            label_list.append("Medium")
            label_list.append("Low")
            for lines in tqdm(file):
                lines_split = lines.split(",")
                if lines_split[1] == "U:100":
                    break
                if lines_split[1] in allgraphs:
                    labels[lines_split[1]].append(lines_split[0])
                    edge, labels[lines_split[1]] = self.get_new_graph(lines_split, labels[lines_split[1]])
                    allgraphs[lines_split[1]].append(edge[0])
                    if label_list.__contains__(lines_split[0]):
                        continue
                    else:
                        label_list.append(lines_split[0])
                else:
                    allgraphs[lines_split[1]] = []
                    labels[lines_split[1]] = []
                    labels[lines_split[1]].append(lines_split[1])
                    labels[lines_split[1]].append("High")
                    labels[lines_split[1]].append("Medium")
                    labels[lines_split[1]].append("Low")
                    labels[lines_split[1]].append(lines_split[0])
                    allgraphs[lines_split[1]].append([labels[lines_split[1]].index(lines_split[1]), 1])
                    allgraphs[lines_split[1]].append([labels[lines_split[1]].index(lines_split[1]), 2])
                    allgraphs[lines_split[1]].append([labels[lines_split[1]].index(lines_split[1]), 3])
                    edge, labels[lines_split[1]] = self.get_new_graph(lines_split, labels[lines_split[1]])
                    allgraphs[lines_split[1]].append(edge[0])
                    label_list.append(lines_split[1])
                    if label_list.__contains__(lines_split[0]):
                        continue
                    else:
                        label_list.append(lines_split[0])
            dataset = {}
            #label_list = self.make_zero_list(labels)
            zero_list = []
            for x in tqdm(range(1, allgraphs.__len__())):
                user1 = "U:" + str(x)
                dataset[user1] = {}
                for y in range(x + 1, x + 2):
                    try:
                        user2 = "U:" + str(y)
                        dataset[user1][user2] = {}
                        dataset[user1][user2]["graph_1"] = allgraphs[user1]
                        dataset[user1][user2]["graph_2"] = allgraphs[user2]
                        dataset[user1][user2]["labels_1"] = labels[user1]
                        dataset[user1][user2]["labels_2"] = labels[user2]
                        dataset[user1][user2]["ged"] = self.my_find_ged(labels[user1], labels[user2], allgraphs[user1], allgraphs[user2])
                        amount_of_graphs += 1
                    except:
                        break
        return dataset, amount_of_graphs, label_list

    @staticmethod
    def create_user_graph_and_labels(edgelist):
        label_list = []
        edge_list = []
        intermed = 0
        both = False
        for edge in edgelist:
            if label_list.__contains__(edge[0]):
                intermed = label_list.index(edge[0])
                both = True
            if label_list.__contains__(edge[1]) and both:
                edge_list.append([intermed, label_list.index(edge[0])])
                intermed = 0
                both = False
                continue
            if label_list.__contains__(edge[1]):
                edge_list.append([])

    @staticmethod
    def make_zero_list(label_list):
        zero_list = []
        for user in tqdm(label_list):
            for labels in label_list[user]:
                if zero_list.__contains__(labels):
                    continue
                else:
                    zero_list.append(labels)
        return zero_list

    @staticmethod
    def get_new_graph(graph, labels):
        edgelist = []
        value = float(graph[2].strip())
        if labels.__contains__(graph[0]):
            position = labels.index(graph[0])
        else:
            labels.append(graph[0])
            position = labels.index(graph[0])
        if value > 3.5:
            edgelist.append([1, position])
        elif value > 2.5:
            edgelist.append([2, position])
        else:
            edgelist.append([3, position])
        return edgelist, labels

    @staticmethod
    def my_find_ged(labels1, labels2, graph1, graph2):
        """
        Given 2 users labels and graphs this function finds their Graph Edit Distance aka. how many changes is required
        to make graph 1 look like graph 2.

        Parameters:
        labels1 (list): List of every label in graph1
        labels2 (list): List of every label in graph2
        graph1 (list): Edgelist for graph1
        graph2 (list): Edgelist for graph2

        Returns:
        gedscore (integer): Graph Edit Distance for graph1 and graph2
        """
        gedscore = 0
        similarnodes = []
        for node in labels1:
            if labels2.__contains__(node):
                similarnodes.append(node)
                continue
            else:
                gedscore += 1
        for node in labels2:
            if labels1.__contains__(node):
                continue
            else:
                gedscore += 1
        return gedscore

f = SimGNNDatasetCreator()
dataset, amount_of_runs, labels = f.make_dataset()
label_dict = {}
for label in labels:
    label_dict[label] = labels.index(label)
SimGNN.main_SimGNN(dataset, [], amount_of_runs, label_dict)
