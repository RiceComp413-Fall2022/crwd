from typing import List, Dict, Tuple

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date, datetime, timezone, timedelta
from pytz import timezone
import os

from src.backup import Backup
from src.service import Service
from src import config

BACKUP_CSV_PATH = './backup.csv'

# Create app instance
app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

# Read .env file
load_dotenv()

# Read PASSKEY from environment
PASSKEY = os.getenv('PASSKEY', '')
if PASSKEY is None:
    print('No PASSKEY defined - check .env file. Exiting.')
    quit()

# Read GitHub credentials from environment
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN', '')
GIST_ID = os.getenv('GIST_ID', '')
if '' in [GITHUB_ACCESS_TOKEN, GITHUB_ACCESS_TOKEN]:
    print('Github credentials not defined.')
    print('Check .env for GITHUB_ACCESS_TOKEN and GIST_ID. Exiting.')
    quit()

# Create Backup instance
chaus_backup = Backup(GITHUB_ACCESS_TOKEN, GIST_ID, 'chaus.csv')
audreys_backup = Backup(GITHUB_ACCESS_TOKEN, GIST_ID, 'audreys.csv')
brochstein_backup = Backup(GITHUB_ACCESS_TOKEN, GIST_ID, 'brochstein.csv')

# Use US central timezone
TIMEZONE = timezone('US/Central')

# Create Service instance
date = date.today()
opening_time = datetime(date.year, date.month, date.day, 8, 0, 0)
chaus_service_obj = Service(chaus_backup, PASSKEY, config.CHAUS_OPEN_HOURS, TIMEZONE)
audreys_service_obj = Service(audreys_backup, PASSKEY, config.AUDREYS_OPEN_HOURS, TIMEZONE)
broch_service_obj = Service(brochstein_backup, PASSKEY, config.BROCHSTEIN_OPEN_HOURS, TIMEZONE)

# Map location name to Service
location_name_to_service = {'chaus': chaus_service_obj, 'audreys': audreys_service_obj, 'brochstein': broch_service_obj}

# different updates
chaus_service_obj.restore_from_backup()  # Restore from backup
audreys_service_obj.restore_from_backup()
broch_service_obj.restore_from_backup()

@app.route('/')
def hello() -> str:
    return 'Hello, World!'


@app.route('/getCurrentStatus/<location>')
def get_curr_status_route(location) -> Dict:
    if location not in location_name_to_service:
        return {
            'msg': 'N/A',
            'updatedMsg': 'N/A',
            'backgroundColor': 'white',
            'textColor': 'black'
        }
    return location_name_to_service[location].get_curr_status()


@app.route('/getDailyData/<location>/<offset>')
def get_daily_data_route(offset, location) -> Dict:
    if location not in location_name_to_service:
        return {}
    return location_name_to_service[location].get_daily_data(offset)


@app.route('/updateTotalDevices/<location>/<numDevices>/<passkey>')
def update_total_devices_route(numDevices, passkey, location) -> str:
    if location not in location_name_to_service:
        return 'ERROR: Location not recognized.'
    status = location_name_to_service[location].update_total_devices(numDevices, passkey)
    return status


@app.route('/getDummyData')
def get_data_route() -> List[Tuple[str, int]]:
    return chaus_service_obj.get_dummy_data()


if __name__ == '__main__':
    app.run()
