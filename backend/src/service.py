from typing import List, Dict, Tuple
import pandas as pd
from datetime import datetime
import math

from src import dummy_data

class Service:
    def __init__(self, opening_time: datetime):
        self.capacity = 102
        self.opening_time = opening_time
        self.data = []


    def get_dummy_data(self) -> List[Tuple[str, int]]:
        '''
        Sets the global data variable by generating dummy data.
        '''
        curr_time = datetime.now()
        diff = curr_time - self.opening_time
        # calc how many minutes have passed since opening
        num_minutes = math.ceil(diff.total_seconds() / 60)
        minutes_between_values = 30
        num_values = math.ceil(num_minutes / minutes_between_values)
        # get a crowd value for each minute
        people_data = dummy_data.generate_dummy_data(num_values, minutes_between_values, initial_n_devices=50)
        return people_data


    def get_all_data(self) -> Dict[str, float]:
        '''
        Creates a list of percentages of how busy Chaus was at every minute from opening to now.
        '''
        data = self.data if len(self.data) != 0 else self.get_dummy_data()
        datetime_to_perc = {tup[0]: tup[1]/ self.capacity * 100 for tup in data}
        return datetime_to_perc


    def get_curr_status(self):
        '''
        Returns a message that indicates how busy Chaus is at the moment.
        '''
        current_crowd = self.data[len(self.data) - 1][1]
        perc = current_crowd/self.capacity * 100
        time = self.data[len(self.data) - 1][0]
        message = ''
        if perc > 90:
            message = 'Chaus is super busy!'
        elif perc > 60:
            message = 'Chaus is busy!'
        elif perc > 30:
            message = 'Now is a good time to go to Chaus!'
        else:
            message = 'Chaus is empty!'
        return {'msg': message, 'perc': perc, 'time': time}


    def update_total_devices(self, num_devices) -> None:
        time = datetime.now()
        pair = (time.strftime("%d/%m/%Y %H:%M"), int(num_devices))
        self.data.append(pair)
        return
