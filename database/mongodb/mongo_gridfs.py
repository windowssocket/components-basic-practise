from pymongo import MongoClient
import gridfs
import bson.binary
import pprint

client = MongoClient("mongodb+srv://xidongc:chen19910531@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority")
db = client.blog
fs = gridfs.GridFS(db)

f = open("files/grid_test.txt", "rb")
content = bson.binary.Binary(f.read())
a = fs.put(content, filename="grid_test.txt", bar="test")
out = fs.get(a)
print(out.read())

files = fs.find()
for file in files:

    if file.filename == "grid_test.txt":
        with open(file.filename, 'wb') as f:
            # data = file.read()
            # f.write(data)
            print("### file.files ###")
            pprint.pprint(file.chunkSize)
            pprint.pprint(file.uploadDate)


print(out.filename)
print(out.bar)
db.binary.insert({'filename': 'files/grid_test.txt', 'data': content})

data = db.binary.find_one({"filename": "files/grid_test.txt"})

with open(data['filename'], "wb") as f:
    print(data['data'])
    f.write(data['data'])

client.close()
