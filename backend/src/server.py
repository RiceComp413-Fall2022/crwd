from tokenize import String
from typing import List, Dict, Tuple
from flask import Flask
from flask_cors import CORS
from service import Service
import datetime
# from main import app

app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

@app.route('/getDummyData')
def get_data_route() -> List[Dict]:
    return service_obj.get_dummy_data()


@app.route('/')
def hello() -> String:
    return 'Hello, World!'


@app.route('/getCurrentStatus')
def get_curr_status_route():
    return service_obj.get_curr_status()


@app.route('/getAllData')
def get_all_data_route() -> Dict:
    return service_obj.get_all_data()


@app.route('/updateTotalDevices/<numDevices>')
def update_total_devices_route(numDevices):
    service_obj.update_total_devices(numDevices)


if __name__ == '__main__':
    date = datetime.date.today()
    opening_time = datetime.datetime(date.year, date.month, date.day, 8, 0, 0)
    service_obj = Service(opening_time)
    app.run()
