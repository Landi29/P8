import csv
import Build_TET
import Paths

def find_all_keys_in_dicts(keys1, keys2):
    '''
    description: this function combines two list without dublication.
    parameters: keys1 and keys2 is two lists.
    return: the output is a list containing all element in key1 and key2.
    '''
    for key in keys2:
        if key not in keys1:
            keys1.append(key)
    return keys1

def manhatten_distance(tet1, tet2):
    '''
    description: this function finds the manhatten distance by treationg the tet histograms as
                 vectors and compreing the elements in the vectors.
    parameters: tet1 and tet2 are tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    distance = 0.0
    if tet1 != tet2:
        structure1 = tet1.histogram()
        structure2 = tet2.histogram()
        keys = find_all_keys_in_dicts(list(structure1), list(structure2))
        for key in keys:
            distance += abs(structure1.get(key, 0) - structure2.get(key, 0))
    return distance

def graph_edit_distance(tet1, tet2):
    '''
    description: this funktion find the grap edit distance by going through the count of children
                 to find how many edits is needed for the two trees to be equivalent.
    parameters: tet1 and tet2 are tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    distance = 0.0
    if tet1 != tet2:
        structure1 = tet1.count_children()
        structure2 = tet2.count_children()
        keys = find_all_keys_in_dicts(list(structure1), list(structure2))
        for key in keys:
            distance += cost(key) * abs(structure1.get(key, 0) - structure2.get(key, 0))
    return distance

def cost(stringkey):
    '''
    description: this function finds a cost of an edit.
    parameters: stringkey is the key representing what edit needs to be performed.
    return: the return is the cost of the edit type.
    '''
    rating = stringkey.replace('[', '').replace(']', '').split(',')[0]
    switcher = {
        'low': 0.25,
        'mid': 0.5,
        'high': 1,
    }
    return switcher[rating]

def knn(user, others, k=3):
    '''
    description: this is a simpel implementation of knn finding the k nearest neighbors
                 and making predictions.
    parameters: user is a user you want to recommend to, others are all other trees
                and k is the nomber of neighbors we want to compare with.
    return: the return is a sorted list of recommendet movies.
    '''
    sims = []
    for other in others:
        if user != other:
            sims.append([other, graph_edit_distance(user, other)])
    bestk = sorted(sims, key=lambda x: x[-1])[:k]
    predictions = pred(user, bestk)
    return sorted(predictions, key=lambda x: x[-1])

def pred(user, others):
    '''
    description: This function calculates a prediction on the users rating on movies
                 others has seen that the user have not seen.
    parameters: user is a user you want to recommend to, others are the k other users.
    return: The return is a list of recommendet movies.
    '''
    user_database = userdatabase()
    #ra average
    average_rating_user = 0
    seenbyuser = list(user_database[user.getroot()])
    for rating in user_database[user.getroot()].values():
        average_rating_user += rating
    average_rating_user = average_rating_user / len(user_database[user.getroot()])

    others = reasing_sims(others)

    others_average_rating = {}
    naighborseen = []
    for other in others:
        for movie in user_database[other[0].getroot()]:
            if movie not in seenbyuser:
                naighborseen.append(movie)
        average_rating_other_user = 0
        for rating in user_database[other[0].getroot()].values():
            average_rating_other_user += rating
        others_average_rating[other[0].getroot()] = average_rating_other_user \
            / (len(user_database[other[0].getroot()].values()))

    predictions = []
    for movie in naighborseen:
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
        if sumrating >= 4:
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
    TETS = Build_TET.load_tets(Paths.TETS_PATH)
    GROUPS = Build_TET.grouping(TETS)

    for predrating in knn(list(TETS.values())[0], list(TETS.values())):
        print('{} predicted rating: {}'.format(predrating[0], predrating[1]))
    print('\ndone')
