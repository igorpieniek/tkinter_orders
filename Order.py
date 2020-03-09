from tkinter import *
from Genre import Genre

class Order():
    def __init__(self,root):
        self.genre = Genre()
        self.root = root


        self.inputFrame = []
        self.Dummys = []
        self.Stands = []


    def addInputFrame(self):
        self.inputFrame.append( LabelFrame(self.root, padx = 5, pady=5) )
        self.inputFrame[-1].grid(row = len(self.inputFrame) ,column = 1, stick = N+W)




    def addFrames(self):
        self.addElementsFrame = LabelFrame(self.root, padx = 5, pady=5,width =300, background = "blue")
        self.addElementsFrame.grid(row = 0,column = 1, stick = W+N+E)

        self.controlFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.controlFrame.grid(row= 0, rowspan = 2,column = 0, stick = W+N+S)

    def addDummyClick(self):
        self._updateDummysObj()
        self._updateStandsObj()
        self._updateInputFrames()

        self.addInputFrame()
        self.Dummys.append(DummyLine( self.inputFrame[len(self.inputFrame) - 1]))
  
    def _updateInputFrames(self):
        print("Ilosc ramek " +str(len(self.inputFrame)))
        for i in range(len(self.inputFrame)):
            print("Licznik " + str(i))
            self.inputFrame[i].grid(row = 1+i ,column = 1, stick = N+W)

    def _updateDummysObj(self):
        counter = 0
        while counter < len(self.Dummys):
            if len(self.Dummys) != 0 and self.Dummys[counter].toDelate == True:
                self.Dummys.pop(counter)
                self.inputFrame[counter].destroy()
                self.inputFrame.pop(counter)

            else : counter += 1

    def addStateClick(self):
        self._updateDummysObj()
        self._updateStandsObj()
        self._updateInputFrames()

        self.addInputFrame()
        self.Stands.append(StandsLine( self.inputFrame[len(self.inputFrame) - 1]))


    def _updateStandsObj(self): # could be merged with updateDummys by reference
        counter = 0
        while counter < len(self.Stands):
            if len(self.Stands) != 0 and self.Stands[counter].toDelate == True:
                self.Stands.pop(counter)
                self.inputFrame[counter].destroy()
                self.inputFrame.pop(counter)

            else : counter += 1


    def backClick():
        pass

    def saveClick():
        pass
   
    def generatePDFClick():
        pass

    def addMainButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj manekiny",padx=10, pady=7, command = lambda:self.addDummyClick()))
        self.buttons[0].grid(row = 0,  column = 0,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj statyw",padx=10, pady=7, command = lambda:self.addStateClick()))
        self.buttons[1].grid(row = 0, column = 1,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.controlFrame, text= "Cofnij",padx=10, pady=3, command = lambda:self.backClick()))
        self.buttons[2].grid( sticky=S)

        self.buttons.append(Button(self.controlFrame, text= "Zapisz",padx=10, pady=3, command = lambda:self.saveClick()))
        self.buttons[3].grid( sticky=S)

        self.buttons.append(Button(self.controlFrame, text= "Generuj PDF",padx=10, pady=3, command = lambda:self.generatePDFClick()))
        self.buttons[4].grid( sticky=S)
    

    def genreOptAction(self, gen):
        if gen == self.genre.gen[0]:
            pass
        else:
            pass


    def process(self):
        self.addFrames()
        self.addMainButtons()
        self.addDummyClick()



####################################################################################################################
class DummyLine():

    def __init__(self,root):
        self.root = root
        self.model = []
        self.modelopt = []
        self.color = []
        self.coloropt = []
        self.number = []
        self._genreButtons = []
        self._delateButtons = []
        self.genre = Genre()
        self._colorNum = 0

        self.toDelate = False

        self.addDummyClick()

    def addDummyClick(self):     
        self._addModel()
        self._addDummyColor()
        self._addNumberEntry()
    
        self._genreButtons.append( Button(self.root, text= "dodaj rodzaj",padx=10, pady=0, command = lambda:self._addInputLine()) )
        self._genreButtons[len(self._genreButtons)-1].grid( row =1, column = 0)

        self._delateButtons.append( Button(self.root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) )
        self._delateButtons[len(self._delateButtons)-1].grid( row = 0, column = 3)

    def _addModel(self):
        self.model.append(StringVar())
        self.model[ len(self.model)-1 ].set(self.genre.dummys[0])
        self.modelopt.append( OptionMenu(self.root,  self.model[ len(self.model)-1 ],*self.genre.dummys) )
        self.modelopt[ len(self.modelopt)-1 ].configure(width = 5)
        self.modelopt[ len(self.modelopt)-1 ].grid(padx=20, pady=0, row=0, column=0)

    def _addDummyColor(self):
        self.color.append(StringVar())
        self.color[ len(self.color)-1 ].set(self.genre.color[self._colorNum])
        self.coloropt.append( OptionMenu(self.root, self.color[ len(self.color)-1 ],*self.genre.color) )
        self.coloropt[ len(self.coloropt)-1 ].config(width = 10)
        self.coloropt[ len(self.coloropt)-1 ].grid(padx=20, pady=0,  row= self._colorNum, column=1)


    def _addNumberEntry(self):
        self.number.append( Entry(self.root, width=4) )
        self.number[len(self.number)-1].grid( row= self._colorNum , column=2)

    def _addInputLine(self):
        if   self._colorNum < len(self.genre.color) -1:
            self._colorNum += 1
            self._addDummyColor()
            self._addNumberEntry()
        
    
    def _delThisInputFrame(self):
        if len(self.color)>1:
            self.color.pop(-1)
            self.coloropt[-1].destroy()
            self.coloropt.pop(-1)

            self.number[-1].destroy()
            self.number.pop(-1)
            self._colorNum -= 1
        else:
            self.toDelate = True
            self.root.destroy()
        
#############################################################################################
class StandsLine():
    def __init__(self,root):
         self.root = root
         self.genre = Genre()
         self.toDelate = False

         self._addStand()

    def _addStand(self):
        self._addModel()
        self._addNumberEntry()

        self._delateButton = Button(self.root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) 
        self._delateButton.grid( row = 0, column = 3)


    def _addNumberEntry(self):
        self.number = Entry(self.root, width=4) 
        self.number.grid( row= 0 , column=2)
    
    def _addModel(self):
        self.model = StringVar()
        self.model.set(self.genre.stands[0])
        self.modelopt = OptionMenu(self.root,  self.model,*self.genre.stands) 
        self.modelopt.configure(width = 5)
        self.modelopt.grid(padx=20, pady=0, row=0, column=0)

    def _delThisInputFrame(self):
        self.toDelate = True
        self.root.destroy()