from tkinter import *

from windowManager import windowManager
from Order import Order
from History import History
from Database import Database
from startModule import *

root = Tk()
root.geometry('550x450')
root.title('')

data = Database()
manager = windowManager(root,data)


root.mainloop()
