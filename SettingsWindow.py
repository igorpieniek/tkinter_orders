from tkinter import filedialog
from tkinter import *

class SettingsWindow():
    """description of class"""
    def __init__(self, *, root, windowManager):
        self.__root = root
        self.__windowManager = windowManager

        self.addFrames()
        self.__addNaviFrameElements()
        self.addPathSection()

    def __addNaviFrameElements(self):
        pathButton = Button(self.naviFrame,text="Cofnij", command=self.__changeWindow)
        pathButton.grid(row=0, column=0)

    def __changeWindow(self):
        self.__windowManager.backToLastWindow()

    def browseToPath(self):
         filename = filedialog.askdirectory()
         print(filename)
         path = StringVar()
         path.set(filename)
         self.pathEntry.config(textvariable = path)
         file = open('config.txt', 'w')
         file.write(filename)
         file.close()


    def addFrames(self):
        self.pathFrame = LabelFrame(self.__root, padx = 5, pady=5)
        self.pathFrame.grid(row= 1, stick = W + N + S)
        self.naviFrame = LabelFrame(self.__root, padx = 5, pady=5)
        self.naviFrame.grid(row= 0, stick = W + N + S)

    def addPathSection(self):
        infoLabel = Label(self.pathFrame, text= "Ściezka folderu do zapisu plików PDF",padx=10, pady=0)
        infoLabel.grid(row=0, column=0)

        pathFromConfig = StringVar()
        try: 
            file = open('config.txt')
            pathFromConfig.set(file.read()) 
            file.close()
        except: print('So such file!')

        self.pathEntry = (Entry(self.pathFrame, width=45 ,textvariable = pathFromConfig ))
        self.pathEntry.grid(row= 1 , column=0,padx = 10, pady=3, sticky = N + W + E)

        pathButton = Button(self.pathFrame,text="Wybierz folder", command=self.browseToPath)
        pathButton.grid(row=1, column=1)

