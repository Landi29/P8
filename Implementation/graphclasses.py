class user_node:

    def __init__(self,id):
        self.id = id

    def __str__(self):
        return("%s" % (self.id))



class movie_node:

    def __init__(self,id,title,genre):
        self.id = id
        self.title = title
        self.genre = genre

    def __str__(self):
        return("%s;%s;%s" % (self.id,self.title,self.genre))



class rating_edge:

    def __init__(self,rating,movie_id,user_id):
        self.rating = rating
        self.movie_id = movie_id
        self.user_id = user_id

    def __str__(self):
        return("%s;%s;%s" % (self.rating,self.movie_id,self.user_id))