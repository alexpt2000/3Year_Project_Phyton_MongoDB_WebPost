import datetime
import uuid
from common.database import Database


class Post(object):
    def __init__(self, post_id, post_title, post_content, authorName, author, created_time=datetime.datetime.utcnow(),
                 _id=None):
        self.post_id = post_id
        self.post_title = post_title
        self.post_content = post_content
        self.authorName = authorName
        self.author = author
        self.created_time = created_time
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='post', data=self.json())

    def json(self):
        return {'post_id': self.post_id,
                'post_title': self.post_title,
                'post_content': self.post_content,
                'authorName': self.authorName,
                'author': self.author,
                'created_time': self.created_time,
                '_id': self._id}

    @classmethod
    def from_mongo(cls, id):
        posts = Database.find_one(collection='post', query={'_id': id})
        return cls(**posts)

    @staticmethod
    def from_post(id):
        return [post for post in Database.find(collection='post', query={'post_id': id})]
