from tkinter import *
from tkinter import ttk
from Database import Database
import datetime

class History(object):
    def __init__(self,root,database):          
        self._root = root
        self._database = database

        self.__monthNames = ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 
                             'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień']
        self.__updateAvailableYears()
        self._addFrames();
        self.__addButtons()
        self.__addDateOptions()
        self._addTree()
        self._addLines()
        self._tree.pack()


    def _addFrames(self):
        self.__controlFrame = LabelFrame(self._root,width =300)
        self.__controlFrame.grid(row = 0,column = 0, stick = W+N+E)

        self.__editFrame = LabelFrame(self._root, width =50)
        self.__editFrame.grid(row = 0,column = 1, stick = W+N+E)

        self.__treeFrame = LabelFrame(self._root, padx = 5, pady=5)
        self.__treeFrame.grid(row= 1,column = 0, columnspan= 2, stick = W+N+S)
    
    def __addButtons(self):
        
        self.__OKButton = Button(self.__controlFrame, text= "OK",padx=10, pady=7, command = lambda:self.__updateTree() )
        self.__OKButton.grid(row = 0, column = 2, padx=5, pady=3)

        self.__editButton = Button(self.__editFrame, text= "edytuj",padx=10, pady=7, state = DISABLED,command = lambda:self.__editOrder() )
        self.__editButton.grid(row = 0, column = 0, padx=5, pady=3)

    def __addDateOptions(self):
        self.__month = StringVar()
        self.__month.set(self.__monthNames[datetime.date.today().month-1])
        self.__monthOpt = OptionMenu(self.__controlFrame,  self.__month, *self.__monthNames) 
        self.__monthOpt.configure(width = 10)
        self.__monthOpt.grid(padx=20, pady=0, row=0, column=0)

        self.__year = IntVar()
        self.__year.set(datetime.date.today().year)
        self.__yearOpt = OptionMenu(self.__controlFrame,  self.__year, *self.__availableYears) 
        self.__yearOpt.configure(width = 10)
        self.__yearOpt.grid(padx=20, pady=0, row=0, column=1)



    def _addTree(self):
        self._tree = ttk.Treeview(self.__treeFrame, columns = ( "Lp.","Nazwa firmy", "Data zamówienia","Nr faktury","Kwota",) )
        self._tree['show'] = 'headings' #removig first column

        self._tree.heading("Lp.",text="Lp.")
        self._tree.heading("Nazwa firmy", text="Nazwa firmy")
        self._tree.heading("Data zamówienia", text="Data zamówienia")
        self._tree.heading("Nr faktury", text="Nr faktury")
        self._tree.heading("Kwota", text="Kwota")

        self._tree.column("Lp.", width=20, minwidth=20, stretch=NO)
        self._tree.column("Nazwa firmy", width=90, minwidth=40)
        self._tree.column("Data zamówienia", width=100, minwidth=50)
        self._tree.column("Nr faktury", width=90, minwidth=50)
        self._tree.column("Kwota", width=40, minwidth=30)

        #self._tree.heading("#0",text="name",anchor=w)
        #self._tree.heading("one", text="date modified",anchor=w)
        #self._tree.heading("two", text="type",anchor=w)
        #self._tree.heading("three", text="size",anchor=w)
    def __updateTree(self):
        #TODO : update tree after OK click - read month & year, clear tree + add orders from this month
        pass
    def __editOrder(self):
        #TODO: open new Order window with marked order
        pass
    def __updateAvailableYears(self):
        self.__availableYears = self._database.getAllYears()
        
    def _readDatabase(self,month = None,year = None):

        if month == None : month = datetime.date.today().month
        if year == None : year = datetime.date.today().year
        self._rawArray = self._database.getOrderby_orderMonthandYear( month,year)

    def _addLines(self):
        self._readDatabase()
        for index,line in enumerate(self._rawArray):
            self._tree.insert("",str(index),values = (str(index), 
                                                 line[7], 
                                                 str(line[0])+'-'+str(line[1])+'-'+str(line[2]),
                                                 line[6],
                                                 str(line[8]) ) )

                    
