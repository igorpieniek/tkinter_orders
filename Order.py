from tkinter import *
from Genre import Genre
from PDFgen import *

class Order():
    def __init__(self,root):
        self.genre = Genre()
        self.pdf = PDFgen()
        self.root = root

        self.inputFrame = []
        self.Dummys = []
        self.Stands = []
        self.allProducts = []
        self._lineNumToDel = []


    def addInputFrame(self):
        self.inputFrame.append( LabelFrame(self.allInputsFrame, padx = 5, pady=5) )
        self.inputFrame[-1].grid(row = len(self.inputFrame)-1 ,column = 0, stick = N+W)



    def addFrames(self):
        self.addElementsFrame = LabelFrame(self.root, padx = 5, pady=5,width =300, background = "blue")
        self.addElementsFrame.grid(row = 0,column = 1, stick = W+N+E)

        self.allInputsFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.allInputsFrame.grid(row= 1,column = 1, stick = W+N+S)

        self.controlFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.controlFrame.grid(row= 0, rowspan = 2,column = 0, stick = W+N+S)

    def addDummyClick(self):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(DummyLine( self.inputFrame[len(self.inputFrame) - 1] , len(self.inputFrame) - 1) )

    def addStateClick(self):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(StandsLine( self.inputFrame[len(self.inputFrame) - 1], len(self.inputFrame) - 1) )

    def _inputUpdate(self):
        if self.allProducts and self.inputFrame: 
            self._updateProductsObj()
            self._updateInputFrames()
            self._lineNumToDel = []

    def _updateInputFrames(self):
        if self._lineNumToDel:
            counter = self._lineNumToDel[0]
            dynCounter = 0
            for counter in self._lineNumToDel:             
                self.inputFrame.pop(counter - dynCounter)              

            for i in range(len(self.inputFrame)):
                self.inputFrame[i].grid(row = self.allProducts[i].lineNum ,column = 0)


    def _updateProductsObj(self):
        counter = 0
        while counter < len(self.allProducts):
            if len(self.allProducts) != 0 and self.allProducts[counter].toDelate == True:
                self._lineNumToDel.append( self.allProducts[counter].lineNum)
                self.allProducts.pop(counter)
                k = counter
                while k < len(self.allProducts):
                    self.allProducts[k].lineNum -= 1
                    k +=1

            else: counter +=1


    def backClick():
        pass

    def saveClick():
        pass
   
    def generatePDFClick(self):
        self.pdf.process(self.allProducts)
        for i in range(len(self.allProducts)):   
            if isinstance(self.allProducts[i],DummyLine ):
                for k in range(len(self.allProducts[i].color)):
                    print(str(self.allProducts[i].model[0].get()) + " "+
                          str(self.allProducts[i].color[k].get()) + " "+
                          str(self.allProducts[i].number[k].get()))
            if isinstance(self.allProducts[i],StandsLine ): 
                for k in range(len(self.allProducts[i].value)):
                    print(str(self.allProducts[i].model[0].get()) + " "+
                          str(self.allProducts[i].value[k]))

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

    def __init__(self,root ,lineNum):
        self.root = root
        self.lineNum = lineNum

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
    def __init__(self,root, lineNum):
         self.root = root
         self.lineNum = lineNum

         self.genre = Genre()
         self.toDelate = False
         self.value = []

         self._addStand()

    def _addStand(self):
        self._addModel()
        self._addNumberEntry()

        self._delateButton = Button(self.root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) 
        self._delateButton.grid( row = 0, column = 3, stick = N+E)


    def _addNumberEntry(self):
        self.number = Entry(self.root, width=4) 
        self.number.grid( row= 0 , column=2)
        self.value.append(self.number.get())
    
    def _addModel(self):
        self.model = StringVar()
        self.model.set(self.genre.stands[0])
        self.modelopt = OptionMenu(self.root,  self.model,*self.genre.stands) 
        self.modelopt.configure(width = 5)
        self.modelopt.grid(padx=20, pady=0, row=0, column=0)

    def _delThisInputFrame(self):
        self.toDelate = True
        self.root.destroy()