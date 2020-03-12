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
    #NEW ORDER
#elif manager.getStatus() == 2:
    #HISTORY



root.mainloop()
