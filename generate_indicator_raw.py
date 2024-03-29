import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import os
from datetime import datetime
import yfinance as yf

class Data:
    def __init__(self):
        # Define the symbol for the VIX
        symbol = "^VIX"

        # Create a Ticker object 
        vix = yf.Ticker(symbol)

        # Retrieve the historical data
        self.vix = vix.history(period="15y")

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
            print("Insufficient data points for a 30-day rolling window.")
            self.vix['Indicator'] = np.nan
        else:
            min_periods = 30 * 5 // 7  # Adjust min_periods based on 5-day trading week

            # Define a custom function to fit the t-distribution within each rolling window
            def fit_t_distribution(window):
                if len(window.dropna()) < min_periods:
                    return np.nan  # Not enough data to fit the distribution
                else:
                    params = t.fit(window.dropna(), fscale=1)
                    dof, loc, scale = params
                    # Calculate the CDF for the last value in the window
                    return t.cdf(window.iloc[-1], dof, loc=loc, scale=scale)

            # Apply the custom function to each rolling window of the closing prices
            self.vix['Indicator'] = self.vix['Close'].rolling(window=30).apply(fit_t_distribution, raw=False)

        # Save the indicator values to a CSV file. Only include Date (index) and Indicator columns
        self.vix[['Indicator']].to_csv('data/vix_indicator_raw.csv')


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

    def plot_price_and_indicator(self, date_range):
        self.calculate_indicator()
        if not self.vix['Indicator'].isnull().all():  # Check if 'Indicator' is not all NaN
            fig, ax1 = plt.subplots(figsize=(18, 4))
            ax2 = ax1.twinx()

            # Filter data based on the specified date range
            if date_range == '3m':
                start_date = self.vix.index[-1] - pd.DateOffset(months=3)
            elif date_range == '6m':
                start_date = self.vix.index[-1] - pd.DateOffset(months=6)
            elif date_range == '1y':
                start_date = self.vix.index[-1] - pd.DateOffset(years=1)
            elif date_range == '3y':
                start_date = self.vix.index[-1] - pd.DateOffset(years=3)
            elif date_range == '10y':
                start_date = self.vix.index[-1] - pd.DateOffset(years=10)
            else:
                start_date = self.vix.index[0]

            filtered_data = self.vix.loc[start_date:]

            # Plot price
            ax1.plot(filtered_data.index, filtered_data['Close'], color='blue', label='Price')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('VIX', color='blue')
            ax1.tick_params('y', colors='blue')

            # Plot indicator
            ax2.plot(filtered_data.index, filtered_data['Indicator'], color='black', label='Indicator')
            ax2.set_ylabel('Indicator', color='black')
            ax2.tick_params('y', colors='black')

            # Set title and legend
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            plt.title(f"VIX and Cumulative Probability Indicator - {date_range.upper()} (Updated {current_time})")
            fig.legend(loc='upper left')

            # Create the "images" folder if it doesn't exist
            if not os.path.exists('images'):
                os.makedirs('images')

            # Save the plot as SVG and PNG files
            print(f"Saving plot for raw {date_range}...")
            plt.savefig(f'images/vix_indicator_{date_range}_r.svg', format='svg')

            plt.show()
        else:
            print("Indicator contains only NaN values.")

if __name__ == "__main__":
    data = Data()

    date_ranges = ['3m', '6m', '1y', '3y', '10y', 'max']
    for date_range in date_ranges:
        data.plot_price_and_indicator(date_range)