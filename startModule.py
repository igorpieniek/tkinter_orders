from tkinter import *



class startModule():
    def __init__(self, root):
        self.root = root
    def newOrder():
        return
    def history():
        return
    def addButtons():
        buttons = []
        buttons.append(Button(self.root, text= "Nowe zamówienie",padx=10, pady=7, command = newOrder))
        buttons.append(Button(self.root, text= "Historia zamówień",  padx=10, pady=7, command = history))
        buttons.append(Button(self.root, text= "Zamknij", padx=10, pady=7, command = root.quit))

        for i in range(len(buttons)):
            buttons[i].pack()

    def startFrameProcess():
        addButtons()



