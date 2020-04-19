

from basicProduct import *
from Genre import *
import datetime




class OrderManager():
    """description of class
       Class to save temporary order data, but also to do all needed conversions"""
    def __init__(self, *,productArray=None,**kwargs ):
        self.__isEmpty = True
        self.__genre = Genre()

        if not productArray: #in case no argument was added
            print('Empty order manager added!')
        else:
            from Order import DummyLine
            from Order import WoodLine
            from Order import StandsLine
            if isinstance(productArray[0], DummyLine) or isinstance(productArray[0], StandsLine) or isinstance(productArray[0], WoodLine):
                # there we have event from order window
                # TODO: CONVERTING DATA TO BASIC ARRAY
                orderInfo = {
                                'companyName': None,
                                'dateOrder':None,
                                'dateCollect':None,
                                'invoice':None,
                                'payment': None, }
                orderInfo.update(kwargs)
                self.convertOrderData(productArray, orderInfo)
            elif  isinstance(productArray[0], list):
                #there we have reading from database event (from history call)
                self.convertToOrder(productArray)
            else: print('Wrong format of array!')
                

    def convertOrderData(self, array, orderInfo):
        if not self.__isEmpty: # if object is not empty 
            print('Order was already added')
            return
        else:           
            self.__isEmpty = False
            self.__companyName = orderInfo['companyName']
            self.__invoiceNum =  orderInfo['invoice']
            self.__payment = orderInfo['payment']
            self.__dateOrder = orderInfo['dateOrder'] #datatime format
            self.__dateCollect =   orderInfo['dateCollect'] #datatime format

            dummyDict = {line[0]: [] for line in array if line.getModel() in self.__genre.dummys} #get all names of dummys in order
            woodenstands = []
            stands = []
            for frame in array: #sorting data
                for i in range( len( frame.getDate() ) ):
                    if frame.getModel() in self.genre.dummys:
                        dummyDict[ frame.getModel() ].append(Dummy(model = frame.getModel(), kind = frame.getKind(i), num = frame.getNumber(i)))
                    elif frame.getModel() == 'Statyw drewniany':
                        woodenstands.append(WoodenStand(kind =frame.getKind(i), num =frame.getNumber(i) ))
                    elif frame.getModel() == 'Statyw metalowy':
                        stands.append(Stand(kind = frame.getKind(i), num =frame.getNumber(i) ))
        
            self.__products = {'dummy': dummyDict, 'woodenStands': woodenstands, 'stands': stands}
            self.__buildMainDict()        

    def convertToOrderFromDatabase(self, array):
        if not self.__isEmpty: 
            print('Order was already added')
            return
        else:
            self.__isEmpty = False
            self.__companyName = array[0][8]
            self.__invoiceNum =  array[0][7]
            self.__payment = array[0][9]
            self.__dateOrder = datetime.date(day = array[0][1], month = array[0][2], year =array[0][3])
            self.__dateCollect =  datetime.date(day = array[0][4], month = array[0][5], year =array[0][6])

            productsRaw = [el[10:] for el in array] # geting only product info

            dummyDict = {line[0]: [] for line in productsRaw if line[0] in self.genre.dummys} #get all names of dummys in order
            woodenstands = []
            stands = []
            for line in productsRaw: #sorting data
                if line[0] in self.genre.dummys:
                    dummyDict[line[0]].append(Dummy(model = line[0], kind = line[1], num = line[2]))
                elif line[0] == 'Statyw drewniany':
                    woodenstands.append(WoodenStand(kind =line[1], num =line[2]))
                elif line[0] == 'Statyw metalowy':
                    stands.append(Stand(kind =line[1], num =line[2]))

            self.__products = {'dummys': dummyDict, 'woodenStands': woodenstands, 'stands': stands}
            self.__buildMainDict()
 
              
    def getDataToDatabase(self):
        if self.__isEmpty: raise NameError('Error: obj is empty!')
        else:
            outArray = []
            basic = [self.order['dateOrder'].day, self.order['dateOrder'].month, self.order['dateOrder'].year,
                     self.order['dateCollect'].day,  self.order['dateCollect'].month, self.order['dateCollect'].year,
                     self.order['invoice'].day, self.order['companyName'], self.order['payment'] ]

            for prod in range( len( self.order['products'] ) ) : #level of list of products (dummys, stands etc.)
                for line in range( len( prod ) ):        #level of searching in every products
                    if isinstance(line, dict):
                        for basicprod in line:  outArray.append( basic + basicprod.getData() ) # level of every dummy obj                                       
                    else: outArray.append( basic + basicprod.getData()) ## TODO: add products

            for el in outArray: print(el)

    def __buildMainDict(self):
        if  self.__isEmpty or not self.__products :
            raise NameError('Error: update main dictionary is impossible- there is no data in object!')
        else:
            self.order = {
                             'companyName': self.__companyName,
                             'dateOrder':self.__dateOrder,
                             'dateCollect':self.__dateCollect,
                             'invoice': self.__invoiceNum,
                             'payment': self.__payment, 
                             'products': self.__products}
                
         





