from pymongo import MongoClient
from Analysis import Analysis


client = MongoClient(port=27017)
db = client.NewDB
col = db.Trips
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


# k = 0
# for i in range(10):
#     print('yoo '+ str(k))
#     k += 1