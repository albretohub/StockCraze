#This module is for the yfinance  API that provides data for stock

import yfinance as yf
import pandas as pd
import time
from datetime import datetime
''''
    Period and interval to number conversion using the list index
'''

class StockDataHist:


    def __init__(self,ticker_symbol,period ,interval ):
        self.ticker_symbol = ticker_symbol
        self.period = period #values can be 1d, 5d, 1wk, 1mo, 3mo
        self.interval = interval# values can be 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        self.volume = None
        self.history_dataframe = None
        self.period_list = ['1d','5d','1wk','1mo','3mo']
        self.interval_list = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
        self.period_index = self.period_list.index(self.period)
        self.interval_index = self.interval_list.index(self.interval)
        self.FiftyWeekHigh = None
        self.FiftyWeekLow = None
        self.marketCap = None
        self.sector = None
        self.latest_data = None
        self.country = None
        self.companyName = None
        self.currentPrice = None
        self.TodayOnlyVolume = None
        self.status = None
    def load_data(self):
        if self.period_index > 0 and self.interval_index > 7:
            try:
                ''''
                    To access Volume data set the period at least 1week and interval at 1day,,,lesser cannot be access.
                '''
                ticker = yf.Ticker(self.ticker_symbol)
                historical_data = ticker.history(period=self.period,interval = self.interval,prepost = True)  # price data

                if historical_data.empty:
                    raise Exception
                else:
                    Initial_PriceData = pd.DataFrame(historical_data)
                    self.history_dataframe  = Initial_PriceData

            except Exception as e:
                print(f"Data Fetch Error: Check internet connection or the stock details")
            finally:
                print(f"Finish")
        else:
            try:
                ''''
                    To access Volume data set the period at least 1week and interval at 1day,,,lesser cannot be access.
                '''
                ticker = yf.Ticker(self.ticker_symbol)
                historical_data = ticker.history(period=self.period,interval = self.interval,prepost = True)  # price data

                if historical_data.empty:
                    raise Exception
                else:
                    Initial_PriceData = pd.DataFrame(historical_data)
                    self.history_dataframe = Initial_PriceData.drop('Volume',axis =1)#dropping the Volume column because it's empty

            except Exception as e:
                print(f"Data Fetch Error: Check internet connection or the stock details")
            finally:
                print(f"Finish")

    def auto_update_stock_data_incremental(self, interval="1m", duration_minutes=5):
        """
        Automatically fetch only new stock data every minute without re-downloading full day.

        Parameters:
            ticker (str): Stock ticker symbol (e.g., 'AAPL')
            interval (str): Data interval ('1m', '5m', etc.)
            duration_minutes (int): Total duration to update in minutes
        """

        end_time = time.time() + duration_minutes * 60
        latest_data = pd.DataFrame()  # store all fetched data
        last_timestamp = None  # track last fetched row

        stock = yf.Ticker(self.ticker_symbol)

        while time.time() < end_time:
            try:
                # Check market state
                info = stock.info
                market_state = info.get("marketState", "CLOSED").upper()
                is_active = market_state == "OPEN"

                # Fetch recent intraday data
                new_data = stock.history(period="1d", interval=interval)

                if new_data.empty:
                    print(f"{datetime.now()}: No new data available.")
                else:
                    df = new_data.reset_index()

                    # Filter only new rows
                    if last_timestamp is not None:
                        df = df[df['Datetime'] > last_timestamp]

                    if not df.empty:
                        latest_data = pd.concat([latest_data, df], ignore_index=True)
                        last_timestamp = df['Datetime'].max()
                        status = "ACTIVE" if is_active else "INACTIVE"
                        print(f"{datetime.now()}: Added {len(df)} new rows | Market Status: {status}")
                        print(latest_data.tail(1))  # show last 5 rows
                    else:
                        print(f"{datetime.now()}: No new rows since last update | Market Status: {'ACTIVE' if is_active else 'INACTIVE'}")

            except Exception as e:
                print(f"Error: {e}")

            time.sleep(60)  # wait 1 minute before next fetch

    def Stock_Info(self):
        try:
            ticker = yf.Ticker(self.ticker_symbol)
            self.FiftyWeekHigh = ticker.info.get("fiftyTwoWeekHigh", "N/A")
            self.FiftyWeekLow = ticker.info.get("fiftyTwoWeekLow", "N/A")
            self.marketCap = ticker.info['marketCap']
            self.sector = ticker.info['sector']
            self.country = ticker.info['country']
            self.companyName = ticker.info.get('shortName', 'N/A')
            self.currentPrice = ticker.info['currentPrice']
            self.TodayOnlyVolume  = ticker.info['volume']
            self.status = "Online"
        except Exception as e:
                print(f"Data Fetch Error: Check internet connection or the stock details")
                self.status = "Offline or Error"
        finally:
                print(f"Finish Stock_Info")

    def show(self):# this unit is for testing the output dataframe only
        # Display a summary of the fetched data
        #print("52weekHigh: "+ str(self.FiftyWeekHigh))
       # print("52weekLow: "+ str(self.FiftyWeekLow))
        #print("52weekLow: "+ str(self.marketCap))
       # print("52weekLow: "+ str(self.country))
       # print("52weekLow: "+ str(self.sector))
       # print(f"Summary of Historical Data for {self.ticker_symbol}:")
       # print("Current Price: "+str(self.currentPrice))
       # print("Today's Volume: "+str(self.TodayOnlyVolume))
        print(self.history_dataframe[['Open', 'High', 'Low', 'Close','Volume']])

#sample = StockDataHist("AAPL",'1d','1m')
#sample.load_data()
#sample.auto_update_stock_data_incremental('1m',5)
#sample.show()
