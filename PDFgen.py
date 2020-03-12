from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Border, Side, Alignment

class PDFgen():
    def __init__(self):
         self.ex = Workbook()
    
         self.er = self.ex.active

         bd = Side(style='thin', color="000000")
         self.border = Border(left=bd, top=bd, right=bd, bottom=bd)




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
        #self.er['A'].width = 15
        self.er['A2'] = 'Model'
        self.er['B2'] = 'Suma'
        self.er['C2'] = 'Rodzaj'
        self.er['D2'] = 'Ilość'

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
        dummyObjtoDel = []
        woodObjtoDel =[]
        standsObjtoDel = []

        # Update of colour and number
        for i in range(len(self._dummys)):
            dummyLineToDel = []
            for k in range(len(self._dummys[i].color)):
                if not int(self._dummys[i].number[k].get()):
                    dummyLineToDel.append(k)    
            if len( dummyLineToDel) > 0 and len( dummyLineToDel) < len(self._dummys[i].color)  :
                counter = 0
                while counter < len(dummyLineToDel):
                    self._dummys[i].color.pop(dummyLineToDel[counter]-counter)
                    self._dummys[i].number.pop(dummyLineToDel[counter]-counter)
                    counter +=1
            elif len( dummyLineToDel) == len(self._dummys[i].color):
                dummyObjtoDel.append(i)

        # Update dummy obj in case all is empty
        if dummyObjtoDel:
            counter = 0
            while counter < len(dummyObjtoDel):
                self._dummys.pop(dummyObjtoDel[counter]-counter)
                counter +=1

        # Update wood stands
        for i in range(len(self._woodStands)):
            woodLineToDel = []
            for k in range(len(self._woodStands[i].color)):
                if not int(self._woodStands[i].number[k].get()): 
                    woodLineToDel.append(k)    
            if len( woodLineToDel) > 0 and len( woodLineToDel) < len(self._woodStands[i].color)  :
                counter = 0
                while counter < len(woodLineToDel):
                    self._woodStands[i].color.pop(woodLineToDel[counter]-counter)
                    self._woodStands[i].number.pop(woodLineToDel[counter]-counter)
                    counter +=1
            elif len( woodLineToDel) == len(self._woodStands[i].color):
                woodObjtoDel.append(i)

        # Update wood stands obj in case all is empty
        if woodObjtoDel:
            counter = 0
            while counter < len(woodObjtoDel):
                self._woodStands.pop(woodObjtoDel[counter]-counter)
                counter +=1
        # Update stands obj incase its empty
        for i in range(len(self._stands)):
            if not int(self._stands[i].number.get()): standsObjtoDel.append(i)
        if standsObjtoDel:
            counter = 0
            while counter < len(standsObjtoDel):
                self._stands.pop(standsObjtoDel[counter]-counter)
                counter +=1
        


    def _addToExcel(self):
        lastRow = 3
        # write all dummies
        for i in range(len(self._dummys)):
            self.er['A'+ str(lastRow)] = str(self._dummys[i].model[0].get())
            self.er['B'+ str(lastRow)] = str(self._dummys[i].sumCalculate())
            self.er['A'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center')
            self.er['B'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center')
            k =0
            while k < len(self._dummys[i].color):
                self.er['C'+ str(k+lastRow)] = self._dummys[i].color[k].get()
                self.er['D'+ str(k+lastRow)] = self._dummys[i].number[k].get()
                self.er['C'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                self.er['D'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                k+=1
            self.er.merge_cells('B'+ str(lastRow) +':'+ 'B'+str(lastRow -1+ len(self._dummys[i].color)))
            self.er.merge_cells('A'+ str(lastRow) +':'+ 'A'+str(lastRow -1+ len(self._dummys[i].color)))
            lastRow += len(self._dummys[i].color)
        
        # write all woodStands
        for i in range(len(self._woodStands)):
            self.er['A'+ str(lastRow)] = 'Statyw\n drewniany'
            self.er['B'+ str(lastRow)] = str(self._woodStands[i].sumCalculate())
            self.er['A'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center',wrap_text = True)
            self.er['B'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center')
            k =0
            while k < len(self._woodStands[i].color):
                self.er['C'+ str(k+lastRow)] = self._woodStands[i].color[k].get()
                self.er['D'+ str(k+lastRow)] = self._woodStands[i].number[k].get()
                self.er['C'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                self.er['D'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                k+=1
            self.er.merge_cells('B'+ str(lastRow) +':'+ 'B'+str(lastRow -1+ len(self._woodStands[i].color)))
            self.er.merge_cells('A'+ str(lastRow) +':'+ 'A'+str(lastRow -1+ len(self._woodStands[i].color)))
            lastRow += len(self._woodStands[i].color)

        # write all normal stands
        for q in range(len(self._stands)):
            self.er['A'+ str(q+lastRow)] = 'Statyw \n metalowy'
            self.er['C'+ str(q+lastRow)] = self._stands[q].model.get()
            self.er['D'+ str(q+lastRow)] = self._stands[q].number.get()
            self.er['A'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center',wrap_text = True )
            self.er['D'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
 
      
        for row in self.er['A2':'E'+str(len(self._stands)+lastRow-1)]:
            for cell in row:
                cell.border = self.border
        
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
