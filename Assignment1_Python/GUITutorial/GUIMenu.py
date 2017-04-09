from Tkinter import *

def doNothing():
	print "OK OK I won't"

root = Tk()

#*******Main Menu*****
menu = Menu(root)
root.config(menu = menu)

subMenu = Menu(menu, tearoff=0)
menu.add_cascade(label = 'File', menu = subMenu)
subMenu.add_command(label = 'Open Database', command = doNothing)
subMenu.add_command(label = 'New...', command = doNothing)
subMenu.add_separator()
subMenu.add_command(label = 'Exit', command = root.quit)

editMenu = Menu(menu,  tearoff=0)
menu.add_cascade(label = 'file in', menu = editMenu)
editMenu.add_command(label = 'Redo', command = doNothing)

#*******The Toolbar*****
toolbar = Frame(root, bg = 'blue')
insertButt = Button(toolbar, text = 'Insert Image', command = doNothing)
insertButt.grid(row = 0, column = 0, padx = 4 , pady = 1)
printButt = Button(toolbar, text = 'Print', command = doNothing)
printButt.grid(row = 0, column = 1, padx = 4 , pady = 1)


toolbar.grid(row = 0, sticky = W, columnspan = 2 )

#********Add Entry
label_1 = Label(root, text = 'host')
label_2 = Label(root, text = 'User')
label_3 = Label(root, text = 'Password')
label_4 = Label(root, text = 'Database Name')
label_5 = Label(root, text = 'Port')
entry_1 = Entry(root)
entry_2 = Entry(root)
entry_3 = Entry(root)
entry_4 = Entry(root)
entry_5 = Entry(root)

label_1.grid(row = 1, sticky = E)  #NSWE to show the place
label_2.grid(row = 2, sticky = E)
label_3.grid(row = 3, sticky = E)
label_4.grid(row = 4, sticky = E)
label_5.grid(row = 5, sticky = E)
entry_1.grid(row = 1, column = 1)
entry_2.grid(row = 2, column = 1)
entry_3.grid(row = 3, column = 1)
entry_4.grid(row = 4, column = 1)
entry_5.grid(row = 5, column = 1)

c = Checkbutton(root, text = 'keep me signed in')
c.grid(row = 6, columnspan = 2)

#*******Status bar*****
status = Label(root, text = 'Prepare to', bd = 1, relief = SUNKEN, anchor =W)
status.grid(row = 7, sticky=N+E+S+W)



root.mainloop()