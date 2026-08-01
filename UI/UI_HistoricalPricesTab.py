import datetime
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from Auxilliary.StockData_Historical import StockDataHist as sd
from Auxilliary.StockData_CSV import Stock_CSV
from Auxilliary.Database_Interface1 import Data_Interface as di

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
    def rowCount(self, index):
        return self._data.shape[0]
    def columnCount(self, index):
        return self._data.shape[1]
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
class HistoricalPrice_Tab(QWidget):# data fetched online using yfinance module via Stockdata_Historical.py file
    def __init__(self,StockSymbol,StockName):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName
        self.table = QtWidgets.QTableView()
        self.label = QLabel()
        self.data_frame = None

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(1)

        self.layout1 = QVBoxLayout()#layout for the table
        self.layout2 = QVBoxLayout()#layout for the stats

        self.layout1 = QVBoxLayout()#layout for the table
        self.layout2 = QVBoxLayout()#layout for the stats

        self.TitleStats = QLabel("  QuickStats")
        self.TitleStats.setFont(QFont("Arial",30,10,False))
        self.TitleStats.setStyleSheet("qproperty-alignment: AlignCenter; background-color: Green; color: Yellow")

        self.NumEntriesLabel = QLabel()
        self.NumEntriesLabel.setFont(QFont("Arial",12))
        self.NumEntriesLabel.setStyleSheet("qproperty-alignment: AlignCenter; background-color: grey")
        self.NumEntries = None

        self.DateRangeLabel =  QLabel()
        self.DateRangeLabel.setFont(QFont("Arial",12))
        self.DateRangeLabel.setStyleSheet("qproperty-alignment: AlignCenter; background-color: grey; font: white")

        self.HighestClosingPringrice = QLabel()
        self.HighestClosingPringrice.setFont(QFont("Arial",10))
        self.HighestClosingPringrice.setStyleSheet("qproperty-alignment: AlignCenter; background-color: White; font:Bold")

        self.LowestClosingPrice = QLabel()
        self.LowestClosingPrice.setFont(QFont("Arial",10))
        self.LowestClosingPrice.setStyleSheet("qproperty-alignment: AlignCenter; background-color: Red; font:Bold")

        self.HighestVolume = QLabel()
        self.HighestVolume.setFont(QFont("Arial",10))
        self.HighestVolume.setStyleSheet("qproperty-alignment: AlignCenter; background-color: white; font:Bold")

        self.LowestVolume = QLabel()
        self.LowestVolume.setFont(QFont("Arial",10))
        self.LowestVolume.setStyleSheet("qproperty-alignment: AlignCenter; background-color: red; font:Bold")

        self.OpenAv = QLabel()
        self.OpenAv.setFont(QFont("Arial",10))
        self.OpenAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.HighAv = QLabel()
        self.HighAv.setFont(QFont("Arial",10))
        self.HighAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.LowAv = QLabel()
        self.LowAv.setFont(QFont("Arial",10))
        self.LowAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.CloseAv = QLabel()
        self.CloseAv.setFont(QFont("Arial",10))
        self.CloseAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.VolumeAv = QLabel()
        self.VolumeAv.setFont(QFont("Arial",10))
        self.VolumeAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")


        try:
            data = sd(self.StockSymbol,'1mo','1d')
            data.load_data()
            data.show()
            data = data.history_dataframe.drop('Dividends',axis =1)
            data = data.drop('Stock Splits',axis =1)
            indexes = data.index.strftime("%B %d,%Y")
            data.index = indexes
            data = data.round(4)
            self.data_frame = data
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.layout1.addWidget(self.table)
            print("Helo")

        except Exception as e:
            print("Importing data error! "+ str(e))
            self.label.setText("data not found ")
            self.layout1.addWidget(self.label)

        self.layout2.addWidget(self.TitleStats)
        self.NumEntries = len(self.data_frame)
        self.NumEntriesLabel.setText("Number of Entries: "+str(self.NumEntries))
        self.layout2.addWidget(self.NumEntriesLabel)

        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)
        #self.setLayout(self.layout1)


class HistoricalPrice_Tab_CSV(QWidget):# data fetched online using CSV files downloaded
    def __init__(self,StockSymbol,StockName):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName
        self.table = QtWidgets.QTableView()
        self.csv_file_Exist = False
        self.reader = None
        self.data_frame = None

        self.AddToDatabase_button= QPushButton("Export to Database")
        self.label = QLabel()

        self.main_layout = QHBoxLayout()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.AddToDatabase_button)

        csv_filename = str(StockName)+ '.csv'


        try:
            CSV_Data = Stock_CSV(StockSymbol,StockName)
            CSV_Data.load_data_csv()
            self.data_frame = CSV_Data.data_frame
            self.csv_file_Exist = CSV_Data.csv_file_Exist
            #print( self.data_frame)

            if self.csv_file_Exist:
                self.model = TableModel(self.data_frame)
                self.table.setModel(self.model)
                self.layout1.addWidget(self.table)
            else:
                raise Exception

        except Exception as e:
            print("Opening File error! "+ str(e))
            self.label.setText("CSV File not found ")
            self.layout1.addWidget(self.label)

        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)

class HistoricalPrice_Tab_Database(QWidget):# data fetched using data from database
    def __init__(self,StockSymbol,StockName):#retrive all data available.
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName
        self.table = QtWidgets.QTableView()
        self.table.setFixedSize(800,700)
        self.month = None
        self.year = None
        self.data_frame = None

        self.label = QLabel()

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(1)

        self.layout1 = QVBoxLayout()#layout for the table
        self.layout2 = QVBoxLayout()#layout for the stats

        self.TitleStats = QLabel("  QuickStats")
        self.TitleStats.setFont(QFont("Arial",30,10,False))
        self.TitleStats.setStyleSheet("qproperty-alignment: AlignCenter; background-color: Green; color: Yellow")

        self.NumEntriesLabel = QLabel()
        self.NumEntriesLabel.setFont(QFont("Arial",12))
        self.NumEntriesLabel.setStyleSheet("qproperty-alignment: AlignCenter; background-color: grey")
        self.NumEntries = None

        self.DateRangeLabel =  QLabel()
        self.DateRangeLabel.setFont(QFont("Arial",12))
        self.DateRangeLabel.setStyleSheet("qproperty-alignment: AlignCenter; background-color: grey; font: white")

        self.HighestClosingPringrice = QLabel()
        self.HighestClosingPringrice.setFont(QFont("Arial",10))
        self.HighestClosingPringrice.setStyleSheet("qproperty-alignment: AlignCenter; background-color: White; font:Bold")

        self.LowestClosingPrice = QLabel()
        self.LowestClosingPrice.setFont(QFont("Arial",10))
        self.LowestClosingPrice.setStyleSheet("qproperty-alignment: AlignCenter; background-color: Red; font:Bold")

        self.HighestVolume = QLabel()
        self.HighestVolume.setFont(QFont("Arial",10))
        self.HighestVolume.setStyleSheet("qproperty-alignment: AlignCenter; background-color: white; font:Bold")

        self.LowestVolume = QLabel()
        self.LowestVolume.setFont(QFont("Arial",10))
        self.LowestVolume.setStyleSheet("qproperty-alignment: AlignCenter; background-color: red; font:Bold")

        self.OpenAv = QLabel()
        self.OpenAv.setFont(QFont("Arial",10))
        self.OpenAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.HighAv = QLabel()
        self.HighAv.setFont(QFont("Arial",10))
        self.HighAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.LowAv = QLabel()
        self.LowAv.setFont(QFont("Arial",10))
        self.LowAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.CloseAv = QLabel()
        self.CloseAv.setFont(QFont("Arial",10))
        self.CloseAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        self.VolumeAv = QLabel()
        self.VolumeAv.setFont(QFont("Arial",10))
        self.VolumeAv.setStyleSheet("qproperty-alignment: AlignCenter; background-color: cyan; font:Bold")

        try:
            database = di(StockSymbol,StockName)
            self.data_frame = database.SelectAll()
            #print( len(self.data_frame))

            if len(self.data_frame)!= 0 :
                self.model = TableModel(self.data_frame)
                self.table.setModel(self.model)
                self.layout1.addWidget(self.table)
            else:
                raise Exception

        except Exception as e:
            print("Importing data error! "+ str(e))
            self.label.setText("data not found ")
            self.layout1.addWidget(self.label)


        self.layout2.addWidget(self.TitleStats)

        self.NumEntries = len(self.data_frame)
        self.NumEntriesLabel.setText("Number of Entries: "+str(self.NumEntries))
        self.layout2.addWidget(self.NumEntriesLabel)

        self.DateRangeLabel.setText("Date range: "+ str(self.data_frame['Date'].iloc[self.NumEntries-1])+" - "+str(self.data_frame['Date'].iloc[0]))
        self.layout2.addWidget(self.DateRangeLabel)

        maxClosePrice = self.data_frame["Close"].values.max()
        indexmax = self.data_frame['Close'].idxmax()
        self.HighestClosingPringrice.setText("Highest Closing Price: "+str(maxClosePrice) +" at "+str(self.data_frame['Date'].iloc[indexmax]))
        self.layout2.addWidget(self.HighestClosingPringrice)

        minClosePrice = self.data_frame["Close"].values.min()
        indexmin = self.data_frame['Close'].idxmin()
        self.LowestClosingPrice.setText("Lowest Closing Price: "+str(minClosePrice) +" at "+str(self.data_frame['Date'].iloc[indexmin]))
        self.layout2.addWidget(self.LowestClosingPrice)

        highestVol = self.data_frame['Volume'].values.max()
        indexmax = self.data_frame['Volume'].idxmax()
        self.HighestVolume.setText("Highest Volume: "+str(highestVol) + " at "+str(self.data_frame['Date'].iloc[indexmax]))
        self.layout2.addWidget(self.HighestVolume)

        lowestVol = self.data_frame['Volume'].values.min()
        indexmin = self.data_frame['Volume'].idxmin()
        self.LowestVolume.setText("Lowest Volume: "+str(lowestVol) + " at "+str(self.data_frame['Date'].iloc[indexmin]))
        self.layout2.addWidget(self.LowestVolume)

        average = float(self.data_frame['Open'].values.mean()).__round__(2)
        self.OpenAv.setText("Average Opening price: "+ str(average))
        self.OpenAv.setWordWrap(True)
        self.layout2.addWidget(self.OpenAv)

        average = float(self.data_frame['High'].values.mean()).__round__(2)
        self.HighAv.setText("Average High price: "+ str(average))
        self.layout2.addWidget(self.HighAv)

        average = float(self.data_frame['Low'].values.mean()).__round__(2)
        self.LowAv.setText("Average Low price: "+ str(average))
        self.layout2.addWidget(self.LowAv)

        average = float(self.data_frame['Close'].values.mean()).__round__(2)
        self.CloseAv.setText("Average Closing price: "+ str(average))
        self.layout2.addWidget(self.CloseAv)

        average = self.data_frame['Volume'].values.mean()
        self.VolumeAv.setText("Average Volume: "+ str(average))
        self.layout2.addWidget(self.VolumeAv)

        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)
