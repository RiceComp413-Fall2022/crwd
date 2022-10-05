from typing import Tuple, List
from datetime import datetime, timedelta
from random import gauss

def generate_dummy_data(n_rows, interval_minutes, initial_n_devices=50) -> List[Tuple[str, int]]:
    '''
    Creates a list of (time, n_devices) values where n_devices is randomly generated.
    - n_rows the number of values generated.
    - interval_minutes the number of minutes between generated values
    - initial_n_devices (optional) the initial value of n_devices,
                        which is randomly incremented/decremented at each time step.
    '''
    start_time = datetime.now()
    n_devices = initial_n_devices
    result = []
    # Start at the time furthest in the past and word towards the present
    for i in range(n_rows - 1, -1, -1):
        time = start_time - timedelta(minutes=i*interval_minutes)
        # Add a random value to n_devices and prevent negatives
        n_devices = max(0, n_devices + round(gauss(0, 10)))
        pair = (time.strftime("%m/%d/%Y %H:%M"), n_devices)
        result.append(pair)
    
    return result
