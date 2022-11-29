from typing import Dict, Optional, Tuple

import os
import time
import urllib.request
import base64
import gitlab

try:
    import config
except ImportError:
    print('Missing config.py. Exiting.')
    exit()


def main():
    '''Read the data from IT and update the server, in a loop'''
    print('Running main() in read_IT_data.py')

    # Check backend connection
    print('Checking backend connection.')
    while not check_backend_connection(config.BACKEND_URL):
        print('Failed to connect to backend. Sleeping for 10 seconds.')
        time.sleep(10)

    # Run main loop: read from Gitlab, write to backend
    prev_time = None
    while True:
        # Wait for a minute (besides the first iteration)
        if prev_time is not None:
            time.sleep(60)
        # Read times and counts from IT GitLab
        latest_IT_data = get_latest_IT_data(config.PROJECT_ID, config.GITLAB_URL, config.GITLAB_TOKEN, config.LOCATION_TO_FILENAME)
        if not latest_IT_data:
            print('Failed to read data from GitLab. Sleeping for 1 minute.')
            prev_time = ''
            continue
        new_time, _ = list(latest_IT_data.values())[0]
        # Check if the data is new
        if new_time == prev_time:
            print('No new data. Sleeping for 1 minute.')
            continue
        # Report the data to the backend
        print(f'New data! {latest_IT_data}')
        report_to_backend(latest_IT_data, backend_url=config.BACKEND_URL, password=config.BACKEND_PASSWORD)
        prev_time = new_time


#################################################
#            Read IT Data From GitLab           #
#################################################


def get_latest_IT_data(
    project_id: str, 
    gitlab_url: str, 
    gitlab_token: str, 
    location_to_filename: Dict[str,str]) -> Dict[str, Tuple[str, int]]:
    '''Returns the latest time and device count from the IT data on GitLab for each provided location'''
    result: Dict[str, Tuple[str, int]] = {}
    # Get data for each location
    for location_name, filename in location_to_filename.items():
        data = get_latest_IT_data_single_location(project_id, gitlab_url, gitlab_token, filename)
        if data:
            result[location_name] = data
    return result


def get_latest_IT_data_single_location(
    project_id: str,
    gitlab_url: str, 
    gitlab_token: str,
    csv_file_name: str) -> Optional[Tuple[str, int]]:
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

def report_to_backend(location_to_data: Dict[str, Tuple[str, int]], backend_url: str, password: str) -> None:
    '''Reports the given number of devices to the backend.'''
    print(f'Reporting data to backend.')
    for location, data in location_to_data.items():
        _, count = data
        report_single_count_to_backend(location, count, backend_url, password)


def report_single_count_to_backend(location_name: str, n_devices: int, backend_url: str, password: str) -> None:
    '''Reports the given number of devices to the backend.'''
    print(f'Reporting {n_devices} devices at {location_name} to backend.')

    # Call endpoint on backend: updateCount/location_name/n/password
    request_url = f'{backend_url}/updateCount/{location_name}/{n_devices}/{password}'
    print(f'Making request to: {request_url}')
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
