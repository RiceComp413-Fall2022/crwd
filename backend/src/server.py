from typing import List, Dict
from flask import Flask
from flask_cors import CORS
from service import Service
import datetime
# from main import app

app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

@app.route('/getData')
def get_data_route() -> List[Dict]:
    return service_obj.get_dummy_data()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/getCurrentCrowd')
def get_curr_crowd_route():
    return service_obj.get_crowd_message()


@app.route('/getCrowd')
def get_crowd_route():
    return service_obj.get_crowd_perc()


@app.route('/updateTotalDevices/<numDevices>')
def update_total_devices_route(numDevices):
    service_obj.update_total_devices(numDevices)
    return service_obj.data


if __name__ == '__main__':
    date = datetime.date.today()
    opening_time = datetime.datetime(date.year, date.month, date.day, 8, 0, 0)
    service_obj = Service(opening_time)
    app.run()