# create simple dummy object
from Genre import *

class Stand(object):
    def __init__(self,color = None, num = None):
        self._genre = Genre()
        self._isLocked = False
        self._model = 'Statyw metalowy'
        self._color = None
        self._number = None

        if color and num: 
            self.addOption(color,num)

    def __del__(self):
        del self._model,self._color, self._number
    
    def __str__(self):
        if  self._model and self._color and self._number:
           return 'Model: ' + self._model +' Color: '+ self._color+' Number: '+str(self._number)+ ' isLocekd = ' + str(self._isLocked)
        else: return 'Empty object'
        

    def addOption(self, color, num):
        # check in color is valid
        if self._isLocked: print('This object was used, you cant change it ! ')
        if not color in self._genre.stands : error('No such color of wooden stand on genre list!')

        if num > 0: # onlyy if number is  
            self._color = color
            self._number = num
            self._isLocked = True
        else: print('0 of this model -> it isnt added')


    def getData(self):
        if not self._model  : return None
        output = [self._model, self._color, self._number]
        return output
  
    def isEmpty(self):
        if  self._model and self._color and self._number: return False
        else: return True