from Auxilliary.StockData_CSV import Stock_CSV
from Auxilliary.Database import StockData
import pandas as pd
from datetime import datetime as dt


class Data_Interface():
    def __init__(self, csv_file,Stockname):#CSV to Database
        self.stock_name = Stockname
        self.csv_file = csv_file

        self.CSV_Data = Stock_CSV(None,self.csv_file)
        self.CSV_Data.load_data_csv()

        self.database = StockData(self.stock_name)
        print(self.database.All_Tables())

    def Insert_Entry(self):#Input data from a csv file only..
        print("Hi")
        dataframe = pd.DataFrame(self.CSV_Data.data_frame)
        num_entry = len(dataframe)
        i = 0
        while i <= num_entry-1:
            data = dataframe.iloc[i]
            date = data["Date"]

            fmt = self.CSV_Data.detect_date_format(date)
            day = int(dt.strptime(date,fmt).strftime("%d"))
            month = dt.strptime(date,fmt).strftime("%B")
            year = dt.strptime(date,fmt).strftime("%Y")

            self.database.new_table(month,year)
            self.database.Insert(month,year,day,data["Open"],data["High"],data["Low"],data['Close'],self.CSV_Data.volume_data[i])

            i = i+1

    def SelectDataMonthly(self,month,year):# To be program for date range selection
        self.month = month
        self.year = year
        #Columns = ("Date("+self.month+"_"+str(self.year)+")","Open","High","Low","Close","Volume")
        #print(self.database.SelectMonthly(self.month,self.year))
        Columns = ("Date","Open","High","Low","Close","Volume")
        data_frame = pd.DataFrame(self.database.SelectMonthly(self.month,self.year),columns=Columns)
        return data_frame

    def SelectAll(self):
        tables = self.database.All_Tables()
        All_data = list()


        for table in tables:
            month, year = str(table).split("_")
            index = 0
            self.entries = list(self.database.SelectMonthly(month,year))
            num_entries = len(self.entries)

            formatted_entries = list()

            for data in self.entries:
                formatted_entries.append(list(data))

            while index <= num_entries-1:
                raw_date = dt.strptime(month + " "+str(self.entries[index][0])+" "+year,'%B %d %Y')
                formatted_entries[index][0] = str(dt.strftime(raw_date,'%b/%d/%y'))
                index =index+1

            for data in formatted_entries:
                All_data.append(data)

        Columns = ("Date","Open","High","Low","Close","Volume")
        data_frame = pd.DataFrame(All_data,columns=Columns)
        return data_frame


