from Tkinter import *
import tkMessageBox

def doNothing():
    print "OK OK I won't"

root = Tk()
canvas = Canvas(root, width = 200, height = 100)
canvas.pack()
blackLine = canvas.create_line(0,0,200,50)
redLine = canvas.create_line(0,100,200,50, fill = 'red')
greenBox = canvas.create_rectangle(25, 25, 130, 60, fill = 'green')

canvas.delete(redLine) #if you want to delete a object
canvas.delete(ALL) #if you want to delete all objects

root.mainloop()