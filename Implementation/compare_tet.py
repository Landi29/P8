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
        if user != other:
            sims.append([other,comparetets(user, other)])
    bestk = sorted(sims, key=lambda x: x[-1])[:k]
    predictions = pred(user, bestk)
    return sorted(predictions, key=lambda x: x[-1])

def pred(user, others):
    #ra average
    average_rating_user = 0
    seenbyuser = list(User_database[user.getroot()])
    for rating in User_database[user.getroot()].values():
        average_rating_user += rating
    average_rating_user = average_rating_user / len(User_database[user.getroot()])

    others = reasing_sims(others)

    others_average_rating ={}
    naighborseen = []
    for other in others:
        for movie in User_database[other[0].getroot()]:
            if movie not in seenbyuser:
                naighborseen.append(movie)
        average_rating_other_user = 0
        for rating in User_database[other[0].getroot()].values():
            average_rating_other_user += rating
        others_average_rating[other[0].getroot()] = average_rating_other_user / (len(User_database[other[0].getroot()].values()))

    predictions = []
    for movie in naighborseen:
        sumrating = average_rating_user
        sum_simularity = 0
        for other in others:
            if isinstance(User_database[other[0].getroot()].get(movie, False), float):
                sum_simularity += other[1]
        for other in others:
            if isinstance(User_database[other[0].getroot()].get(movie, False), float):
                sumrating += (other[1] / sum_simularity) * (User_database[other[0].getroot()][movie] - others_average_rating[other[0].getroot()])
        if sumrating >= 4:
            predictions.append((movie, sumrating))
    return predictions

def reasing_sims(sims):
    for i in range(int(len(sims)/2)):
        temp = sims[i][1]
        sims[i][1] = sims[-(i+1)][1]
        sims[-(i+1)][1] = temp
    return sims


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

    for predrating in knn(Tets[0], Tets):
        print('{} predicted rating: {}'.format(predrating[0], predrating[1]))
    print('\ndone')
