from openpyxl import Workbook



class PDFgen():
    def __init__(self):
         self.ex = Workbook()
    
         self.er = self.ex.active
         self.er['A2'] = 'model'
         self.er['B2'] = 'rodzaj'
         self.er['C2'] = 'ilość'
        

         self._productsList = []
         self._dummys = []
         self._stands = []

    def process(self, prodList):
        self._copyProducts(prodList)
        self._sortProducts()
        self._addToExcel()
        self._generatePDF()
    
    def _copyProducts(self,prodList):
        self._productsList = prodList

    def _sortProducts(self):
        from Order import DummyLine, StandsLine
        for i in range(len(self._productsList)):   
             if isinstance(self._productsList[i],DummyLine ):
                 self._dummys.append(self._productsList[i])
             elif isinstance(self._productsList[i],StandsLine ):
                 self._dummys.append(self._productsList[i])

    def _addToExcel(self):
        lastRow = 3
        for i in range(len(self._dummys)):
            self.er['A'+ str(i+lastRow)] = self._dummys[i].model[0].get()
            k =0
            while k < len(self._dummys[i].color):
                self.er['B'+ str(i+k+lastRow)] = self._dummys[i].color[k].get()
                self.er['C'+ str(i+k+lastRow)] = self._dummys[i].number[k].get()
                k+=1
            lastRow += len(self._dummys[i].color)-1
        
        self.ex.save('tkinter_test.xlsx')

    def _generatePDF(self):
        pass
