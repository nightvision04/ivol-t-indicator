"""
In this module I want to pull in vix data, as well as fundamentals, and days of the week, 
weeks of the month etc to determine what are the best predictors of cycles for thhe vix. 
cycles in terms of day bars.

The vix data can be loaded from data/VIX.csv (contains the columns Date, Open, High, Low, Close, Adj Close, Volume).
"""

import pandas as pd
import numpy as np

class Data:
"""
This class loads the data and provides methods to access the data.
"""

    def __init__(self):
        self.vix = pd.read_csv('data/VIX.csv')
        self.vix['Date'] = pd.to_datetime(self.vix['Date'])
        self.vix.set_index('Date', inplace=True)
        self.vix = self.vix.sort_index()
        self.vix['Day'] = self.vix.index.dayofweek
        self.vix['Week'] = self.vix.index.week
        self.vix['Month'] = self.vix.index.month
        self.vix['Year'] = self.vix.index.year
        self.vix['DayName'] = self.vix.index.day_name()
        self.vix['MonthName'] = self.vix.index.month_name()
        self.vix['Weekday'] = self.vix.index.weekday
        self.vix['WeekdayName'] = self.vix.index.weekday_name
        self.vix['Weekday'] = self.vix.index.weekday
        self.vix['WeekdayName'] = self.vix.index.weekday_name
        self.vix['WeekNumber'] = self.vix.index.week
        self.vix['DayOfYear'] = self.vix.index.dayofyear
        self.vix['DayOfMonth'] = self.vix.index.day
        self.vix['DayOfWeek'] = self.vix.index.dayofweek
        self.vix['DayOfWeekName'] = self.vix.index.day_name()

    def get_vix(self):
        return self.vix

