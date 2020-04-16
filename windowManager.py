from History import History
from Database import Database
from startModule import StartModule
from Order import Order
from tkinter import *

class windowManager():
    def __init__(self,root):
        self.__root = root

        self.__currentWindow = self.__windowInit('start')
        self.__topWindow = []

    def __windowInit(self, name, reArray =None):
        if name == 'start': return StartModule(self.__root,)
        elif name == 'order':  return Order(self.__root, reArray )
        elif name == 'history':  return  History(self.__root, )
        else: print('No such window name')

    def backToLastWindow(self):
        if isinstance(self.__currentWindow, Order) or isinstance(self.__currentWindow, History):
            self.__clearWindow()
            del self.__currentWindow
            self.__currentWindow = self.__windowInit('start')
        else: print('There is no option to get back!')

    def changeWindow(self, name):
        if  isinstance(self.__currentWindow, StartModule): 
            self.__clearWindow()
            del self.__currentWindow
            self.__currentWindow = self.__windowInit(name)

    def newRebuildOrderWindow(self,*,array):
        self.__topWindow = TopLevel(self.__root)
        reOrder = self.__windowInit('order', array)


    def __clearWindow(self):
        for widget in self.__root.winfo_children():
            widget.destroy()



