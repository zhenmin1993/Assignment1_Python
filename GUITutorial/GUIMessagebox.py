from Tkinter import *
import tkMessageBox

def doNothing():
    print "OK OK I won't"

root = Tk()
tkMessageBox.showinfo(title='Computer Application', message='Are you sure?')
answer = tkMessageBox.askquestion('Question 1', 'Do you like faces?')

if answer == 'yes': 
    print ('oh yes')




root.mainloop()