import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import os

import yfinance as yf



class Data:
    def __init__(self):
        #self.vix = pd.read_csv('data/VIX.csv')

        # Define the symbol for the VIX
        symbol = "^VIX"

        # Create a Ticker object
        vix = yf.Ticker(symbol)

        # Retrieve the historical data
        self.vix = vix.history(period="max")

        self.vix

        # self.vix['Date'] = pd.to_datetime(self.vix['Date'])
        # self.vix.set_index('Date', inplace=True)
        self.vix = self.vix.sort_index()
        self.vix['CloseLog'] = np.log(self.vix['Close'])
        self.vix['Day'] = self.vix.index.dayofweek
        self.vix['Week'] = self.vix.index.isocalendar().week
        self.vix['Month'] = self.vix.index.month
        self.vix['Year'] = self.vix.index.year
        self.vix['DayName'] = self.vix.index.day_name()
        self.vix['MonthName'] = self.vix.index.month_name()
        self.vix['Weekday'] = self.vix.index.weekday
        self.vix['WeekofMonth'] = self.vix.index.day // 7 + 1

    def get_vix(self):
        return self.vix

    def plot_vix(self, week_of_month=None):
        self.vix['CloseLog'].plot()
        if week_of_month is not None:
            vlines = self.vix[self.vix['WeekofMonth'] == week_of_month].index
            plt.vlines(vlines, ymin=self.vix['CloseLog'].min(), ymax=self.vix['CloseLog'].max(), colors='r', linestyles='dashed')
        plt.yscale('log')
        plt.show()

    def calculate_indicator(self):
        print(f"Length of self.vix: {len(self.vix)}")
        print(f"Number of duplicate index values: {self.vix.index.duplicated().sum()}")

        if len(self.vix) < 30:
            print("Insufficient data points for 30-day rolling average.")
            self.vix['Indicator'] = np.nan
        else:
            min_periods = 30 * 5 // 7  # Adjust min_periods based on 5-day trading week
            rolling_avg_30 = self.vix['Close'].rolling(window=30, min_periods=min_periods).mean().dropna()
            print(f"30-day rolling average shape: {rolling_avg_30.shape}")

            if not rolling_avg_30.empty:
                params = t.fit(rolling_avg_30, fscale=1)
                dof = params[0]
                self.vix['Indicator'] = rolling_avg_30.apply(lambda x: t.cdf(x, dof, loc=params[1], scale=params[2])) 
            else:
                print("30-day rolling average is empty.")
                self.vix['Indicator'] = np.nan

    def plot_indicator(self):
        self.calculate_indicator()
        if not self.vix['Indicator'].isnull().all():  # Check if 'Indicator' is not all NaN
            self.vix['Indicator'].plot()
            plt.title("Cumulative Probability Indicator")
            plt.show()

            # Assertions to verify the indicator values
            assert self.vix['Indicator'].min() >= 0
            assert self.vix['Indicator'].max() <= 1
        else:
            print("Indicator contains only NaN values.")

    def plot_price_and_indicator(self):
        self.calculate_indicator()
        if not self.vix['Indicator'].isnull().all():  # Check if 'Indicator' is not all NaN
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            # Plot price
            ax1.plot(self.vix.index, self.vix['Close'], color='blue', label='Price')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Price', color='blue')
            ax1.tick_params('y', colors='blue')

            # Plot indicator
            ax2.plot(self.vix.index, self.vix['Indicator'], color='red', label='Indicator')
            ax2.set_ylabel('Indicator', color='red')
            ax2.tick_params('y', colors='red')

            # Set title and legend
            plt.title("Price and Cumulative Probability Indicator")
            fig.legend(loc='upper left')

            # Create the "images" folder if it doesn't exist
            if not os.path.exists('images'):
                os.makedirs('images')

            # Save the plot as SVG and PNG files
            plt.savefig('images/vix_indicator.svg', format='svg')
            plt.savefig('images/vix_indicator.png', format='png')

            plt.show()
        else:
            print("Indicator contains only NaN values.")

if __name__ == "__main__":
    data = Data()
    print(data.get_vix().head())
    print(data.vix['Close'].head())
    print(data.vix['Close'].isnull().sum())
    #data.plot_vix(week_of_month=2)
    #data.plot_indicator()
    data.plot_price_and_indicator()