from typing import Any, List, Dict, Optional, Tuple
import pandas as pd
from datetime import tzinfo, datetime
import math
import os

from src import dummy_data

class Service:

    CHAUS_CAPACITY = 102

    def __init__(self, 
                 opening_time: datetime, 
                 backup_csv_path: str, 
                 passkey: str, 
                 timezone: Optional[tzinfo] = None):
        self.opening_time = opening_time
        self.data: List[Tuple[str, int]] = []
        self.backup_csv_path = backup_csv_path
        self.passkey = passkey
        self.timezone = timezone


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
        datetime_to_perc = { 
            date: round(count / self.CHAUS_CAPACITY * 100, 1) 
            for date, count in self.data
        }
        return datetime_to_perc


    def get_curr_status(self) -> Dict[str, Any]:
        '''
        Returns a message that indicates how busy Chaus is at the moment.
        '''
        # Handle no data
        if len(self.data) == 0:
            return {'msg': 'No data yet.', 'perc': 0.0, 'time': 'N/A'}

        current_crowd = self.data[-1][1]
        perc = current_crowd / self.CHAUS_CAPACITY * 100
        time = self.data[len(self.data) - 1][0]
        if perc > 90:
            message = 'Chaus is super busy!'
        elif perc > 60:
            message = 'Chaus is busy!'
        elif perc > 30:
            message = 'Now is a good time to go to Chaus!'
        else:
            message = 'Chaus is empty!'

        return {'msg': message, 'perc': perc, 'time': time}


    def update_total_devices_comp(self, num_devices: int) -> None:
        time = datetime.now().strftime("%m/%d/%Y %H:%M")
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.backup_to_csv(time, num_devices)
        return
    

    def update_total_devices(self, num_devices: int, passkey: str) -> str:
        if passkey != os.getenv('PASSKEY'):
            return 'update failed'
        time = datetime.now(self.timezone).strftime("%m/%d/%Y %H:%M")
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.backup_to_csv(time, num_devices)
        return 'update succeeded'
    

    def get_csv(self) -> str:
        '''Convert the data to a csv string'''
        dataframe = pd.DataFrame(self.data, columns=['datetime', 'count'])
        return dataframe.to_csv(index=False)
    

    def get_csv_browser(self) -> str:
        '''Convert the data to a csv string that will display correctly in a browser'''
        # Use <br> as the line terminator to display correctly in browser
        return self.get_csv().replace('\n', '<br>')
    

    def backup_to_csv(self, time: str, count: int) -> None:
        '''Backup one value to a local CSV file'''
        print(f"Backing up ({time}, {count}) to csv")
        dataframe = pd.DataFrame([(time, count)])
        dataframe.to_csv(self.backup_csv_path, mode='a', index=False, header=False)


    def restore_from_csv(self) -> None:
        '''Restore the contents of self.data from a local CSV file'''
        print("Restoring data from csv")
        try:
            dataframe = pd.read_csv(self.backup_csv_path, header=None)
        except FileNotFoundError:
            print("Warning: No backup file found.")
            return

        data_list = list(dataframe.itertuples(index=False, name=None))
        self.data = data_list
