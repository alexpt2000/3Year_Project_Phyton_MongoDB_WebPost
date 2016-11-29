import pymongo

# one class to deal with the database manipulation.
# initialize,insert and find one or a collection of posts/users.


class Database(object):

    # deployment uri and password ,local database commented out.
    # URI = "mongodb://127.0.0.1:27017"
    URI = "mongodb://webgmit:gmit123@ds135797.mlab.com:35797/webposts"

    DATABASE = None

# initialize the database
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['webposts']

# insert data into the database
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

# find a collection /items ie; posts, which is linked to a user
#  from the database.
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)


# find one  item ie; email, id , name which is linked to a user
#  from the database.
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
