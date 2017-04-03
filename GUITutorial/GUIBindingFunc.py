from Tkinter import *           # 
root = Tk()                     # 
                                # 
def printName(event):
	print ('Hello My name is Tao')

button_1 = Button(root, text = 'print my name')
button_1.bind('<Button-1>', printName)
button_1.grid(row = 0)

root.mainloop()