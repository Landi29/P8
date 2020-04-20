"""Module for reading and discretizing movielens data
into a graph representation of edges and nodes"""

import csv
import requests
import pathlib
import tqdm
import numpy as np

#Filepaths for movielens datadump
RATINGPATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings.csv'
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movies.csv'
MOVIELINKPATH = pathlib.Path.cwd() / 'Movielens_data' / 'links.csv'
MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'

RATINGPATH_2 = pathlib.Path.cwd() / 'Movielens_data' / 'ratings_10m.dat'
CLEANED_RATINGPATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings_cleaned.csv'
GRAPH_DATA_PATH_2 = pathlib.Path.cwd() / 'Movielens_data' / 'graph_10m.csv'
USER_NODES_PATH_2 = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes_10m.csv'
CLEANED_USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'cleaned_user_nodes.csv'
CLEANED_GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph_cleaned.csv'
CLEANED_GRAPH_DATA_PATH_2 = pathlib.Path.cwd() / 'Movielens_data' / 'graph_10m_cleaned.csv'


#API-key from OMDB Api (limit: 1000 daily)
APIKEY = "ad37bdca"


#Read the ratings csv file one line at a time, only keep the data we need
#As output we get a csv file where each line corresponds to en edge in the graph (Head,Tail,Weight) (MovieId, UserId, Rating)
def disc_rating_data(inputfile, savepath, number_of_users):
    """Reads a csv file with rating data, changes it into a graph
    representaition of (Head,Tail,Weight) and writes it into a new file
    
    Parameters:
        inputfile (filepath): filepath for the file to read, should be in the form of an edgelist
        savepath (filepath): filepath where to save the graph, saves as an csv file
        number_of_users (int): number of users to make a graph from, if given 'None' will use whole dataset
    """

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)
        reader = csv.reader(fp)
        next(reader)
        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        if number_of_users is None:
            print("No number given, discretizing whole dataset")
            for rating in reader:
                filewriter.writerow(["M:"+rating[1], "U:"+rating[0], rating[2]])
        else:
            print("Discretizing the first "+str(number_of_users)+" users")
            for rating in reader:
                if int(rating[0]) <= number_of_users:
                    filewriter.writerow(["M:"+rating[1], "U:"+rating[0], rating[2]])
                else:
                    break
        nf.close()

def disc_rating_data_2(inputfile, savepath):
    """Reads a .dat file with rating data, changes it into a graph
    representaition of (Head,Tail,Weight) and writes it into a new file as .csv
    
    Parameters:
        inputfile (filepath): filepath for the file to read, should be in the form of an edgelist
        savepath (filepath): filepath where to save the graph, saves as an csv file
        number_of_users (int): number of users to make a graph from, if given 'None' will use whole dataset
    """

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)

        for rating in fp:
            edge = rating.split("::")
            filewriter.writerow(["1"+edge[1], "2"+edge[0], edge[2]])
            
    
    nf.close()

#Read the movies csv file and take out the information we need, including release year
#As output we get a csv file where each line is a node for a movie of the form (movieId,movieTitle,ReleaseYear,genres)
def disc_movie_data():
    """Reads file with movie data, finds missing information
    using OMDB and writes it into a new file"""

    with open(MOVIEPATH, "r", encoding='utf-8') as fp:
        nf = open(MOVIE_NODES_PATH, "w+", newline='', encoding='utf-8')
        filewriter = csv.writer(nf)

        #File that links the movieID to an IMDBid
        linkfile = open(MOVIELINKPATH, "r", encoding='utf-8')

        #movie is an array of the form [movieID,movietitle,genres]
        for movie in csv.reader(fp):
            movietitle = movie[1]

            #Certain movietitles are missing the year it was released
            #if so, make api call to get the year from OMDB
            if "(" in movietitle:
                #Find substring from movie title that contains the year, it is always at the end of title as (year)
                movieyear = movietitle[-5:-1]
            else:
                #link is an array of the form [movieID,imdbID,tmdbID]
                for link in csv.reader(linkfile):
                    if link[0] == movie[0]:
                        imdbid = link[1]
                        try:
                            response = requests.get("http://www.omdbapi.com/?i=tt"+imdbid+"&APIKEY="+APIKEY)
                            moviejson = response.json()
                            movieyear = moviejson["Year"]
                        except:
                            print("Failed response")
                            movieyear = "unknown"
                        break
                    else:
                        pass

            filewriter.writerow([movie[0], movie[1], movieyear, movie[2]])

        nf.close
        linkfile.close



#Read the ratings csv file and convert the data into users
#As output we get a csv file where each line is a node for a user of the form (userId, ratingcount)
def disc_user_data(inputfile, savepath):
    """Reads file with user data, counts how many ratings each user
    have done and writes it into a new file"""

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)

        currentid = '1'
        counter = 0

        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        for rating in csv.reader(fp):

            #skip line if not a rating
            if "user" in rating[1]:
                pass
            #count up if the same user has made multiple ratings
            elif rating[0] == currentid:
                counter += 1
            #Write to file once we find a different userid, remember to count the current row we're at
            else:
                filewriter.writerow([currentid, counter])
                currentid = rating[0]
                counter = 1
        nf.close()


def avg_total_rating(inputfile):
    """Hello"""


    total_rating = 0
    number_of_users = 0

    with open(inputfile, "r") as fp:

        for user in csv.reader(fp):
            total_rating += int(user[1])
            number_of_users += 1
    
        avg_rating = (total_rating/number_of_users)

    print(avg_rating)
    print(number_of_users)

    return avg_rating
             

def users_above_avg_rating(inputfile,rating_threshold):
    """hallo"""

    ratings_above_threshold = 0
    users = []

    with open(USER_NODES_PATH, "r") as fp:

        for user in csv.reader(fp):
            if int(user[1]) > rating_threshold:
                ratings_above_threshold += 1
                users.append(user[0])
            else:
                pass
    
    print(ratings_above_threshold)

    return users


def remove_users_from_graph(inputfile, savepath):

    #find liste af users over en given total rating ved brug af users_above_avg_rating
    Users_to_remove = users_above_avg_rating(USER_NODES_PATH, 1500)

    #TODO gå igennem ratings.csv eller graph.csv og fjern usersne fra listen fået tidligere
    #dette gøres nok bedst ved at åbne filen med edges/ratings at læse fra også lave en ny fil at skrive de linjer man gerne vil gemme til.
    #givet vi har 7000 users over 1000 rating og 25 millioner ratings skal vi worst case lave 175 milliarder checks..
    #kunne gemme den id vi kigger på at fjerne lige nu, og tjekke mod den indtil id'en i listen ikke længere matcher
    #en anden løsning ville være at fjerne useren fra listen når vi har fjernet alle hans ratings

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)
        reader = csv.reader(fp)
    
        index = 0
        cut = int(Users_to_remove[0])
        #in case first line is a header run this
        next(reader)

        for edge in reader:
            #Get the userid we want to remove/cut
            #Get the id we're currently looking at in the edge/graph file
            currentid = int(edge[0])
            if currentid < cut:
                filewriter.writerow(edge)
            elif currentid == cut:
                continue
            else:
                #In case that the user id for the edge we're looking at is bigger than the ID we want to remove
                #We will have to do some additional checks.
                index += 1
                #TODO fix index out of range error
                if index >= len(Users_to_remove):
                    cut = np.inf
                elif currentid == Users_to_remove[index]:
                    continue
                else:
                    cut = int(Users_to_remove[index])
        nf.close()



if __name__ == "__main__":
    #remove_users_from_graph(RATINGPATH, CLEANED_RATINGPATH)
    #disc_user_data(CLEANED_RATINGPATH, CLEANED_USER_NODES_PATH)
    #avg_total_rating(USER_NODES_PATH)
    #avg_total_rating(CLEANED_USER_NODES_PATH)
    disc_rating_data(CLEANED_RATINGPATH,CLEANED_GRAPH_DATA_PATH, 500)