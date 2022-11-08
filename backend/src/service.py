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
        '''Returns dummy data for testing.'''
        curr_time = datetime.now()
        diff = curr_time - self.opening_time
        # calc how many minutes have passed since opening
        num_minutes = math.ceil(diff.total_seconds() / 60)
        minutes_between_values = 30
        num_values = math.ceil(num_minutes / minutes_between_values)
        # get a crowd value for each minute
        people_data = dummy_data.generate_dummy_data(num_values, minutes_between_values, initial_n_devices=50)
        return people_data


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


    def get_curr_status(self) -> Dict[str, Any]:
        '''Returns messages indicating how busy Chaus is at the moment.'''
        # Handle no data
        if len(self.data) == 0:
            return {'msg': 'No data yet.', 'perc': 0.0, 'time': 'N/A'}

        # Default to white text
        text_color = 'white'

        if self.is_chaus_open():
            # Chaus is open -> msg1: "Chaus is X% busy", msg2: "Updated Y ago"
            # Get last value
            formatted_time, count = self.data[-1]

            # Convert time to "time ago" (e.g. "3 minutes ago")
            last_update_time = datetime.strptime(formatted_time, self.STORED_DATE_FORMAT)
            # Remove timezone info for comparison (required by timeago)
            current_time = datetime.now(self.timezone).replace(tzinfo=None)
            time_ago_message = timeago.format(last_update_time, current_time)

            perc = int(count / config.MAX_CAPACITY * 100)
            if perc > 90:
                background_color = '#322620' #bistro
            elif perc > 60:
                background_color = '#50392F' #dark liver horses
            elif perc > 30:
                background_color = '#6D4C3D' #coffee
            else:
                background_color = '#A58B7A' #beaver
                text_color = 'black'
            message1 = f'Chaus is {perc}% full'
            message2 = f'Updated {time_ago_message}'
        else:
            # Chaus is closed -> msg1: "chaus is closed!", msg2: "Chaus will open at X"
            message1 = 'Chaus is closed!'
            # Use grey background
            background_color = '#C1C1C1'
            # get the current time
            today = datetime.now(self.timezone)
            opening_today = config.OPEN_HOURS[today.weekday()][0]
            # Before opening time today -> return the opening time
            if today.time() < opening_today.time():
                message2 = f'Chaus will open at {opening_today.time()}'
            else:
                # After closing time today -> return the opening time opening time for the next day (weekday % 6) + 1
                opening_tmrw = config.OPEN_HOURS[(today.weekday() % 6) + 1][0]
                message2 = f'Chaus will open at {opening_tmrw.time()} tomorrow'
        return {
            'msg1': message1,
            'msg2': message2,
            'backgroundColor': background_color,
            'textColor': text_color
        }


    def is_chaus_open(self) -> bool:
        '''Returns true if chaus is currently open, false otherwise'''
        today = datetime.now(self.timezone)
        opening = config.OPEN_HOURS[today.weekday()][0]
        closing = config.OPEN_HOURS[today.weekday()][1]
        return today.time() >= opening.time() and today.time() <= closing.time()


    def update_total_devices(self, num_devices: int, passkey: str) -> str:
        '''Saves an updated value for the number of devices'''
        if passkey != os.getenv('PASSKEY'):
            return 'update failed'
        time = datetime.now(self.timezone).strftime(self.STORED_DATE_FORMAT)
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.save_to_backup()
        return 'update succeeded'


    def save_to_backup(self) -> None:
        '''Saves all data to a backup'''
        print(f"Backing up data.")
        dataframe = pd.DataFrame(self.data, columns=['datetime', 'count'])
        csv_string = dataframe.to_csv(index=False)
        self.backup.save(csv_string)


    def restore_from_backup(self) -> None:
        '''Restores the contents of self.data from a backup'''
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
