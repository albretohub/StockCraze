# -*- coding: utf-8 -*-
"""

@author: Albreto Sepio

                This module is for Prediction VS Actual next day Closing Price charting.
"""

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel,QHBoxLayout,QPushButton # import PyQt5 before matplotlib
import matplotlib
import matplotlib.pyplot as plt

from matplotlib import style
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")
style.use("ggplot")

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class bestfeatVSClosing(QWidget):
    def __init__(self,StockSymbol,StockName,bestfeat_price,closing_price,bestfeat_index,date_data,year):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName

        self.bestfeat_price = bestfeat_price
        self.closing_price =closing_price
        self.date_data = date_data
        self.bestfeat_index = bestfeat_index
        self.year = year


        # Charting the desired values
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=3, height=2, dpi=100)
        # Create toolbar, passing canvas as first parament, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        self.Chart_best_feat()

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(toolbar)
        self.layout1.addWidget(self.sc)
        self.setLayout(self.layout1)

    def Chart_best_feat(self):
         self.sc.axes.plot(self.date_data,self.closing_price,c = 'Blue',label = "Next Day Close")
         self.sc.axes.plot(self.date_data,self.bestfeat_price,c = 'Green',label = self.bestfeat_index)
         self.sc.axes.set_title(self.StockName + "("+ self.StockSymbol+")",font = "ARIAL",fontsize = 30)
         self.sc.axes.set_xlabel("Date ("+ str(self.year)+")",font = "ARIAL",fontsize = 20)
         self.sc.axes.set_ylabel("Price",font = "ARIAL",fontsize = 20)
         self.sc.axes.tick_params(axis = 'x')
         self.sc.axes.legend()






