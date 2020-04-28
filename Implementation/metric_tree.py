import random
import pickle
from compare_tet import distance_v2_start as dist
from build_tet import load_tets
import Paths
from tqdm import tqdm

def mt_build(dmax, nmax, depth, data):
    '''
    description: This function constructs the metric tree and subtrees
    parameters: dmax is the wished max depth of the tree, nmax is the maximal number of entities
    in a bucket, depth is the current depth and data is the data that is being categorized in the mt
    return: the return is the full mt
    '''
    print("building at " + str(depth))
    node = MTnode()
    if depth == dmax or len(data) <= nmax:
        node.bucket = data
        return node
    node.split_point1, node.split_point2 = get_random_pair(data)
    data1, data2 = split_data(data, node.split_point1, node.split_point2)
    node.left = mt_build(dmax, nmax, depth+1, data1)
    node.right = mt_build(dmax, nmax, depth+1, data2)

def mt_search(node, searched):
    '''
    description: This function searches an mt
    parameters: node is an mt or submt, searched is the element you wish to find entities like
    and k is the number of entities you wish to find
    return: the return is the estimated nearest bucket
    '''
    if node.isleaf():
        return node.bucket
    if dist(searched, node.z1) <= dist(searched, node.z2):
        return mt_search(node.left, searched)
    else:
        return mt_search(node.right, searched)

def get_random_pair(data):
    '''
    description: This function gets two random entities from the date
    parameters: data is the entities you want to find two random of
    return: the return is two entities from data
    '''
    random1 = random.randint(0, len(data))
    random2 = random.randint(0, len(data))
    while random1 == random2:
        random1 = random.randint(0, len(data))
        random2 = random.randint(0, len(data))
    return data[random1], data[random2]

def split_data(masterdata, splitpoint1, splitpoint2):
    '''
    description: This function splits data in two according to the distance to the split points
    parameters: masterdata is the data you wish to split splitpoint1 and splitpoint2 is
    the entities you wish to split around
    return: returns the split dataset
    '''
    data1 = []
    data2 = []
    for data in tqdm(masterdata):
        if dist(data, splitpoint1) <= dist(data, splitpoint2):
            data1.append(data)
        else:
            data2.append(data)
    return data1, data2

class MTnode:
    '''
    a mt is part of a tree structure that is easily searched
    '''
    def __init__(self):
        self.left = None
        self.right = None
        self.split_point1 = None
        self.split_point2 = None
        self.bucket = None

    def isleaf(self):
        '''
        description: tells if a node is a leaf node
        return: returns a boolean, true if leaf and false if not
        '''
        if self.left is None and self.right is None:
            return True
        return False

if __name__ == "__main__":

    MT = mt_build(dmax=10, nmax=10000, depth=0, data=list(load_tets(Paths.TETS_PATH).values()))

    pickle.dump(MT, open("saveMT.p", "wb"))
    print('done')
