from typing import List, Dict, Tuple

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date, datetime, timezone, timedelta
from pytz import timezone
import os

from src.service import Service

BACKUP_CSV_PATH = './backup.csv'

# Create app instance
app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

# Read .env file
load_dotenv()

# Read PASSKEY from environment
PASSKEY = os.getenv('PASSKEY')
if PASSKEY is None:
    print('No PASSKEY defined - check .env file. Exiting.')
    quit()

# Use US central timezone
TIMEZONE = timezone('US/Central')

# Create Service instance
date = date.today()
opening_time = datetime(date.year, date.month, date.day, 8, 0, 0)
service_obj = Service(opening_time, BACKUP_CSV_PATH, PASSKEY, TIMEZONE)
service_obj.restore_from_csv()  # Restore from backup


@app.route('/')
def hello() -> str:
    return 'Hello, World!'


@app.route('/getDummyData')
def get_data_route() -> List[Tuple[str, int]]:
    return service_obj.get_dummy_data()


@app.route('/getCurrentStatus')
def get_curr_status_route():
    return service_obj.get_curr_status()


@app.route('/getAllData')
def get_all_data_route() -> Dict:
    return service_obj.get_all_data()


@app.route('/getAllDataCSV')
def get_all_data_csv_route() -> str:
    return service_obj.get_csv_browser()


# TODO: remove this endpoint. For development / testing only.
@app.route('/updateTotalDevices/<numDevices>')
def comp_update_total_devices_route(numDevices) -> str:
    service_obj.update_total_devices_comp(numDevices)
    return 'update succeeded'


@app.route('/updateTotalDevices/<numDevices>/<passkey>')
def update_total_devices_route(numDevices, passkey) -> str:
    status = service_obj.update_total_devices(numDevices, passkey)
    return status


if __name__ == '__main__':
    app.run()
