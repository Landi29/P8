import csv
import build_tet
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
