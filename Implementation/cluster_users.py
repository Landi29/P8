import pathlib
import Paths
import Build_TET



'''
For each TET:
Sort the children on genre.
For each genre, count the amount of movies rated with that genre.
This value will be a value in the vector.
It is also possible to multiply each rating with a weight from 0 to 1, so a rating of a movie
with genre [[Adventure],[Animation],[Children],[Comedy],[Fantasy]] counts as 1 if the rating is high,
1*0.5 if the rating is mid and 1*0.1 if the rating is low. 
'''

#def create_vectors(tets, save_path):
   #vectors = []

TETS = Build_TET.load_tets(Paths.TETS_PATH,100)
GENRES = []

def init_vector_map():
    vector_map = {}
    for genre in GENRES:
        vector_map[genre] = 0
    return vector_map

    
for tet in TETS['U:4'].getchildren():
    vector_map = {}
    weight = 0
    tet_data = tet.tostring().replace('[','').replace(']','').split(',')
    if tet_data[0] == 'low':
        weight = 0.1
    elif tet_data[0] == 'mid':
        weight = 0.5
    else:
        weight = 1
    for genre in tet_data[1:]:
        vector_map[genre] = vector_map[genre] + (1*weight)
    


