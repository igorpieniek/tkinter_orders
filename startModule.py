from tkinter import *

from History import *





class StartModule():
    def __init__(self,root):
        self._status = -1
        self._root = root
        self.clearWindow()
        self.process()

    def _newOrder(self):
        from Order import Order
        self._status = 1
        self.clearWindow()
        order = Order(self._root )
        order.process()

    def _history(self):
        self._status = 2
        self.clearWindow()
        history = History(self._root )

    def addButtons(self):
        self.buttons = []
        self.buttons.append(Button(self._root, text= "Nowe zamówienie",padx=10, pady=7, command = lambda:self._newOrder()))
        self.buttons.append(Button(self._root, text= "Historia zamówień",  padx=10, pady=7, command = lambda: self._history()))
        self.buttons.append(Button(self._root, text= "Zamknij", padx=10, pady=7, command = lambda: self._end()))

        for i in range(len(self.buttons)):
            self.buttons[i].pack()
    def _end(self):
        self._root.destroy()

    def clearWindow(self):
        for widget in self._root.winfo_children():
            widget.destroy()

    def process(self):
        self.addButtons()
        return self._status



