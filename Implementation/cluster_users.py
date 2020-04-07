import csv
import Paths
import Build_TET

def get_all_genres(movie_nodes_path):
    '''
    Description: This function returns a list of all the movie genres.
    Parameters:
    * movie_nodes_path: The path to the csv file containing the movie nodes.
    '''
    genres_index = 3
    all_genres = []
    with open(movie_nodes_path, 'r') as movies_file:
        line1 = True
        for movie in csv.reader(movies_file):
            if line1:
                line1 = False
            else:
                genres = movie[genres_index].split('|')
                for genre in genres:
                    if genre not in all_genres:
                        all_genres.append(genre)
    return all_genres

def init_vector_map(genres):
    '''
    Description: The function returns an initial vector map where each key is a genre
    ande each value is 0.

    Parameters:
    * genres: The list of all movie genres.
    '''
    vector_map = {}
    for genre in genres:
        vector_map[genre] = 0
    return vector_map

def create_vectors(tets, genres):
    '''
    Description: The function creates a vector representation of the given tets.
    The function uses a weight value, which is set according to the rating.

    Parameters:
    * tets: The tets to vectorize.
    * genres: A list of all the movie genres.
    '''
    vectors = []
    for tet in tets.values():
        vector_map = init_vector_map(genres)
        for child in tet.getchildren():
            weight = 0
            tet_data = child.tostring().replace('[', '').replace(']', '').split(',')
            if tet_data[0] == 'low':
                weight = 0.1
            elif tet_data[0] == 'mid':
                weight = 0.5
            else:
                weight = 1
            for genre in tet_data[1:]:
                # Set the updated value to be value + (1*weight).
                vector_map[genre] = vector_map[genre] + (1*weight)
        # When the tet has been processed, add it to the vectors list.
        vectors.append(list(vector_map.values()))
    return vectors

# Constants to be used when calling create_vectors(tets,genres).
TETS = Build_TET.load_tets(Paths.TETS_PATH, 100)
ALL_GENRES = sorted(get_all_genres(Paths.MOVIE_NODES_PATH))
VECTORS = create_vectors(TETS, ALL_GENRES)

for vector in VECTORS:
    print(vector)
