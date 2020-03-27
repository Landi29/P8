"""Module for loading the graph data into lists"""

import discretizedata
import csv

#Filepaths for graph representation of movielens data
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USERPATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
EDGEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
