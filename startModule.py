from tkinter import *


class StartModule():
    def __init__(self,*,root,  windowManager, openMenu = True):
        self.__windowManager = windowManager
        self._root = root
        if openMenu:
            self.process()

    def __newOrder(self):
        self.__windowManager.changeWindow('order')

    def __history(self):
        self.__windowManager.changeWindow('history')
    
    def __settings(self):
        pass

    def __end(self):
        self._root.destroy()

    def addButtons(self):
        self.buttons = []
        self.buttons.append(Button(self._root, text= "Nowe zamówienie",padx=10, pady=7, command = lambda:self.__newOrder()))
        self.buttons.append(Button(self._root, text= "Historia zamówień",  padx=10, pady=7, command = lambda: self.__history()))
        self.buttons.append(Button(self._root, text= "Ustawienia", padx=10, pady=7, command = lambda: self.__settings()))
        self.buttons.append(Button(self._root, text= "Zamknij", padx=10, pady=7, command = lambda: self.__end()))

        for i in range(len(self.buttons)):
            self.buttons[i].pack()



    def process(self):
        self.addButtons()



