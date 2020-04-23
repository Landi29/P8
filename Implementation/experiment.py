import compare_tet
import Paths
import csv
from build_tet import load_tets
from tqdm import tqdm

def knn(user, others, compare_model, extradata, k=4, user_database=None, filterv=4):
    '''
    description: this is a simpel implementation of knn finding the k nearest neighbors
                 and making predictions.
    parameters: user is a user you want to recommend to, others are all other trees
                and k is the nomber of neighbors we want to compare with.
    return: the return is a sorted list of recommendet movies.
    '''
    if compare_model.split('_')[1] is not None and compare_model.split('_')[1] == "tet":
        others = list(extradata.values())
        user = others[0]
    sims = []
    if user_database is None:
        user_database = userdatabase()
    for other in tqdm(others):
        if user != other:
            sims.append([other, comparemethod(user, other, compare_model)])
    bestk = sorted(sims, key=lambda x: x[-1])[:k]
    predictions = pred(user, bestk, user_database, filterv)
    return sorted(predictions, key=lambda x: x[-1])

def comparemethod(user, other, method):
    if method == "manhatten_tet":
        return compare_tet.manhatten_distance(user, other)
    elif method == "GED_tet":
        return compare_tet.graph_edit_distance(user, other)
    elif method == "manhatten_brute":
        return manhatten_bruteforce(user, other)
    else:
        print("missing method")

def manhatten_bruteforce(user, other):
    distance = 0.0
    if user != other:
        keys = compare_tet.find_all_keys_in_dicts(list(user), list(other))
        for key in keys:
            distance += abs(user.get(key, 0) - other.get(key, 0))
    return distance

def pred(user, others, user_database, filtervalue=None):
    '''
    description: This function calculates a prediction on the users rating on movies
                 others has seen that the user have not seen.
    parameters: user is a user you want to recommend to, others are the k other users.
    return: The return is a list of recommendet movies.
    '''
    #ra average
    average_rating_user = 0
    seen_by_user = list(user_database[user.getroot()])
    for rating in user_database[user.getroot()].values():
        average_rating_user += rating
    average_rating_user = average_rating_user / len(user_database[user.getroot()])

    others = reasing_sims(others)

    others_average_rating = {}
    naighbor_seen = []
    for other in others:
        for movie in user_database[other[0].getroot()]:
            if movie not in seen_by_user and movie not in naighbor_seen:
                naighbor_seen.append(movie)
        average_rating_other_user = 0
        for rating in user_database[other[0].getroot()].values():
            average_rating_other_user += rating
        others_average_rating[other[0].getroot()] = average_rating_other_user \
            / (len(user_database[other[0].getroot()].values()))

    predictions = []
    for movie in naighbor_seen:
        sumrating = average_rating_user
        sum_simularity = 0
        for other in others:
            if isinstance(user_database[other[0].getroot()].get(movie, False), float):
                sum_simularity += other[1]
        for other in others:
            if isinstance(user_database[other[0].getroot()].get(movie, False), float):
                sumrating += (other[1] / sum_simularity) \
                * (user_database[other[0].getroot()][movie] \
                - others_average_rating[other[0].getroot()])
        if filtervalue is not None:
            if sumrating >= filtervalue:
                predictions.append((movie, sumrating))
        else:
            predictions.append((movie, sumrating))
    return predictions

def reasing_sims(sims):
    '''
    description: this function reasigns the distande ratings to use them as simularety values.
    parameters: sims is a list of tubles containg userid and distance.
    return: the return is a list tubles where the disance has been reasinged
            to be used at simularety values.
    '''
    for i in range(int(len(sims)/2)):
        temp = sims[i][1]
        sims[i][1] = sims[-(i+1)][1]
        sims[-(i+1)][1] = temp
    return sims

def userdatabase():
    '''
    description: this function construnts a dictionary of users with movies they have seen
                 and the rating given, to use as a moch database over the users
    return: the return is a dictionary of users with movies tey have seen and the rating given
    '''
    users = {}
    with open(Paths.GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
        graph_data = csv.reader(read)
        for line in graph_data:
            if users.get(line[1], None) is None:
                user = {}
                user[line[0]] = float(line[2])
                users[line[1]] = user
            else:
                user = users[line[1]]
                user[line[0]] = float(line[2])
    return users

if __name__ == "__main__":
    users = userdatabase()
    tets = load_tets(Paths.TETS_PATH)
    # models manhatten_tet, GED_tet, manhatten_brute
    res = knn(list(users.values())[0], list(users.values()), "manhatten_tet", tets, user_database = users)
    print(res)

    