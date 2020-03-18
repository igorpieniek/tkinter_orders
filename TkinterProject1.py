from tkinter import *

from windowManager import windowManager
from Order import Order


root = Tk()
root.geometry('600x800')

global manager
manager = windowManager(0)

from startModule import startModule
startwin = startModule(root)

orderFrame = LabelFrame(root, padx = 10, pady=10,width=500)
orderFrame.grid(row = 0, column  =0)


order = Order(orderFrame)

if manager.getStatus() == 'START':
      #START WINDOW
    order.process()
    #status = startwin.process()
    #if status != -1:  
     #   manager.setStatus(manager.options[status])
  
elif manager.getStatus() == 'NEW_ORDER':
    order.process()


# SQLite3 test
#import sqlite3

#conn = sqlite3.connect('orders.db')

#c = conn.cursor()
#c.execute("""CREATE TABLE orders (
#            day_order integer,
#            mouth_order integer,
#            year_order integer,
#            day_collect integer,
#            mouth_collect integer,
#            year_collect integer,
#            fv_num text,
#            company text,
#            payment integer,
#            object  text,
#            color   text,
#            quantity    integer         
#            )""")
#c.execute("INSERT INTO orders VALUES (10,10,2010,12,12,2012, 'EX10/2015', 'dummyMASTERS', 2137, 'D5', 'czarny', 125)")
#c.execute("SELECT * FROM orders WHERE year_order = 2010")
#k = c.fetchall()
#conn.commit()

#conn.close()

root.mainloop()
