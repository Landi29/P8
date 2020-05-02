"""Module for reading and discretizing movielens data
into a graph representation of edges and nodes"""

import csv
import json
import requests
import Paths



def disc_rating_data(inputfile, savepath, number_of_users):
    """Reads a csv file with rating data, changes it into a graph
    representaition of (Head,Tail,Weight) and writes it into a new file

    Parameters:
        inputfile (filepath): filepath for the file to read, should be in the form of an edgelist
        savepath (filepath): filepath where to save the graph, saves as an csv file
        number_of_users (int): number of users to make a graph from, given 'None' will use whole dataset
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
        #in case that you only wanna discretize a subset of the data
        else:
            print("Discretizing the first "+str(number_of_users)+" users")
            for rating in reader:
                if int(rating[0]) <= number_of_users:
                    filewriter.writerow(["M:"+rating[1], "U:"+rating[0], rating[2]])
                else:
                    break
        nf.close()

def disc_rating_data_dat(inputfile, savepath):
    """Reads a .dat file with rating data, changes it into a graph
    representaition of (Head,Tail,Weight) and writes it into a new file as .csv

    Parameters:
        inputfile (filepath): filepath for the file to read, should be in the form of an edgelist
        savepath (filepath): filepath where to save the graph, saves as an csv file
    """

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)

        for rating in fp:
            edge = rating.split("::")
            filewriter.writerow(["M:"+edge[1], "U:"+edge[0], edge[2]])


    nf.close()


def disc_movie_data():
    """
    Reads file with movie data, finds missing information
    using OMDB and writes it into a new file.
    Output is of the form (moveID,movieTitle,ReleaseYear,Genres)
    """

    #API-key from OMDB Api (limit: 1000 daily)
    APIKEY = "ad37bdca"

    with open(Paths.MOVIEPATH, "r", encoding='utf-8') as fp:
        nf = open(Paths.MOVIE_NODES_PATH, "w+", newline='', encoding='utf-8')
        filewriter = csv.writer(nf)

        #Load file that links the movieID to an IMDBid
        linkfile = open(Paths.MOVIELINKPATH, "r", encoding='utf-8')

        #movie is an array of the form [movieID,movietitle,genres]
        for movie in csv.reader(fp):
            movietitle = movie[1]

            #Certain movietitles are missing the year it was released
            #if so, make api call to get the year from OMDB
            if "(" in movietitle:
                #Find substring from movie title that contains the year
                movieyear = movietitle[-5:-1]
            else:
                #link is an array of the form [movieID,imdbID,tmdbID]
                for link in csv.reader(linkfile):
                    #find the corresponding movie in linkfile and get the imdbID
                    if link[0] == movie[0]:
                        imdbid = link[1]
                        #make an api call to the omdb database
                        try:
                            response = requests.get("http://www.omdbapi.com/?i=tt"+
                                                    imdbid+"&APIKEY="+APIKEY)
                            moviejson = response.json()
                            movieyear = moviejson["Year"]
                        except:
                            print("Failed response")
                            movieyear = "unknown"
                        #Break so that we don't continue the for loop
                        break

            filewriter.writerow([movie[0], movie[1], movieyear, movie[2]])

        nf.close()
        linkfile.close()

def disc_movie_data_100k(inputfile, outputfile):
    """
    Reads the file with movie data for the 100k grouplens dataset.
    Discretizes it into the form we need (Movieid, Title, Release, Genres)

    Parameters:
    Inputfile (filepath): Filepath for the 100k .data file from grouplens
    Outputfile (filepath): Filepath for where you want to save the discretized data
    """


    with open(inputfile, "r") as fp:
        nf = open(outputfile, "w", newline='', encoding='utf-8')
        writer = csv.writer(nf)

        #List of genres in the dataset
        genre_list = ['Unknown', 'Action', 'Adventure', 'Animation', "children's",
                      'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
                      'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
                      'War', 'Western']

        for movie in fp:
            movie = movie.split('|')
            genres = movie[5:]
            genre_for_movie = ''

            #Movies use one-hot encoding for their genres in the dataset
            #This should be replaced with the actual genre
            for genre_binary, genre_string in zip(genres, genre_list):
                if '1' in genre_binary:
                    genre_for_movie = genre_for_movie + genre_string + '|'
            genre_for_movie = genre_for_movie[:-1]

            movie = [movie[0], movie[1], movie[2], genre_for_movie]

            writer.writerow(movie)

        nf.close()

def disc_movie_data_1m(inputfile, outputfile):
    """
    Reads the file with movie data for the 1 million grouplens dataset.
    Discretizes it into the form we need (Movieid, Title, Release, Genres)

    Parameters:
    Inputfile (filepath): Filepath for the 1 million .dat file from grouplens
    Outputfile (filepath): Filepath for where you want to save the discretized data
    """

    with open(inputfile, "r") as fp:
        nf = open(outputfile, "w", newline='')
        writer = csv.writer(nf)

        for movie in fp:
            movie = movie.split('::')
            #Get the Id, Title, Year it was released, genres
            #Strip genres to get rid of newline and quotes
            movie = movie[0], movie[1], movie[1][-5:-1], movie[2].strip()
            writer.writerow(movie)

        nf.close()

def discretize_100k_data(inputpath, outputfile):
    """
    Reads the file with ratings data for the 100k grouplens dataset.
    Discretizes it into the form we need (MovieId, UserId, Rating)

    Parameters:
    Inputfile (filepath): Filepath for the 100k ratings file from grouplens
    Outputfile (filepath): Filepath for where you want to save the discretized data
    """

    with open(inputpath, "r") as fp:
        nf = open(outputfile, "w", newline='')
        writer = csv.writer(nf)
        #Used to keep list of all edges
        edges = []
        for rating in fp:
            #Split it into a list and add it to list of all edges
            edge = rating.split('\t')
            edges.append([int(edge[0]), edge[1], edge[2]])

        #Sort the list on the UserID as dataset is not in order
        edges = sorted(edges, key=lambda x: x[0])

        for edge in edges:
            writer.writerow(edge)

        nf.close()

#Read the ratings csv file and convert the data into users
#As output we get a csv file where each line is a node for a user of the form (userId, ratingcount)
def disc_user_data(inputfile, savepath):
    """
    Reads the file with user data from the grouplens datasets
    counts how many ratings each user have and writes it into a new file

    Parameters:
    inputfile (filepath): Filepath for the user file from grouplens datasets
    savepath (filepath): Filepath where you want to save the discretized data
    """

    with open(inputfile, "r") as fp:
        nf = open(savepath, "w+", newline='')
        filewriter = csv.writer(nf)

        #All list are ordered by User, so we always start with User 1.
        currentid = 'U:1'
        counter = 0

        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        for rating in csv.reader(fp):

            #skip line if not a rating
            if "user" in rating[1]:
                pass
            #count up if the same user has made multiple ratings
            elif rating[1] == currentid:
                counter += 1
            #Write to file once we find a different userid
            else:
                filewriter.writerow([currentid, counter])
                currentid = rating[1]
                #Reset counter to 1 (including the current rating)
                counter = 1
        nf.close()


def avg_total_rating(inputfile):
    """
    Takes a discretized user dataset using disc_user_data()
    Finds the avarage numbers of ratings each user have made.

    Parameters:
    inputfile (filepath): Filepath for the discretized user data

    Return:
    Avg_rating (int): Avarage number of ratings for all users
    """

    with open(inputfile, "r") as fp:
        total_rating = 0
        number_of_users = 0

        for user in csv.reader(fp):
            total_rating += int(user[1])
            number_of_users += 1

        #Calculate the average
        avg_rating = (total_rating/number_of_users)

    return avg_rating


def split_into_folds(inputpath, outputpath):
    """
    Splits graph/rating data into 10 different folds
    Folds are saved in a json file as a dictionary

    Parameters:
    inputpath (filepath): Filepath for the graph data to split
    outputpath (filepath): Filepath for where you want to save the folds
    """

    #The dictionaries we use
    userdict = {}
    folddict = {}

    #Create a dictionary of users and their ratings
    with open(inputpath, "r") as fp:
        reader = csv.reader(fp)

        #Get the value of the user in the dictionary (empty list if doesn't exist)
        #Append the edge to the users value
        for edge in reader:
            temp = userdict.get(edge[1], [])
            temp.append(edge)
            userdict[edge[1]] = temp

    #The fold to start from
    fold = 0

    #Get the values for all users in the dictionary
    for user in userdict.values():

        #Get the value of the fold in the dictionary (empty list if doesn't exist)
        #Append the edge to that folds value
        for rating in user:
            temp = folddict.get("fold"+str(fold), [])
            temp.append(rating)
            folddict["fold"+str(fold)] = temp
            fold += 1
            #when fold is equal 10 we reset as we start from 0.
            if fold == 10:
                fold = 0

    #Write the dictionary into a json file
    json.dump(folddict, open(outputpath, "w"))

    print("Folds created and saved")



if __name__ == "__main__":
    print("Hallo")
    #disc_movie_data_100k(MOVIEPATH_100K, MOVIE_NODES_PATH_100K)
    #disc_movie_data_1m(MOVIEPATH_1M, MOVIE_NODES_PATH_1M)
