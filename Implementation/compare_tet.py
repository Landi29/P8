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

def distance_v2_start(tet1, tet2):
    '''
    description: this function is the starter function for the distance function that takes leaves into account 
    parameters: tet1 and tet2 are tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    distance = 0.0
    if tet1 != tet2:
        structure1 = tet1.histogram()
        structure2 = tet2.histogram()
        distance = distance_v2(structure1,structure2)
    return distance

def distance_v2(histogram1, histogram2):
    '''
    description: uses the histograms and goes through them to to find leaf level of the tet to decern distance
    parameters: histogram1 and histogram2 are string histogram descriptions of a tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    distance = 0.0
    if  isinstance(histogram1, str):
        leaves1 = histogram1.replace('[', '').replace(']', '').split(',')[1:]
        leaves2 = histogram2.replace('[', '').replace(']', '').split(',')[1:]
        return len(list(set(leaves1).symmetric_difference(set(leaves2))))

    for key1 in histogram1:
        key1root = key1.replace('[', '').replace(']', '').split(',')[0]
        for key2 in histogram2:
            key2root = key2.replace('[', '').replace(']', '').split(',')[0]
            if key1root == key2root:
                distance += histogram1[key1] * histogram2[key2] * distance_v2(key1, key2)
    return distance

def distance_v3(tet1, tet2):
    '''
    description: uses the histograms and goes through them to to find leaf level of the tet to decern distance
    parameters: histogram1 and histogram2 are string histogram descriptions of a tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    
    if tet1 == tet2:
        return 0
    
    histogram1 = tet1.histogram()
    histogram2 = tet2.histogram() 
    distance = 0.0
    for key1 in histogram1:
        histogramsplit1 = key1.replace('[', '').replace(']', '').split(',')
        for key2 in histogram2:
            histogramsplit2 = key2.replace('[', '').replace(']', '').split(',')
            distance += histogram1[key1] * histogram2[key2] * (low_mid_high_dif(histogramsplit1[0], histogramsplit2[0]) + leaf_distance_v3(histogramsplit1[1:], histogramsplit2[1:]))
    return distance

def leaf_distance_v3(leaves1, leaves2):
    '''
    description: uses the histograms and goes through them to to find leaf level of the tet to decern distance
    parameters: histogram1 and histogram2 are string histogram descriptions of a tets.
    return: the output is a distance between the two tets. A low distance is better than a high.
    '''
    return len(list(set(leaves1).symmetric_difference(set(leaves2))))

def low_mid_high_dif(rating1, rating2):
    if rating1==rating2:
        return 0
    elif  (rating1 == 'low' and rating2 == 'high') or (rating1 == 'high' and rating2 == 'low'):
        return 2
    else:
        return 1


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

if __name__ == "__main__":
    TETS = build_tet.load_tets(Paths.TETS_PATH, 1000)
    #GROUPS = build_tet.grouping(TETS)

    dis = distance_v3(list(TETS.values())[0], list(TETS.values())[1])
    print('Distance: {}'.format(dis))
    print('\ndone')
