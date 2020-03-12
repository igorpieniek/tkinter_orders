from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Border, Side, Alignment, Font

class PDFgen():
    def __init__(self):
         self.ex = Workbook()
    
         self.er = self.ex.active






    def process(self, prodList):
        self._clearExcelSheet()
        self._addDefaultCells()
        self._copyProducts(prodList)
        self._sortProducts()
        self._delEmptyLines()
        self._addToExcel()
        self._generatePDF()

    def _clearExcelSheet(self):
        for row in self.er['A1':'G37']:
            for cell in row:
                cell.value = None

        
    def _addDefaultCells(self):
        self.er['A2'] = 'Model'
        self.er['B2'] = 'Suma'
        self.er['C2'] = 'Rodzaj'
        self.er['D2'] = 'Ilość'
        self.er['E2'] = 'Uwagi'

        headerFont = Font(size=16, bold= True )
        for row in self.er['A2':'E2']:
            for cell in row:
                cell.font = headerFont

        bd = Side(style='thin', color="000000")
        self.border = Border(left=bd, top=bd, right=bd, bottom=bd)

        self.er.column_dimensions['A'].width = 20
        self.er.column_dimensions['C'].width = 12
        self.er.column_dimensions['E'].width = 34

        self._restFont = Font(size=14 )

    def _copyProducts(self,prodList):
        self._productsList = []
        self._productsList = prodList

    def _sortProducts(self):
        self._dummys = []
        self._stands = []
        self._woodStands = []
        from Order import DummyLine, StandsLine, WoodLine
        for i in range(len(self._productsList)):   
             if isinstance(self._productsList[i],DummyLine ):
                 self._dummys.append(self._productsList[i])
             elif isinstance(self._productsList[i],StandsLine ):
                 self._stands.append(self._productsList[i])
             elif isinstance(self._productsList[i],WoodLine ):
                 self._woodStands.append(self._productsList[i])

    def _delEmptyLines(self):
        self._dummys = self. _delEmptyLine(self._dummys)
        self._stands = self. _delEmptyLine(self._stands)
        self._woodStands = self. _delEmptyLine(self._woodStands)

    def _delEmptyLine(self, prodList):
        ObjtoDel = []
        for i in range(len(prodList)):
            LineToDel = []
            for k in range(len(prodList[i].color)):
                if not int(prodList[i].number[k].get()):
                    LineToDel.append(k)    
            if len( LineToDel) > 0 and len(LineToDel) < len(prodList[i].color)  :
                counter = 0
                while counter < len(LineToDel):
                    prodList[i].color.pop(LineToDel[counter]-counter)
                    prodList[i].number.pop(LineToDel[counter]-counter)
                    counter +=1
            elif len( LineToDel) == len(prodList[i].color):
                ObjtoDel.append(i)

        # Update dummy obj in case all is empty
        if ObjtoDel:
            counter = 0
            while counter < len(ObjtoDel):
                prodList.pop(ObjtoDel[counter]-counter)
                counter +=1
        return prodList



    def _addToExcel(self):
        lastRow = 3
        # write all dummies
        elementList = [self._dummys, self._woodStands, self._stands]
        for product in elementList:
            for i in range(len(product)):
                if   product == elementList[0] :self.er['A'+ str(lastRow)] = str(product[i].model[0].get())
                elif product == elementList[1] :self.er['A'+ str(lastRow)] = 'Statyw drewniany'
                elif product == elementList[2] :self.er['A'+ str(lastRow)] = 'Statyw metalowy'
                self.er['B'+ str(lastRow)] = str(product[i].sumCalculate())
                self.er['A'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center',wrap_text = True)
                self.er['B'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center')
                k =0
                while k < len(product[i].color):
                    self.er['C'+ str(k+lastRow)] = product[i].color[k].get()
                    self.er['D'+ str(k+lastRow)] = product[i].number[k].get()
                    self.er['C'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                    self.er['D'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                    k+=1
                self.er.merge_cells('B'+ str(lastRow) +':'+ 'B'+str(lastRow -1+ len(product[i].color)))
                self.er.merge_cells('A'+ str(lastRow) +':'+ 'A'+str(lastRow -1+ len(product[i].color)))
                lastRow += len(product[i].color)
        

      
        for row in self.er['A2':'E'+str(lastRow-1)]:
            for cell in row:
                cell.border = self.border
        for row in self.er['A3':'E'+str(lastRow-1)]:
            for cell in row:
                cell.font = self._restFont    
        
        self.ex.save('tkinter_test.xlsx')


    def _generatePDF(self):
        import win32com.client

        o = win32com.client.Dispatch("excel.application")
        o.Visible = False
        wb_path = r'c:\users\igor\source\repos\tkinterproject1\tkinterproject1\tkinter_test.xlsx'
        wb = o.Workbooks.Open(wb_path)
        ws_index_list = [1] 
        path_to_pdf = r'c:\users\igor\desktop\test.pdf'
        wb.WorkSheets(ws_index_list).Select()
        wb.ActiveSheet.ExportAsFixedFormat(0, path_to_pdf)
        wb.Close(True, wb_path)
