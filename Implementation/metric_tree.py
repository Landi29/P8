import random
from compare_tet import graph_edit_distance as dist
from build_tet import build_tets, moviedict, load_tets
import Paths
import pickle

def mt_build(dmax,nmax,d, data):
    print(d)
    node = mtnode()
    if d == dmax or len(data) <= nmax:
        node.bucket == data
        return node
    node.z1, node.z2 = get_random_pair(data)
    data1, data2 = split_data(data, node.z1, node.z2)
    node.left = mt_build(dmax, nmax, d+1, data1)
    node.right = mt_build(dmax, nmax, d+1, data2)

def mt_search(node, h, k):
    if node.isleaf():
        return sorted(node.bucket, key=lambda x: dist(x,h))[:k]
    if dist(h, node.z1) <= dist(h, node.z2):
        return mt_search(node.left, h, k)
    else:
        return mt_search(node.right, h, k)

def get_random_pair(data):
    r1 = random.randint(0,len(data))
    r2 = random.randint(0,len(data))
    while r1 == r2:
        r1 = random.randint(0,len(data))
        r2 = random.randint(0,len(data))
    return data[r1], data[r2]

def split_data(masterdata, z1, z2):
    data1 = []
    data2 = []
    for data in masterdata:
        if dist(data, z1) <= dist(data, z2):
            data1.append(data)
        else:
            data2.append(data)
    return data1, data2

class mtnode:
    def __init__(self):
        self.left = None
        self.right = None
        self.z1 = None
        self.z2 = None
        self.bucket = None
    
    def isleaf(self):
        if self.left == None and self.right == None:
            return True
        return False

if __name__ == "__main__":
    with open(Paths.GRAPH_DATA_PATH, 'r', encoding="utf-8") as read:
        graph_data = read.readlines()

    mt = mt_build(dmax=10, nmax=10000, d=0, data=list(load_tets(Paths.TETS_PATH).values()))

    pickle.dump(mt, open( "save.p", "wb" ) )
    print('done')