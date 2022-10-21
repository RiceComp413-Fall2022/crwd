import urllib.request

BACKEND_URL = 'http://chaus-crowd.herokuapp.com'

def check_backend_connection() -> bool:
    try:
        with urllib.request.urlopen(BACKEND_URL) as request:
            response = request.read().decode('UTF-8')
            print(f'Received message from server: {response}')
            return True
    except:
        return False


def report_n_devices(nDevices, password):
    '''Reports the given number of devices to the backend.'''
    print(f'Reporting nDevices ({nDevices}) to backend.')

    # Call endpoint on backend: updateTotalDevices/n/password
    request_url = f'{BACKEND_URL}/updateTotalDevices/{nDevices}/{password}'
    try:
        urllib.request.urlopen(request_url)
    except:
        print('Failed to report to backend. Check connection.')
