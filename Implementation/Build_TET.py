''' build_TET(Data M, Labeled tablett, TET_node parent, TET_node root)
    1. parent.weight= positive_class_frequency(tt)
    2. current_score = predictive_score(M, root)
    3. EXT:=possible_extensions(parent, θvars, θdepth)
    4. for all σ(V ,W) ∈ EXT compute RIG(tt,σ(V ,W))
    5. CAND:= candidate_extensions(EXT,RIG-values, θRIG)
    6. for all σ(V ,W) ∈ CAND
    7. tt = construct_tt(M, tt,σ(V ,W))
    8. nextChild = newTET_node(σ(V ,W))
    9. add nextChild as childto parent
    10. build_TET(M, tt' , nextChild, root)
    11. new_score == predictive_score(M, root)
    12. if new_score −current_score < θscore
    13. remove nextChild from parent
    14. else current_score=new_score
'''

# Movie(m)
# User(u)
# rated(u,m) den her kan splittes til 3 grupper tror jeg dårlig <3, middel =3 og god >3
# genre(m,g) måske den skal splittes til mange individuelle genre of blive true false

# TETet kunne gøres  med genre og/eller tags.
# tags skal bare rydes op og måske klassefiseres til mindre grupper da mange er en variation af the samme
# eller ligger tæt op af hinanden.

# User(u) -> rated(u,m) -> genre(m, g)
# User(u) -> rated(u,m) -> tag(m, t)
# User(u) -> rated(u,m) -> (genre(m, g), tag(m, t))

import csv
import pathlib
import TET
from datetime import datetime
from tqdm import tqdm
import sys

# TAGSPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'tags.dat'
# MOVIESPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'movies.dat'
# RELEVNACEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'tag_relevance.dat'

MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
TETS_PATH = pathlib.Path.cwd() / 'TET.csv'

# read flash.dat to a list of lists
# datContent = [i.strip().split() for i in open("./flash.dat").readlines()]
# with open(MOVIESPATH, 'r') as read:
#    listof = read.readlines():

with open(GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
    GRAPH_DATA = read.readlines()

def moviedict():
    movie_dict = {}
    with open(MOVIE_NODES_PATH, 'r', encoding="utf-8") as read:
        MOVIE_NODES = read.readlines()
        for movie in MOVIE_NODES:
            movie = movie.strip().split(',')
            movie[3] = movie[3].split('|')
            movie_dict['M:'+movie[0]] = movie
    return movie_dict

def userdict():
    user_dict = {}
    with open(USER_NODES_PATH, 'r', encoding="utf-8") as read:
        USER_NODES = read.readlines()
        for user in USER_NODES:
            user = user.strip().split(',')
            user_dict['U:'+ user[0]] = True
    return user_dict

Globaltets={}

# For all users, you call the rated function.
# This function then searches the whole graph to get the ratings for that one user.
# But going through the graph ones should give you all the information you need
# in order to create a ratings vector for all users. 
# If you only go through the graph ones, and then create all the ratings vectors,
# you will increase the speed. 
# If the dictionary of all ratings is too big for main memory, you can then save it to a file,
# and use that file in your function. If not, you can use the dictionary of all rating vectors directly.

# You also call the genre() function on each movie to get the list of genres for each of the movies.
# Since the genre function goes through the list of all movies, you go through this list
# for each movie.
# If you go through the list once, you actually have all the information you need, so you can precompute
# all the genres for each movie by going through the list once and saving it as a dictionary, 
# where the key is the movie id and the value is a list or string of genres. The dictionary will give you a 
# fast lookup time for the genres and you then only have to go through the list once. 

def TETfindTree(user):
    if user in Globaltets:
        return Globaltets[user]
    return TET.TET(root=user)

def constructchild(movieid, rating):
    movie = moviedict[movieid] 
    genres = []
    for genre in movie[3]:
        genres.append(TET.TETChild(genre))
    if float(rating) < 2.5: 
        return TET.TETChild("low", children = genres)
    elif float(rating) > 3.5: 
        return TET.TETChild("high", children = genres)
    else:
        return TET.TETChild("mid", children = genres)

def buildTETs2(edges):
    print("built tet")
    user_dict = userdict()
    for edge in tqdm(edges):
        edge = edge.strip().split(',')
        if user_dict.get(edge[1], False):
            temp_tet = TETfindTree(edge[1])
            temp_tet.addchild(constructchild(edge[0], edge[2]))
            Globaltets[edge[1]]=temp_tet
    return

#G=[USER_NODES+MOVIE_NODES[1:], GRAPH_DATA[1:]]
print(str(datetime.now()) + ": start")
#tets = buildTETs(G)
moviedict = moviedict()

buildTETs2(GRAPH_DATA)

with open(TETS_PATH, "w", newline='') as file:
    filewriter = csv.writer(file)
    print("save TETs")
    for tet in tqdm(Globaltets.values()):
        filewriter.writerow([tet.tostring()])

print("done")
sys.exit()