from typing import Any, List, Dict, Optional, Tuple
import pandas as pd
from datetime import tzinfo, datetime
import math
import os
from io import StringIO

from src.backup import Backup
from src import dummy_data

class Service:

    CHAUS_CAPACITY = 102
    STORED_DATE_FORMAT = '%m/%d/%Y %H:%M'

    def __init__(self, 
                 opening_time: datetime, 
                 backup: Backup, 
                 passkey: str, 
                 timezone: Optional[tzinfo] = None):
        self.opening_time = opening_time
        self.data: List[Tuple[str, int]] = []
        self.backup = backup
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

        # Get last value
        formatted_time, count = self.data[-1]

        # Reformat time as AM/PM
        time = datetime.strptime(formatted_time, self.STORED_DATE_FORMAT)
        formatted_time = time.strftime('%-I:%M %p on %m/%d/%Y')

        perc = round(count / self.CHAUS_CAPACITY * 100, 1)
        if perc > 90:
            message = 'Chaus is super busy!'
        elif perc > 60:
            message = 'Chaus is busy!'
        elif perc > 30:
            message = 'Now is a good time to go to Chaus!'
        else:
            message = 'Chaus is empty!'

        return {'msg': message, 'perc': perc, 'time': formatted_time}


    def update_total_devices_comp(self, num_devices: int) -> None:
        time = datetime.now().strftime(self.STORED_DATE_FORMAT)
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.save_to_backup()
        return
    

    def update_total_devices(self, num_devices: int, passkey: str) -> str:
        if passkey != os.getenv('PASSKEY'):
            return 'update failed'
        time = datetime.now(self.timezone).strftime(self.STORED_DATE_FORMAT)
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.save_to_backup()
        return 'update succeeded'
    

    def save_to_backup(self) -> None:
        '''Backup all data.'''
        print(f"Backing up data.")
        dataframe = pd.DataFrame(self.data, columns=['datetime', 'count'])
        csv_string = dataframe.to_csv(index=False)
        self.backup.save(csv_string)


    def restore_from_backup(self) -> None:
        '''Restore the contents of self.data from a backup'''
        print("Restoring data from backup.")
        try:
            backup_str = self.backup.restore()
        except:
            print("Error: Failed to restore from backup.")
            return

        try:
            # Convert string to IO for pandas to read
            backup_str_io = StringIO(backup_str)
            dataframe = pd.read_csv(
                backup_str_io,
                dtype={'datetime': str, 'count': int}
            )
        except:
            print("Error: Failed to read backup as csv.")
            return

        # Convert the data frame to a list
        self.data = list(dataframe.itertuples(index=False, name=None))
        print(f'Restored {len(self.data)} values from backup.')
