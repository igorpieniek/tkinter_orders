# create simple dummy object
from Genre import *

class Dummy(object):
    def __init__(self, model=None, color = None, num = None):
        self._genre = Genre()
 
        if model: self._model = model


        if color: self._color = color
        else: self._color = []

        if num: self._number = num
        else: self._color = []
    
    def addOption(self, color, num):
        # check in color is valid
        if isinstance(color, list):
            for col in color:
                if not col in self._genre.color: error('No such color on genre list!')
        else:
           if not color in self._genre.color: error('No such color on genre list!')
        
        if num > 0: # onlyy if number is  
            self._color.append(color)
            self._number.append(num)

    def delateOption(self, lineNumber):
        if self._color:
            self._color.pop(lineNumber)
            self._number.pop(lineNumber)

    def getData(self):
        output = []
        for a in range(len(self._color)):
            output.append([self._color[a], self._number[a]])
        return output

    def setModel(self, model):
        # check in color is valid
        if not model in self._genre.dummys: error('No such color on genre list!')
        self._model = model    