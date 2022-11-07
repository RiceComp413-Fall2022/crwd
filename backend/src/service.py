from typing import Any, List, Dict, Optional, Tuple
import pandas as pd
from datetime import tzinfo, datetime
import math
import os
from io import StringIO
import timeago

from src.backup import Backup
from src import dummy_data
from src import config

class Service:

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
        Creates a list of percentages of how busy Chaus was at every minute.
        '''
        datetime_to_perc = { 
            date: round(count / config.MAX_CAPACITY * 100, 1) 
            for date, count in self.data
        }
        return datetime_to_perc
    
    def get_daily_data(self) -> Dict[str, float]:
        '''
        Creates a list of percentages of how busy Chaus was at every minute from opening to now.
        '''
        today = datetime.now(self.timezone)
        opening = config.OPEN_HOURS[today.weekday()][0]
        closing = config.OPEN_HOURS[today.weekday()][1]
        datetime_to_perc = {}
        for date, count in self.data:
            formatted = datetime.strptime(date, '%m/%d/%Y %H:%M')
            if formatted.date() == today.date():
                if formatted.time() >= opening.time() and formatted.time() <= closing.time():
                    datetime_to_perc[date] = round(count / config.MAX_CAPACITY * 100, 1)
        return datetime_to_perc


    def chaus_is_open(self) -> str:
        today = datetime.now(self.timezone)
        opening = config.OPEN_HOURS[today.weekday()][0]
        closing = config.OPEN_HOURS[today.weekday()][1]
        if today.time() >= opening.time() and today.time() <= closing.time():
            return 'true'
        return 'false'


    def get_curr_status(self) -> Dict[str, Any]:
        '''
        Returns a message that indicates how busy Chaus is at the moment.
        '''
        # Handle no data
        if len(self.data) == 0:
            return {'msg': 'No data yet.', 'perc': 0.0, 'time': 'N/A'}

        # Get last value
        formatted_time, count = self.data[-1]

        # Convert time to "time ago" (e.g. "3 minutes ago")
        last_update_time = datetime.strptime(formatted_time, self.STORED_DATE_FORMAT)
        # Remove timezone info for comparison (required by timeago)
        current_time = datetime.now(self.timezone).replace(tzinfo=None)
        time_ago_message = timeago.format(last_update_time, current_time)

        perc = int(count / config.MAX_CAPACITY * 100)
        if perc > 90:
            backgroundcolor = '#E0785F'
            textcolor = 'white'
        elif perc > 60:
            backgroundcolor = '#FCA44D'
            textcolor = '#741B47'
        elif perc > 30:
            backgroundcolor = '#FFD45E'
            textcolor = '#073763'
        else:
            backgroundcolor = '#81B29A'
            textcolor = 'white'
        message = 'Chaus is ' + str(perc) + '% full'
        return {'msg': message, 'perc': perc, 'time': time_ago_message, 'backgroundcolor': backgroundcolor, 'textcolor': textcolor}


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
