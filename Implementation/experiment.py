import csv
import json
import math
import pickle
from datetime import datetime
from tqdm import tqdm
import compare_tet
from build_tet import load_tets, build_tets, save_tets, moviedict
import metric_tree
import Paths

def knn(user, others, compare_model, extradata, user_database, k=4, item=None, filterv=None):
    '''
    description: this is a simple implementation of knn finding the k nearest neighbors
                 and making predictions.
    parameters: user is a user you want to recommend to, others are all other trees
                and k is the nomber of neighbors we want to compare with.
    return: the return is a sorted list of recommendet movies.
    '''
    sims = []
    if compare_model == "manhatten_brute":
        for other in others:
            if user != other:
                sims.append([other, 1/(1 + manhatten_bruteforce(extradata[user],
                                                                extradata[other]))])
        best_k = sorted(sims, key=lambda x: x[1], reverse=True)[:k]

    elif compare_model == "node2vec":
        sims = extradata.wv.most_similar(user.replace("U:", "2"), topn=1000000)
        best_k = []
        count = 0
        for sim in sims:
            if list(sim[0])[0] == '2':
                temp = list(sim[0])
                temp[0] = 'U:'
                temp = ''.join(temp)
                best_k.append([temp, sim[1]])
                count += 1
            if count >= k:
                break

    elif compare_model.split('_')[1] is not None and compare_model.split('_')[1] == "tet":
        others = list(extradata.values())
        usertet = extradata[user]
        for other in others:
            if usertet != other:
                sims.append([other.getroot(), 1/(1 + tet_compare_method(usertet, other,
                                                                        compare_model))])
        best_k = sorted(sims, key=lambda x: x[1], reverse=True)[:k]
    else:
        print("missing method knn classification")

    return pred(user, best_k, user_database, item, filterv)

def tet_compare_method(user, other, method):
    '''
    description: because of the dufferent implementation on how to find distance
                 with the tet this function in designed to be an easy way of changeing the method.
    parameters: user is a tet for the user to compare to, other is a tet to compare to and
                method is the method you want to use to find the distance.
    return: the return is a distance between user and other
    '''
    returnmethod = None

    if method == "manhatten_tet":
        returnmethod = compare_tet.manhatten_distance(user, other)
    elif method == "GED_tet":
        returnmethod = compare_tet.graph_edit_distance(user, other)
    elif method == "distancev2_tet":
        returnmethod = compare_tet.distance_v2_start(user, other)
    elif method == "distancev3_tet":
        returnmethod = compare_tet.distance_v3(user, other)
    else:
        print("missing method for tet compareson")
        return ValueError("missing method for tet compareson")

    return returnmethod

def manhatten_bruteforce(user, other):
    '''
    description: this method is meant to find the manhatten distance between two vectors.
    parameters: user is a user vector and other is a another uservector.
    return: the return is the manhatten distance between user and other.
    '''
    distance = 0.0
    if user != other:
        keys = compare_tet.find_all_keys_in_dicts(list(user), list(other))
        for key in keys:
            distance += abs(user.get(key, 0) - other.get(key, 0))
    return distance

def pred(user, others, user_database, item=None, filtervalue=None):
    '''
    description: This function calculates a prediction on the users rating on movies
                 others has seen that the user have not seen.
    parameters: user is a user you want to recommend to, others are the k other users.
    return: The return is a list of recommendet movies.
    '''
    average_rating_user = average_rating(user_database[user])
    seen_by_user = list(user_database[user])

    others_average_rating = {}
    seen_by_neighbors = []
    for other in others:
        seen_by_neighbors = find_and_add_differences(seen_by_user, user_database[other[0]],
                                                     seen_by_neighbors)
        others_average_rating[other[0]] = average_rating(user_database[other[0]])

    predictions = {}
    if item is None:
        for movie in seen_by_neighbors:
            sum_simularity = sum_similarities(others, movie, user_database)
            pred_rating = average_rating_user + rating_influence(others, movie, sum_simularity,
                                                                 user_database,
                                                                 others_average_rating)
            if filtervalue is not None:
                if pred_rating >= filtervalue:
                    predictions[movie] = round(pred_rating, 2)
            else:
                predictions[movie] = round(pred_rating, 2)
    else:
        sum_simularity = sum_similarities(others, item, user_database)
        pred_rating = average_rating_user + rating_influence(others, item, sum_simularity,
                                                             user_database, others_average_rating)
        predictions[item] = round(pred_rating, 2)

    return predictions

def root_mean_squre_error(result_predictions, expected_predictions):
    '''
    description: this function finds the error beween the expected and the predicted.
    parameters: result_predictons is the canculated predictions and
                expected_predictions is the predictions we would like to find.
    return: return is the root means square error between result and expected.
    '''
    rmse = 0
    total = 0
    for key in expected_predictions:
        if result_predictions.get(key, False):
            for expected_prediction in expected_predictions[key]:
                rmse += (result_predictions[key].get(key, 0) -
                         expected_predictions[key][expected_prediction])**2
                total += 1
    return math.sqrt(rmse/total)

def average_rating(user):
    '''
    description: calculated the average rating for a user.
    parameters: user is a dictionatty of movierations for a user.
    return: the users average rating.
    '''
    return sum(user.values()) / len(user)

def find_and_add_differences(list1, dict1, rlist):
    '''
    description: this function finds the element in a dictionarry and
                 adds it to a list if its not in the list1 or rlist.
    parameters: list1 is a list of items, dict1 is a dictionary with keys of items
                and rlist is a list the result are stored in.
    return: the return is a list of items that are not in list1.
    '''
    for movie in dict1:
        if movie not in rlist and movie not in list1:
            rlist.append(movie)
    return rlist

def sum_similarities(similarities, film, database):
    '''
    description: find the total simularety score for a movie.
    parameters: simulareties is a list of tubles tuples with a userid and a simularety score,
                film is a you want to find the total simularety score for and
                database is a userdatabase with movieretings.
    return: the return is the total simularety score for film.
    '''
    rsum = 0
    for sim in similarities:
        if database[sim[0]].get(film, False):
            rsum += sim[1]
    return rsum

def rating_influence(others, movie, sum_simularity, database, others_average_rating):
    '''
    description: this method calculates the influence of the neighbours to a users rating.
    parameters: others is a list of tubles tuples with a userid and a simularety score,
                movie is a movie id, sum_simularity is the sumed simularety for the movie,
                database is a userdatabase with movie ratings
                and others_average_rating is the users in the list of others average rating.
    return: the return is the influende other would give to a movierating.
    '''
    influence = 0
    for other in others:
        if database[other[0]].get(movie, False):
            influence += (other[1] / sum_simularity) * (database[other[0]][movie] -
                                                        others_average_rating[other[0]])
    return influence

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
    '''
    description: jsonuserdatabase loads a folds and transforms them to edgelist and userdatabase.
    parameters: load_path is the past to the folds file and
                folds is a list of folds that you wish to load.
    return: the return is a userdatabase and an edgelist coresponding to the folds.
    '''
    edgelist = []
    users = {}
    with open(load_path, 'r', encoding="utf-8") as read:
        graph_data = json.load(read)
        for fold in folds:
            edgelist += graph_data[fold]
    for edge in tqdm(edgelist):
        if not users.get(edge[1], False):
            user = {}
            user[edge[0]] = float(edge[2])
            users[edge[1]] = user
        else:
            user = users[edge[1]]
            user[edge[0]] = float(edge[2])
    return users, edgelist

if __name__ == "__main__":
    with open("test.csv", "w", newline='', encoding='utf-8') as write:
        FILE_WRITER = csv.writer(write)
        FOLDS = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        # brute experiment
        TRAINING_DATA, EDGELIST = jsonuserdatabase(Paths.Folds_100k_PATH, FOLDS[:-2])
        VALIDATION_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[8]])[0]
        TEST_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[9]])[0]
        # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
        COMPARISON_METHOD = "manhatten_brute"

        RESULT_PREDICTIONS = {}
        START = datetime.now()
        for person in tqdm(list(TRAINING_DATA)):
            RESULT_PREDICTIONS[person] = knn(person, list(TRAINING_DATA), COMPARISON_METHOD,
                                             TRAINING_DATA, TRAINING_DATA, k=10)
        FINISHED = datetime.now()

        V_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, VALIDATION_EXPECTED_PREDICTIONS)
        T_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, TEST_EXPECTED_PREDICTIONS)
        print(0)
        print('validation root mean square error: ' + str(V_ERROR))
        print('test root mean square error: ' + str(T_ERROR))
        print('experiment time: ' + str(FINISHED - START))
        FILE_WRITER.writerow(['fold', 'validation_error', 'test_error', 'time taken on test'])
        FILE_WRITER.writerow(['fold 0-7 100k', V_ERROR, T_ERROR, FINISHED - START])


        # node2vec experiment
        TRAINING_DATA, EDGELIST = jsonuserdatabase(Paths.Folds_100k_PATH, FOLDS[:-2])
        with open('n2v_models/Folds_100k_1.pkl', 'rb') as f:
            N2V_MODEL = pickle.load(f)
        VALIDATION_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[8]])[0]
        TEST_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[9]])[0]
        # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
        COMPARISON_METHOD = "node2vec"

        RESULT_PREDICTIONS = {}
        START = datetime.now()
        for person in tqdm(list(TRAINING_DATA)):
            RESULT_PREDICTIONS[person] = knn(person, list(TRAINING_DATA), COMPARISON_METHOD,
                                             N2V_MODEL, TRAINING_DATA, k=10)
        FINISHED = datetime.now()

        V_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, VALIDATION_EXPECTED_PREDICTIONS)
        T_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, TEST_EXPECTED_PREDICTIONS)
        print(0)
        print('validation root mean square error: ' + str(V_ERROR))
        print('test root mean square error: ' + str(T_ERROR))
        print('experiment time: ' + str(FINISHED - START))
        FILE_WRITER.writerow(['fold', 'validation_error', 'test_error', 'time taken on test'])
        FILE_WRITER.writerow(['fold 0-7 100k', V_ERROR, T_ERROR, FINISHED - START])


        # tet experiment
        TRAINING_DATA, EDGELIST = jsonuserdatabase(Paths.Folds_100k_PATH, FOLDS[:2])
        TETS = build_tets(EDGELIST, moviedict(Paths.MOVIE_NODES_100k_PATH),
                          Paths.USER_NODES_100k_PATH)
        save_tets(TETS, Paths.TETS_0_7_100k_PATH)

        #TET_CLASSIFIER = metric_tree.mt_build(dmax = 10, nmax= 1000, depth = 0,
        #                                      data=list(TETs.values()))
        #pickle.dump(TET_CLASSIFIER, open("TETmt_9_6_100k.p", "wb"))

        VALIDATION_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[8]])[0]
        TEST_EXPECTED_PREDICTIONS = jsonuserdatabase(Paths.Folds_100k_PATH, [FOLDS[9]])[0]
        # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
        COMPARISON_METHOD = "distancev3_tet"

        RESULT_PREDICTIONS = {}
        START = datetime.now()
        for person in tqdm(list(TRAINING_DATA)):
            RESULT_PREDICTIONS[person] = knn(person, list(TRAINING_DATA), COMPARISON_METHOD,
                                             TETS, TRAINING_DATA, k=10)
        FINISHED = datetime.now()

        V_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, VALIDATION_EXPECTED_PREDICTIONS)
        T_ERROR = root_mean_squre_error(RESULT_PREDICTIONS, TEST_EXPECTED_PREDICTIONS)
        print(0)
        print('validation root mean square error: ' + str(V_ERROR))
        print('test root mean square error: ' + str(T_ERROR))
        print('experiment time: ' + str(FINISHED - START))

        FILE_WRITER.writerow(['fold 0-7 100k', V_ERROR, T_ERROR, FINISHED - START])
