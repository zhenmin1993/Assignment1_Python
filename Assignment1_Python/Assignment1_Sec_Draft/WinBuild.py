from xml.dom.minidom import parse
import xml.dom.minidom

import MySQLdb

from Tkinter import *
import tkMessageBox
import Tkinter as tk

from GUI_Class import *

import sys
import os




def LoginButtonFunc(): 
    print 'Connecting to MySQL server'
    Message = 'Connecting to MySQL server'

    var_Log.set('Connecting to MySQL server')
    Stat_Para_Log_Init = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_Log_Init, LogStructStatus, var_Log.get())
    win.root.update()

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

        var_Log.set('Connected to MySQL server')
        Stat_Para_Log_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
        win.AddStatus(Stat_Para_Log_success, LogStructStatus, var_Log.get())
        win.root.update()
        tkMessageBox.showinfo(title='Computer Application', \
            message='Server Connected! Please Continue!')


    except:
        Message = 'Connection Failed! Please Check!'
        print 'Connection Failed! Please Check!'

        var_Log.set('Connection Failed! Please Check!')
        Stat_Para_Log_fail = {'bd':1,'anchor':W, 'fg':'red'}
        win.AddStatus(Stat_Para_Log_fail, LogStructStatus, var_Log.get())
        win.root.update()





def ExitButtonFunc():
    answer = tkMessageBox.askquestion('Computer Application', 'Are you sure to EXIT?')

    if answer == 'yes':
        win.DestroySelf()      
        sys.exit()


def Update_Status(New_Message, Fon_Color):    
    var_TotStatus.set(New_Message)
    Stat_Para_Tot_update= {'bd':1,'anchor':W, 'fg':Fon_Color}
    TotStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3}
    win.AddStatus(Stat_Para_Tot_update, TotStructStatus, var_TotStatus.get())
    win.root.update()




def ConfirmButtonFunc():
    fname_EQ =  var_EQName.get()
    fname_SSH = var_SSHName.get()
    global collection_EQ
    global collection_SSH
    while True:

        identify = 0
        try:
            DOMTree_EQ = xml.dom.minidom.parse(fname_EQ)
            collection_EQ = DOMTree_EQ.documentElement
            print '\nEQ data read success\n'

            var_EQCheck.set('EQ data read succeed!')
            Stat_Para_EQCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
            win.AddStatus(Stat_Para_EQCheck_success, EQCheckStructStatus, var_EQCheck.get())
            win.root.update()

            identify = 1

        except:
            identify = 3
            print '\nWrong EQ file name or file does not exist!'

            var_EQCheck.set('Wrong EQ file name or file does not exist!')

            Stat_Para_EQCheck_fail = {'bd':1,'anchor':W, 'fg':'red'}
            win.AddStatus(Stat_Para_EQCheck_fail, EQCheckStructStatus, var_EQCheck.get())
            win.root.update()
            break
            


        if identify ==1:

            try:
                DOMTree_SSH = xml.dom.minidom.parse(fname_SSH)
                collection_SSH = DOMTree_SSH.documentElement
                print 'SSH data read success\n'

                var_SSHCheck.set('SSH data read succeed!')

                Stat_Para_SSHCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
                win.AddStatus(Stat_Para_SSHCheck_success, SSHCheckStructStatus, var_SSHCheck.get())
                win.root.update()
                identify =2

                var_TabCheck.set('File Name checking passed!')
                Stat_Para_TabCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
                win.AddStatus(Stat_Para_TabCheck_success, TabCheckStructStatus, var_TabCheck.get())
                win.root.update()

                break
            
        
            

            except:
                identify = 3
                print 'Wrong SSH file name or file does not exist!\n'

                var_SSHCheck.set('Wrong SSH file name or file does not exist!')

                Stat_Para_SSHCheck_fail= {'bd':1,'anchor':W, 'fg':'red'}
                win.AddStatus(Stat_Para_SSHCheck_fail, SSHCheckStructStatus, var_SSHCheck.get())
                win.root.update()
                break

    if identify ==2:
        try:
            execfile("SearchFile.py")

        except:
            identify = 3
            var_WriteStatus.set('Searching File Failed')
            Stat_Para_NoConnect = {'bd':1,'anchor':W, 'fg':'red'}
            WriteStructStatus = {'row':15, 'sticky':N+E+S+W, 'columnspan':3}
            win.AddStatus(Stat_Para_NoConnect, WriteStructStatus, var_WriteStatus.get())


    if identify == 3: 

        New_Message = 'Failed! Please check above message!'
        Update_Status(New_Message, 'red')



    try:
        cur_test = cur
        conn_test = conn
        connect_condition = 'OK'

    except:
        tkMessageBox.showinfo(title='Computer Application', \
            message='No Connection to MySQL Server! Please First Login!')
        New_Message = 'No Connection to MySQL Server! Please First Login!'
        Update_Status(New_Message, 'red')

    if connect_condition is 'OK':
        try:
            answer = tkMessageBox.askquestion('Computer Application', 'Creating new tables?')
            New_Table_Choice = 0
            if answer == 'yes': New_Table_Choice = 1
               
            execfile("Find_Feed.py")
            New_Message = '''Succeed! Please Exit and check Database 5bus!\nServer Now Disconnected for Protection!'''
            Update_Status(New_Message, '#228B22')

            tkMessageBox.showinfo(title='Computer Application', message='All Tables Are Now Ready!')


        except:
            New_Message = '''Failed! Please Check'''
            Update_Status(New_Message, 'red')








win = MyWindow()


Lab_Para_Title = {'bg':'grey', 'fg':'black'}
TitleStructLab = {'row':0,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Computer Application in Power Systems\n Assignment 1' , Lab_Para_Title, TitleStructLab  )


Lab_Para_Log = {'bg':'brown', 'fg':'white'}
LogStructLab = {'row':1,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Please Log In First' , Lab_Para_Log, LogStructLab )


Lab_Para_host = {'bg':None, 'fg':'black'}
hostStructLab = {'row':2,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('host' , Lab_Para_host, hostStructLab)


global var_host
var_host=StringVar()
var_host.set('localhost')

Entr_Para_host = {'off':400,'on':300, 'show':None}
hostStructEntr = {'row':2, 'column':1,'sticky':W}
win.AddEntry(var_host , Entr_Para_host , hostStructEntr)


Lab_Para_User = {'bg':None, 'fg':'black'}
UserStructLab = {'row':3,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('User' , Lab_Para_User, UserStructLab)


global var_user
var_user=StringVar()
var_user.set('root')

Entr_Para_User = {'off':400,'on':300, 'show':None}
UserStructEntr = {'row':3, 'column':1,'sticky':W}
win.AddEntry(var_user, Entr_Para_User , UserStructEntr)



Lab_Para_Passwd = {'bg':None, 'fg':'black'}
PasswdStructLab = {'row':4,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Password' , Lab_Para_Passwd, PasswdStructLab)


global var_passwd
var_passwd=StringVar()
var_passwd.set('1993')

Entr_Para_Passwd = {'off':400,'on':300, 'show':'*'}
PasswdStructEntr = {'row':4, 'column':1,'sticky':W}
win.AddEntry(var_passwd, Entr_Para_Passwd , PasswdStructEntr)



Lab_Para_dbName = {'bg':None, 'fg':'black'}
dbNameStructLab = {'row':5,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Database Name' , Lab_Para_dbName, dbNameStructLab)


global var_dbName
var_dbName=StringVar()
var_dbName.set('5bus')

Entr_Para_dbName = {'off':400,'on':300, 'show':None}
dbNameStructEntr = {'row':5, 'column':1,'sticky':W}
win.AddEntry(var_dbName, Entr_Para_dbName , dbNameStructEntr)



Lab_Para_Port = {'bg':None, 'fg':'black'}
PortStructLab = {'row':6,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Port' , Lab_Para_Port, PortStructLab)


global var_port
var_port=StringVar()
var_port.set(3306)

Entr_Para_Port = {'off':400,'on':300, 'show':None}
PortStructEntr = {'row':6, 'column':1,'sticky':W}
win.AddEntry(var_port, Entr_Para_Port , PortStructEntr)



LogStructImag = {'row':2,'rowspan':4,'columnspan':2, 'column':2,'sticky':W+E+N+S, 'padx':5, 'pady':5}
file_name = 'pic2.gif'
win.AddImage('pic2.gif', LogStructImag)


LogStructButt = {'row':7,'column':2,'padx':4,'pady':1}
win.AddButton('Log In', LoginButtonFunc, LogStructButt)


ExitStructButt = {'row':7,'column':3,'padx':4,'pady':1}
win.AddButton('Exit', ExitButtonFunc, ExitStructButt)



global var_Log
var_Log=StringVar()
var_Log.set('Waiting For Operation')


Stat_Para_Log = {'bd':1,'anchor':W, 'fg':'black'}
LogStructStatus = {'row':8, 'sticky':N+E+S+W, 'columnspan':3}

win.AddStatus(Stat_Para_Log, LogStructStatus, var_Log.get())



Lab_Para_FileName = {'bg':'brown', 'fg':'white'}
FileNameStructLab = {'row':9,'columnspan':4, 'sticky':N+E+S+W, 'rowspan':1, 'column':0}
win.AddLabel('Input the file name here' , Lab_Para_FileName, FileNameStructLab)



Lab_Para_EQName = {'bg':None, 'fg':'black'}
EQNameStructLab = {'row':10,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('EQ File Name' , Lab_Para_EQName, EQNameStructLab)

global var_EQName
var_EQName=StringVar()
var_EQName.set('microgrid_EQ.xml')

Entr_Para_EQName = {'off':400,'on':300, 'show':None}
EQNameStructEntr = {'row':10, 'column':1,'sticky':W}
win.AddEntry(var_EQName, Entr_Para_EQName , EQNameStructEntr)


Lab_Para_SSHName = {'bg':None, 'fg':'black'}
SSHNameStructLab = {'row':11,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('SSH File Name' , Lab_Para_SSHName, SSHNameStructLab)


global var_SSHName
var_SSHName=StringVar()
var_SSHName.set('microgrid_SSH.xml')

Entr_Para_SSHName = {'off':400,'on':300, 'show':None}
SSHNameStructEntr = {'row':11, 'column':1,'sticky':W}
win.AddEntry(var_SSHName, Entr_Para_SSHName , SSHNameStructEntr )



ConfirmStructButt = {'row':12,'column':2,'padx':4,'pady':1}
win.AddButton('Confirm', ConfirmButtonFunc, ConfirmStructButt)

Exit2StructButt = {'row':12,'column':3,'padx':4,'pady':1}
win.AddButton('Exit', ExitButtonFunc, Exit2StructButt)


global var_EQCheck
var_EQCheck=StringVar()

Stat_Para_EQCheck = {'bd':1,'anchor':W, 'fg':'black'}
EQCheckStructStatus = {'row':13, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_EQCheck, EQCheckStructStatus, var_EQCheck.get())


global var_SSHCheck
var_SSHCheck=StringVar()

Stat_Para_SSHCheck = {'bd':1,'anchor':W, 'fg':'black'}
SSHCheckStructStatus = {'row':14, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_SSHCheck, SSHCheckStructStatus, var_SSHCheck.get())



global var_TabCheck
var_TabCheck=StringVar()

Stat_Para_TabCheck = {'bd':1,'anchor':W, 'fg':'black'}
TabCheckStructStatus = {'row':15, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_TabCheck, TabCheckStructStatus, var_TabCheck.get())


global var_WriteStatus
var_WriteStatus=StringVar()

Stat_Para_Write = {'bd':1,'anchor':W, 'fg':'black'}
WriteStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_Write, WriteStructStatus, var_WriteStatus.get())


global var_TotStatus
var_TotStatus=StringVar()

Stat_Para_Tot = {'bd':1,'anchor':W, 'fg':'black'}
TotStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_Tot, TotStructStatus, var_TotStatus.get())

Lab_Para_Separate = {'bg':None, 'fg':None}
SeparateStructLab = {'row':0,'columnspan':1, 'sticky':E, 'rowspan':17, 'column':4}
win.AddLabel(None, Lab_Para_Separate, SeparateStructLab)


Lab_Para_Bus = {'bg':'grey', 'fg':'black'}
BusStructLab = {'row':0,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':5}
win.AddLabel('5-Bus\nMatrix' , Lab_Para_Bus, BusStructLab)



win.root.mainloop()