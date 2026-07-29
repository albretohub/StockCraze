
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QTabWidget
from UI.UI_ChartingTab import MainChart
from UI.UI_VolumeDate_Chart import MainChart2
from UI.UI_OpenHighLowClose_Charting import MainChart3
from Auxilliary.StockData_CSV import Stock_CSV
from Auxilliary.Database_Interface1 import Data_Interface
from datetime import datetime as dt
import calendar as cal


class MainChartingWindow(QWidget):
    def __init__(self,StockSymbol,StockName):
        super().__init__()
        self.setWindowTitle("Charting Volume Vs Date")
        self.StockSymbol = StockSymbol
        self.StockName = StockName
        self.formatted_dates = list()


        #CSV_Data = Stock_CSV(StockSymbol,StockName)
        #CSV_Data.load_data_csv()
       # CSV_Data.reverse_data()
        #CSV_Data.date_formatter()

        database = Data_Interface(StockSymbol,StockName) # To be program with exception handling module befor charting commence
        data_frame = database.SelectAll()

        #data variables coupled with CSV data
        #self.date_data = CSV_Data.formatted_dates
        #self.open_data = CSV_Data.open_data
        #self.high_data = CSV_Data.high_data
        #self.low_data = CSV_Data.low_data
        #self.close_data =CSV_Data.close_data
        #self.volume_data = CSV_Data.volume_data
        #self.years = str(CSV_Data.year_range)

        self.date_data = data_frame['Date']
        self.open_data = data_frame['Open']
        self.high_data = data_frame['High']
        self.low_data = data_frame['Low']
        self.close_data =data_frame['Close']
        self.volume_data = data_frame['Volume']
        self.year_range = None

        self.reverse_data()
        self.date_formatter()



        self.sub_tabs = QTabWidget()
        self.sub_tabs.setTabPosition(QTabWidget.North)
        self.sub_tabs.setMovable(True)
        self.sub_tabs.addTab(MainChart(StockSymbol,StockName,self.formatted_dates,self.close_data,self.year_range),QIcon("Source Images/chart-up.png"),"Close/Date")
        self.sub_tabs.addTab(MainChart2(StockSymbol,StockName,self.formatted_dates,self.volume_data,self.year_range),QIcon("Source Images/chart-up.png"),"Volume/Date")
        self.sub_tabs.addTab(MainChart3(StockSymbol,StockName,self.formatted_dates,self.open_data,self.high_data,self.low_data,self.close_data
                                        ,self.year_range), QIcon("Source Images/chart-up.png"),"Open/High/Low/Close")



        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.sub_tabs)
        self.setLayout(self.layout1)

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

    def detect_date_format(self,date_string):
        for fmt in("%m/%d/%y","%m/%d/%Y"):
            try:
                parsed =dt.strptime(date_string,fmt)
                return fmt
            except ValueError:
                continue
        return None

    def date_formatter(self):#Charting All Data

        format = '%b/%d/%y'
        print(format)

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
            self.formatted_dates.append(raw_date.strftime('%m/%d'))


