from typing import List, Dict, Tuple

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date, datetime, timezone, timedelta
from pytz import timezone
import os

from src.backup import Backup
from src.service import Service

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
service_obj = Service(opening_time, chaus_backup, PASSKEY, TIMEZONE)
service_obj.restore_from_backup()  # Restore from backup


@app.route('/')
def hello() -> str:
    return 'Hello, World!'


@app.route('/getCurrentStatus')
def get_curr_status_route():
    return service_obj.get_curr_status()


@app.route('/getDailyData/<offset>')
def get_daily_data_route(offset) -> Dict:
    return service_obj.get_daily_data(offset)


@app.route('/updateTotalDevices/<numDevices>/<passkey>')
def update_total_devices_route(numDevices, passkey) -> str:
    status = service_obj.update_total_devices(numDevices, passkey)
    return status


@app.route('/getDummyData')
def get_data_route() -> List[Tuple[str, int]]:
    return service_obj.get_dummy_data()


if __name__ == '__main__':
    app.run()
