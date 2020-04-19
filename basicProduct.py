# create simple product object

class BasicProduct():
    def __init__(self, *, model=None, kind = None, num = None):
        self.__isLocked = False
        self.__model = None
        self.__kind = None
        self.__number = None

        if model and kind and num: 
            self.addOption(model,kind,num)

    def __del__(self):
        del self.__model,self.__kind, self.__number
    
    def __str__(self):
        if  self.__model and self.__kind and self.__number:
           return 'Model: ' + self.__model +' Kind: '+ self.__kind+' Number: '+str(self.__number)+ ' isLocekd = ' + str(self.__isLocked)
        else: return 'Empty object'
        

    def addOption(self, model,kind, num):
        # check in kind is valid
        if self.__isLocked: print('This object was used, you cant change it ! ')

        if num > 0: # onlyy if number is  
            self.__model = model
            self.__kind = kind
            self.__number = num
            self.__isLocked = True
        else: print('0 of this model -> it isnt added')

    def getData(self):
        if not self.__model  : return None
        output = [self.__model, self.__kind, self.__number]
        return output
  
    def isEmpty(self):
        if  self.__model and self.__kind and self.__number: return False
        else: return True    

from Genre import Genre
class Dummy(BasicProduct):
    def __init__(self, *, model=None, kind=None, num=None):
        self.__genre = Genre()
        if not model in self.__genre.dummys : raise NameError('No such model of dummy on genre list!')
        if not kind in self.__genre.color: raise NameError('No such kind of dummy on genre list!')
        super().__init__( model=model, kind=kind, num=num)

class Stand(BasicProduct):
    def __init__(self, *, kind=None, num=None):
        self.__genre = Genre()
        self.__model = 'Statyw metalowy'
        if not kind in self.__genre.stands : raise NameError('No such kind of wooden stand on genre list!')
        super().__init__( model=self.__model, kind=kind, num=num)

class WoodenStand(BasicProduct):
    def __init__(self, *, kind = None, num = None):
        self.__genre = Genre()
        self.__model = 'Statyw drewniany'
        if not kind in self.__genre.woodStands: raise NameError(' No such kind of wooden stand on genre list!')
        super().__init__( model=self.__model, kind=kind, num=num)