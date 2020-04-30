import compare_tet
import Paths
import csv
from build_tet import load_tets, build_tets, save_tets, moviedict
from tqdm import tqdm
import math
import json
import metric_tree
import pickle
from datetime import datetime

def knn(user, others, compare_model, extradata, user_database, k=4, filterv=4):
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
    for other in others:
        if user != other:
            sims.append([other, comparemethod(user, other, compare_model)])
    bestk = sorted(sims, key=lambda x: x[1])[:k]
    return pred(user, bestk, user_database, filterv)

def comparemethod(user, other, method):
    if method == "manhatten_tet":
        return compare_tet.manhatten_distance(user, other)
    elif method == "GED_tet":
        return compare_tet.graph_edit_distance(user, other)
    elif method == "manhatten_brute":
        return manhatten_bruteforce(user, other)
    elif method == "distancev2_tet":
        return compare_tet.distance_v2_start(user, other)
    elif method == "distancev3_tet":
        return compare_tet.distance_v3(user, other)
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

    predictions = {}
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
                predictions[movie] = round(sumrating,2)
        else:
            predictions[movie] = round(sumrating,2)
    return predictions

def root_mean_squre_error(result_predictions, expected_predictions):
    rmse = 0
    T = 0
    for key in expected_predictions:
        if result_predictions.get(key, False):
            for expected_prediction in expected_predictions[key]:
                rmse += (result_predictions[key].get(key,0)-expected_predictions[key][expected_prediction])**2
                T += 1
    return math.sqrt(rmse/T)


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

def csvuserdatabase(load_path):
    '''
    description: this function construnts a dictionary of users with movies they have seen
                 and the rating given, to use as a moch database over the users
    return: the return is a dictionary of users with movies tey have seen and the rating given
    '''
    users = {}
    with open(load_path, 'r', encoding="utf-8") as read:
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

def jsonuserdatabase(load_path, folds):
    edgelist = []
    users = {}
    with open(load_path, 'r', encoding="utf-8") as read:
        graph_data = json.load(read)
        for fold in folds:
            edgelist += graph_data[fold]
    for edge in tqdm(edgelist):
        if users.get(edge[1], True):
            user = {}
            user[edge[0]] = float(edge[2])
            users[edge[1]] = user
        else:
            user = users[edge[1]]
            user[edge[0]] = float(edge[2])
    return users, edgelist

if __name__ == "__main__":
    training_data = jsonuserdatabase(Paths.Folds_100k_PATH, ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7'])[0]
    tets = load_tets(Paths.TETS_0_7_100k_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 1000, depth = 0, data=list(tets.values()))

    validation_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH, ['fold8'])[0]
    test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH, ['fold9'])[0]
    # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
    comparison_method = "distancev3_tet"
    
    result_predictions = {}

    start = datetime.now()
    for person in tqdm(list(training_data)[:5]):
        result_predictions[person] = knn(person, list(training_data), comparison_method, tets, training_data, filterv=None)
    finished = datetime.now()

    v_error = root_mean_squre_error(result_predictions, validation_expected_predictions)
    t_error = root_mean_squre_error(result_predictions, validation_expected_predictions)
    print('validation root mean square error: ' + str(v_error))
    print('test root mean square error: ' + str(t_error))
    
    with open("experiment_resultat_100k.csv", "a", newline='', encoding='utf-8') as write:
        filewriter = csv.writer(write)
        filewriter.writerow(['fold', 'validation_error', 'test_error', 'time taken on test'])
        filewriter.writerow(['fold 0-7 100k', v_error, t_error, finished - start])
