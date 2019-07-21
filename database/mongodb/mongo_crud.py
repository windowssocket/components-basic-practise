from mongod import Mongod
import datetime
import pprint
from bson.json_util import dumps
import json
from pymongo import ASCENDING, TEXT

conn = Mongod()
userCollection = conn.db.users
articleCollection = conn.db.articles
moviesCollection = conn.db.movies

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

movies = [{
   "title": 'Fight Club',
   "directed_by": 'David Fincher',
   "stars": ['Brad Pitt', 'Edward Norton', 'Helena Bonham Carter'],
   "tags": 'drama',
   "debut": datetime.datetime(1991, 10, 15),
   "likes": 224360,
   "dislikes": 40127,
   "comments": [
      {
         "user": 'user3',
         "message": 'My first comment',
         "dateCreated": datetime.datetime(2008, 9, 13),
         "like": 0
      },
      {
         "user": 'user2',
         "message": "My first comment too!",
         "dateCreated": datetime.datetime(2003, 10, 11),
         "like": 14
      },
      {
         "user": 'user7',
         "message": 'Good Movie!',
         "dateCreated": datetime.datetime(2009, 10, 11),
         "like": 2
      }
   ]
}, {
   "title": "Seven",
   "directed_by": 'David Fincher',
   "stars": ['Morgan Freeman', 'Brad Pitt',  'Kevin Spacey'],
   "tags": ['drama', 'mystery', 'thiller'],
   "debut": datetime.datetime(1995, 9, 22),
   "likes": 134370,
   "dislikes": 1037,
   "comments": [
      {
         "user": 'user3',
         "message": 'Love Kevin Spacey',
         "dateCreated": datetime.datetime(2002, 9, 13),
         "like": 0
      },
      {
         "user": 'user2',
         "message": 'Good works!',
         "dateCreated": datetime.datetime(2013, 10, 21),
         "like": 14
      },
      {
         "user": 'user7',
         "message": 'Good Movie!',
         "dateCreated": datetime.datetime(2009, 10, 11),
         "like": 2
      }
   ]
}]

# insert/create
userCollection.insert_one(ken)  # insert one
moviesCollection.insert_many(movies)  # insert many

# query
cursor = moviesCollection.find({'directed_by': 'David Fincher'})
cursor.limit(3)
# other please refer # cursor.skip(2); # cursor.sort([('dataCreated', -1)])

# load result using bson
result = dumps(cursor)
# convert string to json
result = json.loads(result)

# wrapped part of result into json obj
retData = []
for r in result:
    tmp = dict()
    tmp['title'] = r['title']
    tmp['stars'] = r['stars']
    retData.append(tmp)

# bson string
j_obj = json.dumps(retData)

# verify json  json refer: https://pythonspot.com/json-encoding-and-decoding-with-python/
result = json.loads(j_obj)
for r in result:
    for k, v in r.items():
        print(k + "--->" + str(v))

# projector {'id' not shown in final results}
cursor = userCollection.find_one({"username": author}, {'_id': 0})

pprint.pprint(cursor)
print(cursor['username'] + "->" + cursor['password'])

# query with multiple
# and
cursor = moviesCollection.find({"directed_by": "David Fincher", "stars": "Morgan Freeman"})
for c in cursor:
    pprint.pprint(c)

# or
cursor = moviesCollection.find({
  "$or": [{'stars': 'Robin Wright'},
          {'stars': 'Morgan Freeman'}]
})
for c in cursor:
    pprint.pprint(c)

# incline func， others refer: $lt, $ne, $lte ...
cursor = moviesCollection.find({'likes': {'$gt': 500000}})
for c in cursor:
    pprint.pprint(c)

# insert record
if userCollection.find_one({"username": author}):
    document = articleCollection.insert_one(article)
    pprint.pprint(article)
else:
    raise ValueError("not found")

# update record
moviesCollection.update({'title': 'Seven'},
                        {'$inc': {'like': 2}}
                        )

# multi doc update:
# https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update
moviesCollection.update({'title': 'Seven'}, {"$push": {'tags': ['popular', 'great']}}, multi=True)

# replace
moviesCollection.update({'title': 'Seven'}, {'$set': {'dislikes': 134371}})

# delete
moviesCollection.remove({'tags': 'romance'})

# create index
moviesCollection.create_index([("directed_by", ASCENDING)])

# create txt index
moviesCollection.create_index([("title", TEXT)])

# get index
result = moviesCollection.list_indexes()
for r in result:
    pprint.pprint(r)

# use text index search
result = moviesCollection.find({"$text": {"$search": "Fight"}})
for r in result:
    pprint.pprint(r)

# delete index
moviesCollection.drop_index("directed_by_1")

# drop collection
userCollection.drop()
articleCollection.drop()
moviesCollection.drop()
