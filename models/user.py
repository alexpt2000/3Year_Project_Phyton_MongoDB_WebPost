import uuid
import datetime
from flask import session

from common.database import Database
from models.allPosts import AllPosts

# one class to deal with users
# users objects are created
# and all activities that a user might want to do are dealt with in this class.
# creates an user object(with an name, email password and sets _id to none )
# an auto generated id is created and given a hex unique value

# initialize a user object with attributes of
# name ,email password and auto generated id.


class User(object):
    def __init__(self, name, email, password, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_name(cls, name):
        data = Database.find_one(collection='users', query={'name': name})
        print(data)
        if data is not None:
            return cls(**data)

# (**data) a python shortcut is an easy way of returning all the elements of the user
#  instead of writing ie: name, email,password and unique id(_id)
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection='users', query={'email': email})
        print(data)
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='users', query={'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, name, email, password):
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(name, email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_posts(self):
        return AllPosts.get_post_from_author_id(self._id)

    def new_post(self, title, description):
        post = AllPosts(authorName=self.name, author=self.email, title=title, description=description,
                        author_id=self._id)
        post.save_to_mongo()

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())

    def json(self):
        return {'name': self.name,
                'email': self.email,
                'password': self.password,
                '_id': self._id}

    @classmethod
    def from_mongo(cls):
        posts = Database.find(collection='posts', query={})
        return [post for post in posts]
