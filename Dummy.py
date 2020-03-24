# create simple dummy object
from Genre import *

class Dummy(object):
    def __init__(self, model=None, color = None, num = None):
        self._genre = Genre()
        self._isLocked = False
        self._model = None
        self._color = None
        self._number = None

        if model and color and num: 
            self.addOption(model,color,num)

    def __del__(sel):
        del self._model,self._color, self._number

    def addOption(self, model,color, num):
        # check in color is valid
        if self._isLocked: print('This object was used, you cant change it ! ')
        if not model in self._genre.model: error('No such dummy model on genre list!')
        if not color in self._genre.color: error('No such color on genre list!')

        if num > 0: # onlyy if number is  
            self._model = model
            self._color = color
            self._number = num
            self._isLocked = True
        else: print('0 of this model -> it isnt added')


    def getData(self):
        output = []
        if not self._model  : return output
        output.append([self._model, self._color, self._number])
        return output
  