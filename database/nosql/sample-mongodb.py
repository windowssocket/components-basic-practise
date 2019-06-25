import pymongo
from pymongo import MongoClient


class SampleMongodb(object):

    def __init__(self):
        self.client = None

    def createclient(self):
        self.client = MongoClient('localhost', 27017)

    def insert_data(self):
        db = self.client['pymongo_test']
        posts = db.posts
        post1 = {
            'name': 'helloworld application',
            'author': 'xidong',
            'content': 'helloworld application description'
        }
        post2 = {
            'name': 'helloworld application',
            'author': 'xidong'
        }
        post3 = {
            'name': 'helloworld application',
            'content': 'helloworld application description'
        }
        result = posts.insert_many([post1, post2, post3])
        print("insert success {}".format(result.inserted_ids))

    def search_data(self):
        db = self.client['pymongo_test']
        posts = db.posts
        xidong_posts = posts.find({'author': 'xidong'})
        print([post for post in xidong_posts])



s = SampleMongodb()
s.createclient()
s.insert_data()
s.search_data()
