import csv
import json
import math
import pickle
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from build_tet import load_tets, build_tets, save_tets, moviedict, construct_child
import compare_tet
import metric_tree
import Paths

def knn(user, others, items, compare_model, extradata, user_database, k=4, filterv=None):
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
        sims = sorted(sims, key=lambda x: x[1], reverse=True)

    elif compare_model == "node2vec":
        temp_sims = extradata.wv.most_similar(user.replace("U:", "2"), topn=1000000)
        for sim in temp_sims:
            if list(sim[0])[0] == '2':
                temp = list(sim[0])
                temp[0] = 'U:'
                temp = ''.join(temp)
                sims.append([temp, sim[1]])
        sims = sorted(sims, key=lambda x: x[1], reverse=True)

    elif compare_model.split('_')[1] is not None and compare_model.split('_')[1] == "tet":
        others = list(extradata.values())
        usertet = extradata[user]
        for other in others:
            if usertet != other:
                sims.append([other.getroot(), 1/(1 + tet_compare_method(usertet, other,
                                                                        compare_model))])
        sims = sorted(sims, key=lambda x: x[1], reverse=True)

    else:
        print("missing method knn classification")

    if len(compare_model.split('_')) == 3 and compare_model.split('_')[2] == "2":
        predictions = {}
        for item in items:
            subtet = construct_child(item, 'none', moviedict(Paths.MOVIE_NODES_100k_PATH))
            count = 0
            best_k_tree = []
            for sim in sims:
                if extradata[sim[0]].haschild(subtet):
                    best_k_tree.append([extradata[sim[0]], sim[1]])
                    count += 1
                if count >= k:
                    break
            predictions[item] = predtree(extradata[user], best_k_tree, user_database, subtet, filterv)
        return predictions

    predictions = {}
    for item in items:
        count = 0
        best_k = []
        for sim in sims:
            if user_database[sim[0]].get(item, False):
                best_k.append(sim)
                count += 1
            if count >= k:
                break
        predictions[item] = pred(user, best_k, user_database, item, filterv)
    return predictions

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
    elif method.split('_')[0] == "distancev3":
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

    return round(pred_rating, 2)

def predtree(user, others, user_database, item=None, filtervalue=None):
    average_rating_user = average_tree_rating(user)

    others_average_rating = {}
    for other in others:
        others_average_rating[other[0].getroot()] = average_tree_rating(other[0])
 
    sum_simularity = tree_sum_similarities(others)
    pred_rating = average_rating_user + tree_rating_influence(others, item, sum_simularity,
                                                            user_database, others_average_rating)

    return torating(round(pred_rating, 2))

def root_mean_squre_error(result_predictions, expected_predictions):
    '''
    description: this function finds the error beween the expected and the predicted.
    parameters: result_predictons is the canculated predictions and
                expected_predictions is the predictions we would like to find.
    return: return is the root means square error between result and expected.
    '''
    rmse = 0
    total = 0
    for user in expected_predictions:
        if result_predictions.get(user, False):
            for expected_prediction in expected_predictions[user]:
                if isinstance(result_predictions[user].get(expected_prediction, 0), str):
                    rmse += (tree_rating_enummerater(result_predictions[user].get(expected_prediction, 'none')) -
                                tree_rating_enummerater(Otorating(expected_predictions[user][expected_prediction])))**2
                else:
                    rmse += (result_predictions[user].get(expected_prediction, 0) -
                                expected_predictions[user][expected_prediction])**2
                total += 1
    return math.sqrt(rmse/total)

def mean_average_error(result_predictions, expected_predictions):
    mae = 0
    total = 0
    for user in expected_predictions:
        if result_predictions.get(user, False):
            for expected_prediction in expected_predictions[user]:
                if isinstance(result_predictions[user].get(expected_prediction, 0), str):
                    mae += abs(tree_rating_enummerater(result_predictions[user].get(expected_prediction, 'none')) -
                                tree_rating_enummerater(Otorating(expected_predictions[user][expected_prediction])))
                else:
                    mae += abs(result_predictions[user].get(expected_prediction, 0) -
                                expected_predictions[user][expected_prediction])
                total += 1
    return mae/total

def average_rating(user):
    '''
    description: calculated the average rating for a user.
    parameters: user is a dictionatty of movierations for a user.
    return: the users average rating.
    '''
    try:
        return sum(user.values()) / len(user)
    except:
        return 3

def average_tree_rating(user):
    user = list(map(lambda x: x.getroot(), user.getchildren()))
    user = list(map(tree_rating_enummerater, user))
    return sum(user) / len(user)

def tree_rating_enummerater(rating):
    if rating == "low":
        return 1
    elif rating == "mid":
        return 2
    elif rating == "high":
        return 3
    else:
        return 0

def torating(prediction):
    if abs(prediction - 1) <  0.5:
        return 'low'
    elif abs(prediction - 2) <  0.5:
        return 'mid'
    else:
        return 'high'

def Otorating(prediction):
    if float(prediction) < 2.5:
        return "low"
    elif float(prediction) > 3.5:
        return "high"
    else:
        return "mid"

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

def tree_sum_similarities(similarities):
    rsum = 0
    for sim in similarities:
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

def tree_rating_influence(others, movie, sum_simularity, database, others_average_rating):
    influence = 0
    for other in others:
        part = []
        for tree in other[0].getchildrenlike(movie):
            part.append(tree_rating_enummerater(tree.getroot()) - others_average_rating[other[0].getroot()])
        influence += (other[1] / sum_simularity) * (sum(part)/len(part))
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
    for edge in edgelist:
        if not users.get(edge[1], False):
            user = {}
            user[edge[0]] = float(edge[2])
            users[edge[1]] = user
        else:
            user = users[edge[1]]
            user[edge[0]] = float(edge[2])
    return users, edgelist

def fold_split_reconstruction(folds, start, number):
    '''
    description: thid function findt the folds you want to use for a specific iteration
    parameters: folds is a list of foldkeys, start is the foldnumber you wish to start from
                and number is the nomber of folds you want
    return: return is the list of folds for an iteration
    '''
    folds_size = len(folds)
    result = []
    reset = start - folds_size
    for i in range(start, start+number):
        if i >= folds_size:
            if reset < 0:
                reset = 0
            i = reset
            reset += 1
        result.append(folds[i])
    return result

def base_experiment():
    '''
    description: runs 10fold experimant on base results
    '''
    with open("base_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7

        start = datetime.now()
        edgelist = jsonuserdatabase(Paths.Folds_100k_PATH,
                                    fold_split_reconstruction(folds, 0, 10))[1]
        sum_rating = 0
        for edge in edgelist:
            sum_rating += float(edge[2])

        ovar_all_average_rating = sum_rating/len(edgelist)
        result_predictions = {}

        for edge in edgelist:
            temp_person = result_predictions.get(edge[1], {})
            temp_person[edge[0]] = ovar_all_average_rating
            result_predictions[edge[1]] = temp_person

        finished = datetime.now()

        for i in range(10):
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            num2 += 1

def abstract_base_experiment():
    '''
    description: runs 10fold experimant on base results
    '''
    with open("abstract_base_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7

        start = datetime.now()
        edgelist = jsonuserdatabase(Paths.Folds_100k_PATH,
                                    fold_split_reconstruction(folds, 0, 10))[1]
        sum_rating = 0
        for edge in edgelist:
            sum_rating += float(edge[2])

        ovar_all_average_rating = sum_rating/len(edgelist)
        result_predictions = {}

        for edge in edgelist:
            temp_person = result_predictions.get(edge[1], {})
            temp_person[edge[0]] = ovar_all_average_rating
            result_predictions[edge[1]] = temp_person

        finished = datetime.now()
        
        result_predictions = ratingstoabstract(result_predictions)
        for i in range(10):
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]
            
            
            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            num2 += 1

def brutefoce_experiment():
    '''
    description: runs 10fold experimant with a bruteforce method
    '''
    with open("Bruteforce_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7
        for i in range(len(folds)):
            # brute experiment
            training_data = jsonuserdatabase(Paths.Folds_100k_PATH,
                                             fold_split_reconstruction(folds, i, 8))[0]
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]


            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "manhatten_brute"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(list(training_data)):
                wish_to_predict = list(test_expected_predictions[person])
                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, training_data, training_data,
                                                 k=10)
            finished = datetime.now()

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-brute.p', 'wb'))
            num2 += 1

def node2vec_experiment():
    '''
    description: runs 10fold experimant with the Node2vec method
    '''
    with open("node2vec_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7
        for i in range(len(folds)):
            training_data = jsonuserdatabase(Paths.Folds_100k_PATH,
                                             fold_split_reconstruction(folds, i, 8))[0]
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]

            with open(Paths.N2V_MODELS_PATH / Path('Folds_100k_' + str(i+1) + '.pkl'), 'rb') as modelfile:
                n2v_model = pickle.load(modelfile)

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "node2vec"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(list(training_data)):
                wish_to_predict = list(test_expected_predictions[person])
                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, n2v_model, training_data, k=10)
            finished = datetime.now()

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-n2v.p','wb'))
            num2 += 1

def tet_experiment():
    '''
    description: runs 10fold experimant with tet comparison
    '''
    with open("tet_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        movie_database = moviedict(Paths.MOVIE_NODES_100k_PATH)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7

        for i in range(len(folds)):
            training_data, edgelist = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                       fold_split_reconstruction(folds, i, 8))
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]

            tets = build_tets(edgelist, movie_database, Paths.USER_NODES_100k_PATH)

            save_tets(tets, Paths.TETS_PATH / Path('TET_' + str(i) + '_' + str(num2) + '_100k.csv'))

            #TET_CLASSIFIER = metric_tree.mt_build(dmax = 10, nmax= 1000, depth = 0,
            #                                      data=list(TETs.values()))
            #pickle.dump(TET_CLASSIFIER, open("TETmt_9_6_100k.p", "wb"))

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "distancev3_tet"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(list(training_data)):
                wish_to_predict = list(test_expected_predictions[person])
                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, tets, training_data, k=10)
            finished = datetime.now()

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-tet.p', 'wb'))
            num2 += 1

def abstract_tet_experiment():
    '''
    description: runs 10fold experimant with tet comparison
    '''
    with open("abstract_tet_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        movie_database = moviedict(Paths.MOVIE_NODES_100k_PATH)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7

        for i in range(len(folds)):
            training_data, edgelist = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                       fold_split_reconstruction(folds, i, 8))
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]

            tets = build_tets(edgelist, movie_database, Paths.USER_NODES_100k_PATH)

            save_tets(tets, Paths.TETS_PATH / Path('TET_' + str(i) + '_' + str(num2) + '_100k.csv'))

            #TET_CLASSIFIER = metric_tree.mt_build(dmax = 10, nmax= 1000, depth = 0,
            #                                      data=list(TETs.values()))
            #pickle.dump(TET_CLASSIFIER, open("TETmt_9_6_100k.p", "wb"))

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "distancev3_tet_2"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(list(training_data)):
                wish_to_predict = list(test_expected_predictions[person])
                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, tets, training_data, k=10)
            finished = datetime.now()

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-abstract_tet.p', 'wb'))
            num2 += 1
            
def tet_senario_experiment():
    '''
    description: runs 10fold experimant with tet comparison
    '''
    with open("tet_senario_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        movie_database = moviedict(Paths.MOVIE_NODES_100k_PATH)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7

        for i in range(len(folds)):
            master_training_data, edgelist = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                       fold_split_reconstruction(folds, i, 8))
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]

            #TET_CLASSIFIER = metric_tree.mt_build(dmax = 10, nmax= 1000, depth = 0,
            #                                      data=list(TETs.values()))
            #pickle.dump(TET_CLASSIFIER, open("TETmt_9_6_100k.p", "wb"))

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "distancev3_tet_2"

            result_predictions = {}

            totaltime = datetime.now() - datetime.now()
            for person in tqdm(master_training_data):
                wish_to_predict = list(test_expected_predictions[person])
            
                for item in wish_to_predict:
                    training_data = remove_relation(master_training_data, item)

                tets = build_tets(edgelist, movie_database, Paths.USER_NODES_100k_PATH)
                
                start = datetime.now()
                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, tets, training_data, k=10)
                totaltime += datetime.now() - start

            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(totaltime))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, totaltime])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-tet_scenario.p', 'wb'))
            num2 += 1

def node2vec_senario_experiment():
    '''
    description: runs 10fold experimant with the Node2vec method
    '''
    with open("node2vec_senario_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7
        for i in range(len(folds)):
            master_training_data = jsonuserdatabase(Paths.Folds_100k_PATH,
                                             fold_split_reconstruction(folds, i, 8))[0]
            
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]
            
            
            with open(Paths.N2V_MODELS_PATH / Path('Folds_100k_' + str(i+1) + '.pkl'), 'rb') as modelfile:
                n2v_model = pickle.load(modelfile)

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "node2vec"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(master_training_data):
                wish_to_predict = list(test_expected_predictions[person])
            
                for item in wish_to_predict:
                    training_data = remove_relation(master_training_data, item)

                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, n2v_model, training_data, k=10)
            finished = datetime.now()
            
            result_predictions = ratingstoabstract(result_predictions)
            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-n2v_scenario.p', 'wb'))
            num2 += 1

def abstract_node2vec_senario_experiment():
    '''
    description: runs 10fold experimant with the Node2vec method
    '''
    with open("abstract_node2vec_senario_experiment.csv", "w", newline='', encoding='utf-8') as write:
        file_writer = csv.writer(write)
        folds = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5',
                 'fold6', 'fold7', 'fold8', 'fold9']
        file_writer.writerow(['fold', 'RMSE', 'MAE', 'time taken on test'])
        num2 = 7
        for i in range(len(folds)):
            master_training_data = jsonuserdatabase(Paths.Folds_100k_PATH,
                                             fold_split_reconstruction(folds, i, 8))[0]
            
            test_expected_predictions = jsonuserdatabase(Paths.Folds_100k_PATH,
                                                               fold_split_reconstruction(folds,
                                                                                         i+8, 2))[0]
            
            
            with open(Paths.N2V_MODELS_PATH / Path('Folds_100k_' + str(i+1) + '.pkl'), 'rb') as modelfile:
                n2v_model = pickle.load(modelfile)

            # models: manhatten_tet, GED_tet, manhatten_brute, distancev3_tet, distancev2_tet
            comparison_method = "node2vec"

            result_predictions = {}
            start = datetime.now()
            for person in tqdm(master_training_data):
                wish_to_predict = list(test_expected_predictions[person])
            
                for item in wish_to_predict:
                    training_data = remove_relation(master_training_data, item)

                result_predictions[person] = knn(person, list(training_data), wish_to_predict,
                                                 comparison_method, n2v_model, training_data, k=10)
            finished = datetime.now()
            
            result_predictions = ratingstoabstract(result_predictions)
            RMSE = root_mean_squre_error(result_predictions, test_expected_predictions)
            MAE = mean_average_error(result_predictions, test_expected_predictions)

            print(i)
            print('test root mean square error: ' + str(RMSE))
            print('test mean average error: ' + str(MAE))
            print('experiment time: ' + str(finished - start))

            if num2 >= len(folds):
                num2 = 0
            file_writer.writerow(['fold' + str(i) + '-' + str(num2) + '-100k',
                                  RMSE, MAE, finished - start])
            pickle.dump(result_predictions, open('fold' + str(i) + '-' + str(num2) + '-100k-res-abstract_n2v_scenario.p', 'wb'))
            num2 += 1

def remove_relation(userdatabase, item):
    for person in userdatabase:
        temp = userdatabase[person]
        if temp.get(item, False):
            del temp[item]
            userdatabase[person] = temp
    return userdatabase

def ratingstoabstract(predictions):
    for user in predictions:
        for movie in predictions[user]:
            predictions[user][movie] = Otorating(predictions[user][movie])
    return predictions

if __name__ == "__main__":
    #print('start base')
    #base_experiment()
    #abstract_base_experiment()
    #print('start brute')
    #brutefoce_experiment()
    #print('start N2V')
    #node2vec_experiment()
    #abstract_node2vec_senario_experiment()
    #node2vec_senario_experiment()
    #print('start TET')
    #tet_experiment()
    #abstract_tet_experiment()
    #tet_senario_experiment()
    print('done')
