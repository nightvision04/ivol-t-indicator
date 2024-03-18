"""
In this module I want to pull in vix data, as well as fundamentals, and days of the week, 
weeks of the month etc to determine what are the best predictors of cycles for thhe vix. 
cycles in terms of day bars.

The vix data can be loaded from data/VIX.csv (contains the columns Date, Open, High, Low, Close, Adj Close, Volume).

Create a function that plots the vix data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        

    def get_vix(self):
        return self.vix

    def plot_vix(self):
        self.vix['Close'].plot()
        plt.show()

if __name__ == "__main__":
    data = Data()
    print(data.get_vix().head())
    data.plot_vix()

