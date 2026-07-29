import os

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QFileDialog, QMessageBox,QDialog,QHBoxLayout
from PyQt5.QtGui import QIcon
from UI.UI_New_Stock_window import MyForm
from Auxilliary.Database_Interface1 import Data_Interface
from Auxilliary.My_Stock_shelve import Stock_shelve as ss

class Tabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.searchButton = QPushButton(QIcon("Source Images/magnifier-zoom.png"),"Search Stock")
        self.searchButton.setFixedSize(150,100)
        self.searchButton.pressed.connect(self.SearchStock)

        self.importButton = QPushButton(QIcon("Source Images/folder-import.png"),"Import Data")
        self.importButton.setFixedSize(150,100)
        self.importButton.pressed.connect(self.Import_Dialog)

        self.layout.addWidget(self.searchButton,0,2)
        self.layout.addWidget(self.importButton,1,2)
        self.setLayout(self.layout)
        self.dlg = QDialog()

    def SearchStock(self):
        self.ui = MyForm()
        self.ui.show()
        self.ui.exec()
        #To be coded for trading platform API for data needed.

    def Import_Dialog(self):
        print("click")


        self.dlg.setFixedSize(300,150)

        self.dlg.setWindowTitle("Create a Database")
        self.dlg.setWindowIcon(QIcon("database--plus.png"))

        QBtn = QPushButton("Import CSV")
        QBtn2 = QPushButton("Import Excel")

        QBtn.pressed.connect(self.openFileDialog2)


        self.layout = QVBoxLayout()
        self.layout2 = QHBoxLayout()

        self.StockLineEdit = QLineEdit()
        self.StockLineEdit.setPlaceholderText("Enter Stock Name Here!")
        self.TickerLineEdit = QLineEdit()
        self.TickerLineEdit.setPlaceholderText("Enter Ticker Symbol Here!")

        self.layout.addWidget(self.StockLineEdit)
        self.layout.addWidget(self.TickerLineEdit)
        self.layout.addLayout(self.layout2)
        self.layout2.addWidget(QBtn)
        self.layout2.addWidget(QBtn2)

        self.dlg.setLayout(self.layout)
        self.dlg.exec()

    def openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','/home')
        excelFile = os.path.normpath(fname[0])
        name, extension = os.path.splitext(excelFile)
        print(fname)
        print(type(fname))

        if extension == ".xlsx":
            print(excelFile)
            print(extension)
            #To be coded for Excel Manipulator and Databse connection.
            return
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("File Type Error!")
            dlg.setText("File Selected not an excel!")
            dlg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec_()
            if button == QMessageBox.Retry:
                    self.openFileDialog()
            else:
                return

    def openFileDialog2(self):
        Table_name = self.StockLineEdit.text()
        fname = QFileDialog.getOpenFileName(self, 'Open file','/home')
        csvFile = os.path.normpath(fname[0])
        name, extension = os.path.splitext(csvFile)

        if extension == ".csv":
            print(csvFile)
            Interface = Data_Interface(csvFile,Table_name)
            Interface.Insert_Entry()
            stockshelve = ss()
            stockshelve.my_stock_shelve_add_data(self.StockLineEdit.text(),self.TickerLineEdit.text())
            self.dlg.close()
            return
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("File Type Error!")
            dlg.setText("File Selected not a CSV!")
            dlg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec_()
            if button == QMessageBox.Retry:
                    self.openFileDialog2()
            else:
                return
        self.dlg.close()



