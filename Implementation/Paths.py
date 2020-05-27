"""
Module containg different filepaths that are used
or can be used throughout the project
"""

import pathlib

FOLDS_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'Folds_100k.json'
SIMGNN_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'SimGNN'
RATINGPATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings.csv'
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movies.csv'
MOVIELINKPATH = pathlib.Path.cwd() / 'Movielens_data' / 'links.csv'
MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
MOVIE_NODES_100k_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes_100k.csv'
MOVIE_NODES_1m_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes_1m.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
USER_NODES_100k_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes_100k.csv'
USER_NODES_1m_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes_1m.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
TETS_PATH = pathlib.Path.cwd() / 'TETS'
N2V_MODELS_PATH = pathlib.Path.cwd() / 'n2v_models' 
Folds_PATH = pathlib.Path.cwd() / 'Movielens_data' /'Folds.json'
Folds_100k_PATH = pathlib.Path.cwd() / 'Movielens_data' /'Folds_100k.json'
Folds_1m_PATH = pathlib.Path.cwd() / 'Movielens_data' /'Folds_1m.json'
