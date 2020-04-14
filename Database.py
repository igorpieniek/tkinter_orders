import sqlite3

class Database(object):
    def __init__(self):
        self._conn = sqlite3.connect('orders.db')

        self._c = self._conn.cursor()
        try:
            self._c.execute("""CREATE TABLE orders (
                        index integer,
                        day_order integer,
                        mouth_order integer,
                        year_order integer,
                        day_collect integer,
                        mouth_collect integer,
                        year_collect integer,
                        fv_num text,
                        company text,
                        payment integer,
                        object  text,
                        color   text,
                        quantity    integer         
                        )""")
        except:
              print('database init OK!')
    def insertOrder(self,order):
        ind = self.__getNextIndex()
        for oneLine in order:
            with self._conn:
                self._c.execute("""INSERT INTO orders VALUES (:index :day_order, :mouth_order, :year_order, :day_collect,
                                :mouth_collect, :year_collect, :fv_num, :company, :payment,:object, :color, :quantity)""", 
                                {'index': ind,
                                 'day_order': oneLine[0], 
                                 'mouth_order': oneLine[1], 
                                 'year_order': oneLine[2],
                                 'day_collect': oneLine[3], 
                                 'mouth_collect': oneLine[4], 
                                 'year_collect': oneLine[5],
                                 'fv_num': oneLine[6],
                                 'company': oneLine[7], 
                                 'payment': oneLine[8],
                                 'object' : oneLine[9],
                                 'color' : oneLine[10],
                                 'quantity' : oneLine[11]
                                })


    def getOrderby_companyName(self,name):
        self._c.execute("SELECT * FROM orders WHERE company=:companyName", {'companyName': name})
        return self._c.fetchall()

    def getOrderby_orderMonthandYear(self,month,year):
        self._c.execute("SELECT * FROM orders WHERE mouth_order=:month AND year_order=:year", {'month': month, 'year': year})
        rawArray = self._c.fetchall()
        output = []
        if rawArray: 
            last = rawArray[0][:9]
            output.append(rawArray[0])
            for line in rawArray:
                 if not line[:9] == last : 
                     output.append(line)
                     last = line[:9]
        return output

    def update_Payment(self, order, pay):
        with self._conn:
            self._c.execute("""UPDATE employees SET pay = :pay
                        WHERE first = :first AND last = :last""",
                      {'first': emp.first, 'last': emp.last, 'pay': pay})


    def remove_order(self, order):
        with conn:
            c.execute("DELETE from employees WHERE first = :first AND last = :last",
                      {'first': emp.first, 'last': emp.last})  

    def getOrderList_month_year(self, month, year):
        raw = self.getOrderby_orderMonthandYear(month,year)
        # rebuilding list of products
        #TODO:

    def getOneOrder(self, *,companyName, day_order, month_order, year_order):
        self._c.execute("""SELECT * FROM orders WHERE company=:companyName AND 
                         day_order= :day_order AND
                        mouth_order = :month_order AND 
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
        if self.__getColumn( 'index' ): return False
        else: return True

    #function that get current individual order index
    def __getNextIndex(self):
        indexList = self.__getColumn( 'index' )
        if not indexList: return 0
        return max( indexList )

    def __getColumn(self, column):
        try:
            rawList = [el[0] for el in self._c.execute("SELECT "+column+" FROM orders" ) ]
        except:
            print('No such element or empty database!')
            return []
        else: return list(set(rawList))

