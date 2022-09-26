from tokenize import String
from typing import List, Dict
import dummy_data
import pandas as pd
import datetime
import math

class Service:
    def __init__(self, opening_time):
        self.capacity = 102
        self.opening_time = opening_time
        self.data = self.get_data()


    def get_data(self) -> List[Dict]:
        '''
        Sets the global data variable by generating dummy data.
        '''
        curr_time = datetime.datetime.now()
        diff = curr_time - self.opening_time
        # calc how many minutes have passed since opening
        num_values = math.ceil(diff.total_seconds() / 60)
        # get a crowd value for each minute
        people_data = dummy_data.generate_dummy_data(num_values, 1, initial_n_devices=50)
        return people_data
        

    def get_crowd(self) -> List[float]:
        '''
        Creates a list of percentages of how busy Chaus was at every minute from opening to now.
        '''
        df = pd.DataFrame(self.data, columns =['DateTime', 'NumPeople'])
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['CrowdPercentage'] = df['NumPeople'] / self.capacity * 100
        return list(df['CrowdPercentage'])


    def get_current_crowd(self) -> String:
        '''
        Returns a message that indicates how busy Chaus is at the moment.
        '''
        current_crowd = self.data[len(self.data) - 1][1]
        perc = current_crowd/self.capacity * 100
        message = ''
        if perc > 90:
            message = 'Chaus is super busy!'
        elif perc > 60:
            message = 'Chaus is busy!'
        elif perc > 30:
            message = 'Now is a good time to go to Chaus!'
        else:
            message = 'Chaus is empty!'
        return message