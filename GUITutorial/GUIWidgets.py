from Tkinter import *           # 
root = Tk()                     # 
                                # 
one = Label(root, text = 'One', bg = 'red', fg='white')
one.pack(side = TOP)
two = Label(root, text = 'Two', bg = 'green', fg='black')
two.pack(fill = X)
three = Label(root, text = 'Three', bg = 'blue', fg='white')
three.pack(side = LEFT, fill = Y)

root.mainloop()