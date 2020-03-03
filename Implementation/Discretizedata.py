import csv


#Filepath for movielens files
#Change accordingly if needed
ratingpath = "C:\\Users\\RedTop\\Desktop\\Movielens data\\ratings.csv"
moviepath = "C:\\Users\\RedTop\\Desktop\\Movielens data\\movies.csv"

#Read the ratings csv file and only keep the data that we need, by reading it one line at a time
#As output we get a txt file where each line corresponds to en edge in the graph (Head,Tail,Weight) (MovieId, UserId, Rating)


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
    with open(moviepath, "r") as fp:
        nf = open("movies.txt","w+")

        for line in fp:
            fl = fp.readline()
            linearray = fl.split(",")
            print(linearray)

        #CLean and split the information further to split the movietitle into title and year

            if len(linearray) == 4:
                titleyear = linearray[2].split(" (")
                titleyear[1] = titleyear[1][0:4]
                titleyear[0] = (linearray[1] + titleyear[0])

                nf.write(linearray[0]+","+titleyear[0]+","+titleyear[1]+","+linearray[2])
            else:
                titleyear = linearray[1].split(" (")
                titleyear[1] = titleyear[1][0:4]
                nf.write(linearray[0]+","+titleyear[0]+","+titleyear[1]+","+linearray[2])

            print(titleyear)




#Read the ratings csv file and convert the data into users
#As output we get a txt file where each line is a node for a user of the form (userId, ratingcount)
#def discuserdata():
#    with open("C:\\Users\\RedTop\\Desktop\\Movielens data\\ratings.csv", "r") as fp:




def removefromstring(match, characters):

    # Go through the list and remove any occurencess of given characters
    trantab = match.maketrans("", "", characters)
    cleanedstring = match.translate(trantab)
    return cleanedstring

discratingdata()