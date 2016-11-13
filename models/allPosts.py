import uuid
import datetime
from common.database import Database
from models.post import Post


class AllPosts(object):
    def __init__(self, authorName, author, title, description, author_id, _id=None):
        self.authorName = authorName
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {'authorName': self.authorName,
                'author': self.author,
                'author_id': self.author_id,
                'title': self.title,
                'description': self.description,
                '_id': self._id}

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(post_id=self._id,
                    post_title=title,
                    post_content=content,
                    authorName=self.authorName,
                    author=self.author,
                    created_time=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_post(self._id)

    @classmethod
    def from_mongo(cls, id):
        post = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post)

    @classmethod
    def get_post_from_author_id(cls, author_id):
        posts = Database.find(collection='posts', query={'author_id': author_id})
        return [cls(**post) for post in posts]
