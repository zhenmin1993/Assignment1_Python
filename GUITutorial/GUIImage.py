from Tkinter import *
import tkMessageBox



def doNothing():
    print "OK OK I won't"

root = Tk()
photo = PhotoImage(file = 'goog.gif')
label = Label(root, image = photo)
label.pack()

root.mainloop()