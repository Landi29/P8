"""Module for loading the graph data into lists"""

import discretizedata
import csv

#Filepaths for graph representation of movielens data
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USERPATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
EDGEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'


def load_movie_data(self)
"""Loads the movie node data into a list"""

def load_user_data(self)
"""Loads the user node data into a list"""

def load_edge_data(self)
"""Loads the graph edge data into a list"""
#Potentionally only load in chunks of the data