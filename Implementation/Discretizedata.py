import csv
import json
import requests

#Filepath for movielens files
#Change accordingly if needed
ratingpath = "C:\\Users\\RedTop\\Desktop\\Movielens data\\ratings.csv"
moviepath = "C:\\Users\\RedTop\\Desktop\\Movielens data\\movies.csv"

#Read the ratings csv file and only keep the data that we need, by reading it one line at a time
#As output we get a txt file where each line corresponds to en edge in the graph (Head,Tail,Weight) (MovieId, UserId, Rating)

movietitle = "Sleepless in Seattle (1993)"


print(movieyear)

def discratingdata():
    with open(ratingpath, "r") as fp:
        nf = open("graph.csv","w+", newline='')
        filewriter = csv.writer(nf)

        #for each line, split it into an array
        for line in csv.reader(fp):
        
            #save the information as a string and read it into a file
            #each line in the file is now of the form (MovieId, UserId, Rating)
            filewriter.writerow([line[1],line[0],line[2]])

        nf.close()

#Read the movies csv file and convert the data to a more readable/useable format
#As output we get a txt file where each line is a node for a movie of the form (movieId,movieTitle,ReleaseYear,genres)
def discmoviedata():
    with open(moviepath, "r", encoding='utf-8') as fp:
        nf = open("movies.csv","w+", newline='')
        filewriter = csv.writer(nf)
        counter = 0
        for line in csv.reader(fp):
            movietitle = line[1]

            if "(" in movietitle:
                movieyear = movietitle[-5:-1]                
            else:
                response = requests.get("http://www.omdbapi.com/?t="+movietitle+"&apikey=ad37bdca")
                movie = response.json()
                movieyear = movie["Year"]



        #CLean and split the information further to split the movietitle into title and year



#Read the ratings csv file and convert the data into users
#As output we get a txt file where each line is a node for a user of the form (userId, ratingcount)
#def discuserdata():
#    with open("C:\\Users\\RedTop\\Desktop\\Movielens data\\ratings.csv", "r") as fp:


def removefromstring(match, characters):

    # Go through the list and remove any occurencess of given characters
    trantab = match.maketrans("", "", characters)
    cleanedstring = match.translate(trantab)
    return cleanedstring

#discmoviedata()