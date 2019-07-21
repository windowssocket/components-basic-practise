from pymongo import MongoClient, GEO2D
import pprint
from bson.son import SON  #Serialized Ocument Notation to_dict()

client = MongoClient("mongodb+srv://xidongc:chen19910531@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority")
db = client.blog
db.places.delete_many({})
db.places.create_index([("loc", GEO2D)])

results = db.places.insert_many([{"loc": [2, 5]},
                                   {"loc": [30, 5]},
                                   {"loc": [1, 2]},
                                   {"loc": [4, 4]}])
print(results.inserted_ids)

for doc in db.places.find({"loc": {"$near": [3, 6]}}).limit(3):
    pprint.pprint(doc)

query = {"loc": {"$within": {"$box": [[2, 2], [5, 6]]}}}
for doc in db.places.find(query).sort('_id'):
    pprint.pprint(doc)

command = SON([('geoNear', 'places'), ('near', [1, 2])])
result = db.command(command)
pprint.pprint(result)



