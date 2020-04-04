import Build_TET
import pathlib
from tqdm import tqdm

def comparetets(tet1, tet2):
    sim = 0
    if tet1 != tet2:
        structure1 = tet1.count_children()
        structure2 = tet2.count_children()
        keys = find_all_keys_in_dicts(list(structure1),list(structure2))
        sim = manhatten_distance(structure1, structure2, keys)
    return sim

def find_all_keys_in_dicts(keys1,keys2):
    for key in keys2:
        if key not in keys1:
            keys1.append(key)
    return keys1

def manhatten_distance(structure1, structure2, keys):
    distance = 0.0
    for key in keys:
        distance += abs(structure1.get(key, 0) - structure2.get(key, 0))
    return distance

if __name__ == "__main__":
    TETS_PATH = pathlib.Path.cwd() / 'TET.csv'
    Tets = list(Build_TET.load_tets(TETS_PATH).values())
    N_Tets = len(Tets)
    for tet1 in tqdm(range(N_Tets)):
        for tet2 in range(tet1+1, N_Tets):
            comparetets(Tets[tet1], Tets[tet2])
            #print(str(tet1) + ' and ' + str(tet2) + ': ' + str(comparetets(Tets[tet1], Tets[tet2])))