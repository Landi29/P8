"""
Module containg different filepaths that are used
or can be used throughout the project
"""

import pathlib

RATINGPATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings.csv'
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movies.csv'
MOVIELINKPATH = pathlib.Path.cwd() / 'Movielens_data' / 'links.csv'
MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
TETS_PATH = pathlib.Path.cwd() / 'Movielens_data' /'TET.csv'
NETWORKX_GRAPH = pathlib.Path.cwd() / 'Movielens_data' / 'movielens.edgelist'
NETWORKX_GRAPH_MODUL = pathlib.Path.cwd() / 'Movielens_data' / 'movielens_module.edgelist'
CLEANED_GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph_cleaned.csv'
RATING_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings.csv'

GRAPH_DATA_PATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'graph_100k.csv'
NETWORKX_GRAPH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'graph_100k.edgelist'
USER_NODES_PATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes_100k.csv'
MOVIEPATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'movies.item'
MOVIE_NODES_PATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'Movie_nodes_100k.csv'
DATAPATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'u_100k.data'
RATINGPATH_100K = pathlib.Path.cwd() / 'Movielens_data' / 'ratings_100k.csv'
GRAPH_DATA_PATH_1M = pathlib.Path.cwd() / 'Movielens_data' / 'graph_1m.csv'

RATINGPATH_1M = pathlib.Path.cwd() / 'Movielens_data' / 'ratings_1m.dat'
USER_NODES_PATH_1M = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes_1m.csv'
MOVIEPATH_1M = pathlib.Path.cwd() / 'Movielens_data' / 'movies_1m.dat'
MOVIE_NODES_PATH_1M = pathlib.Path.cwd() / 'Movielens_data' / 'Movie_nodes_1m.csv'
FOLDS_JSON = pathlib.Path.cwd() / 'Movielens_data' / 'Folds_1m.json'
EXPERIMENT_DATA_PATH = pathlib.Path.cwd() / 'Experiment_data'
EXPERIMENT_DATA_OUTPUT_PATH = pathlib.Path.cwd() / 'Experiment_data' / 'Output'