import shelve


class Stock_shelve:

    def __init__(self):
        self.my_stockshelve = None
        self.stocks_tuple_list = list()

    def my_stock_shelve_add_data(self,stockname,symbol):
        self.my_stockshelve = shelve.open("Data/mystocks")
        newstock = (stockname,symbol)
        self.stocks_tuple_list = list(self.values())
        print(self.stocks_tuple_list)
        self.stocks_tuple_list.append(newstock)
        print(self.stocks_tuple_list)
        self.my_stockshelve['saved_stocks'] = self.stocks_tuple_list
        self.my_stockshelve.close()

    def values(self):
        stocklist = list()
        try:
            self.my_stockshelve = shelve.open("Data/mystocks")
            stocklist = self.my_stockshelve['saved_stocks']
        except:
            stocklist = []
        return stocklist
        self.my_stockshelve.close()


#S = Stock_shelve()
