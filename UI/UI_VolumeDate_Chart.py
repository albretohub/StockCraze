# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 19:59:39 2025

@author: Albreto Sepio

            This module is for Volume data charting.
"""

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QTabWidget,QStackedLayout,QPushButton # import PyQt5 before matplotlib
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

class MainChart2(QWidget):
    def __init__(self,StockSymbol,StockName,date_data,volume_data,years):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName

        #data variables coupled with CSV data
        self.date_data = date_data
        self.volume_data = volume_data
        self.years = years


        # Charting the desired values
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=3, height=2, dpi=100)
        # Create toolbar, passing canvas as first parament, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        self.Chart_Volume_Date(self.volume_data,self.date_data)


        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(toolbar)
        self.layout1.addWidget(self.sc)
        self.setLayout(self.layout1)


    def Chart_Volume_Date(self,volume,dates):
         self.volume = volume
         self.dates = dates
         self.sc.axes.bar(dates,volume)
         self.sc.axes.set_title(self.StockName + "("+ self.StockSymbol+")",font = "ARIAL",fontsize = 30)
         self.sc.axes.set_xlabel("Date ("+ str(self.years)+")",font = "ARIAL",fontsize = 20)
         self.sc.axes.set_ylabel("Volume",font = "ARIAL",fontsize = 20)
         self.sc.axes.tick_params(axis = 'x')

    def print_me(self):
        print("ME!")




