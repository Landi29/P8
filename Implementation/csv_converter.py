import csv
import Paths
with open (Paths.SMALL_GRAPH_RATINGS_PATH) as data:
    ratings = data.readlines()
with open(Paths.SMALL_GRAPH_RATINGS_CSV_PATH,'wb') as output:
    writer = csv.writer(output)
    writer.writerows(ratings)