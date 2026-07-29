# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:37:05 2023

@author: Albreto Sepio
"""
#This module will be used along side with the main-StockDatabase API module..

import sqlite3


class StockData:

    def __init__(self,stock_name):
        self.stock_name = stock_name
        self.database = None
        self.cursor = None
        self.connection()
        self.tables = list()
        self.entries = None
        self.message = None #For dialog message

    def connection(self):
        database_name = str(self.stock_name)+ '.db'
        try:
            self.database = sqlite3.connect('Data/'+database_name)
            self.cursor = self.database.cursor()

        except Exception as e:
            print("Connectionn error! "+ e)


    def new_table(self,month,year):
        table_name =  month+"_"+str(year)
        table_list = self.All_Tables()
        self.connection()

        if table_name in table_list:
            print("Table "+ table_name+" already in database")
        else:
            self.cursor.execute("DROP TABLE IF EXISTS " + table_name)

            sql ='''CREATE TABLE ''' + table_name+'''(
            DAY INT,
            OPEN FLOAT,
            HIGH FLOAT,
            LOW FLOAT,
            CLOSE FLOAT,
            VOLUME INT)'''

            self.cursor.execute(sql)
            self.message = "Table created successfully..."
            print("Table created successfully........")


    def Insert(self,month,year,day,openPrice,high,low,closePrice,volume):

        table_name =  month+"_"+str(year)
        data_existence = self.SelectByDate(day, month, year)
        self.connection()

        try:
            if len(data_existence) == 0 :
                data_tuple = (day,openPrice,high,low,closePrice,volume)
                sqlite_insert_with_param = """INSERT INTO """+ table_name+"""
                                  (DAY,OPEN,HIGH,LOW,CLOSE,VOLUME) 
                                  VALUES (?, ?, ?, ?, ?, ?);"""
                self.cursor.execute(sqlite_insert_with_param,data_tuple)
                self.message = "Data inserted successfully."
                print("Data inserted successfully........")
            else:
                #To be coupled with UPDATING function..
                self.message = str(day) + "-" +table_name+" already Exist"
                print(self.message)
        except Exception as e:
            self.message = "Error Inserting data"
        self.database.commit()
        self.close()

    def Update(self,month,year,day,openPrice,high,low,closePrice,volume):

        table_name =  month+"_"+str(year)
        try:
            self.DeleteDate(day, month, year)
            self.Insert(month,year,day,openPrice,high,low,closePrice,volume)
            self.message = "Data updated successfully."
            print("Data updated successfully........")
        except Exception as e:
            self.message = "Error updating data"

    def All_Tables(self):
        self.connection()
        self.cursor.execute('''SELECT name from sqlite_master WHERE type = 'table';''')
        all_tables = self.cursor.fetchall()

        if len(all_tables) != 0:
            for table in all_tables:
                if table[0] not in self.tables:
                    self.tables.append(table[0])

        self.database.commit()
        self.close()
        return self.tables


    def SelectMonthly(self,month,year):
        self.connection()
        table_name =  month+"_"+str(year)

        try:
            self.cursor.execute('''SELECT * from '''+ table_name)
            self.entries = self.cursor.fetchall()
            self.message = table_name+" Entries selected"

        except Exception as e:
            self.message = table_name+" not Available"
            print(table_name+" not Available")

        # Commit your changes in the database
        self.database.commit()
        self.close()
        return self.entries


    def SelectByDate(self,day,month,year):
        self.connection()
        table_name =  month+"_"+str(year)
        entry = None

        try:
            self.cursor.execute('''SELECT * from '''+ table_name+''' WHERE DAY = '''+str(day))
            entry = self.cursor.fetchall()
            self.message = str(day)+"-"+table_name+" Selected"
        except Exception as e:
            self.message = str(day)+"-"+table_name+" not Available"
            print(table_name+" not Available")

        self.database.commit()
        self.close()
        return entry

    def DeleteMonth(self,month,year):
        self.connection()
        table_name =  month+"_"+str(year)

        try:
            self.cursor.execute('''DROP TABLE '''+ table_name)
        except Exception as e:
            self.message =month+"_"+str(year)+" deleted.. "
            print(  month+"_"+str(year)+" deleted... ")

        self.database.commit()
        self.close()

    def DeleteDate(self,day,month,year):
        self.connection()
        table_name =  month+"_"+str(year)

        try:
            self.cursor.execute('''DELETE FROM '''+ table_name+''' WHERE DAY = '''+str(day))
        except Exception as e:
            self.message =str(day)+month+"_"+str(year)+" entry deleted.. "
            print(self.message)

        self.database.commit()
        self.close()

    def close(self):

        #Closing the connection
        self.database.close()
