from tkinter import *

from windowManager import windowManager

root = Tk()
root.geometry('400x400')

global manager
manager = windowManager(0)

from startModule import startModule

if manager.getStatus == 0:
    startwin = startModule(root)
    #START WINDOW
#elif manager.getStatus() == 1:
    #NEW ORDER
#elif manager.getStatus() == 2:
    #HISTORY

#############################################
#root = tk()



#start = entry(root, width=50 )
#start.pack()


#labels = []
#labels.append(label(root, text ="hello  world!"))
#labels.append(label(root, text ="label2"))


#labels[0].grid(row = 0, column = 0, padx = 20, pady = 10)
#labels[1].grid(row = 1, column = 1)

#def click():
#    if not start.get():
#        return
#    else:
#        label1 = label(root, text = start.get())
#        label1.pack()
#        root.destroy()
      

#buttons = []
#buttons.append(button(root, text= "przycisk", padx=10, pady=7, command = click, fg= "blue"))

#buttons[0].pack()

root.mainloop()
