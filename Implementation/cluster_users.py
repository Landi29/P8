import pathlib
import Paths
import Build_TET
import csv



'''
For each TET:
Sort the children on genre.
For each genre, count the amount of movies rated with that genre.
This value will be a value in the vector.
It is also possible to multiply each rating with a weight from 0 to 1, so a rating of a movie
with genre [[Adventure],[Animation],[Children],[Comedy],[Fantasy]] counts as 1 if the rating is high,
1*0.5 if the rating is mid and 1*0.1 if the rating is low. 
'''

def get_all_genres(path):
    all_genres = []
    with open(path, 'r') as movies_file:
        line1 = True
        for movie in csv.reader(movies_file):
            if line1:
                line1 = False
            else:
                genres = movie[3].split('|')
                for genre in genres:
                    if genre not in all_genres:
                        all_genres.append(genre)
    return all_genres
                
def init_vector_map(genres):
    vector_map = {}
    for genre in genres:
        vector_map[genre] = 0
    return vector_map

def truncate(n, decimals=5):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

TETS = Build_TET.load_tets(Paths.TETS_PATH,100)
ALL_GENRES = sorted(get_all_genres(Paths.MOVIE_NODES_PATH))


def create_vectors(tets, genres):
    vectors = []
    for tet in tets.values():
        vector_map = init_vector_map(genres)
        for child in tet.getchildren():
            weight = 0
            tet_data = child.tostring().replace('[','').replace(']','').split(',')
            if tet_data[0] == 'low':
                weight = 0.1
            elif tet_data[0] == 'mid':
                weight = 0.5
            else:
                weight = 1
            for genre in tet_data[1:]:
                vector_map[genre] = vector_map[genre] + (1*weight)
        #vector = [truncate(x,5) for x in list(vector_map.values())]
        #vectors.append(vector)
        vectors.append(list(vector_map.values()))
    return vectors

vectors = create_vectors(TETS,ALL_GENRES)

for vector in vectors:
    print(vector)
