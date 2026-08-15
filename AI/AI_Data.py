import datetime
from Auxilliary.Database_Interface1 import Data_Interface as di
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QPushButton, QLabel, QToolBar, QAction, QStatusBar,  QTabWidget, QTabBar, QWidget,QVBoxLayout
from AI.AI_Correllation_Tab import Correllation as crln
from AI.AI_ChartingPred_Actual import Pred_Act as pa
from AI.AI_bestFeat_Closing import  bestfeatVSClosing as bf
from Auxilliary.StockData_Historical import StockDataHist as sd
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime as dt

class Machine_learning(QWidget):
    def __init__(self,StockSymbol,StockName,start,end,interval):
        super().__init__()
        self.StockName = StockName
        self.StockSymbol = StockSymbol
        self.start = start
        self.end = end
        self.interval = interval
        self.date_data = None


        self.filename = None
        self.message = QLabel()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.date_range = None
        self.date_data = None
        self.year_range = None
        self.formatted_dates =list()

        self.corr_Indexes = list()
        self.corr_values = list()

        self.main_dataframe = None
        self.next_day_closing = None
        self.Closing_diff = list()

        self.model = None
        self.score= None

        self.import_data()
        self.setLayout(self.layout)

        self.price_pred= list()
        self.actual_price = list()

    def import_data(self):
        try:
            data = sd(self.StockSymbol,'1mo',str(self.start),str(self.end),self.interval)
            data.load_data()
            #data.show()
            data = data.history_dataframe.drop('Dividends',axis =1)
            data = data.drop('Stock Splits',axis =1)
            indexes = data.index.strftime("%B %d,%Y")
            data.index = indexes
            data = data.round(4)
            self.main_dataframe = data

            #database = di(self.StockSymbol,self.StockName)
            #self.main_dataframe = database.SelectAll()
            lenght = len(self.main_dataframe)
            self.date_data =  self.main_dataframe.index.tolist()
            self.date_range = str(str(self.date_data[0]) + " - " + str(self.date_data[lenght - 1]))
            #self.date_range = str(self.main_dataframe['Date'].iloc[lenght-1] + ' - ' +str(self.main_dataframe['Date'].iloc[0]))



            if len(self.main_dataframe) == 0 :
                raise Exception
            else:
                self.One_day_diff()
                self.correllation(self.main_dataframe)
                self.Polynomial_Regression()
                self.Sub_Tabs()


        except Exception as e:
            self.message.setText("Importing data error! "+ str(e)+" data not found ")
            self.layout.addWidget(self.message)

    def One_day_diff(self):
         close = list(self.main_dataframe['Close'])
         close_diff = list()

         open = list(self.main_dataframe['Open'])
         open_diff = list()

         high = list(self.main_dataframe['High'])
         high_diff = list()

         low = list(self.main_dataframe['Low'])
         low_diff = list()

         volume = list(self.main_dataframe['Volume'])
         volume_diff = list()

         data_lenght = len(close)
         close_diff.append(0)
         open_diff.append(0)
         high_diff.append(0)
         low_diff.append(0)
         volume_diff.append(0)

         i = 1
         while i<data_lenght:
             close_diff.append(float(close[i]- close[i-1]).__round__(2))
             open_diff.append(float(open[i]- open[i-1]).__round__(2))
             high_diff.append(float(high[i]- high[i-1]).__round__(2))
             low_diff.append(float(low[i]- low[i-1]).__round__(2))
             volume_diff.append(float(volume[i]- volume[i-1]).__round__(2))
             i = i+1

         #print(close)
         #print(close_diff)
         self.Closing_diff = close_diff
        # print(open)
         #print(open_diff)
         #print(high)
         #print(high_diff)
         #print(low)
         #print(low_diff)
         #print(volume)
         #print(volume_diff)

    def correllation(self,dataframe):
        dataframe = dataframe.reset_index(drop=True)
        print(dataframe)

        #Create the NEXT closing price list ,change the last item as the average of close difference + the last item of close
        closing = list(dataframe['Close'])
        closing.pop(0)
        self.Closing_diff = pd.Series(self.Closing_diff)
        av = self.Closing_diff.mean()
        closing.append(closing[len(closing)-1] + float(av).__round__(2))

        dataframe["N_D_Close"] = closing
        self.next_day_closing = dataframe["N_D_Close"]
        corr = dataframe.corr()
        #print(corr)

        #---get the top 5 features that has the highest correlation---
        corr_Indexes = list(dataframe.corr().abs().nlargest(6, 'N_D_Close').index)
        corr_Indexes.remove('N_D_Close')
        self.corr_Indexes = corr_Indexes

        #---print the top 5 correlation values---
        corr_values = list(dataframe.corr().nlargest(5, 'N_D_Close').values[0])
        corr_values.remove(1)
        corr_values.sort(reverse=True)
        self.corr_values = corr_values

    def Polynomial_Regression(self):# uses best correlation feature as an independent var ,Single regression
        first_feat = self.corr_Indexes[0]
        #second_feat = self.corr_Indexes[1]

        x = np.c_[self.main_dataframe[first_feat]]
        y = self.next_day_closing

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,random_state=5)

        #---use a polynomial function of degree n---
        degree = 1
        score = 0
        increase = True
        while increase:#looping until we get the degree with highest score
            polynomial_features= PolynomialFeatures(degree = degree)
            x_train_poly = polynomial_features.fit_transform(x_train)

            self.model = LinearRegression()
            self.model.fit(x_train_poly, y_train)

            x_test_poly = polynomial_features.fit_transform(x_test)

            tmp_score = self.model.score(x_test_poly,y_test)
            #print('R-Squared: %.4f' % tmp_score)

            if tmp_score > score:
                score = tmp_score
                self.score = score
                degree = degree+1
            else:
                increase = False
                break

        self.price_pred = self.model.predict(x_test_poly)
        self.actual_price = y_test
        #print(self.price_pred)
        #print(y_test)
        # save the model to disk
        self.filename = self.StockName+'('+self.StockSymbol+')'+'.sav'
        # write to the file using write and binary mode
        pickle.dump(self.model, open(self.filename, 'wb'))

        #print("Best degree at "+ str(degree)+ " with score "+str(float(score*100).__round__(2)) + "%" )


    def Sub_Tabs(self):

            self.sub_tabs = QTabWidget()
            self.sub_tabs.setTabPosition(QTabWidget.North)
            self.sub_tabs.setMovable(True)
            self.sub_tabs.addTab(crln(self.date_range,self.corr_Indexes,self.corr_values,self.score),QIcon("Source Images/AI.png"),"Correllation Table")
            self.sub_tabs.addTab(pa(self.StockSymbol,self.StockName,self.price_pred,self.actual_price,self.date_range),QIcon("Source Images/AI.png"),"Price Chart")

            best = self.main_dataframe[self.corr_Indexes[0]]
            best = list(best)
            best.reverse()
            self.next_day_closing = list(self.next_day_closing)
            self.next_day_closing.reverse()
            #self.date_data= self.main_dataframe['Date']
            #self.date_data = list(self.date_data)
            self.date_data.reverse()
            self.date_formatter()
            self.sub_tabs.addTab(bf(self.StockSymbol,self.StockName,best,self.next_day_closing,self.corr_Indexes[0],
                                    self.formatted_dates,self.year_range),QIcon("Source Images/AI.png"),"Model chart")

            self.layout.addWidget(self.sub_tabs)

    def date_formatter(self):#Charting All Data

        format = '%B %d,%Y'
        print(format)

        date_str1 = dt.strptime(self.date_data[0],format)
        date_str2 = dt.strptime(self.date_data[len(self.date_data)-1],format)

        date_year1 = date_str1.year
        date_year2 = date_str2.year


        if(date_year2 == date_year1):
            self.year_range = date_year1
        else:
            self.year_range = str(date_year1) + "-"+ str(date_year2)


        for date in self.date_data:
            raw_date = dt.strptime(date,format)
            self.formatted_dates.append(raw_date.strftime('%m/%d'))




