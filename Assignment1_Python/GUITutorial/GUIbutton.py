from Tkinter import *
root = Tk()
#theLabel = Label(root, text = 'This is easy')
#theLabel.pack()
topframe = Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)
button1 = Button(topframe, text = 'press1', fg = 'red')
button2 = Button(topframe, text = 'press2', fg = 'blue')
button3 = Button(topframe, text = 'press3', fg = 'green')
button4 = Button(bottomframe, text = 'press4', fg = 'purple')

button1.pack(side = LEFT)
button2.pack(side = LEFT)
button3.pack(side = LEFT)
button4.pack(side = RIGHT)


root.mainloop()