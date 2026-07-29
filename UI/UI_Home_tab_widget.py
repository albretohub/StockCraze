from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QVBoxLayout,QHBoxLayout
import shelve

class Home_Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()

        self.font = QFont()
        self.font.setPointSize(30)
        self.font.setFamily("Arial")
        self.font.Bold

        self.font2 = QFont()
        self.font2.setPointSize(20)
        self.font2.setFamily("Times New Roman")
        self.font2.Bold

        self.Welcomelabel = QLabel("Welcome\nSTOCK ANALYZER")
        self.Welcomelabel.setFont(self.font)
        self.RecentStocklabel  = QLabel("Recent Stock:")
        self.RecentStocklabel.setFont(self.font2)

        self.layout.addWidget(self.Welcomelabel)
        self.layout.addWidget(self.RecentStocklabel)
        self.setLayout(self.layout)
        self.recent_stock()
    def recent_stock(self):
        shelfile = shelve.open("Data/Recent_Stock_data")
        recent = ""
        try:
            recent = shelfile['recent']
        except:
            recent = "No Stocks available"
        self.RecentStocklabel.setText("Recent Stock: " + recent )


