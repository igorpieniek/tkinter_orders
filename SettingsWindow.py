from tkinter import filedialog
from tkinter import *

class SettingsWindow():
    """description of class"""
    def __init__(self, *, root):
        self.__root = root

        self.addButton()

    def addButton(self):
        def browse_button():
            # Allow user to select a directory and store it in global var
            # called folder_path
            global folder_path
            filename = filedialog.askdirectory()
            folder_path.set(filename)
            print(filename)

        button2 = Button(text="Browse", command=browse_button)
