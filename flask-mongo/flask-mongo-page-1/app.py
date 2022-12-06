from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flaskmongo

clubs = db.clubs

@app.route('/', methods=['POST','GET'])
def create_or_index():
    if request.method == 'POST':
        getjson = request.get_json(silent=True)
        data_insert = clubs.insert_one({
            'name' : getjson["name"],
            'city' : getjson["city"],
            'country' : getjson["country"],
            'stadium' : getjson["stadium"]
        })
        get_data = clubs.find_one({ "_id" : data_insert.inserted_id })
        get_data["_id"] = str(get_data["_id"]) # convert ObjectId Type to String Type Class
        return jsonify(get_data)
    else:
        get_data = clubs.find()
        collect_data = []
        for data in get_data:
            data["_id"] = str(data["_id"]) # convert ObjectId Type to String Type Class
            collect_data.append(data)
        return jsonify(collect_data)

@app.route('/<id>', methods=['POST', 'GET', 'DELETE'])
def view_edit_delete(id, args=None):
    if request.method == 'POST':
        getjson = request.get_json(silent=True)
        clubs.update_one({ "_id" : ObjectId(id) }, {
            "$set" : {
                'name' : getjson["name"],
                'city' : getjson["city"],
                'country' : getjson["country"],
                'stadium' : getjson["stadium"]
            }
        })
        return jsonify({
            'error' : False,
            'messages' : 'Success Edit Data'
        })
    elif request.method == 'GET':
        get_data = clubs.find_one({ "_id" : ObjectId(id) })
        get_data["_id"] = str(get_data["_id"]) # convert ObjectId Type to String Type Class
        return jsonify(get_data)
    else:
        clubs.delete_one({ "_id" : ObjectId(id) })
        return jsonify({
            'error' : False,
            'messages' : 'Success Delete Data'
        })

app.run('127.0.0.1', port=8000, debug=True)