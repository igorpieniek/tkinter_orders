from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Border, Side, Alignment, Font

class PDFgen():
    def __init__(self):
         self.ex = Workbook()  
         self.er = self.ex.active

    def process(self, order):
        self._clearExcelSheet()
        self.__copyProducts(order)
        self._addDefaultCells()
        #self._delEmptyLines()
        self._addToExcel()
        self._generatePDF()

    def _clearExcelSheet(self):
        for row in self.er['A1':'G37']:
            for cell in row:
                cell.value = None

    def __copyProducts(self, order):
        self.__orderOBJ = order
        self.__order = order.getOrderDict()
        
    def _addDefaultCells(self):
        self.er['A2'] = 'Model'
        self.er['B2'] = 'Suma'
        self.er['C2'] = 'Ilość'
        self.er['D2'] = 'Rodzaj'
        self.er['E2'] = 'Uwagi'

        headerFont = Font(size=16, bold= True )
        for row in self.er['A2':'E2']:
            for cell in row:
                cell.font = headerFont

        bd = Side(style='thin', color="000000")
        self.border = Border(left=bd, top=bd, right=bd, bottom=bd)

        self.er.column_dimensions['A'].width = 20
        self.er.row_dimensions[1].height=30
        self.er.column_dimensions['D'].width = 12
        self.er.column_dimensions['E'].width = 34

        self._restFont = Font(size=14 )
        self._companyFont = Font(size = 18, bold =True)

        self.__addCompanyName() # add company name to 


    def __addCompanyName(self):
        self.er.merge_cells('A1:B1')
        self.er['A1'] =  self.__order['companyName']
        self.er['A1'].alignment = Alignment(horizontal='left', vertical='center')
        cell = self.er['A1']
        cell.font = self._companyFont

    def __addOrderDate(self):
        pass
    def __addCollectDate(self):
        pass
    def __addPayment(self):
        pass
    def __addInvoice(self):
        pass



    def _addToExcel(self):
        lastRow = 3
        # write all dummies

        for model,products in self.__order['products'].items():
                self.er['A'+ str(lastRow)] = products[0].getModel()
                self.er['B'+ str(lastRow)] = self.__order['sum'][model]
                self.er['A'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center',wrap_text = True)
                self.er['B'+ str(lastRow)].alignment = Alignment(horizontal='center', vertical='center')
                k =0
                while k < len(products):
                    self.er['D'+ str(k+lastRow)] = products[k].getKind()
                    self.er['C'+ str(k+lastRow)] = products[k].getNumber()
                    self.er['C'+ str(k+lastRow)].alignment = Alignment(horizontal='right', vertical='center')
                    self.er['D'+ str(k+lastRow)].alignment = Alignment(horizontal='center', vertical='center')
                    k+=1
                self.er.merge_cells('B'+ str(lastRow) +':'+ 'B'+str(lastRow -1+ len(products )))
                self.er.merge_cells('A'+ str(lastRow) +':'+ 'A'+str(lastRow -1+ len(products )))
                lastRow += len(products)
        

      
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
