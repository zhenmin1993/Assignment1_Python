from Tkinter import *

class TaoButton:

	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		self.printButton = Button(frame, text = 'print message', command = self.printMessage)
		self.printButton.pack(side = LEFT)
		self.quitButton = Button(frame, text = 'quit', command = frame.quit)
		self.quitButton.pack(side = LEFT)

	def printMessage(self):
		print 'Wow, this worked'


root = Tk()

b = TaoButton(root)

root.mainloop()