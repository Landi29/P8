"""SimGNN class and runner."""

import glob
import torch
import numpy as np
from tqdm import tqdm, trange
from torch_geometric.nn import GCNConv
from simgnn.layers import AttentionModule, TenorNetworkModule
from simgnn.utils import process_pair, calculate_loss, calculate_normalized_ged

class SimGNN(torch.nn.Module):
    """
    SimGNN: A Neural Network Approach to Fast Graph Similarity Computation
    https://arxiv.org/abs/1808.05689
    """
    def __init__(self, args, number_of_labels):
        """
        :param args: Arguments object.
        :param number_of_labels: Number of node labels.
        """
        super(SimGNN, self).__init__()
        self.args = args
        self.number_labels = number_of_labels
        self.setup_layers()

    def calculate_bottleneck_features(self):
        """
        Deciding the shape of the bottleneck layer.
        """
        if self.args.histogram == True:
            self.feature_count = self.args.tensor_neurons + self.args.bins
        else:
            self.feature_count = self.args.tensor_neurons

    def setup_layers(self):
        """
        Creating the layers.
        """
        self.calculate_bottleneck_features()
        self.convolution_1 = GCNConv(self.number_labels, self.args.filters_1)
        self.convolution_2 = GCNConv(self.args.filters_1, self.args.filters_2)
        self.convolution_3 = GCNConv(self.args.filters_2, self.args.filters_3)
        self.attention = AttentionModule(self.args)
        self.tensor_network = TenorNetworkModule(self.args)
        self.fully_connected_first = torch.nn.Linear(self.feature_count,
                                                     self.args.bottle_neck_neurons)
        self.scoring_layer = torch.nn.Linear(self.args.bottle_neck_neurons, 1)

    def calculate_histogram(self, abstract_features_1, abstract_features_2):
        """
        Calculate histogram from similarity matrix.
        :param abstract_features_1: Feature matrix for graph 1.
        :param abstract_features_2: Feature matrix for graph 2.
        :return hist: Histsogram of similarity scores.
        """
        scores = torch.mm(abstract_features_1, abstract_features_2).detach()
        scores = scores.view(-1, 1)
        hist = torch.histc(scores, bins=self.args.bins)
        hist = hist/torch.sum(hist)
        hist = hist.view(1, -1)
        return hist

    def convolutional_pass(self, edge_index, features):
        """
        Making convolutional pass.
        :param edge_index: Edge indices.
        :param features: Feature matrix.
        :return features: Absstract feature matrix.
        """
        features = self.convolution_1(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_2(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_3(features, edge_index)
        return features

    def forward(self, data):
        """
        Forward pass with graphs.
        :param data: Data dictiyonary.
        :return score: Similarity score.
        """
        edge_index_1 = data["edge_index_1"]
        edge_index_2 = data["edge_index_2"]
        features_1 = data["features_1"]
        features_2 = data["features_2"]

        abstract_features_1 = self.convolutional_pass(edge_index_1, features_1)
        abstract_features_2 = self.convolutional_pass(edge_index_2, features_2)

        if self.args.histogram == True:
            hist = self.calculate_histogram(abstract_features_1,
                                            torch.t(abstract_features_2))

        pooled_features_1 = self.attention(abstract_features_1)
        pooled_features_2 = self.attention(abstract_features_2)
        scores = self.tensor_network(pooled_features_1, pooled_features_2)
        scores = torch.t(scores)

        if self.args.histogram == True:
            scores = torch.cat((scores, hist), dim=1).view(1, -1)

        scores = torch.nn.functional.relu(self.fully_connected_first(scores))
        score = torch.sigmoid(self.scoring_layer(scores))
        return score

class SimGNNTrainer(object):
    """
    SimGNN model trainer.
    """
    def __init__(self, args, labels):
        """
        :param args: Arguments object.
        """
        self.args = args
        self.global_labels = labels
        self.training_graphs = self.args.training_graphs
        self.testing_graphs = self.args.testing_graphs
        self.number_of_labels = len(self.global_labels)
        self.setup_model()

    def setup_model(self):
        """
        Creating a SimGNN.
        """
        self.model = SimGNN(self.args, self.number_of_labels)

    def create_batches(self):
        """
        Creating batches from the training graph list.
        :return batches: List of lists with batches.
        """
        intermediate = []
        if isinstance(self.training_graphs, dict):
            for graph in self.training_graphs:
                for graph_pair in self.training_graphs[graph]:
                    intermediate.append(self.training_graphs[graph][graph_pair])
            self.training_graphs = intermediate
        #random.shuffle(self.training_graphs)
        batches = []
        for graph in range(0, len(self.training_graphs), self.args.batch_size):
            batches.append(self.training_graphs[graph:graph+self.args.batch_size])
        return batches

    def transfer_to_torch(self, data):
        """
        Transferring the data to torch and creating a hash table.
        Including the indices, features and target.
        :param data: Data dictionary.
        :return new_data: Dictionary of Torch Tensors.
        """
        new_data = dict()
        edges_1 = data["graph_1"] + [[y,x] for x,y in data["graph_1"]]

        edges_2 = data["graph_2"] + [[y,x] for x,y in data["graph_2"]]

        edges_1 = torch.from_numpy(np.array(edges_1, dtype=np.int64).T).type(torch.long)
        edges_2 = torch.from_numpy(np.array(edges_2, dtype=np.int64).T).type(torch.long)

        features_1, features_2 = [], []

        for n in data["labels_1"]:
            features_1.append([1.0 if self.global_labels[n] == i else 0.0 for i in self.global_labels])

        for n in data["labels_2"]:
            features_2.append([1.0 if self.global_labels[n] == i else 0.0 for i in self.global_labels])

        features_1 = torch.FloatTensor(np.array(features_1))
        features_2 = torch.FloatTensor(np.array(features_2))

        new_data["edge_index_1"] = edges_1
        new_data["edge_index_2"] = edges_2

        new_data["features_1"] = features_1
        new_data["features_2"] = features_2

        norm_ged = data["ged"]/(0.5*(len(data["labels_1"])+len(data["labels_2"])))

        new_data["target"] = torch.from_numpy(np.exp(-norm_ged).reshape(1, 1)).view(-1).float()
        return new_data

    def process_batch(self, batch):
        """
        Forward pass with a batch of data.
        :param batch: Batch of graph pair locations.
        :return loss: Loss on the batch.
        """
        self.optimizer.zero_grad()
        losses = 0
        for data in batch:
            data = self.transfer_to_torch(data)
            prediction = self.model(data)
            losses = losses + torch.nn.functional.mse_loss(data["target"], prediction)
        losses.backward(retain_graph=True)
        self.optimizer.step()
        loss = losses.item()
        return loss

    def fit(self):
        """
        Fitting a model.
        """
        print("\nModel training.\n")
        self.optimizer = torch.optim.Adam(self.model.parameters(),
                                          lr=self.args.learning_rate,
                                          weight_decay=self.args.weight_decay)

        self.model.train()
        epochs = trange(self.args.epochs, leave=True, desc="Epoch")
        for epoch in epochs:
            batches = self.create_batches()
            self.loss_sum = 0
            main_index = 0
            for index, batch in tqdm(enumerate(batches), total=len(batches), desc="Batches"):
                loss_score = self.process_batch(batch)
                main_index = main_index + len(batch)
                self.loss_sum = self.loss_sum + loss_score * len(batch)
                loss = self.loss_sum/main_index
                epochs.set_description("Epoch (Loss=%g)" % round(loss, 5))

    def score(self):
        """
        Scoring on the test set.
        """
        print("\n\nModel evaluation.\n")
        self.model.eval()
        self.scores = []
        self.ground_truth = []
        for graph_pair in tqdm(self.testing_graphs):
            for graph_pair_two in self.testing_graphs[graph_pair]:
                data = self.testing_graphs[graph_pair][graph_pair_two]
                self.ground_truth.\
                append(calculate_normalized_ged(data))
                data = self.transfer_to_torch(data)
                target = data["target"]
                prediction = self.model(data)
                self.scores.append(calculate_loss(prediction, target))
        self.print_evaluation()

    def predictionScore(self, graph_pairs):
        """
        Scoring on the test set.
        """
        print("\n\nModel evaluation.\n")
        self.model.eval()
        data = graph_pairs
        data = self.transfer_to_torch(data)
        prediction = self.model(data)
        return prediction

    def print_evaluation(self):
        """
        Printing the error rates.
        """
        norm_ged_mean = np.mean(self.ground_truth)
        base_error = np.mean([(n-norm_ged_mean)**2 for n in self.ground_truth])
        model_error = np.mean(self.scores)
        print("\nBaseline error: " +str(round(base_error, 5))+".")
        print("\nModel test error: " +str(round(model_error, 5))+".")
