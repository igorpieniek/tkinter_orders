# create simple product object

class BasicProduct():
    def __init__(self, *, model=None, kind = None, num = None):
        self.__isLocked = False
        self.__model = None
        self.__kind = None
        self.__number = None

        if model and kind and num: 
            self.addOption(model,kind,num)
    
    def __str__(self):
        if  self.__model and self.__kind and self.__number:
           return 'Model: ' + self.__model +' Kind: '+ self.__kind+' Number: '+str(self.__number)+ ' isLocekd = ' + str(self.__isLocked)
        else: return 'Empty object'

    def __eq__(self, obj):
        if not isinstance(obj, BasicProduct): raise NameError('Error: you cant compare ', type(obj), ' with object using BasicProduct class!')
        elif not type(obj) == type(self): return False
        else:
            if obj.isEmpty() and self.isEmpty(): return True
            elif self.getData() == obj.getData(): return True
            else: return False
  

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

    def __getSmth(self, pos):
        temp = self.getData()
        if  temp: return temp[pos]
        else: return temp
    
    def getModel(self):
        return self.__getSmth(0)

    def getKind(self):
        return self.__getSmth(1)

    def getNumber(self):
         return self.__getSmth(2)

  
    def isEmpty(self):
        return not self.__isLocked   

from Genre import Genre
class Dummy(BasicProduct):
    def __init__(self, *, model=None, kind=None, num=None):
        self.__genre = Genre()
        if model and not model in self.__genre.dummys : raise NameError('No such model of dummy on genre list!')
        if kind and not kind and not kind in self.__genre.color: raise NameError('No such kind of dummy on genre list!')
        super().__init__( model=model, kind=kind, num=num)

class Stand(BasicProduct):
    def __init__(self, *, kind=None, num=None):
        self.__genre = Genre()
        self.__model = 'Statyw metalowy'
        if kind and not kind in self.__genre.stands : raise NameError('No such kind of wooden stand on genre list!')
        super().__init__( model=self.__model, kind=kind, num=num)

class WoodenStand(BasicProduct):
    def __init__(self, *, kind = None, num = None):
        self.__genre = Genre()
        self.__model = 'Statyw drewniany'
        if kind and not kind in self.__genre.woodStands: raise NameError(' No such kind of wooden stand on genre list!')
        super().__init__( model=self.__model, kind=kind, num=num)

class Accessories(BasicProduct):
    def __init__(self, *, kind = None, num = None):
        self.__genre = Genre()
        self.__model = 'Akcesoria'
        if kind and not kind in self.__genre.accessories: NameError(' No such kind of accesories on genre list!')
        super().__init__( model=self.__model, kind=kind, num=num)