from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Database import Database
from startModule import *
import datetime
from Order import *

class History(object):
    def __init__(self,*,root, database,windowManager):          
        self._root = root
        self.__windowManager = windowManager
        self._database = database
        if self._database.isDatabaseEmpty():
            self.__databaseErrorAction()
            return

        self.__monthNames = ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 
                             'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień']
        self.__todeleteOrder = {} # declaration of order dictionary to removing from database

        self.__updateAvailableYears()
        self._addFrames();
        self.__addButtons()
        self.__addDateOptions()
        self.__addScrollbar()
        self._addTree()
        self.__updateTree()


    def _addFrames(self):
        self.__controlFrame = LabelFrame(self._root, width=407, height=40)
        self.__controlFrame.grid_propagate(False)
        self.__controlFrame.grid(row = 0,column = 0, stick = W+N+S)


        self.__treeFrame = LabelFrame(self._root, padx = 5, pady=5,)
        self.__treeFrame.grid(row= 1,column = 0,  stick = W+N+S)
    
    def __addButtons(self):       
        self.__backButton = Button(self.__controlFrame, text= "cofnij",padx=10, pady=2, command = lambda:self.__backToMainMenu() )
        self.__backButton.grid(row = 0, column = 2, padx=5, pady=3)

        self.__delButton = Button(self.__controlFrame, text= "usuń",padx=10, pady=2, state=DISABLED, command = lambda:self.__deleteOrder() )
        self.__delButton.grid(row = 0, column = 3, padx=5, pady=3)


    def __addDateOptions(self):
        self.__month = StringVar()
        self.__month.set(self.__monthNames[datetime.date.today().month-1])
        self.__monthOpt = OptionMenu(self.__controlFrame,  self.__month, command = lambda x : self.__updateTree(), *self.__monthNames) 
        self.__monthOpt.configure(width = 10)
        self.__monthOpt.grid(padx=5, pady=0, row=0, column=0)

        self.__year = IntVar()
        self.__year.set(datetime.date.today().year)
        self.__yearOpt = OptionMenu(self.__controlFrame,  self.__year, command = lambda x : self.__updateTree(), *self.__availableYears) 
        self.__yearOpt.configure(width = 10)
        self.__yearOpt.grid(padx=5, pady=0, row=0, column=1)



    def _addTree(self):
        self._tree = ttk.Treeview(self.__treeFrameCanv, columns = ( "Lp.","Nazwa firmy", "Data zamówienia","Nr faktury","Kwota",) )
        self._tree['show'] = 'headings' #removig first column

        self._tree.heading("Lp.",text="Lp.")
        self._tree.heading("Nazwa firmy", text="Nazwa firmy")
        self._tree.heading("Data zamówienia", text="Data zamówienia")
        self._tree.heading("Nr faktury", text="Nr faktury")
        self._tree.heading("Kwota", text="Kwota")

        self._tree.column("Lp.", width=20, minwidth=20, stretch=NO)
        self._tree.column("Nazwa firmy", width=100, minwidth=40)
        self._tree.column("Data zamówienia", width=100, minwidth=50)
        self._tree.column("Nr faktury", width=100, minwidth=50)
        self._tree.column("Kwota", width=60, minwidth=30)

        self._tree.bind("<ButtonRelease-1>", self.__singleClick) #single mouse click action
        self._tree.bind("<Double-1>", self.__OnDoubleClick) #double mouse click action


        self._tree.configure(height = 25)
        self._tree.grid(padx=5, pady=5, )
    
    def __addScrollbar(self):
        def scrollAction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas = Canvas( self.__treeFrame)
        self.__treeFrameCanv = Frame(canvas)
        self.__scroll = Scrollbar(self.__treeFrame, orient = 'vertical', command = canvas.yview)
        canvas.configure( yscrollcommand = self.__scroll.set )
        self.__scroll.pack( side = 'right', fill = 'y' )
        canvas.pack( side = 'left' )
        canvas.create_window( (0,0),window= self.__treeFrameCanv, anchor='nw' )
        self.__treeFrameCanv.bind("<Configure>", scrollAction)

    def __updateTree(self):
        self.__delButton.configure(state=DISABLED)
        self._tree.delete(*self._tree.get_children()) #clear all tree window
        month = self.__monthNames.index(self.__month.get()) + 1 # getting month number (+1 because of numering starts from 1)
        year = int(self.__year.get())
        self._readDatabase(month,year)
        self._addLines()

    def __singleClick(self,event):
        if self._tree.selection():
            self.__delButton.configure(state=ACTIVE)
            item  = self._tree.item( self._tree.focus() )['values']
            dateSep = item[2].split('-')
            dateSep = [int(i) for i in dateSep]
            self.__todeleteOrder = {  'day_order' :dateSep[0],
                                      'month_order': dateSep[1],
                                      'year_order' : dateSep[2],
                                        'company': item[1]}

    def __OnDoubleClick(self,event):
        if self._tree.selection():
            it = self._tree.item( self._tree.focus() )['values']
            dateSep = it[2].split('-')
            dateSep = [int(i) for i in dateSep]
            order = self._database.getOneOrder(companyName = it[1], 
                                       day_order =   dateSep[0],
                                       month_order = dateSep[1],
                                       year_order =  dateSep[2]  )
            for line in order: print(line)

            self.__windowManager.newRebuildOrderWindow(array = order)
    
    def __deleteOrder(self):
        if self.__todeleteOrder: self._database.remove_order(self.__todeleteOrder)
        print('Order deleted')
        self.__updateTree()

    def __updateAvailableYears(self):
        self.__availableYears = self._database.getAllYears()
        
    def _readDatabase(self,month = None,year = None):

        if month == None : month = datetime.date.today().month
        if year == None : year = datetime.date.today().year
        self._rawArray = self._database.getOrderby_orderMonthandYear( month,year)



    def _addLines(self):
        for index,line in enumerate(self._rawArray):
            self._tree.insert("",str(index),values = (str(index), 
                                                 line[7], 
                                                 str(line[0])+'-'+str(line[1])+'-'+str(line[2]),
                                                 line[6],
                                                 str(line[8]) ) )
    def __databaseErrorAction(self):
        messagebox.showerror('Błąd!', 'Żadne zamówienie nie zostało wprowadzone\nBaza danych jest pusta!')
        self._root.destroy()

                    
    def __backToMainMenu(self):
        self.__windowManager.backToLastWindow()
       