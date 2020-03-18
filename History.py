from tkinter import *

class History(object):
    def __init__(self,root,database):
        self._root = Toplevel(root)
        self._database = database
    

    def _addTree(self):
        self._tree = Treeview(self._root)
        self._tree.column("Lp.", width=270, minwidth=270, stretch=NO)
        self._tree.column("Data zamówienia", width=270, minwidth=270)
        self._tree.column("Nazwa firmy", width=270, minwidth=270)
        self._tree.column("Nr faktury", width=270, minwidth=270)
        self._tree.column("Kwota", width=270, minwidth=270)

        self._tree.heading("#0",text="Name",anchor=tk.W)
        self._tree.heading("one", text="Date modified",anchor=tk.W)
        self._tree.heading("two", text="Type",anchor=tk.W)
        self._tree.heading("three", text="Size",anchor=tk.W)

   