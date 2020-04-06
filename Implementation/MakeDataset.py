"""Contains functionality for creating the dataset used in SimGNN"""
import pathlib
from tqdm import tqdm

class SimGNNDatasetCreator:
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
    GRAPHLIST_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graphlists.edgelist'
    JSON_FILE = pathlib.Path.cwd() / 'Movielens_data' / 'training.pkl'
    def __init__(self):
        """
        INIT file for SimGNNDatasetCreator.
        Will from the graph.csv file which contains an edgelist create every user graph
        It will then use these values to create the dataset used for SimGNN.
        Currently the amount of data entries per user is set to 10
        """
        with open(self.GRAPH_DATA_PATH, "r") as file:
            next(file)
            labels = {}
            allgraphs = {}
            for lines in file:
                lines_split = lines.split(",")
                if lines_split[1] in allgraphs:
                    allgraphs[lines_split[1]].append([lines_split[0], lines_split[1], lines_split[2]])
                    labels[lines_split[1]].append(lines_split[0])
                else:
                    allgraphs[lines_split[1]] = []
                    labels[lines_split[1]] = []
                    allgraphs[lines_split[1]].append([lines_split[0], lines_split[1], lines_split[2]])
                    labels[lines_split[1]].append(lines_split[1])
                    labels[lines_split[1]].append(lines_split[0])
            dataset = {}
            for x in tqdm(range(1, allgraphs.__len__())):
                user1 = "U:" + str(x)
                dataset[user1] = {}
                for y in range(x+1, x+11):
                    try:
                        user2 = "U:" + str(y)
                        dataset[user1][user2] = {}
                        dataset[user1][user2]["graph_1"] = allgraphs[user1]
                        dataset[user1][user2]["graph_2"] = allgraphs[user2]
                        dataset[user1][user2]["label_1"] = labels[user1]
                        dataset[user1][user2]["label_2"] = labels[user2]
                        dataset[user1][user2]["GED"] = self.my_find_ged(labels[user1], labels[user2], allgraphs[user1], allgraphs[user2])
                    except:
                        break

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
        for node in labels1:
            if labels2.__contains__(node):
                continue
            else:
                gedscore += 1
        for node in labels2:
            if labels1.__contains__(node):
                continue
            else:
                gedscore += 1
        return gedscore


SimGNNDatasetCreator()
JSON_FILE = pathlib.Path.cwd() / 'Movielens_data' / 'training.json'