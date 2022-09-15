from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv
import json
import certifi

app = Flask(__name__)
CORS(app) # Allow Cross-Origin Resource Sharing

load_dotenv('.env')

CONNECTION_STRING = os.environ.get("CONNECTION_STRING")

def get_database():
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    return client['crwd']

@app.route('/getData')
def get_data():
    db = get_database()
    # get the collection
    collection = db.get_collection("TestData")
    documents = collection.find()
    jsns = [] # list of json objects representing the documents
    for i in range(3):
        for document in documents:
            jsn = {}        
            for key in document:
                if key != '_id':
                    jsn[key] = document[key]
            jsns.append(jsn)
    return jsns

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()