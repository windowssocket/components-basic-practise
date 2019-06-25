from pymongo import MongoClient
import pprint
import datetime

from pymongo.errors import ConnectionFailure

client = MongoClient("mongodb+srv://xidongc:chen19910531@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority")
db = client.test # create database

try:
    status = client.admin.command("serverStatus")
    # pprint.pprint(status)

except ConnectionFailure:
    print("Connection can not be established")

userCollection = client.blog.users
articleCollection = client.blog.articles

author = "ken"

ken = {
    "username": "ken",
    "password": "ken",
    "lang": "EN"
}

article = {
    "title": "my first post",
    "body": "the body",
    "author": author,
    "tags": ["ken", "general", "admin", "Oregon"],
    "posted": datetime.datetime.now()
}

userCollection.insert_one(ken)

if userCollection.find_one({"username": author}):
    document = articleCollection.insert_one(article)
    pprint.pprint(article)
else:
    raise ValueError("not found")

articleCollection.update_one({"author": "ken"}, {"$push": {
    "comments": [{"username": "mary",
                  "comment": "great"}]
}})


# userCollection.drop()
# articleCollection.drop()

