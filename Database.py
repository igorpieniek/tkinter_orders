import sqlite3
import sys


class Database(object):
    def __init__(self):
        self._conn = sqlite3.connect('orders.db')

        self._c = self._conn.cursor()

        try:
            self._c.execute("""CREATE TABLE IF NOT EXISTS orders (
                        id int,
                        day_order int,
                        month_order int,
                        year_order int,
                        day_collect int,
                        month_collect int,
                        year_collect int,
                        fv_num text,
                        company text,
                        payment int,
                        object text,
                        color text,
                        quantity int        
                        )""")
        except:
              print('database init problem: ' ,sys.exc_info()[0])

        else: print('Database init OK!')

    def insertOrder(self,order):
        ind = self.__getNextIndex()
        for prod in order['products'].values():
            for element in prod:
                with self._conn:
                    self._c.execute("""INSERT INTO orders VALUES (:id, :day_order, :month_order, :year_order, :day_collect,
                                    :month_collect, :year_collect, :fv_num, :company, :payment,:object, :color, :quantity)""", 
                                    {'id': ind,
                                     'day_order': order['dateOrder'].day, 
                                     'month_order': order['dateOrder'].month, 
                                     'year_order': order['dateOrder'].year,
                                     'day_collect': order['dateCollect'].day, 
                                     'month_collect': order['dateCollect'].month, 
                                     'year_collect': order['dateCollect'].year,
                                     'fv_num': order['invoice'],
                                     'company': order['companyName'], 
                                     'payment': order['payment'],
                                     'object' : element.getModel(),
                                     'color' : element.getKind(),
                                     'quantity' : element.getNumber()
                                    })


    def getOrderby_companyName(self,name):
        self._c.execute("SELECT * FROM orders WHERE company=:companyName", {'companyName': name})
        return self._c.fetchall()

    def getOrderby_orderMonthandYear(self,month,year):
        self._c.execute("SELECT * FROM orders WHERE month_order=:month AND year_order=:year", {'month': month, 'year': year})
        rawArray = self._c.fetchall()
        output = []
        if rawArray: 
            last = rawArray[0][1:10]
            output.append(list(rawArray[0][1:]))
            for line in rawArray:
                 if not line[1:10] == last : 
                     output.append(list(line[1:]))
                     last = line[1:10]  
                     
        return  sorted(output, key=lambda a_entry: a_entry[0]) # sort all output orders by day order
                                                               # SO says its slower than NumPy - maybe to change in the future

    def remove_order(self, order):
        self._c.execute("""DELETE from orders WHERE day_order = :day_order 
                        AND month_order = :month_order
                        AND year_order = :year_order
                        AND company = :company""",
                      {'day_order': order['dateOrder'].day,
                      'month_order': order['dateOrder'].month,
                      'year_order': order['dateOrder'].year,
                       'company': order['companyName'] }) 
        self._conn.commit()

    def getOrderList_month_year(self, month, year):
        raw = self.getOrderby_orderMonthandYear(month,year)
        # rebuilding list of products
        #TODO:

    def getOneOrder(self, *,companyName, day_order, month_order, year_order):
        self._c.execute("""SELECT * FROM orders WHERE company=:companyName AND 
                         day_order= :day_order AND
                        month_order = :month_order AND 
                        year_order = :year_order """, 
                        {'companyName': companyName, 
                         'day_order' :  day_order, 
                         'month_order': month_order, 
                         'year_order': year_order})
        return self._c.fetchall()

    def getAllYears(self):
        return self.__getColumn( 'year_order' )

    # Check random column value-> if something exist return False
    def isDatabaseEmpty(self):
        if self.__getColumn( 'id' ): return False
        else: return True

    #function that get current individual order index
    def __getNextIndex(self):
        indexList = self.__getColumn( 'id' )
        if not indexList: return 0
        return max( indexList )

    def __getColumn(self, column):
        try:
            rawList = [el[0] for el in self._c.execute("SELECT "+column+" FROM orders" ) ]
        except:
            print('No such element or empty database!')
            return []
        else: return list(set(rawList))


    def updateOrder(self, newOrd, prevOrd): #orderManager objects
        from orderManager import OrderManager
        if isinstance(newOrd, dict) and isinstance(prevOrd, dict) :
            self.remove_order(prevOrd)
            self.insertOrder(newOrd)
        elif isinstance(newOrd, OrderManager) and isinstance(prevOrd, OrderManager):
            self.remove_order(prevOrd.getOrderDict())
            self.insertOrder(newOrd.getOrderDict())
        else : return False
        return True