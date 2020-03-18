from tkinter import *
from Genre import Genre
from PDFgen import *
from tkcalendar import Calendar, DateEntry
from Database import *
import datetime

class Order():
    def __init__(self,root):
        self.genre = Genre()
        self.pdf = PDFgen()
        self.root = root
        self._database = Database()

        self.inputFrame = []
        self.Dummys = []
        self.Stands = []
        self.allProducts = []
        self._lineNumToDel = []
        self._payment = 0
        self._orderDate= datetime.date.today()
        self._collectDate= datetime.date.today()
    
    # Add new input frame for every Dummy/Stand/WoodenStand object
    def addInputFrame(self):
        self.inputFrame.append( LabelFrame(self.allInputsFrame, padx = 5, pady=5) )
        self.inputFrame[-1].grid(row = len(self.inputFrame)-1 ,column = 0, stick = N+W)

    # Add rest constans frames on order window 
    def addFrames(self):
        self.addElementsFrame = LabelFrame(self.root, padx = 5, pady=5,width =300, background = "blue")
        self.addElementsFrame.grid(row = 1,column = 1, stick = W+N+E)

        self.allInputsFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.allInputsFrame.grid(row= 2,column = 1, stick = W+N+S)

        self.controlFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.controlFrame.grid(row= 1, rowspan = 2,column = 0, stick = W+N+S)
        
        self.nameFrame = LabelFrame(self.root, padx = 5, pady=5)
        self.nameFrame.grid(row= 0, columnspan = 2,column = 0, stick = W+N+S)
    
    # Actions after click of button: creating new objects depends on what user want to add. Functions 
    # also update sequence of frames obcject in case some of them was previous delated
    def addDummyClick(self):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(DummyLine( self.inputFrame[len(self.inputFrame) - 1] , len(self.inputFrame) - 1) )

    def addStateClick(self):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(StandsLine( self.inputFrame[len(self.inputFrame) - 1], len(self.inputFrame) - 1) )

    def addStateWoodClick(self):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(WoodLine( self.inputFrame[len(self.inputFrame) - 1], len(self.inputFrame) - 1) ) 

    # Main objects update function. It contains 2 smaller functions. One is updating products object and second
    # to update frames which was connected to product object 
    def _inputUpdate(self):
        if self.allProducts and self.inputFrame: 
            self._updateProductsObj()
            self._updateInputFrames()
            self._lineNumToDel = []

    # Function that update product object frames
    def _updateInputFrames(self):
        if self._lineNumToDel:
            counter = self._lineNumToDel[0] 
            for counter in self._lineNumToDel:             
                self.inputFrame.pop(counter)   #delate chosen frames           

            for i in range(len(self.inputFrame)):
                self.inputFrame[i].grid(row = self.allProducts[i].lineNum ,column = 0) # update frames which ramains

    # Function that update parameters in object in case one of them was deleted before
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


    def backClick(self):
        temp = self._database.getOrderby_companyName('FEMI')
        for i in temp:
            print(i)

    def saveClick(self):
        # save to database
        arrayToSend = []
        for prod in self.allProducts:
            for i in range(len(prod.color)):
                if isinstance(prod,DummyLine ):
                     object = str(prod.model[0].get())
                elif isinstance(prod,StandsLine ):
                     object = 'statyw metalowy'
                elif isinstance(prod,WoodLine ):
                     object = 'statyw drwniany'
                arrayToSend.append([self._orderDate.day,   self._orderDate.month,   self._orderDate.year ,
                                    self._collectDate.day, self._collectDate.month, self._collectDate.year,
                                    self.invoice.get(), self.company.get(), self._getPayment(),
                                    object, prod.color[i].get(), int(prod.number[i].get()) ])
        self._database.insertOrder(arrayToSend)
   
    def generatePDFClick(self):
        self._inputUpdate()
        self.pdf.process(self.allProducts,self.company)

    def addMainButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj\nmanekiny",padx=5, pady=7, command = lambda:self.addDummyClick()))
        self.buttons[0].grid(row = 0,  column = 0,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj\nstatyw",padx=5, pady=7, command = lambda:self.addStateClick()))
        self.buttons[1].grid(row = 0, column = 1,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj statyw\ndrewniany",padx=5, pady=7, command = lambda:self.addStateWoodClick()))
        self.buttons[2].grid(row = 0, column = 2,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.controlFrame, text= "Cofnij",padx=10, pady=3, command = lambda:self.backClick()))
        self.buttons[3].grid(row =0, column = 0, sticky=N)

        self.buttons.append(Button(self.controlFrame, text= "Zapisz",padx=10, pady=3, command = lambda:self.saveClick()))
        self.buttons[4].grid( row =1, column = 0, sticky=N)

        self.buttons.append(Button(self.controlFrame, text= "Generuj PDF",padx=10, pady=3, command = lambda:self.generatePDFClick()))
        self.buttons[5].grid(row =2, column = 0, sticky=N)

        self.buttons.append(Button(self.nameFrame, text='Data zamówienia', command=lambda:self._orderDateFun(0)))
        self.buttons[6].grid(row = 0, column = 3, padx=5, pady=3)

        self.buttons.append(Button(self.nameFrame, text='Data odbioru', command=lambda: self._orderDateFun(1)))
        self.buttons[7].grid(row = 0, column = 4, padx=5, pady=3)

    def addEntrySection(self):
        self.companyLabel = Label(self.nameFrame, text= "Nazwa firmy",padx=10, pady=0 )
        self.companyLabel.grid(row=0, column=0)
        self.company = ( Entry(self.nameFrame, width=15 ,textvariable = StringVar()) )
        self.company.grid( row= 1 , column=0,padx = 10, pady=3, sticky = N+W+E)

        self.invoiceLabel = Label(self.nameFrame, text= "Faktura nr",padx=10, pady=0 )
        self.invoiceLabel.grid(row=0, column=1)
        self.invoice = ( Entry(self.nameFrame, width=15 ,textvariable = StringVar()) )
        self.invoice.grid( row= 1 , column=1,padx = 10, pady=3, sticky = N+W+E)

        self.paymentLabel = Label(self.nameFrame, text= "Płatność",padx=10, pady=0 )
        self.paymentLabel.grid(row=0, column=2)
        self.paymentEntry = ( Entry(self.nameFrame, width=5 ,textvariable = IntVar()) )
        self.paymentEntry.grid( row= 1 , column=2,padx = 10, pady=3, sticky = N+W+E)

        today = str(datetime.date.today().day)+'-'+str(datetime.date.today().month)+'-'+str(datetime.date.today().year)
        self.DateOrderLabel = Label(self.nameFrame, text = today,padx=10, pady=3 )
        self.DateOrderLabel.grid(row=1, column=3)

        self.DateCollectLabel = Label(self.nameFrame, text = '',padx=10, pady=3 )
        self.DateCollectLabel.grid(row=1, column=4)


    def _orderDateFun(self, ver):
        def print_sel():
            if ver == 0: 
                self._orderDate = cal.selection_get()
                self.DateOrderLabel.config(text = str(self._orderDate.day) +'-'+str(self._orderDate.month) +'-'+str(self._orderDate.year) )
            elif ver==1 :
               self._collectDate = cal.selection_get()
               self.DateCollectLabel.config(text = str(self._collectDate.day) +'-'+str(self._collectDate.month) +'-'+str(self._collectDate.year) )
            top.destroy()

        top = Toplevel(self.root)    
        today = datetime.date.today()
    
        cal = Calendar(top, font="Arial 14", selectmode='day',
                           disabledforeground='red',
                           cursor="hand1", year=today.year, month=today.month, day=today.day)
        cal.pack(fill="both", expand=True)
        Button(top, text="ok", command=print_sel).pack()            

    def _getPayment(self):
        self._payment = int(self.paymentEntry.get())
        return self._payment


    def genreOptAction(self, gen):
        if gen == self.genre.gen[0]:
            pass
        else:
            pass


    def process(self):
        self.addFrames()
        self.addEntrySection()
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
        self.number.append( Entry(self.root, width=4, textvariable = IntVar()) )
        self.number[len(self.number)-1].grid( row= self._colorNum , column=2)

    def _addInputLine(self):
        if   self._colorNum < len(self.genre.color) -1:
            self._colorNum += 1
            self._addDummyColor()
            self._addNumberEntry()

    def sumCalculate(self):
        sum = 0
        for i in range(len( self.number)):
            sum +=int(self.number[i].get())
        return sum
    
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
class WoodLine():

    def __init__(self,root ,lineNum):
        self.root = root
        self.lineNum = lineNum

        self.color = []
        self.coloropt = []
        self.number = []
        self._genreButtons = []
        self._delateButtons = []
        self.genre = Genre()
        self._colorNum = 0

        self.toDelate = False

        self.addWoodClick()

    def addWoodClick(self):     
        self._addModel()
        self._addWoodColor()
        self._addNumberEntry()
    
        self._genreButtons.append( Button(self.root, text= "dodaj rodzaj",padx=10, pady=0, command = lambda:self._addInputLine()) )
        self._genreButtons[len(self._genreButtons)-1].grid( row =1, column = 0)

        self._delateButtons.append( Button(self.root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) )
        self._delateButtons[len(self._delateButtons)-1].grid( row = 0, column = 3)

    def _addModel(self):

        self.model = Label(self.root, text= "Statyw drewniany",padx=10, pady=0 )
        self.model.grid(row=0, column=0)


    def _addWoodColor(self):
        self.color.append(StringVar())
        self.color[ len(self.color)-1 ].set(self.genre.woodStands[self._colorNum])
        self.coloropt.append( OptionMenu(self.root, self.color[ len(self.color)-1 ],*self.genre.woodStands))
        self.coloropt[ len(self.coloropt)-1 ].config(width = 10)
        self.coloropt[ len(self.coloropt)-1 ].grid(padx=20, pady=0,  row= self._colorNum, column=1)


    def _addNumberEntry(self):
        self.number.append( Entry(self.root, width=4,textvariable = IntVar()) )
        self.number[len(self.number)-1].grid( row= self._colorNum , column=2)
    
    def sumCalculate(self):
        sum = 0
        for i in range(len( self.number)):
            sum +=int(self.number[i].get())
        return sum
    def _addInputLine(self):
        if   self._colorNum < len(self.genre.woodStands)-1:
            self._colorNum += 1
            self._addWoodColor()
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
    def __init__(self,root ,lineNum):
        self.root = root
        self.lineNum = lineNum

        self.color = []
        self.coloropt = []
        self.number = []
        self._genreButtons = []
        self._delateButtons = []
        self.genre = Genre()
        self._colorNum = 0

        self.toDelate = False

        self.addStandsClick()

    def addStandsClick(self):     
        self._addModel()
        self._addStandsColor()
        self._addNumberEntry()
    
        self._genreButtons.append( Button(self.root, text= "dodaj rodzaj",padx=10, pady=0, command = lambda:self._addInputLine()) )
        self._genreButtons[len(self._genreButtons)-1].grid( row =1, column = 0)

        self._delateButtons.append( Button(self.root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) )
        self._delateButtons[len(self._delateButtons)-1].grid( row = 0, column = 3)

    def _addModel(self):

        self.model = Label(self.root, text= "Statyw metalowy",padx=10, pady=0 )
        self.model.grid(row=0, column=0)


    def _addStandsColor(self):
        self.color.append(StringVar())
        self.color[ len(self.color)-1 ].set(self.genre.stands[self._colorNum])
        self.coloropt.append( OptionMenu(self.root, self.color[ len(self.color)-1 ],*self.genre.stands))
        self.coloropt[ len(self.coloropt)-1 ].config(width = 10)
        self.coloropt[ len(self.coloropt)-1 ].grid(padx=20, pady=0,  row= self._colorNum, column=1)


    def _addNumberEntry(self):
        self.number.append( Entry(self.root, width=4,textvariable = IntVar()) )
        self.number[len(self.number)-1].grid( row= self._colorNum , column=2)
    
    def sumCalculate(self):
        sum = 0
        for i in range(len( self.number)):
            sum +=int(self.number[i].get())
        return sum

    def _addInputLine(self):
        if   self._colorNum < len(self.genre.stands)-1:
            self._colorNum += 1
            self._addStandsColor()
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
            