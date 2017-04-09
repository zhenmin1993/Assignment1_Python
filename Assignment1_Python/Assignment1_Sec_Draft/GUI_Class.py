from xml.dom.minidom import parse
import xml.dom.minidom


import MySQLdb

from Tkinter import *
import tkMessageBox
import Tkinter as tk 

import sys
import os

#Take one window as a object
class MyWindow():

    def __init__(self):
        self.root = tk.Tk()


    def DestroySelf(self):
        self.root.destroy()


    def AddButton(self, text_butt, ButtonFunc, struct):
        self.OneButton = Button(self.root, text = text_butt, command = ButtonFunc, )
        self.OneButton.grid(row = struct['row'], column = struct['column'], \
            padx = struct['padx'] , pady = struct['pady']) 


    def AddLabel(self, text_lb, para, struct):
        self.OneLabel = Label(self.root, text = text_lb , bg = para['bg'], fg = para['fg'])
        self.OneLabel.grid(row = struct['row'], rowspan = struct['rowspan'],column = struct['column'], \
            columnspan = struct['columnspan'], sticky = struct['sticky'])


    def AddLabelFrame(self, text_lbf, struct):
        self.labelframe = Label(self.root, text = text_lbf)
        self.labelframe.grid(row = struct['row'], rowspan = struct['rowspan'],column = struct['column'], \
            columnspan = struct['columnspan'], sticky = struct['sticky'])


    def AddImage(self, file_name, struct):
        photo = PhotoImage(file = file_name)
        self.OneImage = Label(image=photo)
        self.OneImage.image = photo
        self.OneImage = Label(self.root, image = photo)
        self.OneImage.grid(row = struct['row'], rowspan = struct['rowspan'], column = struct['column'] , \
            columnspan = struct['columnspan'], sticky = struct['sticky'], padx = struct['padx'], \
            pady = struct['pady'])  


    def AddEntry(self, text, para, struct):
        self.OneEntry = Entry(self.root, textvariable=text, show = para['show'] ,insertofftime = para['off'], \
            insertontime = para['on'] )
        self.OneEntry.grid(row = struct['row'] , column = struct['column'] , sticky = struct['sticky'])


    def AddStatus(self, para, struct,  text_add ):
        self.OneStatus = Label(self.root, text = text_add, bd = para['bd'], fg = para['fg'], \
            relief = SUNKEN, anchor = para['anchor'])
        self.OneStatus.grid(row = struct['row'], columnspan = struct['columnspan'], \
            sticky = struct['sticky'])
        

    def AddText(self,struct,text_add):
        self.OneText = Text(self.root)
        self.OneText.insert(INSERT, text_add)
        self.OneText.grid(row = struct['row'], column = struct['column'], \
            columnspan = struct['columnspan'], sticky = struct['sticky'])


