from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.regex import Regex
import re

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flaskmongo

clubs = db.clubs

@app.route('/', methods=['GET'])
def index():
    query = {}
    if "search" in request.args:
        if request.args["search"] != '':
            query = { **query, "$or" : [ 
                                        { "name" : { "$regex" : Regex(request.args["search"]).pattern, "$options" : "i" } },
                                        { "city" : { "$regex" : Regex(request.args["search"]).pattern, "$options" : "i" }  },
                                        { "country" : { "$regex" : Regex(request.args["search"]).pattern, "$options" : "i" } },
                                        { "stadium" : { "$regex" : Regex(request.args["search"]).pattern, "$options" : "i" } }
                                       ] 
                    }
    limit = 10
    if "limit" in request.args:
        if not re.search('[a-zA-Z]+', request.args["limit"]) and re.search('[0-9]+', request.args["limit"]):
            limit = int(request.args["limit"])
        if "last_id" in request.args:
            query = { **query, "_id" : { "$gt" : ObjectId(request.args["last_id"]) } }
    get_data = clubs.find(query).sort("_id", 1).limit(limit)
    count = len(list(get_data.clone()))
    if count == 0:
        return jsonify({
            'error' : True,
            'messages' : 'Data not found'
        })
    response_data = { 'data' : [], 'last_id' : str(get_data[count - 1]["_id"]), 'count' : count }
    for data in get_data:
        data["_id"] = str(data["_id"])
        response_data["data"].append(data)
    return jsonify(response_data)

app.run('127.0.0.1', port=8000, debug=True)