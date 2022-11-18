from typing import Any, List, Dict, Optional, Tuple
import pandas as pd
from datetime import tzinfo, datetime, timedelta
import math
import os
from io import StringIO
import timeago

from src.backup import Backup
from src import dummy_data
from src import config

class Service:

    # The string format of datetimes stored in data
    STORED_DATETIME_FORMAT = '%m/%d/%Y %H:%M'

    # The string format of times stored in predicted_data
    STORED_TIME_FORMAT = '%H:%M'

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
        # Use default values for min/max count until they are calculated with calculate_min_max()
        self.min_count = 0
        self.max_count = 100


    #############################################
    #             API Entry-Points              #
    #############################################

    def get_daily_data(self, day_offset: int) -> Dict[str, Any]:
        '''
        Calculates historical and predicted percentages of how busy Chaus was/is during a given day.
        offset_days: a number describing the day-offset to calculate for.
            e.g. offset_days = 0 means "get data for today"
            e.g. offset_days = -1 means "get data for yesterday"
            e.g. offset_days = 1 means "get data for tomorrow"
        Returns: a dictionary with keys "historical," "predicted," and "msg" 
                 where "msg" is the date that the data is for
        '''
        today = datetime.now(self.timezone)
        target_date = today + timedelta(days = int(day_offset))
        datetime_to_perc = {}
        # Track previous count for smoothing
        last_date = last_count = None
        # Calculate historical data (only for today or earlier)
        if target_date.date() <= today.date():
            opening, closing = config.OPEN_HOURS[target_date.weekday()]
            prev = None
            for date_str, count in self.data:
                date = datetime.strptime(date_str, self.STORED_DATETIME_FORMAT)
                if date.date() == target_date.date():
                    # Only show data from when chaus is open
                    if date.time() >= opening.time() and date.time() <= closing.time():
                        # Calculate a "smoothed" value as the average of current and previous value
                        if prev:
                            smooth = (count + prev) / 2
                        else:
                            smooth = count
                        prev = count
                        last_date = date_str
                        last_count = count
                        datetime_to_perc[date_str] = self.convert_count_to_percent(smooth)
            if last_date and last_count:
                datetime_to_perc[last_date] = self.convert_count_to_percent(last_count)

        predicted_data = self.get_predicted_data(target_date, last_date, last_count)
        # Create a message with the date that the data is calculated for
        msg = f'{target_date.strftime("%A, %B")} {target_date.day}'
        return {'historical' : datetime_to_perc, 'predicted' : predicted_data, 'msg': msg}

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
            last_update_time = datetime.strptime(formatted_time, self.STORED_DATETIME_FORMAT)
            # Remove timezone info for comparison (required by timeago)
            current_time = datetime.now(self.timezone).replace(tzinfo=None)
            time_ago_message = timeago.format(last_update_time, current_time)

            perc = self.convert_count_to_percent(count)
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
            # Use red background
            background_color = '#E0785F'

            # get the current time
            today = datetime.now(self.timezone)
            opening_today = config.OPEN_HOURS[today.weekday()][0]
            # Before opening time today -> return the opening time
            if today.time() < opening_today.time():
                message2 = f'Chaus opens at {opening_today.time().strftime("%-I:%M %p")}'
            else:
                # After closing time today -> return the opening time opening time for the next day (weekday % 6) + 1
                opening_tmrw = config.OPEN_HOURS[(today.weekday() % 6) + 1][0]
                message2 = f'Chaus opens at {opening_tmrw.time().strftime("%-I:%M %p")} tomorrow'
        return {
            'msg1': message1,
            'msg2': message2,
            'backgroundColor': background_color,
            'textColor': text_color
        }

    def update_total_devices(self, num_devices: int, passkey: str) -> str:
        '''Saves an updated value for the number of devices'''
        if passkey != os.getenv('PASSKEY'):
            return 'update failed'
        time = datetime.now(self.timezone).strftime(self.STORED_DATETIME_FORMAT)
        pair = (time, int(num_devices))
        self.data.append(pair)
        self.save_to_backup()
        return 'update succeeded'
    
    
    #############################################
    #               Predictions                 #
    #############################################

    def get_predicted_data(self, date: datetime, last_date_str, last_count) -> Dict[str, float]:
        '''
        Creates a list of percentages of how busy Chaus was at every minute from now to close based on predictions.
        '''
        now = datetime.now(self.timezone)   # For current time
        opening, closing = config.OPEN_HOURS[date.weekday()]
        datetime_to_perc = {}
        # No predictions for past days
        if date.date() < now.date():
            return {}
        predicted_data = self.calculate_predicted_data(date.weekday())
        today = datetime.now(self.timezone)
        if date.date() >= today.date():
            # Use the last observed value as first predicted value
            if date.date() == now.date() and date.time() >= opening.time() and date.time() <= closing.time():
                datetime_to_perc[last_date_str] = self.convert_count_to_percent(last_count)
            # Use values from predicted data from now until closing
            for time_str, count in predicted_data:
                # Extract time from formatted string
                time = datetime.strptime(time_str, self.STORED_TIME_FORMAT).time()
                # Use (today's date) + (time from prediction)
                prediction_datetime = date.replace(hour=time.hour, minute=time.minute, second=0)
                # Filter for times between now and closing time
                if (date.date() > now.date() or time >= now.time()) and time >= opening.time() and time <= closing.time():
                    # Create string with today's date + time from prediction
                    prediction_datetime_str = prediction_datetime.strftime(self.STORED_DATETIME_FORMAT)
                    datetime_to_perc[prediction_datetime_str] = self.convert_count_to_percent(count)
        return datetime_to_perc 

    def calculate_predicted_data(self, weekday) -> List[Tuple[str, int]]:
        '''
        Calculates predicted (time, count) pairs from historical data. 
        The result is stored in self.predicted_data.
        Note: the times are formatted such as "08:30" and do not contain dates
        '''
        print('Calculating predicted data.')
        # Convert all data to dataframe
        df = pd.DataFrame(self.data, columns=['datetime', 'count'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        #df = df.set_index('datetime')
        # Filter dataframe to only include data from specified day
        df = df.set_index('datetime')
        df = df.reset_index()
        df = df[df['datetime'].dt.dayofweek == weekday]
        df = df.set_index('datetime')
        # Convert time to 30-minute intervals
        df_by_30_min = pd.DataFrame(df['count'].resample('30 min').mean())
        # Filter for times after 6am
        df_by_30_min = df_by_30_min.loc[df_by_30_min.index.to_series().dt.hour > 6]
        # Extract the time from the datetime
        df_by_30_min['time'] = df_by_30_min.index.to_series().dt.time
        # Find the mean time per 30-minute interval
        summary_df = df_by_30_min.groupby('time').mean()
        # Use a string (e.g. '08:30') to represent the time
        summary_df = summary_df.set_index(summary_df.index.to_series().astype(str).str.slice(0, 5))
        # Return list of (time_string, count) pairs
        return list(summary_df.itertuples(name=None))


    #############################################
    #            Backup / Restore               #
    #############################################

    def save_to_backup(self) -> None:
        '''Saves all data to a backup'''
        print(f"Backing up data.")
        # Save to csv
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
        print(f'Found {len(self.data)} values in backup.')
        
        # Filter data for only past 30 days
        min_date = (datetime.now(self.timezone) - timedelta(days = 30)).date()
        self.data = [
            (date_str, count) 
            for date_str, count in self.data 
            if datetime.strptime(date_str, self.STORED_DATETIME_FORMAT).date() > min_date
        ]
        print(f'Using {len(self.data)} values from backup from the last 30 days.')

        # Perform required actions after data is loaded
        self.calculate_chaus_capacity()


    #############################################
    #         Capacity Calculations              #
    #############################################

    def calculate_chaus_capacity(self) -> None:
        '''
        Calculates a statistical minimum and maximum counts from the data.
            e.g. if the data typically lies between 10 and 130, this function will compute min_count = 10, max_count = 130.
        The function saves the results to self.min_count and self.max_count, respectively.
        '''
        # Get all counts from the past (when chaus is open)
        all_crowd_values = []
        for date_str, count in self.data:
            date = datetime.strptime(date_str, self.STORED_DATETIME_FORMAT)
            opening, closing = config.OPEN_HOURS[date.weekday()]
            if date.time() >= opening.time() and date.time() <= closing.time():
                all_crowd_values.append(count)

        # Get the 99th percentile as the max value and the 1st percentile as the min value
        percentile1 = int(0.01 * len(all_crowd_values))
        percentile99 = int(0.99 * len(all_crowd_values))
        all_crowd_values.sort()
        self.min_count, self.max_count = all_crowd_values[percentile1], all_crowd_values[percentile99]
        print(f'Calculated min_count = {self.min_count}, max_count = {self.max_count}.')
    
    def convert_count_to_percent(self, count) -> int:
        '''Converts a device count (e.g. 60 devices) to a percent (e.g. 30% full)'''
        # Calculate the percentage using the pre-calculated min/max
        percent = int(((count - self.min_count) / (self.max_count - self.min_count)) * 100)
        # Bound the percentage within [0, 100]
        if percent < 0:
            return 0
        if percent > 100:
            return 100
        return percent


    #############################################
    #          Shared helper functions          #
    #############################################

    def is_chaus_open(self) -> bool:
        '''Returns true if chaus is currently open, false otherwise'''
        today = datetime.now(self.timezone)
        opening = config.OPEN_HOURS[today.weekday()][0]
        closing = config.OPEN_HOURS[today.weekday()][1]
        return today.time() >= opening.time() and today.time() <= closing.time()


    #############################################
    #    Dummy Data (for testing/debugging)     #
    #############################################

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