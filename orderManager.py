from basicProduct import *
from Genre import *
import datetime



class OrderManager():
    """description of class
       Class to save temporary order data, but also to do all needed conversions"""
    def __init__(self, *,productArray=None,**kwargs ):
        self.__isEmpty = True
        self.__genre = Genre()
        self.__order = {}

        if not productArray: #in case no argument was added
            print('Empty order manager added!')
        else:
            from Order import ProductLine

            if isinstance(productArray[0], ProductLine) :
                # there we have event from order window
                # TODO: CONVERTING DATA TO BASIC ARRAY
                orderInfo = {
                                'companyName': None,
                                'dateOrder':None,
                                'dateCollect':None,
                                'invoice':None,
                                'payment': None, }
                orderInfo.update(kwargs)
                self.addOrderData(productArray, orderInfo)
            elif  isinstance(productArray[0], list) or  isinstance(productArray[0], tuple):
                #there we have reading from database event (from history call)
                self.addDatabaseData(productArray)
            else: print('Wrong format of array!')

    def __eq__(self, obj):
        if not isinstance(obj, OrderManager): return False
        elif self.__isEmpty and obj.__isEmpty: return True
        else: return self.__order == obj.__order

    def isEmpty(self):
        return self.__isEmpty

    # Add to object data from all Order obj window
    def addOrderData(self, array, orderInfo):
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

            from Order import DummyLine
            from Order import WoodLine
            from Order import StandsLine
            from Order import AccessoriesLine
            self.__products= []
            for frame in array: #sorting data
                for i in range( len( frame.getData() ) ):
                    objType = frame.getBasicProductType()
                    if objType == Dummy : self.__products.append(objType(model = frame.getModel(), kind = frame.getKind(i), num = frame.getNumber(i)))
                    else : self.__products.append(objType(kind =frame.getKind(i), num =frame.getNumber(i) ))

        self.__buildMainDict()

    # Add to obj all data read from database 
    def addDatabaseData(self, array):
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
            
            self.__products = []
            for line in productsRaw: #sorting data
                if line[0] in self.__genre.dummys:
                      self.__products.append(Dummy(model = line[0], kind = line[1], num = line[2]))
                elif line[0] == 'Statyw drewniany':
                      self.__products.append(WoodenStand(kind =line[1], num =line[2]))
                elif line[0] == 'Statyw metalowy':
                      self.__products.append(Stand(kind =line[1], num =line[2]))
                elif line[0] == 'Akcesoria':
                      self.__products.append(Accessory(kind =line[1], num =line[2]))

            self.__buildMainDict()  
    
    # Return main order dict         
    def getOrderDict(self):
        if self.__isEmpty: return {}
        else: return self.__order

    # Method which convert saved data to array createed in special format to save in database
    def getDataToDatabase(self):
        if self.__isEmpty: raise NameError('Error: obj is empty!')
        else:
            outArray = []
            basic = [self.__order['dateOrder'].day, self.__order['dateOrder'].month, self.__order['dateOrder'].year,
                     self.__order['dateCollect'].day,  self.__order['dateCollect'].month, self.__order['dateCollect'].year,
                     self.__order['invoice'], self.__order['companyName'], self.__order['payment'] ]

            for prod in self.__products  :   outArray.append( basic + prod.getData()) #level of searching in every products#level of list of products (dummys, stands etc.)
        return outArray

    def __sumCalculate(self): 
        sum = {model: 0 for model, line in self.__order['products'].items()}
        for model, frame in self.__order['products'].items():
            for line in frame:
                sum[model]+= line.getNumber()
        self.__sum = sum   


    # Private method to build main object dict
    def __buildMainDict(self):
        if  self.__isEmpty or not self.__products :
            raise NameError('Error: update main dictionary is impossible- there is no data in object!')
        else:
            dummyDict = {line.getModel(): [] for line in self.__products if line.getModel() in self.__genre.dummys}

            listOfobj = (list( dict.fromkeys( [i.__class__ for i in self.__products] ))) #create list of basic product class from product list (without duplicate)
            if Dummy in listOfobj: listOfobj.remove(Dummy) #delate dummy - because of different way of saving
            restProdDict = {obj.__name__ : [] for obj in listOfobj} # create dict, with keys named as classes from listOfObj

            for pro in self.__products:
                if   isinstance(pro, Dummy):  dummyDict[pro.getModel()].append(pro) #special treating of dummy products
                elif pro.__class__ in listOfobj: restProdDict[pro.__class__.__name__].append(pro)


            productsInDict = {}
            productsInDict.update(dummyDict)
            productsInDict.update(restProdDict)
             

            self.__order = {
                             'companyName': self.__companyName,
                             'dateOrder':self.__dateOrder,
                             'dateCollect':self.__dateCollect,
                             'invoice': self.__invoiceNum,
                             'payment': self.__payment, 
                             'products': productsInDict}

            self.__sumCalculate()
            self.__order.update({'sum': self.__sum})
      