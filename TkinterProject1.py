from tkinter import *

from windowManager import windowManager
from Order import Order


root = Tk()
root.geometry('800x400')

global manager
manager = windowManager(0)

from startModule import startModule
startwin = startModule(root)

order = Order(root)

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
