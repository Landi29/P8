import csv
import Paths
from tqdm import tqdm

print("Reading the data.")

ratings = [i.strip().split() for i in open(Paths.SMALL_GRAPH_RATINGS_PATH).readlines()]

print("Converting the data to a csv file.")

with open(Paths.SMALL_GRAPH_RATINGS_CSV_PATH,'w+') as output:
    writer = csv.writer(output)
    
    writer.writerows(ratings)