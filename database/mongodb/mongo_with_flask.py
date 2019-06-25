from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import pprint

app = Flask(__name__)

client = MongoClient("mongodb+srv://xidongc:chen19910531@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority")
db = client.blog
blogs = db.blogs

@app.route('/blogs', methods=['GET', 'POST'])
def blog():

    if request.method == "POST":
        data = request.json
        name = data.get('name', "Uname")
        created_by = data.get("created_by", "Anonymous")
        created_on = datetime.now().timestamp()

        result = blogs.insert_one({
            "name": name,
            "created_by": created_by,
            "created_on": created_on
        })

        pprint.pprint(result)

        response = {
            "msg": "Inserted successfully.",
            "obj_id": str(result.inserted_id)
        }

        return jsonify(response), 201

    elif request.method == 'GET':
        result = blogs.find({}, {'_id': 0})
        response = {
            'data': list(result)
        }
        return jsonify(response)

@app.route('/blogs/<blog_id>', methods=['GET'])
def single_blog(blog_id):
    result = blogs.find_one({'_id':ObjectId(blog_id)})
    result['_id'] = str(result['_id'])
    response = {
        'data': result
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
