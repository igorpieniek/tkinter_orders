from tkinter import *
from Genre import Genre

class Order():
    def __init__(self,root):
        self.genre = Genre()
        self.root = root

    def addFrames(self):
        self.addElementsFrame = LabelFrame(root, padx = 5, pady=5)
        self.addElementsFrame.grid(row = 0,column = 1)
        self.addElementsFrame.pack()

        self.inputFrame = LabelFrame(root, padx = 5, pady=5)
        self.inputFrame.grid(row = 1,column = 1)
        self.inputFrame.pack()

        self.controlFrame = LabelFrame(root, padx = 5, pady=5)
        self.controlFrame.grid(rowspan = 3,column = 0)
        self.controlFrame.pack()
 
        self.orderListFrame = LabelFrame(root, padx = 5, pady=5)
        self.orderListFrame.grid(row = 2,column = 1)
        self.orderListFrame.pack()

    def addOrderClick():
        pass

    def addGenreClick():
        pass

    def backClick():
        pass

    def saveClick():
        pass
   
    def generatePDFClick():
        pass

    def addButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj",padx=10, pady=7, command = lambda:self.addOrderClick()))
        self.buttons[0].grid(column = 0, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj rodzaj",padx=10, pady=7, command = lambda:self.addGenreClick()))
        self.buttons[1].grid(column = 1, sticky=W+N)

        self.buttons.append(Button(self.controlFrame, text= "Cofnij",padx=10, pady=7, command = lambda:self.backClick()))
        self.buttons[2].grid( sticky=S+W)

        self.buttons.append(Button(self.controlFrame, text= "Zapisz",padx=10, pady=7, command = lambda:self.saveClick()))
        self.buttons[3].grid( sticky=S+W)

        self.buttons.append(Button(self.controlFrame, text= "Generuj PDF",padx=10, pady=7, command = lambda:self.generatePDFClick()))
        self.buttons[4].grid( sticky=S+W)

        
        for i in range(len(self.buttons)):
            self.buttons[i].pack()

    def process(self):
        self.addFrames()
        self.addButtons()


