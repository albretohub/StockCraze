
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QToolBar, QAction, QStatusBar, \
    QMessageBox, QTabWidget, QTabBar, QDialog, QInputDialog, QWidget

from UI.UI_Home_tab_widget import Home_Tab
from UI.UI_Tab_widgets import Tabs
from UI.UI_mystocks_tab import MyStockTabs
from UI.UI_HistoricalPricesTab import*
from UI.UI_MainChartingTab import MainChartingWindow
#from UI_ChartingTab import MainChart

import shelve
from AI.AI_Data import Machine_learning
from Auxilliary.My_Stock_shelve import Stock_shelve as ss
from Auxilliary.Date_Input import DateRangeDialog as dr
from Auxilliary.Date_Input import IntervalDialog as id


class MainWindow(QMainWindow):

    stock_approved = False

    def __init__(self):
        super().__init__()
        self.setFixedSize(1200,800)
        self.setWindowIcon(QIcon("Source Images/stockMarket.jpg"))

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        self.Online = None
        self.setWindowTitle('StocKraze')
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.tabCloseRequested.connect(self.delete_Tab)
        self.Home_tab()
        self.RecentStock = None

        self.setCentralWidget(self.tabs)
        self.stocks_tuple = None
        self.stock_shelve()

        new_stock = QAction(QIcon("Source Images/chart-up-color.png"),"Add Stock", self)
        new_stock.setStatusTip("This is your button")
        new_stock.triggered.connect(self.Add_Tab)
        new_stock.setShortcut(QKeySequence("Ctrl+n"))
        toolbar.addAction(new_stock)

        my_stock = QAction(QIcon("Source Images/luggage.png"),"My Stocks", self)
        my_stock.setStatusTip("This is your button")
        my_stock.triggered.connect(self.my_stocks)
        my_stock.setShortcut(QKeySequence("Ctrl+m"))
        toolbar.addAction(my_stock)

        historical_price= QAction(QIcon("Source Images/calendar-blue.png"),"Historical Prices", self)
        historical_price.setStatusTip("This is your button")
        historical_price.triggered.connect(self.historical_prices)
        historical_price.setShortcut(QKeySequence("Ctrl+h"))
        toolbar.addAction(historical_price)

        charting = QAction(QIcon("Source Images/chart.png"),"Charting", self)
        charting.setStatusTip("This is your button")
        charting.triggered.connect(self.Charting)
        charting.setShortcut(QKeySequence("Ctrl+f"))
        toolbar.addAction(charting)

        AI = QAction(QIcon("Source Images/AI.png"),"AI Assistant", self)
        AI.setStatusTip("This is your button")
        AI.triggered.connect(self.AI)
        AI.setShortcut(QKeySequence("Ctrl+f"))
        toolbar.addAction(AI)

        self.new_stock = None


    def Home_tab(self):
        self.tabs.addTab(Home_Tab(),QIcon('Source Images/home.png'),'Home')
        self.tabs.tabBar().setTabButton(0,QTabBar.RightSide,None)

    def Add_Tab(self):
         self.tabs.addTab(Tabs(),QIcon("Source Images/chart-up.png"),"Add new Stock")

    def delete_Tab(self,index):
        self.tabs.removeTab(index)

    def my_stocks(self):
        self.stock_shelve()
        nameAndticker = list()

        for stocks in self.stocks_tuple:
            nameAndticker.append(stocks[0]+"-"+stocks[1])

        MystockDialog = QInputDialog()
        MystockDialog.setFixedSize(500,200)

        selectedStock, ok =  MystockDialog.getItem(self, "Select Stock", "My Stocks", nameAndticker, 0, False)

        if ok :
            stockName ,ticker= selectedStock.split("-")
            self.tabs.addTab(MyStockTabs(ticker,stockName),QIcon("Source Images/chart-up.png"),ticker)

            self.RecentStock = shelve.open('Data/Recent_Stock_data')
            current_stock = stockName + "(" + ticker + ")"
            self.RecentStock['recent'] = current_stock
            self.RecentStock.close()


    def historical_prices(self):
        self.stock_shelve()
        nameAndticker = list()

        for stocks in self.stocks_tuple:
            nameAndticker.append(stocks[0]+"-"+stocks[1])

        MystockDialog = QInputDialog()
        MystockDialog.setFixedSize(500,200)

        selectedStock, ok =  MystockDialog.getItem(self, "Select Stock", "My Stocks", nameAndticker, 0, False)

        if ok :
            stockName ,ticker= selectedStock.split("-")
            start, end, ok2 = dr.getDateRange(title="Choose Report Dates")
            input_start = start.toString("yyyy-MM-dd")
            input_end = end.toString("yyyy-MM-dd")
            input_interval = '1d'

            if ok2:
                interval, ok2 = id.getInterval()
                input_interval = interval
                if ok2:
                    print("Start: "+input_start)
                    print("End:  "+ input_end)
                    print("Selected interval:", interval)

                    #self.tabs.addTab(HistoricalPrice_Tab(ticker,stockName),QIcon("Source Images/chart-up.png"),ticker) # will be used if internet access is available
                    self.tabs.addTab(HistoricalPrice_Tab(ticker,stockName,input_start,input_end,input_interval),QIcon("Source Images/chart-up.png"),ticker)
                    #self.tabs.addTab(HistoricalPrice_Tab_CSV(ticker,stockName),QIcon("chart-up.png"),ticker) # will be used if internet access is not available
                    #self.tabs.addTab(HistoricalPrice_Tab_Database(ticker,stockName),QIcon("Source Images/chart-up.png"),ticker)
                    self.RecentStock = shelve.open('Data/Recent_Stock_data')
                    current_stock = stockName + "(" + ticker + ")"
                    self.RecentStock['recent'] = current_stock
                    self.RecentStock.close()

        else:
            print("Cancelled")

    def Charting(self):
        self.stock_shelve()
        nameAndticker = list()

        for stocks in self.stocks_tuple:
            nameAndticker.append(stocks[0]+"-"+stocks[1])

        MystockDialog = QInputDialog()
        MystockDialog.setFixedSize(500,200)

        selectedStock, ok =  MystockDialog.getItem(self, "Select Stock", "My Stocks", nameAndticker, 0, False)


        if ok :
            stockName ,ticker= selectedStock.split("-")
            start, end, ok2 = dr.getDateRange(title="Choose Report Dates")
            input_start = start.toString("yyyy-MM-dd")
            input_end = end.toString("yyyy-MM-dd")
            input_interval = '1d'

            if ok2:
                interval, ok2 = id.getInterval()
                input_interval = interval
                if ok2:
                    print("Start: "+input_start)
                    print("End:  "+ input_end)
                    print("Selected interval:", interval)

                    self.tabs.addTab(MainChartingWindow(ticker,stockName,input_start,input_end,input_interval),QIcon("Source Images/chart-up.png"),ticker)
                    self.RecentStock = shelve.open('Data/Recent_Stock_data')
                    current_stock = stockName + "(" + ticker + ")"
                    self.RecentStock['recent'] = current_stock
                    self.RecentStock.close()

        else:
            print("Cancelled")


    def AI(self):
        self.stock_shelve()
        nameAndticker = list()

        for stocks in self.stocks_tuple:
            nameAndticker.append(stocks[0]+"-"+stocks[1])

        MystockDialog = QInputDialog()
        MystockDialog.setFixedSize(500,200)

        selectedStock, ok =  MystockDialog.getItem(self, "Select Stock", "AI Assistant", nameAndticker, 0, False)
        if ok :
            stockName ,ticker= selectedStock.split("-")
            self.tabs.addTab(Machine_learning(ticker,stockName),QIcon("Source Images/AI.png"),ticker)
            self.RecentStock = shelve.open('Data/Recent_Stock_data')
            current_stock = stockName + "(" + ticker + ")"
            self.RecentStock['recent'] = current_stock
            self.RecentStock.close()


    def stock_shelve(self):
        stocks_tuple = ss()
        self.stocks_tuple = stocks_tuple.values()
        #print(self.stocks_tuple)





app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec_()
