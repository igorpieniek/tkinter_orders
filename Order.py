from tkinter import *
from Genre import Genre
from PDFgen import *
from tkcalendar import Calendar, DateEntry
from Database import *
import datetime

class Order():
    def __init__(self,root, rawArray = None):
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

        if rawArray: self.__reBuildOrder(rawArray)
    
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
    def addDummyClick(self, prodList = None):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(DummyLine( self.inputFrame[-1] , len(self.inputFrame) - 1, prodList) )

    def addStateClick(self, prodList = None):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(StandsLine( self.inputFrame[-1], len(self.inputFrame) - 1, prodList) )

    def addStateWoodClick(self, prodList = None):
        self._inputUpdate()
        self.addInputFrame()
        self.allProducts.append(WoodLine( self.inputFrame[-1], len(self.inputFrame) - 1, prodList) ) 

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

            for counter in self._lineNumToDel:             
                self.inputFrame.pop(counter)   #delate chosen frames           

            for i in range(len(self.inputFrame)):
                self.inputFrame[i].grid(row = self.allProducts[i].frameNum ,column = 0) # update frames which ramains

    # Function that update parameters in object in case one of them was deleted before
    def _updateProductsObj(self):
        counter = 0
        while counter < len(self.allProducts):
            if len(self.allProducts) != 0 and self.allProducts[counter].toDelate == True:
                self._lineNumToDel.append( self.allProducts[counter].frameNum)
                self.allProducts.pop(counter)
                k = counter
                while k < len(self.allProducts):
                    self.allProducts[k].frameNum -= 1
                    k +=1

            else: counter +=1

    # Function to close adding order window TODO
    def backClick(self):
        temp = self._database.getOrderby_orderMonthandYear(3,2021)
        for i in temp:
            print(i)
    # Action function executed afer clicking "Zapisz" - it create matrix and send it to database class
    def saveClick(self):
        # save to database
        arrayToSend = []
        for prod in self.allProducts:
            for i in range(len( prod.getData() )):
                arrayToSend.append([self._orderDate.day,   self._orderDate.month,   self._orderDate.year ,
                                    self._collectDate.day, self._collectDate.month, self._collectDate.year,
                                    self.invoice.get(), self.company.get(), self._getPayment(),
                                    prod.getModel(), prod.getColor(i), prod.getNumber(i) ])
        self._database.insertOrder(arrayToSend)

    # Fuction that uses pdfprocess and create pdf file
    def generatePDFClick(self):
        self._inputUpdate()
        self.pdf.process(self.allProducts,self.company)

    # Function contains adding all buttons
    def addMainButtons(self):
        self.buttons = []
        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj\nmanekiny",padx=5, pady=7, command = lambda:self.addDummyClick()))
        self.buttons[0].grid(row = 0,  column = 0,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj\nstatyw",padx=5, pady=7, command = lambda:self.addStateClick()))
        self.buttons[1].grid(row = 0, column = 1,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.addElementsFrame, text= "Dodaj statyw\ndrewniany",padx=5, pady=7, command = lambda:self.addStateWoodClick()))
        self.buttons[2].grid(row = 0, column = 2,padx=20, pady=3, sticky=W+N)

        self.buttons.append(Button(self.controlFrame, text= "Cofnij",padx=10, pady=3,width=10, command = lambda:self.backClick()))
        self.buttons[3].grid(row =0, column = 0, sticky=N)

        self.buttons.append(Button(self.controlFrame, text= "Zapisz",padx=10, pady=3,width=10, command = lambda:self.saveClick()))
        self.buttons[4].grid( row =1, column = 0, sticky=N)

        self.buttons.append(Button(self.controlFrame, text= "Generuj PDF\n zamówienie",padx=10, pady=3, width=10, command = lambda:self.generatePDFClick()))
        self.buttons[5].grid(row =2, column = 0, sticky=N)

        self.buttons.append(Button(self.controlFrame, text= "Generuj PDF\n koszulki",padx=10, pady=3,width=10, command = lambda:self.generatePDFClick()))
        self.buttons[6].grid(row =3, column = 0, sticky=N)

        self.buttons.append(Button(self.nameFrame, text='Data zamówienia', command=lambda:self._orderDateFun(0)))
        self.buttons[7].grid(row = 0, column = 3, padx=5, pady=3)

        self.buttons.append(Button(self.nameFrame, text='Data odbioru', command=lambda: self._orderDateFun(1)))
        self.buttons[8].grid(row = 0, column = 4, padx=5, pady=3)
    
    # Add oppurtunity to add company name, invoice number, payment and initialize choosing date
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

    # Add calendar
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
        
    # Update payment and return it
    def _getPayment(self):
        self._payment = int(self.paymentEntry.get())
        return self._payment

    # MAIN process of order object
    def process(self):
        self.addFrames()
        self.addEntrySection()
        self.addMainButtons()
        self.addDummyClick()


    def __reBuildOrder(self, rawArray):
        self.addFrames()
        self.addEntrySection()
        self.addMainButtons()
        dateOrder = datetime.date(day = rawArray[0][0], month = rawArray[0][1], year =rawArray[0][2])
        dateCollect =  datetime.date(day = rawArray[0][3], month = rawArray[0][4], year =rawArray[0][5])
        fvNum = rawArray[0][6]
        compName = rawArray[0][7]
        payment = rawArray[0][8]
        productsRaw = [el[9:] for el in rawArray] # geting onlu product info

        dummyDict = {line[0]: [] for line in productsRaw if line[0] in self.genre.dummys} #get all names of dummys in order
        woodenstands = []
        stands = []
        for line in productsRaw: #sorting data
            if line[0] in self.genre.dummys:
                dummyDict[line[0]].append(Dummy(line[0], line[1], line[2]))
            elif line[0] == 'Statyw drewniany':
                woodenstands.append(WoodenStand(line[1], line[2]))
            elif line[0] == 'Statyw metalowy':
                stands.append(Stand(line[1], line[2]))
        
        #sending data
        if dummyDict:
            for item in dummyDict: self.addDummyClick(dummyDict[item]) #send element
        if woodenstands: self.addStateWoodClick(woodenstands) #send wooden stand element
        if stands: self.addStateClick(stands) #send stand element
        

            



####################################################################################################################
class basicProduct():
    def __init__(self,* ,root ,frameNum, models, kinds,prodObj, rebuildList = None):
        self.__root = root
        self.frameNum = frameNum # number of frame in order array
        self._modelsList = models # list to model menu
        self._kindsList = kinds # list to kind menu
        self._prodObj = prodObj

        self._model = None
        self._modelOpt = None
        self._kind = []
        self._kindOpt = []
        self._number = []
        self.__lineNum = 0 #number of current line in frames

        self.toDelate = False #is number to delete

        self.addButtons() # add buttons 'delete' and 'add genre'

        if rebuildList : self.__rebuildFrame( rebuildList )
        else:  self._addInputLine()

    def addButtons(self):
        self._genreButton =  Button(self.__root, text= "dodaj rodzaj",padx=10, pady=0, command = lambda:self._addInputLine()) 
        self._genreButton.grid( row =1, column = 0)

        self._deleteButton = Button(self.__root, text= "usuń",padx=10, pady=0, command = lambda:self._delThisInputFrame()) 
        self._deleteButton.grid( row = 0, column = 3)

    # Function which add model menu or model label
    def _addModel(self, value = None):
        if isinstance(self._modelsList, str):    self.__addModelAsLabel()
        elif isinstance(self._modelsList, list): self.__addModelAsOptionMenu(value)

    def __addModelAsLabel(self):
        self._model = Label(self.__root, text = self._modelsList, padx=10, pady=0 )
        self._model.grid(row=0, column=0)

    def __addModelAsOptionMenu(self, value):
        [self._model, self._modelOpt ] = self.__addOptionMenu(optList = self._modelsList, 
                                              row = 0,
                                              column = 0,
                                              width = 5,
                                              initValue = value)
    
    # Function which add kind menu (eg. colors)
    def _addKind(self, value = None):
        [kind, menu ] = self.__addOptionMenu(optList = self._kindsList, 
                                              row = self.__lineNum,
                                              column = 1,
                                              width = 10,
                                              initValue = value)
        self._kind.append( kind )
        self._kindOpt.append( menu )

    # Main function of adding and configure option menu
    def __addOptionMenu(self,*, optList, row, column, width, initValue = None):
        outOption = StringVar()
        if initValue:  outOption.set( initValue )
        else : outOption.set(optList[0])
        optionMenu = OptionMenu(self.__root,  outOption, *optList) 
        optionMenu.configure(width = width)
        optionMenu.grid(padx=20, pady=0, row=row, column=column)
        return [outOption, optionMenu]

    # Function that add Entry place -> to write quantity of specified product
    def _addNumberEntry(self, value = None):
        var = IntVar()
        if value : var.set(value) 
        self._number.append( Entry(self.__root, width=4, textvariable = var) )
        self._number[-1].grid( row = self.__lineNum , column=2)
    
    # Function that add new line inside this Frame object
    def _addInputLine(self, kind = None, value = None, model = None):
        if   self.__lineNum < len(self._kindsList) -1:        
            if kind and value:
                if not self._model: self._addModel(model)
                self._addKind( kind )
                self._addNumberEntry(value)
            else:
                if not self._model: self._addModel(model)
                self._addKind()
                self._addNumberEntry()
            self.__lineNum += 1

    # To calculate sum of all products in this frame
    def sumCalculate(self):
        sum = 0
        for i in range(len( self._number)):
            sum +=int(self._number[i].get())
        return sum
    #### poprawione do tego miejsca
    def getData(self):
        allData = []

        for index in range(self.__lineNum):
            if self._prodObj == Dummy:  temp = self._prodObj(self._model.get(), self._kind[index].get(), int(self._number[index].get()) )
            else: temp = self._prodObj(self._kind[index].get(), int(self._number[index].get()) )
            if not temp.isEmpty(): 
                allData.append( temp )
        return allData

    def getModel(self):
        temp = self.getData()
        if temp :  return temp[0].getData()[0]
        else: return temp

    def getColor(self, index = None):
        data = self.getData()
        if not data: return []
        if index == None :
            temp = []
            for el in data:
                temp.append(el.getData()[1])
            return temp
        else : return data[index].getData()[1]

    def getNumber(self, index = None):
        data = self.getData()
        if not data: return []
        if index == None  :
            temp = []
            for el in data:
                temp.append(el.getData()[2])
            return temp
        else : return data[index].getData()[2]

    # Function whitch delete Frame and everything inside frame
    def _delThisInputFrame(self):
        if self.__lineNum  > 1:
            self._kind.pop(-1)
            self._kindOpt[-1].destroy()
            self._kindOpt.pop(-1)

            self._number[-1].destroy()
            self._number.pop(-1)
            self.__lineNum -= 1
        else:
            if self._modelOpt: self._modelOpt.destroy()
            self._genreButton.destroy()
            self._deleteButton.destroy()
            self.toDelate = True
            self.__root.destroy()
    
    # Function to rebuild frame from histry window
    def __rebuildFrame(self, list):
        self._addModel(list[0].getData()[0])
        for el in list: self._addInputLine( el.getData()[1], el.getData()[2] )
####################################################################################################################
from ProductClass.Dummy import *
from ProductClass.WoodenStand import *
from ProductClass.Stand import *

class DummyLine(basicProduct):
    def __init__(self,root ,frameNum, dummysList = None):
        self.__genre = Genre()
        super().__init__(root = root, 
                         frameNum = frameNum,
                         models = self.__genre.dummys , 
                         kinds = self.__genre.color,
                         prodObj = Dummy,
                         rebuildList = dummysList  )
        


#############################################################################################
class WoodLine(basicProduct):
    def __init__(self,root ,frameNum, woodLineList = None):
        self.__genre = Genre()
        super().__init__(root = root, 
                         frameNum = frameNum,
                         models = 'Statyw drewniany' , 
                         kinds = self.__genre.woodStands,
                         prodObj = WoodenStand,
                         rebuildList = woodLineList  )
        
#############################################################################################
class StandsLine(basicProduct):
    def __init__(self,root ,frameNum, standsLineList = None):
        self.__genre = Genre()
        super().__init__(root = root, 
                         frameNum = frameNum,
                         models = 'Statyw metalowy' , 
                         kinds = self.__genre.stands,
                         prodObj = Stand,
                         rebuildList = standsLineList  )

            