from typing import List, Dict, Tuple
from flask import Flask
from flask_cors import CORS
import datetime

from src.service import Service
# from main import app

app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

@app.route('/getData')
def get_data_route() -> List[Tuple[str, int]]:
    return service_obj.get_data()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/getCurrentCrowd')
def get_curr_crowd_route():
    return service_obj.get_current_crowd()


@app.route('/getCrowd')
def get_crowd_route():
    return service_obj.get_crowd()


def run_server():
    global service_obj
    date = datetime.date.today()
    opening_time = datetime.datetime(date.year, date.month, date.day, 8, 0, 0)
    service_obj = Service(opening_time)
    app.run()


if __name__ == '__main__':
    run_server()
