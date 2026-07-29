
from PyQt5.QtWidgets import ( QDialog,QInputDialog)
from UI.UI_new_stock_dialog import *

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.symbol_return)
        self.symbol = None
        self.show()

    def symbol_return(self):
        self.symbol = self.ui.lineEdit.text()
        print(self.symbol)#Soon will be change into progress bar connected with the web crawler module to search fro the given ticker symbol
        #and its historical prices.

