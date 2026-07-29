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

class Pred_Act(QWidget):
    def __init__(self,StockSymbol,StockName,prediction_price,actual_price,date_range):
        super().__init__()
        self.StockSymbol = StockSymbol
        self.StockName = StockName

        self.prediction_price = prediction_price
        self.actual_price =actual_price
        self.date_range = date_range


        # Charting the desired values
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=3, height=2, dpi=100)
        # Create toolbar, passing canvas as first parament, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        self.Chart_Pred_Act()

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(toolbar)
        self.layout1.addWidget(self.sc)
        self.setLayout(self.layout1)

    def Chart_Pred_Act(self):
         self.sc.axes.scatter(self.actual_price,self.prediction_price)
         self.sc.axes.set_title(self.StockName + "("+ self.StockSymbol+")",font = "ARIAL",fontsize = 30)
         self.sc.axes.set_xlabel("Actual Prices "+"(Random Date Range: "+ str(self.date_range)+")" ,font = "ARIAL",fontsize = 20)
         self.sc.axes.set_ylabel("Predicted Prices",font = "ARIAL",fontsize = 20)
         self.sc.axes.tick_params(axis = 'x')






