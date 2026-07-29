import csv
import pandas as pd
import calendar as cal
from datetime import datetime as dt

class Stock_CSV():
    # Assumes that the csv file is in correct format for stock data ,
    # in future should be coded with open file dialog that only opens for csv file.
    # Converts tabulated data of csv into dataframe and series data
    def __init__(self,StockSymbol,StockName):
        #data variables
        self.date_data = None
        self.open_data = None
        self.high_data = None
        self.low_data = None
        self.close_data = None
        self.volume_data = None
        self.year_range =""
        self.formatted_dates = list()


        #file variables
        self.csv_file_Exist = False
        self.csv_file =None
        self.reader = None
        self.data_frame = None
        #self.csv_filename ='tesla.csv'# will be program later
        #self.csv_filename =str(StockName)+ '.csv'# will be program later
        self.csv_filename =str(StockName) #connected for database

    def load_data_csv(self):

        try:
            self.csv_file = open(self.csv_filename)
            self.reader = csv.reader(self.csv_file)
            self.csv_file_Exist = True

            #Cleaning the data frame..
            Columns = ("Date","Open","High","Low","Close","Volume")
            self.data_frame = pd.DataFrame(self.reader,columns=Columns)
            self.data_frame = self.data_frame.drop(index=0)
            self.data_frame = self.data_frame.reset_index(drop=True)

            #Loading all the data
            self.date_data = list(self.data_frame['Date'])
            self.open_data = list(self.data_frame['Open'].astype(float))
            self.high_data = list(self.data_frame['High'].astype(float))
            self.low_data = list(self.data_frame['Low'].astype(float))
            self.close_data = list(self.data_frame['Close'].astype(float))

            #Since volume data in csv is in string formatted with commas we need to convert it to float
            #by removing the commas and casting it to float.
            self.volume_raw_data = list(self.data_frame['Volume'])
            self.volume_data = list()
            for data in self.volume_raw_data:
                float_value = float(data.replace(",",""))
                self.volume_data.append(float_value)

        except Exception as e:
            print("Opening File error! "+ str(e))

    def reverse_data(self):
        # Reverse all entries in the list data for charting purposes..
        self.date_data = list(self.date_data)
        self.date_data.reverse()
        self.open_data  = list(self.open_data)
        self.open_data.reverse()
        self.high_data = list(self.high_data)
        self.high_data.reverse()
        self.low_data = list(self.low_data)
        self.low_data.reverse()
        self.close_data = list(self.close_data)
        self.close_data.reverse()
        self.volume_data = list(self.volume_data)
        self.volume_data.reverse()

    def print(self):
        print(self.data_frame)
        #print(self.date_data)
        #print(self.detect_date_format(self.date_data[0]))

    def detect_date_format(self,date_string):
        for fmt in("%m/%d/%y","%m/%d/%Y"):
            try:
                parsed =dt.strptime(date_string,fmt)
                return fmt
            except ValueError:
                continue
        return None



    def date_formatter(self):

        format = self.detect_date_format(self.date_data[0])

        date_str1 = dt.strptime(self.date_data[0],format)
        date_str2 = dt.strptime(self.date_data[len(self.date_data)-1],format)

        date_year1 = date_str1.year
        date_year2 = date_str2.year


        if(date_year2 == date_year1):
            self.year_range = date_year1
        else:
            self.year_range = str(date_year1) + "-"+ str(date_year2)


        for date in self.date_data:
            raw_date = dt.strptime(date,format)
            self.formatted_dates.append(raw_date.strftime('%b %d'))

        #self.formatted_dates.reverse()

        first_month = cal.month_abbr[dt.strptime(self.formatted_dates[0],'%b %d').month]
        second_month = None

        for date in self.formatted_dates:
            if first_month != cal.month_abbr[dt.strptime(date,'%b %d').month]:
                second_month = cal.month_abbr[dt.strptime(date,'%b %d').month]
                break

        i = 1 #place holder for the index of the second month in the list
        while i < len(self.formatted_dates)-1:
            day = None
            if first_month == cal.month_abbr[dt.strptime(self.formatted_dates[i],'%b %d').month]:
                self.formatted_dates[i] = str(dt.strptime(self.formatted_dates[i],'%b %d').day)
            else:
                i=i+1
                break
            i= i +1

        while i <= len(self.formatted_dates)-1:
            day = None
            if second_month == cal.month_abbr[dt.strptime(self.formatted_dates[i],'%b %d').month]:
                self.formatted_dates[i] = str(dt.strptime(self.formatted_dates[i],'%b %d').day)
            i= i +1



#CSV_Data = Stock_CSV('GOOG','tesla')
#CSV_Data.load_data_csv()
#CSV_Data.print()
