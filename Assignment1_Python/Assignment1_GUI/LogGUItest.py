import xml.dom.minidom
from Tkinter import *
import tkMessageBox



import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os

def purify(rdf_str_raw):
    rdf_str = rdf_str_raw.split('#')[1]
    return rdf_str

def getID(element):
    rdfID = element.getAttribute("rdf:ID")
    return rdfID

def get_about(element):
    rdf_about = element.getAttribute("rdf:about")
    rdf_about = purify(rdf_about)
    return rdf_about


def getContent(element, TagName):
    content = element.getElementsByTagName(TagName)[0].childNodes[0].data
    try:
        content = float(content)
        return content
    except:
        return content

def get_resource(element, TagName):
    find_element = element.getElementsByTagName(TagName)[0]
    rdf_resource = find_element.getAttribute("rdf:resource")
    rdf_resource = purify(rdf_resource) 
    return rdf_resource

def getName(element):
    name = getContent(element, 'cim:IdentifiedObject.name')
    return name

def writeAttrib(element, command,data):
    table_name = element.localName
    record_name = data[1]
    try:  
        cur.execute(command, data) 
        print 'Table',table_name,'Record %s Attributes Write Into Database Succeed!' % record_name 

    except:
        conn.rollback()
        print 'Table',table_name,'Record %s Attributes Write Into Database Failed!' % record_name 

def writeOP(element, command, data):
    table_name = element.localName
    try:  
        cur.execute(command, data) 
        print 'Table',table_name,'Operational Data Write Into Database Succeed!' 

    except:
        conn.rollback()
        print 'Table',table_name,'Operational Data Write Into Database Failed!' 



def write_entry_db():
    print 'Connecting to MySQL server'
    Message = 'Connecting to MySQL server'
    status = Label(topframe, text = 'Connecting to MySQL server', bd = 1, relief = SUNKEN, anchor =W)
    status.grid(row = 8, sticky=N+E+S+W, columnspan = 2)
    host =  var_host.get()
    user = var_user.get()
    passwd =  var_passwd.get()
    db =  var_dbName.get()
    port =  var_port.get()
    port = int(port)


    
    try:
        global conn
        global cur
        conn=MySQLdb.connect(host,user,passwd,db,port)
        cur = conn.cursor()
        Message = 'Connected to MySQL server'
        print 'Connected to MySQL server\n'
        status = Label(topframe, text = Message, bd = 1,fg = '#228B22', relief = SUNKEN, anchor =W)
        status.grid(row = 8, sticky=N+E+S+W, columnspan = 2)

        status = Label(topframe, text = 'Waiting For Table Creating...', bd = 1, relief = SUNKEN, anchor =W)
        status.grid(row = 9, sticky=N+E+S+W, columnspan = 2)

        answer = tkMessageBox.askquestion('Computer Application', 'Server Connected, creating new tables?')

        if answer == 'yes': 
            execfile("Creating_Table.py")
            status = Label(topframe, text = 'Tables Created', fg = '#228B22', bd = 1, relief = SUNKEN, \
                anchor =W)
            status.grid(row = 9, sticky=N+E+S+W, columnspan = 2)

        else: 
            execfile("Existing_Table.py")
            status = Label(topframe, text = "Tables checking, if not exist, creat new table", bd = 1, \
                 relief = SUNKEN, anchor =W)
            status.grid(row = 9, sticky=N+E+S+W, columnspan = 2)

        status = Label(topframe, text = 'Table checking passed, please input the following file names', \
            bd = 1,fg = '#228B22', relief = SUNKEN, anchor =W)
        status.grid(row = 9, sticky=N+E+S+W, columnspan = 2)


    except:
        Message = 'Connection Failed! Please Check!'
        print 'Connection Failed! Please Check!'
        status = Label(topframe, text = Message, bd = 1 , fg = 'red',relief = SUNKEN, anchor =W)
        status.grid(row = 8, sticky=N+E+S+W, columnspan = 2)





    

def quit():
    answer = tkMessageBox.askquestion('Computer Application', 'Are you sure to EXIT?')

    if answer == 'yes': 
            Login.quit
            sys.exit()


def write_entry_file():
    fname_EQ =  var_EQ.get()
    fname_SSH = var_SSH.get()
    global collection_EQ
    global collection_SSH
    while True:

        identify = 0
        try:
            DOMTree_EQ = xml.dom.minidom.parse(fname_EQ)
            collection_EQ = DOMTree_EQ.documentElement
            print '\nEQ data read success\n'
            status = Label(bottomframe, text = 'EQ data read success!', bd = 1, fg = '#228B22',\
                 relief = SUNKEN, anchor =W)
            status.grid(row = 16, sticky=N+E+S+W, columnspan = 2)
            identify = 1

        except:
            identify = 3
            print '\nWrong EQ file name or file does not exist!'
            status = Label(bottomframe, text = 'Wrong EQ file name or file does not exist!', \
                bd = 1, fg='red',relief = SUNKEN, anchor =W)
            status.grid(row = 16, sticky=N+E+S+W, columnspan = 2)
            break
            


        if identify ==1:

            try:
                DOMTree_SSH = xml.dom.minidom.parse(fname_SSH)
                collection_SSH = DOMTree_SSH.documentElement
                print 'SSH data read success\n'
                status = Label(bottomframe, text = 'SSH data read succeed!', bd = 1, fg = '#228B22',\
                    relief = SUNKEN, anchor =W)
                status.grid(row = 17, sticky=N+E+S+W, columnspan = 2)
                break
            
        
            

            except:
                identify = 3
                print 'Wrong SSH file name or file does not exist!\n'

                status = Label(bottomframe, text = 'Wrong SSH file name or file does not exist!', \
                    bd = 1, fg='red', relief = SUNKEN, anchor =W)
                status.grid(row = 17, sticky=N+E+S+W, columnspan = 2)
                break


    if identify == 3: 
        status = Label(bottomframe, text = 'Failed! Please check above message!', bd = 1, fg='red',\
             relief = SUNKEN, anchor =W)
        status.grid(row = 18, sticky=N+E+S+W, columnspan = 2)
        
    else:
        execfile("Assignment1.py")
        status = Label(bottomframe, text = 'Succeed! Please EXIT and check Database 5bus!', bd = 1, \
            fg = '#228B22',relief = SUNKEN, anchor =W)
        status.grid(row = 18, sticky=N+E+S+W, columnspan = 2)







Login = Tk()

topframe = Frame(Login)
topframe.grid(rowspan = 10, columnspan = 2)
bottomframe = Frame(Login)
bottomframe.grid(row = 11, rowspan = 10, columnspan = 2)





course = Label(topframe, text = 'Assignment 1 \n Microgrid Data Parsing', bg = 'grey', fg='black')
course.grid(row = 0, column = 0 ,sticky = E + W)

ST = Label(topframe, text = 'Log In--------------------------------', bg = 'brown', fg='white')
ST.grid(row = 0, column = 1 ,sticky = E + W)

var_host=StringVar()
var_user=StringVar()
var_passwd=StringVar()
var_dbName=StringVar()
var_port=StringVar()
var_host.set('localhost')
var_user.set('root')
var_passwd.set('1993')
var_dbName.set('5bus')
var_port.set(3306)







host = ''
user = ''
passwd = ''
db = ''
port = ''

label__host = Label(topframe , text = 'host')
label__user = Label(topframe , text = 'User')
label__passwd = Label(topframe , text = 'Password')
label__dbName = Label(topframe , text = 'Database Name')
label__port = Label(topframe , text = 'Port')

entry_host = Entry(topframe, textvariable=var_host, insertofftime = 400, insertontime = 300 )
entry_user = Entry(topframe, textvariable=var_user, insertofftime = 400, insertontime = 300  )
entry_passwd = Entry(topframe, textvariable=var_passwd,show = '*', insertofftime = 400, insertontime = 300 )
entry_dbName = Entry(topframe, textvariable=var_dbName, insertofftime = 400, insertontime = 300 )
entry_port = Entry(topframe, textvariable=var_port, insertofftime = 400, insertontime = 300 )

label__host.grid(row = 1, sticky = E)  #NSWE to show the place
label__user.grid(row = 2, sticky = E)
label__passwd.grid(row = 3, sticky = E)
label__dbName.grid(row = 4, sticky = E)
label__port.grid(row = 5, sticky = E)
entry_host.grid(row = 1, column = 1,sticky = W)
entry_user.grid(row = 2, column = 1,sticky = W)
entry_passwd.grid(row = 3, column = 1,sticky = W)
entry_dbName.grid(row = 4, column = 1,sticky = W)
entry_port.grid(row = 5, column = 1,sticky = W)



insertButt = Button(topframe, text = 'Log In', command=write_entry_db)
insertButt.grid(row = 7, column = 0, padx = 4 , pady = 1)
printButt = Button(topframe, text = 'Exit', command=quit)
printButt.grid(row = 7, column = 1, padx = 4 , pady = 1)



status = Label(topframe, bd = 1,text = 'Waiting for MySQL server', relief = SUNKEN, anchor =W)
status.grid(row = 8, sticky=N+E+S+W, columnspan = 2)
status = Label(topframe, text = '                    ', bd = 1, relief = SUNKEN, anchor =W)
status.grid(row = 9, sticky=N+E+S+W, columnspan = 2)




separate = Label(bottomframe, \
    text = '-------------------------Please Login First-------------------------', \
    bg = 'grey', fg='black')
separate.grid(row = 11, columnspan = 2 ,sticky = W)

File_read = Label(bottomframe, text = 'Input File Names', bg = 'brown', fg='white')
File_read.grid(row = 12, columnspan = 2 ,sticky = E + W)

var_EQ=StringVar()
var_SSH=StringVar()
var_EQ.set('microgrid_EQ.xml')
var_SSH.set('microgrid_SSH.xml')

EQ_name = ''
SSH_name = ''

label__EQ = Label(bottomframe , text = 'EQ File Name')
label__SSH = Label(bottomframe , text = 'SSH File Name')


entry_EQ = Entry(bottomframe, textvariable=var_EQ , insertofftime = 400, insertontime = 300)
entry_SSH = Entry(bottomframe, textvariable=var_SSH, insertofftime = 400, insertontime = 300)


label__EQ.grid(row = 13, sticky = E)  #NSWE to show the place
label__SSH.grid(row = 14, sticky = E)

entry_EQ.grid(row = 13, column = 1)
entry_SSH.grid(row = 14, column = 1)

InputButt = Button(bottomframe, text = 'Confirm', command=write_entry_file)
InputButt.grid(row = 15, column = 0, padx = 3 , pady = 1)
ExitButt = Button(bottomframe, text = 'Exit', command=quit)
ExitButt.grid(row = 15, column = 1, padx = 3 , pady = 1)


status = Label(bottomframe, text = 'Waiting for Operation', bd = 1, relief = SUNKEN, anchor =W)
status.grid(row = 16, sticky=N+E+S+W, columnspan = 2)


Login.mainloop()