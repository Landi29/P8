import csv
from sklearn.cluster import KMeans
import numpy as np
import Paths
import Build_TET

def get_all_genres(movie_nodes_path):
    '''
    Description:
    ------------
    This function returns a list of all the movie genres.

    Parameters:
    -----------
    `movie_nodes_path` : The path to the csv file containing the movie nodes.

    Returns:
    -------
    A list of all the movie genres.
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
    Description:
    ------------
    The function returns an initial vector map where each key is a genre
    ande each value is 0.

    Parameters:
    -----------
    `genres` : The list of all movie genres.
    '''
    vector_map = {}
    for genre in genres:
        vector_map[genre] = 0
    return vector_map

def create_vectors(tets, genres):
    '''
    Description:
    ------------
    The function creates a vector representation of the given TETs.

    Parameters:
    -----------
    `tets` : The tets to vectorize.
    `genres` : A list of all the movie genres.

    Returns:
    --------
    A list of vectors represented as a list of lists.
    '''
    vectors = []
    for tet in tets.values():
        vector_map = init_vector_map(genres)
        for child in tet.getchildren():
            rating = 0
            tet_data = child.tostring().replace('[', '').replace(']', '').split(',')
            if tet_data[0] == 'low':
                rating = 0.1
            elif tet_data[0] == 'mid':
                rating = 0.5
            else:
                rating = 1
            for genre in tet_data[1:]:
                # Set the updated value to be value + (1*weight).
                vector_map[genre] = vector_map[genre] + rating
        # When the tet has been processed, add it to the vectors list.
        vectors.append(list(vector_map.values()))
    return vectors

def cluster_users(vectors):
    '''
    Description:
    ------------
    Cluster the TETS in 10 clusters based on their vector representation.

    Parameters:
    -----------
    `vectors` : The TET vectors to cluster.

    Returns:
    --------
    A fitted `sklearn.cluster.KMeans` object.
    '''
    # KMeans object with 10 clusters.
    kmeans = KMeans(n_clusters=10)
    # Fit the clusters. Here, we calculate the center points of each cluster.
    kmeans.fit(vectors)
    # We do not need to predict, since we have no labeled data to test on.
    return kmeans

def get_users_in_cluster(cluster_number, cluster_labels):
    '''
    Description:
    ------------
    Get the vector/TET indeces for all the vectors/TETs in the cluster with label cluster_number.

    Parameters:
    -----------
    `cluster_number` : The cluster to search.
    `cluster_labels` : The list of cluster_labels.

    Returns:
    --------
    A list of integers representing indeces.
    The list of TET vectors can use the indeces directly, where the dictionary of TETs
    need to append the index to the string 'U:' for it to be a valid key.
    '''
    return np.where(cluster_labels == cluster_number)[0]

def print_cluster_information(labels):
    '''
    Description:
    ------------
    The function counts how many vectors there are in each cluster.

    Parameters:
    -----------
    `labels` : The list of labels denoting which cluster a vector belongs to.
    '''
    cluster_info = {}
    for label in labels:
        if label not in cluster_info:
            cluster_info[label] = 1
        else:
            cluster_info[label] += 1
    # The keys are in the order found in labels, so we sort them by their numeric value.
    for key in sorted(list(cluster_info)):
        print("The size of cluster {}: {}".format(key, cluster_info[key]))

if __name__ == "__main__":
    # Constants to be used when calling create_vectors(tets,genres).
    TETS = Build_TET.load_tets(Paths.TETS_PATH, 20000)
    ALL_GENRES = sorted(get_all_genres(Paths.MOVIE_NODES_PATH))

    VECTORS = create_vectors(TETS, ALL_GENRES)
    print("\nCreated the vectors")
    CLUSTERS = cluster_users(VECTORS)
    print("Clustered the TETs")
    print_cluster_information(CLUSTERS.labels_)
