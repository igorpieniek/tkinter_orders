import sqlite3

class Database(object):
    def __init__(self):
        self._conn = sqlite3.connect('orders.db')

        self._c = self._conn.cursor()
        try:
            self._c.execute("""CREATE TABLE orders (
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
        for oneLine in order:
            with self._conn:
                self._c.execute("""INSERT INTO orders VALUES (:day_order, :mouth_order, :year_order, :day_collect,
                                :mouth_collect, :year_collect, :fv_num, :company, :payment,:object, :color, :quantity)""", 
                                {'day_order': oneLine[0], 
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
        return self._c.fetchall()

    def update_Payment(self, order, pay):
        with self._conn:
            self._c.execute("""UPDATE employees SET pay = :pay
                        WHERE first = :first AND last = :last""",
                      {'first': emp.first, 'last': emp.last, 'pay': pay})


    def remove_order(self, order):
        with conn:
            c.execute("DELETE from employees WHERE first = :first AND last = :last",
                      {'first': emp.first, 'last': emp.last})  


