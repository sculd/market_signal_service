import pymongo, urllib
import json, os, ssl
from google.cloud import pubsub_v1
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')
from threading import Thread

_MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
_MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')
_MONGO_DB_PASSWORD = urllib.parse.quote(_MONGO_DB_PASSWORD)

# mongodb+srv://<username>:<password>@market-signal-lcay1.gcp.mongodb.net/test?retryWrites=true&w=majority
_ATLAS_CONNECTION_STRING = 'mongodb+srv://{username}:{password}@market-signal-lcay1.gcp.mongodb.net/test?retryWrites=true&w=majority'.format(username=_MONGO_DB_USERNAME, password=_MONGO_DB_PASSWORD)

_DATABASE_ID = 'crypto_signal'
_COLLECTION_ID = 'crypto_signal'

_client = pymongo.MongoClient(_ATLAS_CONNECTION_STRING, ssl_cert_reqs=ssl.CERT_NONE)

collection = _client[_DATABASE_ID][_COLLECTION_ID]

signal = {
    "symbol": 'btcusd',
    "time": 1589080139,
    "price": 8636.16,
    "change_window_minutes": 60,
    "change_threshold": 0.05,
    "change": 0.06
}

collection.insert_many([signal])

