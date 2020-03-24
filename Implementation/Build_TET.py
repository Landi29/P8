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

with open(MOVIE_NODES_PATH, 'r', encoding="utf-8") as read:
    MOVIE_NODES = read.readlines()
with open(USER_NODES_PATH, 'r', encoding="utf-8") as read:
    USER_NODES = read.readlines()
with open(GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
    GRAPH_DATA = read.readlines()


def User(u):
    if u in USER_NODES:
        return True
    return False


def rated(u,m=None):
    if m == None:
        ratings = []
        low = ["low"]
        mid = ["mid"]
        high = ["high"]
        u = u.strip().split(',')
        for r in GRAPH_DATA:
            if "Id" in r:
                continue
            rsplit = r.strip().split(',')
            if u[0] == rsplit[1]:
                if float(rsplit[2]) < 2.5:
                    low.append(r)
                elif float(rsplit[2]) > 3.5:
                    high.append(r)
                else:
                    mid.append(r)
        ratings.append(low)
        ratings.append(mid)
        ratings.append(high)
        return ratings
    for r in GRAPH_DATA:
        if u.strip().split(',')[0] == r.strip().split(',')[1] and m == r.strip().split(',')[0]:
            return r
    return False


def genre(m, g=None):
    if g == None:
        for movie in MOVIE_NODES:
            if movie.strip().split(',')[0] == m:
                return movie.strip().split(',')[-1]


def buildTETs(graph):
    N = len(USER_NODES)
    tets = []
    with open(TETS_PATH, "w", newline='') as file:
        filewriter = csv.writer(file)
        for vector in graph[0]:
            if User(vector):
                temp_tet = TET.TET(root=vector.rstrip())
                ratings = rated(vector)
                for group in ratings:
                    genres = []
                    genresfound = []
                    for rating in group[1:]:
                        movie = rating.split(',')[0]
                        mgenre = genre(movie)
                        if mgenre in genresfound:
                            i = genresfound.index(mgenre)
                            genres[i].append(movie)
                        else:
                            genresfound.append(mgenre)
                            genres.append([mgenre,movie])
                    for lgenre in genres:
                        temp_tet.addchild(TET.TETChild("1", group[0], lgenre))
                tets.append(temp_tet)
                filewriter.writerow([temp_tet.tostring()])
                if (int(vector.rstrip().split(",")[0]) % 10) == 0:
                    print(str(datetime.now()) + ": " + vector.rstrip().split(",")[0] + "/"+ str(N))
    return tets

G=[USER_NODES+MOVIE_NODES[1:], GRAPH_DATA[1:]]
print(str(datetime.now()) + ": start")
tets = buildTETs(G)

#with open(TETS_PATH, "w", newline='') as file:
#    filewriter = csv.writer(file)
#    for tet in tets:
#        filewriter.writerow([tet.tostring()])

print("done")
