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
# rated(u,m)
# genre(m,g)

import csv
import pathlib

TAGSPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'tags.dat'
MOVIESPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'movies.dat'
RELEVNACEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'tag-genome' / 'tag_relevance.dat'

# read flash.dat to a list of lists
#datContent = [i.strip().split() for i in open("./flash.dat").readlines()]
with open(MOVIESPATH, 'r') as read:
    for i in  read.readlines():
        print('lars')

# write it as a new CSV file
#with open("./flash.csv", "wb") as f:
#    writer = csv.writer(f)
#    writer.writerows(datContent)