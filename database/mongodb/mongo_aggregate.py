from mongod import Mongod
import datetime

conn = Mongod()

articleCollection = conn.db.articles

# aggregate eg: $sum, $first, $avg
l = [
    {"$match": {"posted": {"$lt": datetime.datetime.now()}}},
    {"$group": {"_id": "$title", "num": {"$sum": 1}}},
    {"$limit": 3},
    {'$project': {"_id": 0}}
]

cursor = articleCollection.aggregate(l)
for i in cursor:
    print(i)
