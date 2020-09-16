from pymongo import MongoClient
from Analysis import Analysis
from flask import Flask, jsonify
from flask_cors import CORS
from bson.binary import UUIDLegacy as luuid


app = Flask(__name__)
CORS(app)

#connecting to DataBase
client = MongoClient(port=27017)
db = client.NewDB
col = db.Trips


@app.route('/')
def default():
    return 'Running on 127.0.0.1'


@app.route('/context', methods=['GET'])
def get_context():
    res = col.find_one({}) 
    ana = Analysis(res['cords'])
    context = ana.GetContexts()
    return jsonify(context)


@app.route('/speed', methods=['GET'])
def get_speed():
    res = col.find_one({}) 
    ana = Analysis(res['cords'])
    speed = ana.ReturnSpeed()
    return jsonify(speed)


@app.route('/time', methods=['GET'])
def get_time():
    res = col.find_one({})
    ana = Analysis(res['cords'])
    time = ana.ReturnRunStopTime()
    return jsonify(time)


@app.route('/trips', methods=['GET'])
def get_trips():
    res = col.find({})
    list_trips = []
    item = {}
    k = 0
    for i in res:
        k += 1
        item['id'] = i['_id']
        item['name'] = 'Trip ' + str(k)
        item['safetyscore'] = i['result']['safetyScore']
        list_trips.append(item)
        item = {}
    return jsonify(list_trips) 