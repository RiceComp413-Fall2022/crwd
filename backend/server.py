from flask import Flask
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('.env')

CONNECTION_STRING = os.environ.get("CONNECTION_STRING")

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client['crwd']

@app.route('/getData')
def get_data():
    dbname = get_database()
    print(dbname)
    # Create a new collection
    collection_name = dbname['TestData']
    print(collection_name)
    jsn = []
    item_details = collection_name.find()
    print(item_details, ' item')
    for item in item_details:
        # This does not give a very readable output
        jsn.append(item)
    return jsn

# get_data()

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()