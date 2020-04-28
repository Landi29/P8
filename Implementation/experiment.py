import compare_tet
import Paths
import csv
from build_tet import load_tets
from tqdm import tqdm
import math
import json
import metric_tree
import pickle

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
    for other in tqdm(others):
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
    for key in expected_predictions:
        rmse += (result_predictions.get(key,0)-expected_predictions[key])**2
    return math.sqrt(rmse/len(expected_predictions))


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
    #training_data = jsonuserdatabase(Paths.Folds_PATH, ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7'])[0]
    
    tets = load_tets(Paths.TETS_0_7_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_0_7_PATH, "wb"))
    print(0)

    tets = load_tets(Paths.TETS_1_8_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_1_8_PATH, "wb"))
    print(1)

    tets = load_tets(Paths.TETS_2_9_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_2_9_PATH, "wb"))
    print(2)

    tets = load_tets(Paths.TETS_3_0_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_3_0_PATH, "wb"))
    print(3)

    tets = load_tets(Paths.TETS_4_1_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_4_1_PATH, "wb"))
    print(4)
    tets = load_tets(Paths.TETS_5_2_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_5_2_PATH, "wb"))
    print(5)

    tets = load_tets(Paths.TETS_6_3_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_6_3_PATH, "wb"))
    print(6)

    tets = load_tets(Paths.TETS_7_4_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_7_4_PATH, "wb"))
    print(7)

    tets = load_tets(Paths.TETS_8_5_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_8_5_PATH, "wb"))
    print(8)

    tets = load_tets(Paths.TETS_9_6_PATH)
    tet_classifier = metric_tree.mt_build(dmax = 10, nmax= 10000, depth = 0, data=list(tets.values()))
    pickle.dump(tet_classifier, open(Paths.TETSmt_9_6_PATH, "wb"))
    print(9)

    #validation_expected_predictions = jsonuserdatabase(Paths.Folds_PATH, ['fold8'])[0]
    #test_expected_predictions = jsonuserdatabase(Paths.Folds_PATH, ['fold9'])[0]
    # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
    #comparison_method = "distancev3_tet"
    
    #result_predictions = knn(list(training_data)[0], list(training_data), comparison_method, metric_tree.mt_search(tet_classifier, tets[list(training_data)[0]]), training_data, filterv=None)

    #error = root_mean_squre_error(result_predictions, validation_expected_predictions[list(training_data)[0]])
    #print('root mean square error: ' + str(error))
    