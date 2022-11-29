#!/usr/bin/env python

from datetime import datetime

# map numeric representation of the weekday to (opening, closing) times
# use Jan. 1, 2022 as a temp date
CHAUS_OPEN_HOURS = {0 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              1 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              2 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              3 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              4 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 17, 0, 0)),
              5 : (datetime(2022, 1, 1, 9, 30, 0), datetime(2022, 1, 1, 17, 0, 0)),
              6 : (datetime(2022, 1, 1, 14, 0, 0), datetime(2022, 1, 1, 23, 59, 59))}

# need to update
AUDREYS_OPEN_HOURS = {0 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              1 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              2 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              3 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 23, 59, 59)),
              4 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 17, 0, 0)),
              5 : (datetime(2022, 1, 1, 9, 30, 0), datetime(2022, 1, 1, 17, 0, 0)),
              6 : (datetime(2022, 1, 1, 14, 0, 0), datetime(2022, 1, 1, 23, 59, 59))}

BROCHSTEIN_OPEN_HOURS = {0 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 19, 0, 0)),
              1 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 19, 0, 0)),
              2 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 19, 0, 0)),
              3 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 19, 0, 0)),
              4 : (datetime(2022, 1, 1, 7, 30, 0), datetime(2022, 1, 1, 19, 0, 0)),
              5 : (datetime(2022, 1, 1, 9, 0, 0), datetime(2022, 1, 1, 17, 0, 0)),
              6 : (datetime(2022, 1, 1, 9, 0, 0), datetime(2022, 1, 1, 17, 0, 0))}


