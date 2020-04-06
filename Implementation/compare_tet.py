import Build_TET
import pathlib
from tqdm import tqdm
import csv

def comparetets(tet1, tet2):
    sim = 0
    if tet1 != tet2:
        structure1 = tet1.count_children()
        structure2 = tet2.count_children()
        keys = find_all_keys_in_dicts(list(structure1),list(structure2))
        sim = manhatten_distance(structure1, structure2, keys)
    return sim

def find_all_keys_in_dicts(keys1,keys2):
    for key in keys2:
        if key not in keys1:
            keys1.append(key)
    return keys1

def manhatten_distance(structure1, structure2, keys):
    distance = 0.0
    for key in keys:
        distance += abs(structure1.get(key, 0) - structure2.get(key, 0))
    return distance

def knn(user, others, k=3):
    sims = []
    for other in others:
        sims.append((other,comparetets(user, others[tet2])))
    bestk = sorted(sims, key=lambda x: x[-1])[:k]
    predictions = pred(user, bestk)
    return predictions

def pred(user, others):
    #ra average
    average_rating_user = 0

    seenbyuser = list(User_database[user])
    for rating in User_database[user].values():
        average_rating_user += rating
    average_rating_user = average_rating_user / (len(user) - 1)

    sum_simularity = 0
    # part of W
    for naighbor in others:
        sum_simularity += naighbor[1]

    others_average_rating ={}
    naighborseen = []
    for other in others:
        for movie in other:
            if movie not in seenbyuser:
                naighborseen.append(movie)
        average_rating_other_user = 0
        for rating in User_database[other].values():
            average_rating_other_user += rating
        others_average_rating[other] = average_rating_other_user / (len(User_database[other].values()))

    predictions = {}
    for movie in naighborseen:
        for other in others:
            sumrating += (other[1] / sum_simularity) * (User_database[other][movie] - others_average_rating[other])
        if sumrating > 4:
            predictions[movie] = sumrating
    return predictions

def userdatabase():
    users = {}
    GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'
    with open(GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
        GRAPH_DATA = csv.reader(read)
        for line in GRAPH_DATA:
            if users.get(line[1], None) == None:
                user = {}
                user[line[0]] = float(line[2])
                users[line[1]] = user
            else:
                user = users[line[1]]
                user[line[0]] = float(line[2])
    return users
            
if __name__ == "__main__":
    User_database = userdatabase()
    TETS_PATH = pathlib.Path.cwd() / 'TET.csv'
    Tets = list(Build_TET.load_tets(TETS_PATH).values())
    N_Tets = len(Tets)
    for tet1 in tqdm(range(N_Tets)):
        for tet2 in range(tet1+1, N_Tets):
            comparetets(Tets[tet1], Tets[tet2])
            #print(str(tet1) + ' and ' + str(tet2) + ': ' + str(comparetets(Tets[tet1], Tets[tet2])))