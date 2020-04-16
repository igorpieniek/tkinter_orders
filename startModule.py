from tkinter import *


class StartModule():
    def __init__(self,*,root,  windowManager, openMenu = True):
        self.__windowManager = windowManager
        self._root = root
        if openMenu:
            self.process()

    def _newOrder(self):
        self.__windowManager.changeWindow('order')

    def _history(self):
        self.__windowManager.changeWindow('history')

    def addButtons(self):
        self.buttons = []
        self.buttons.append(Button(self._root, text= "Nowe zamówienie",padx=10, pady=7, command = lambda:self._newOrder()))
        self.buttons.append(Button(self._root, text= "Historia zamówień",  padx=10, pady=7, command = lambda: self._history()))
        self.buttons.append(Button(self._root, text= "Zamknij", padx=10, pady=7, command = lambda: self._end()))

        for i in range(len(self.buttons)):
            self.buttons[i].pack()
    def _end(self):
        self._root.destroy()


    def process(self):
        self.addButtons()



