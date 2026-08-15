from PyQt5.QtWidgets import  QGridLayout, QPushButton, QLabel, QHBoxLayout, QAction,QWidget,QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from sklearn.linear_model import LinearRegression
import pickle

class Correllation(QWidget):

    def __init__(self,date_range,corr_Index,corr_values,score):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.second_layout = QGridLayout()
        self.score = QLabel()

        self.setStyleSheet("qproperty-alignment: AlignCenter ")
        self.date= QLabel("Date Range: "+date_range)
        self.date.setFont(QFont("Arial",15))
        #self.score.setText("Model Score: "+str(float(score*100).__round__(2))+ "%")
        self.score.setFont(QFont("Arial",15))
        self.score.setStyleSheet("qproperty-alignment: AlignLeft;")
        self.main_layout.addWidget(self.score)
        self.Title = QLabel("Correlation Table")
        self.Title.setFont(QFont("Arial",30))
        self.rowLabel1 = QLabel("Next Closing Price")
        self.rowLabel1.setFont(QFont("Arial",15))
        self.col_Label1 = QLabel("  Open")
        self.col_Label1.setFont(QFont("Arial",15))
        self.col_Label2 = QLabel("  High")
        self.col_Label2.setFont(QFont("  Arial",15))
        self.col_Label3 = QLabel("  Low")
        self.col_Label3.setFont(QFont("Arial",15))
        self.col_Label4 = QLabel("  Close")
        self.col_Label4.setFont(QFont("Arial",15))
        self.col_Label5 = QLabel("  Volume")
        self.col_Label5.setFont(QFont("Arial",15))

        self.val_1_1 = QLabel()
        self.val_1_2 = QLabel()
        self.val_1_3 = QLabel()
        self.val_1_4 = QLabel()
        self.val_1_5 = QLabel()

        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.Title)
        self.main_layout.addLayout(self.second_layout)
        self.second_layout.addWidget(self.rowLabel1,1,0)

        self.second_layout.addWidget(self.col_Label1,0,1)
        self.second_layout.addWidget(self.col_Label2,0,2)
        self.second_layout.addWidget(self.col_Label3,0,3)
        self.second_layout.addWidget(self.col_Label4,0,4)
        self.second_layout.addWidget(self.col_Label5,0,5)
        self.main_layout.addWidget(self.date)

        self.corr_Indexes = list(corr_Index)
        self.corr_values = list(corr_values)
        self.values()

        #print(self.corr_Indexes)
        #print(self.corr_values)

    def values(self):
        open = str(float(self.corr_values[self.corr_Indexes.index('Open')] * 100).__round__(3))
        self.val_1_1.setText(open+'%')
        self.val_1_1.setFont(QFont("Arial",10))
        self.second_layout.addWidget(self.val_1_1,1,1)

        high = str(float(self.corr_values[self.corr_Indexes.index('High')] * 100).__round__(3))
        self.val_1_2.setText(high+'%')
        self.val_1_2.setFont(QFont("Arial",10))
        self.second_layout.addWidget(self.val_1_2,1,2)

        low = str(float(self.corr_values[self.corr_Indexes.index('Low')] * 100).__round__(3))
        self.val_1_3.setText(low+'%')
        self.val_1_3.setFont(QFont("Arial",10))
        self.second_layout.addWidget(self.val_1_3,1,3)

        close = str(float(self.corr_values[self.corr_Indexes.index('Close')] * 100).__round__(3))
        self.val_1_4.setText(close+'%')
        self.val_1_4.setFont(QFont("Arial",10))
        self.second_layout.addWidget(self.val_1_4,1,4)

        volume = str(float(self.corr_values[self.corr_Indexes.index('Volume')] * 100).__round__(3))
        self.val_1_5.setText(volume+'%')
        self.val_1_5.setFont(QFont("Arial",10))
        self.second_layout.addWidget(self.val_1_5,1,5)


