

import datetime
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from Auxilliary.StockData_Historical import StockDataHist as sd


class MyStockTabs(QWidget):
    def __init__(self,StockSymbol,StockName):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName

        self.today = datetime.datetime.now()
        self.todayString = self.today.strftime("%B %d,%Y %H:%M:%S")

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()
        self.layout5 = QVBoxLayout()
        self.layout6 = QHBoxLayout()

        self.font = QFont()
        self.font.setPointSize(30)
        self.font.setFamily("Arial")
        self.font.Bold

        self.font2 = QFont()
        self.font2.setPointSize(15)
        self.font2.setFamily("Arial")
        self.font2.Bold

        self.font3 = QFont()
        self.font3.setPointSize(10)
        self.font3.setFamily("Arial")
        self.font3.Bold

        self.stocksymbol = QLabel(StockSymbol)
        self.stocksymbol.setFont(self.font)
        self.stocksymbol.setMargin(10)
        self.stocksymbol.setStyleSheet("qproperty-alignment: AlignCenter; background-color: Grey")
        self.stockname = QLabel(StockName)
        self.stockname.setFont(self.font2)

        self.dateToday =QLabel("As of "+str(self.todayString))
        self.dateToday.setFont(self.font3)

        self.week52LowLabel = QLabel()
        self.week52LowLabel.setFont(self.font3)
        self.week52HighLabel = QLabel()
        self.week52HighLabel.setFont(self.font3)
        self.sectorLabel = QLabel()
        self.sectorLabel.setFont(self.font3)
        self.countryLabel = QLabel()
        self.countryLabel.setFont(self.font3)
        self.marketCapLabel = QLabel()
        self.marketCapLabel.setFont(self.font3)

        self.priceTodayLabel = QLabel()
        self.priceTodayLabel.setFont(self.font3)
        self.TodayVolume = QLabel()
        self.TodayVolume.setFont(self.font3)
        self.percentChangeLabel = QLabel()
        self.percentChangeLabel.setFont(self.font3)
        self.status = QLabel()
        self.status.setFont(self.font3)


        self.refresh = QPushButton(QIcon("refresh.jpg"),"Refresh")
        self.refresh.setFixedSize(150,50)
        self.refresh.pressed.connect(self.Refresh)


        self.layout2.addWidget(self.week52LowLabel)
        self.layout2.addWidget(self.week52HighLabel)
        self.layout2.addWidget(self.priceTodayLabel)
        self.layout2.addWidget(self.TodayVolume)
        self.layout2.addWidget(self.status)
        #self.layout2.addWidget(self.percentChangeLabel)

        self.layout6.addWidget(self.stocksymbol)

        self.layout5.addWidget(self.stockname)
        self.layout5.addWidget(self.dateToday)
        self.layout5.addWidget(self.countryLabel)
        self.layout5.addWidget(self.sectorLabel)
        self.layout5.addWidget(self.marketCapLabel)

        self.layout3.addLayout(self.layout5)
        self.layout3.addLayout(self.layout2)

        self.layout4.addWidget(self.refresh)

        self.layout1.addLayout(self.layout6)
        self.layout1.addLayout(self.layout3)
        self.layout1.addLayout(self.layout4)
        self.setLayout(self.layout1)

        self.StockStats(self.StockName,self.StockSymbol)# data fetches from database

    def StockStats(self,Stockname,StockSymbol):
        #This function must return a list type variable from database
        #example StocKStatList = [week52high,week52High, PriceToday ,PriceYesterday,Sector,Country,marketcap]

        StockProfile = sd(self.StockSymbol,'1d','1m')
        StockProfile.Stock_Info()

        #StockProfile.show()

        StocKStatList = [StockProfile.FiftyWeekLow,StockProfile.FiftyWeekHigh,StockProfile.currentPrice,
                         StockProfile.TodayOnlyVolume,StockProfile.sector,StockProfile.country,StockProfile.marketCap,StockProfile.status]

        self.marketCapLabel.setText("Market Capital: " +str(StocKStatList[6]))
        self.sectorLabel.setText("Sector: " +str(StocKStatList[4]))
        self.countryLabel.setText("Country: " +str(StocKStatList[5]))
        self.week52LowLabel.setText("52-Week Low: " + str(StocKStatList[0]))
        self.week52HighLabel.setText("52-Week High: " +str(StocKStatList[1]))
        self.priceTodayLabel.setText("Current Closing Price: " +str(StocKStatList[2]))
        self.TodayVolume.setText("Today's Volume: " +str(StocKStatList[3]))
        self.stockname.setText("Name: "+str(StockProfile.companyName))
        self.status.setText("Status: "+ str(StocKStatList[7]))
        #self.percentChangeLabel.setText("%Change: "+str((StocKStatList[2]-StocKStatList[3])/StocKStatList[3]))

        return StocKStatList

    def Refresh(self):
        #This function serves to update or refresh the tabs data.
        today = datetime.datetime.now()
        date = today.strftime("%B %d,%Y %H:%M:%S")
        self.dateToday.setText("As of "+str(date))
        self.StockStats(self.StockName,self.StockSymbol)# data fetches from database







