from Order import DummyLine
from Order import StandsLine
from Order import WoodLine
import datetime


class OrderManager():
    """description of class
       Class to save temporary order data, but also to do all needed conversions"""
    def __init__(self, *,productArray=None,**kwargs ):
        if not array: #in case no argument was added
            print('Empty order manager added!')
            self.__isEmpty = True
        else:
            if isinstance(array[0], DummyLine) or isinstance(array[0], StandsLine) or isinstance(array[0], WoodLine):
                # there we have event from order window
                # TODO: CONVERTING DATA TO BASIC ARRAY
                pass
            elif  isinstance(array[0], List):
                #there we have reading from database event (from history call)
                # TODO: CONVERTING DATA TO BASIC ARRAY, and getting all basic data
                pass

    def convertOrderData(self, array):
        if not self.__isEmpty: # if object is not empty 
            pass

    def convertToOrder(self, array):
        self.__companyName = array[0][8]
        self.__invoiceNum =  array[0][7]
        self.__payment = array[0][9]
        self.__dateOrder = datetime.date(day = array[0][1], month = array[0][2], year =array[0][3])
        self.__dateCollect =  datetime.date(day = array[0][4], month = array[0][5], year =array[0][6])

        self.addEntrySection(companyName = self.__reCompanyName, invoiceNum = self.__reInvoiceNum, payValue = self.__rePayment,
                             dateOrder = self.__reDateOrder, dateCollect = self.__reDateCollect)

        productsRaw = [el[10:] for el in array] # geting onlu product info

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
                      




