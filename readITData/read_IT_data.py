from typing import Optional, Tuple

import os
import time
import urllib.request
import base64
import gitlab
from dotenv import load_dotenv


def main():
    '''Read the data from IT and update the server, in a loop'''
    print('Running main() in read_IT_data.py')

    # Read .env file
    load_dotenv()
    GITLAB_URL = os.getenv('GITLAB_URL', '')
    GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', '')
    PROJECT_ID = os.getenv('PROJECT_ID', '')
    CSV_FILE_NAME = os.getenv('CSV_FILE_NAME', '')
    BACKEND_URL = os.getenv('BACKEND_URL', '')
    BACKEND_PASSWORD = os.getenv('BACKEND_PASSWORD', '')
    if '' in [BACKEND_URL, BACKEND_PASSWORD, GITLAB_URL, GITLAB_TOKEN, PROJECT_ID, CSV_FILE_NAME]:
        print('Missing environment variable. Check .env. Exiting.')
        return

    # Check backend connection
    print('Checking backend connection.')
    while not check_backend_connection(BACKEND_URL):
        print('Failed to connect to backend. Sleeping for 10 seconds.')
        time.sleep(10)

    # Run main loop: read from Gitlab, write to backend
    prev_time = ''
    while True:
        # Wait for a minute (besides the first iteration)
        if prev_time != '':
            time.sleep(60)
        # Read time and count from IT GitLab
        latest_IT_data = get_latest_IT_data(PROJECT_ID, GITLAB_URL, GITLAB_TOKEN, CSV_FILE_NAME)
        if latest_IT_data is None:
            print('Failed to read data from GitLab. Sleeping for 1 minute.')
            prev_time = 'N/A'
            continue
        new_time, count = latest_IT_data
        # Check if the data is new
        if new_time == prev_time:
            print('No new data. Sleeping for 1 minute.')
            continue
        # Report the data to the backend
        print(f'New data! Time: {new_time}, Count: {count}')
        report_to_backend(n_devices=count, backend_url=BACKEND_URL, password=BACKEND_PASSWORD)
        prev_time = new_time


#################################################
#            Read IT Data From GitLab           #
#################################################


def get_latest_IT_data(project_id: str, gitlab_url: str, gitlab_token: str, csv_file_name: str) -> Optional[Tuple[str, int]]:
    '''Returns the latest time and device count from the IT data on GitLab'''
    IT_data = read_IT_csv(project_id, gitlab_url, gitlab_token, csv_file_name)
    last_row = extract_last_row(IT_data)
    if last_row is None:
        return None
    time_count = extract_time_count(last_row)
    if time_count is None:
        return None
    return time_count


def read_IT_csv(project_id: str, gitlab_url: str, gitlab_token: str, csv_file_name: str) -> str:
    '''Read the csv data from IT in gitlab'''
    # Create gitlab instance
    gl = gitlab.Gitlab(url=gitlab_url, private_token=gitlab_token, ssl_verify=False)
    
    try:
        # Get the project
        project = gl.projects.get(project_id)
        print("Project: ", project.name)
        print("Gitlab URL: ", project.http_url_to_repo)

        # Get the file
        file = project.files.get(file_path=csv_file_name, ref='main')
        file_content = base64.b64decode(file.content).decode('utf-8')

        return file_content
    except:
        return ''


def extract_last_row(csv: str) -> Optional[str]:
    '''Return the last row of a csv string'''
    # Check for no data
    if len(csv) == 0:
        return None 
    # Remove blank line from end
    if csv[-1] == '\n':
        csv = csv[:-1]
    # Return last row
    rows = csv.split('\n')
    return rows[-1] if rows else None


def extract_time_count(csv_row: str) -> Optional[Tuple[str, int]]:
    '''Extracts a datetime and count from a csv row in the format: date,time,count'''
    columns = csv_row.split(',')
    if len(columns) != 3:
        return None
    
    date, time, device_count = columns
    # Combine date and time
    datetime = f'{date} {time}'
    # Convert device_count to a number
    device_count = int(device_count)
    return datetime, device_count

        
#################################################
#               Report to Backend               #
#################################################


def report_to_backend(n_devices: int, backend_url: str, password: str) -> None:
    '''Reports the given number of devices to the backend.'''
    print(f'Reporting device count ({n_devices}) to backend.')

    # Call endpoint on backend: updateTotalDevices/n/password
    request_url = f'{backend_url}/updateTotalDevices/{n_devices}/{password}'
    try:
        urllib.request.urlopen(request_url)
    except:
        print('Failed to report to backend. Check connection.')


def check_backend_connection(backend_url: str) -> bool:
    try:
        with urllib.request.urlopen(backend_url) as request:
            response = request.read().decode('UTF-8')
            print(f'Received message from server: {response}')
            return True
    except:
        return False


if __name__ == '__main__':
    main()
