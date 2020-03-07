from tkinter import *




class startModule():
    def __init__(self,root):
        self._status = -1
        self.root = root

    def newOrder(self):
        self._status = 1
        self.quit()

    def history(self):
        self._status = 2
        self.quit()

    def addButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.root, text= "Nowe zamówienie",padx=10, pady=7, command = lambda:self.newOrder()))
        self.buttons.append(Button(self.root, text= "Historia zamówień",  padx=10, pady=7, command = lambda: self.history()))
        self.buttons.append(Button(self.root, text= "Zamknij", padx=10, pady=7, command = self.root.quit))

        for i in range(len(self.buttons)):
            self.buttons[i].pack()

    def quit(self):
        for i in range(len(self.buttons)):
            self.buttons[i].pack_forget()

    def process(self):
        self.addButtons()
        return self._status



