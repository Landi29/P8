"""Contains functionality for creating the dataset used in SimGNN"""
from tqdm import tqdm
import json
import Paths

class SimGNNDatasetCreator:
    def make_dataset_fold(self):
        """
        Takes the list of folds and creates the dataset for SimGNN.
        Will create the files so SimGNN can run on them.
        """
        with open(Paths.FOLDS_DATA_PATH, "r") as file:
            folds = json.load(file)
            labels = []
            fold_list = []
            labels.extend(["High", "Medium", "Low"])
            start_val = 0
            end_val = 7
            currentfold_val = start_val
            for _ in range(0, 10):
                for x in range(0, 8):
                    currentfold = "fold" + str(currentfold_val)
                    for line in folds[currentfold]:
                        fold_list.append(line)
                    if currentfold == end_val:
                        break
                    else:
                        currentfold_val += 1
                        if currentfold_val > 9:
                            currentfold_val = 0
                dataset, labels = self.make_dataset(fold_list, labels)
                with open(Paths.SIMGNN_DATA_PATH/str(start_val) + "_to_" + str(end_val) + ".json", "w") as f:
                    json.dump(dataset, f)
                fold_list = []
                start_val = start_val + 1 if start_val < 9 else 0
                end_val = end_val + 1 if end_val < 9 else 0
                currentfold_val = start_val
            labels = self.make_single_fold_set(labels)
            label_dict = {}
            for label in labels:
                label_dict[label] = labels.index(label)
            with open("Movielens_data/SimGNN/label_list.json", "w") as file:
                json.dump(label_dict, file)

    def make_single_fold_set(self, labels):
        """
        Will take the folds file and create the SimGNN dataset from each individual fold to use for test.

        Parameters:
        labels (List): A list of labels of every node seen so far

        Returns:
        labels (List): Contains all labels seen after running through each individual fold.
        """
        with open(Paths.FOLDS_DATA_PATH, "r") as file:
            folds = json.load(file)
        for fold in folds:
            dataset, labels = self.make_dataset(folds[fold], labels)
            with open("Movielens_data/SimGNN/" + fold + ".json", "w") as file:
                json.dump(dataset, file)
        return labels



    def make_dataset(self, graphs, label_list):
        """
        Will from the graph.csv file which contains an edgelist create every user graph
        It will then use these values to create the dataset used for SimGNN.

        Parameters:
        graph (list): List of all edges in the graph.
        label_list (list): A list of already seen labels.

        Return:
        dataset (Dictionary): A dictionary containing each graph pair.
        label_list (list): A list of all seen labels.
        """
        labels = {}
        allgraphs = {}
        for lines in tqdm(graphs):
            if lines[1] in allgraphs:
                # If the user exists in the dictionary of all graphs - We create the edge for the movie and add to the
                # list of edges. We update the labels list as it will be used later on.
                labels[lines[1]].append(lines[0])
                edge, labels[lines[1]] = self.get_new_graph(lines, labels[lines[1]])
                allgraphs[lines[1]].append(edge[0])
                if label_list.__contains__(lines[0]):
                    continue
                else:
                    label_list.append(lines[0])
            else:
                # If the user is not already in the dictionary of all graphs - We add a new index for him where we place
                # his new edges too (1 for high, 2 for medium and 3 for low) this is done to reduce the amount of lookups
                # later in the code. Labels are used to reduce the amount of lookup later when having to find all labels
                allgraphs[lines[1]] = []
                labels[lines[1]] = []
                labels[lines[1]].extend(["High", "Medium", "Low", lines[0], lines[1]])
                allgraphs[lines[1]].extend([[labels[lines[1]].index(lines[1]), 1],
                                            [labels[lines[1]].index(lines[1]), 2],
                                            [labels[lines[1]].index(lines[1]), 3]])
                edge, labels[lines[1]] = self.get_new_graph(lines, labels[lines[1]])
                allgraphs[lines[1]].append(edge[0])
                label_list.append(lines[1])
                if label_list.__contains__(lines[0]):
                    continue
                else:
                    label_list.append(lines[0])
        dataset = {}
        for x in tqdm(range(1, allgraphs.__len__())):
            user1 = "U:" + str(x)
            dataset[user1] = {}
            for y in range(x + 1, allgraphs.__len__()):
                try:
                    user2 = "U:" + str(y)
                    dataset[user1][user2] = {}
                    dataset[user1][user2]["graph_1"] = allgraphs[user1]
                    dataset[user1][user2]["graph_2"] = allgraphs[user2]
                    dataset[user1][user2]["labels_1"] = labels[user1]
                    dataset[user1][user2]["labels_2"] = labels[user2]
                    dataset[user1][user2]["ged"] = self.find_ged(labels[user1], labels[user2])
                except:
                    break
        return dataset, label_list

    @staticmethod
    def get_new_graph(edge, labels):
        """
        Takes a edge and its labels to create a new edge containing high, medium or low.

        Parameters:
        edge (list): Edge of type [MovieNode, UserNode, Rating]
        labels (list): List of labels in current graph

        Returns:
        edgelist (list): New edge containing 1,2 or 3 representing high, medium and low and a movie.
        labels (list): The list of labels containing the new movie too.
        """
        edgelist = []
        value = float(edge[2].strip())
        if labels.__contains__(edge[0]):
            position = labels.index(edge[0])
        else:
            labels.append(edge[0])
            position = labels.index(edge[0])
        if value > 3.5:
            edgelist.append([1, position])
        elif value > 2.5:
            edgelist.append([2, position])
        else:
            edgelist.append([3, position])
        return edgelist, labels

    @staticmethod
    def find_ged(labels1, labels2):
        """
        Given 2 users labels this function finds their Graph Edit Distance aka. how many changes is required
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

