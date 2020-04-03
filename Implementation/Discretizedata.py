"""Module for reading and discretizing movielens data
into a graph representation of edges and nodes"""

import csv
import requests
import pathlib

#Filepaths for movielens datadump
RATINGPATH = pathlib.Path.cwd() / 'Movielens_data' / 'ratings.csv'
MOVIEPATH = pathlib.Path.cwd() / 'Movielens_data' / 'movies.csv'
MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
GRAPH_DATA_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'graph.csv'

#API-key from OMDB Api (limit: 1000 daily)
APIKEY = "ad37bdca"


#Read the ratings csv file one line at a time, only keep the data we need
#As output we get a csv file where each line corresponds to en edge in the graph (Head,Tail,Weight) (MovieId, UserId, Rating)
def disc_rating_data(inputfile, savepath, number_of_users):
    """Reads file with rating data, changes it into a graph
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

#Read the movies csv file and take out the information we need, including release year
#As output we get a csv file where each line is a node for a movie of the form (movieId,movieTitle,ReleaseYear,genres)
def disc_movie_data():
    """Reads file with movie data, finds missing information
    using OMDB and puts it into a new file"""

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
def disc_user_data():
    """Reads file with user data, counts how many ratings each user
    have done and writes it into a new file"""

    with open(RATINGPATH, "r") as fp:
        nf = open(USER_NODES_PATH, "w+", newline='')
        filewriter = csv.writer(nf)

        currentid = '1'
        counter = 0

        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        for rating in csv.reader(fp):

            #skip line if not a rating
            if "user" in rating[0]:
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


if __name__ == "__main__":
    print("Hello")
