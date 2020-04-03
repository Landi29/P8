''' Movie(m)
User(u)
rated(u,m) den her kan splittes til 3 grupper tror jeg dårlig <3, middel =3 og god >3
genre(m,g) måske den skal splittes til mange individuelle genre of blive true false

TETet kunne gøres  med genre og/eller tags.
tags skal bare rydes op og måske klassefiseres til
mindre grupper da mange er en variation af the samme
eller ligger tæt op af hinanden.

User(u) -> rated(u,m) -> genre(m, g)
User(u) -> rated(u,m) -> tag(m, t)
User(u) -> rated(u,m) -> (genre(m, g), tag(m, t))'''

import csv
import pathlib
from tqdm import tqdm
import TET

def moviedict(movie_nodes_path):
    '''
    description: This funktion constructs a movie dictionary from the movies in a file
    parameters: movie_nodes_path is a filepath to a file with movie descriptions
    return: this function returns a dictionary of movies
    '''
    movie_dict = {}
    with open(movie_nodes_path, 'r', encoding="utf-8") as movie_nodes_file:
        for movie in csv.reader(movie_nodes_file):
            movie[3] = movie[3].split('|')
            movie_dict['M:'+movie[0]] = movie
    return movie_dict

def userdict(user_nodes_path):
    '''
    description: This funktion constructs a user dictionary of
                 boolean values from the users in a file
    parameters: user_nodes_path is a filepath to a file with user descriptions
    return: this function returns a dictionary of users
    '''
    user_dict = {}
    with open(user_nodes_path, 'r', encoding="utf-8") as user_nodes_file:
        user_nodes = user_nodes_file.readlines()
        for user in user_nodes:
            user = user.strip().split(',')
            user_dict['U:'+ user[0]] = True
    return user_dict

def tet_find_tree(user, tets):
    '''
    description: This function finds the TET that has user as the root
                 if such a tree does not exist it is build
    parameters: user is a user id as a string and tets is the dictionary of tets
    return: is a TET with user as root
    '''
    if user in tets:
        return tets[user]
    return TET.TET(root=user)

def construct_child(movieid, rating, moviedict):
    '''
    description: construct_child constructs the child whoms root is a rating (low, mid or high) and its children
    parameters: movieid is the movie that an edge between user and movie leads to via rating
                rating is the rating binding a user and a moviedict is
                the dictionary of all movies in the graph
    return: this return a subTET
    '''
    movie = moviedict[movieid]
    genres = []
    for genre in movie[3]:
        genres.append(TET.TETChild(genre))
    if float(rating) < 2.5:
        child = TET.TETChild("low", children=genres)
    elif float(rating) > 3.5:
        child = TET.TETChild("high", children=genres)
    else:
        child = TET.TETChild("mid", children=genres)
    return child

def build_tets(edges, moviedict, user_nodes_path):
    '''
    description: this function builds all the tets in a graph
    parameters: edges are all edges in the graph, moviedict is a dictionary of all movie nodes in
                the graph and user_nodes_path is the filepath to the file with all usernodes
    return: the return is a dictionary of all tets
    '''
    tets = {}
    user_dict = userdict(user_nodes_path)
    print("Starting to built TETs")
    for edge in tqdm(edges):
        edge = edge.strip().split(',')
        if user_dict.get(edge[1], False):
            temp_tet = tet_find_tree(edge[1], tets)
            temp_tet.addchild(construct_child(edge[0], edge[2], moviedict))
            tets[edge[1]] = temp_tet
    return tets

def save_tets(tets, tets_path):
    '''
    description: this function saves the tets in the tets dictionary
    parameters: tets is a dictionary of all tets tets_path is the path to where the trees are saved
    '''
    with open(tets_path, "w", newline='') as tets_file:
        filewriter = csv.writer(tets_file)
        print("save TETs")
        for tet in tqdm(tets.values()):
            tetlist=[tet.getroot()]
            child_count_dict = tet.count_children()
            for child in child_count_dict:
                tetlist.append(child + ':' + str(child_count_dict[child]))
            filewriter.writerow(tetlist)

def load_tets(loadpath):
    tets = {}
    with open(loadpath, 'r', encoding="utf-8") as file:
        for stringtet in tqdm(csv.reader(file)):
            tetchildren=[]
            for stringsubtet in stringtet[1:]:
                stringsubtet = stringsubtet.replace('[' , '').replace(']','').split(':')
                stringsubtet[0] = stringsubtet[0].split(',')
                genres = []
                for genre in stringsubtet[0][1:]:
                    genres.append(TET.TETChild(genre))
                partlist = [TET.TETChild(stringsubtet[0][0], children=genres)] * int(stringsubtet[1]) 
                tetchildren = tetchildren + partlist 
            tets[stringtet[0]] = TET.TET(stringtet[0], children=tetchildren)
    return tets

if __name__ == "__main__":
    '''MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
    USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
    TETS_PATH = pathlib.Path.cwd() / 'TET.csv'

    with open(GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
        GRAPH_DATA = read.readlines()

    MOVIEDICT = moviedict(MOVIE_NODES_PATH)

    TETS = build_tets(GRAPH_DATA, MOVIEDICT, USER_NODES_PATH)

    save_tets(TETS, TETS_PATH)
    
    print("save done")'''

    TETS_PATH = pathlib.Path.cwd() / 'TET.csv'
    TETS = load_tets(TETS_PATH)
    
    print("done")
