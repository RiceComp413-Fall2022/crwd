from typing import List, Dict
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv
import json
import certifi

app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

# Load the Database URI from .env
load_dotenv('.env')
DATABASE_URI = os.environ.get("CONNECTION_STRING")

def get_database():
    tlsCAFile = certifi.where()
    print(f"[INFO] Using TLS CA File: {tlsCAFile}")
    client = MongoClient(DATABASE_URI, tlsCAFile=tlsCAFile)
    return client['crwd']

@app.route('/getData')
def get_data():
    # Check for the database uri
    if DATABASE_URI is None:
        print(f"[ERROR] No connection string!")
        return []
    db = get_database()
    # Get the collection
    collection = db.get_collection("TestData")
    documents = collection.find()
    # Convert each document to JSON
    json_documents: List[Dict] = []
    for document in documents:
        jsn = {}        
        for key in document:
            if key != '_id':
                jsn[key] = document[key]
        json_documents.append(jsn)
    return json_documents

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()