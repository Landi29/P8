import csv
import json
import requests
import time

#Filepaths for movielens datadump
#Change accordingly if needed
ratingpath = "Implementation\\Movielens_data\\ratings.csv"
moviepath = "Implemnetation\\Movielens_data\\movies.csv"
movielinkpath = "Implementation\\Movielens_data\\links.csv"
#API-key from OMDB Api (limit: 1000 daily)
apikey = "ad37bdca"


#Read the ratings csv file one line at a time, only keep the data we need
#As output we get a csv file where each line corresponds to en edge in the graph (Head,Tail,Weight) (MovieId, UserId, Rating)
def disc_rating_data():
    with open(ratingpath, "r") as fp:
        nf = open("Implementation\\Movielens_data\\graphs.csv","w+", newline='')
        filewriter = csv.writer(nf)

        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        for rating in csv.reader(fp):
        
            filewriter.writerow([rating[1],rating[0],rating[2]])

        nf.close()

#Read the movies csv file and take out the information we need, including release year
#As output we get a csv file where each line is a node for a movie of the form (movieId,movieTitle,ReleaseYear,genres)
def disc_movie_data():
    with open(moviepath, "r", encoding='utf-8') as fp:
        nf = open("Implementation\\Movielens_data\\movie_nodes.csv","w+", newline='', encoding='utf-8')
        filewriter = csv.writer(nf)

        #File that links the movieID to an IMDBid
        linkfile = open(movielinkpath, "r", encoding='utf-8')

        counter = 0
        #movie is an array of the form [movieID,movietitle,genres]
        for movie in csv.reader(fp):
            movietitle = movie[1]

            #Certain movietitles are missing the year it was released
            #if so, make api call to get the year from OMDB
            if "(" in movietitle:
                #Take the substring from the movie title that contains the year is, it is always at the end of title as (year)
                movieyear = movietitle[-5:-1]           
            else:
                #link is an array of the form [movieID,imdbID,tmdbID]
                for link in csv.reader(linkfile):
                    if link[0] == movie[0]:
                        imdbid = link[1]
                        try:
                            response = requests.get("http://www.omdbapi.com/?i=tt"+imdbid+"&apikey="+apikey)
                            moviejson = response.json()
                            movieyear = moviejson["Year"]
                        except:
                            print("Failed response")
                            movieyear = "unknown"
                        break
                    else:
                        pass
        
            filewriter.writerow([movie[0],movie[1],movieyear,movie[2]])

        nf.close
        linkfile.close



#Read the ratings csv file and convert the data into users
#As output we get a csv file where each line is a node for a user of the form (userId, ratingcount)
def disc_user_data():
    with open(ratingpath, "r") as fp:
        nf = open("Implementation\\Movielens_data\\user_nodes.csv","w+", newline='')
        filewriter = csv.writer(nf)

        currentid = '1'
        counter = 0

        #rating is an array of the form [UserID,MovieID,Rating,Timestamp]
        for rating in csv.reader(fp):

            #skip line if not a rating
            if "user" in rating[0]:
                pass
            #count up if the same user have made multiple ratings
            elif rating[0] == currentid:
                counter += 1
            #Write to file once we find a different userid, and remember to count the current row we're looking at
            else:
                filewriter.writerow([currentid,counter])
                currentid = rating[0]
                counter = 1
        nf.close()