import pymongo

class Database(object):

    #URI = "mongodb://127.0.0.1:27017"
    URI = "mongodb://webgmit:gmit123@ds135797.mlab.com:35797/webposts"

    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['webposts']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)