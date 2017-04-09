from xml.dom.minidom import parse
import xml.dom.minidom



import MySQLdb

import sys
import os
import time



Table_Names = list()
length = dict()
length['EQ'] = len(collection_EQ.childNodes)
length['SSH'] = len(collection_SSH.childNodes)

all_eles = list()

for count in range(0,length['EQ']):
    name = collection_EQ.childNodes[count].localName
    if name == None : continue
    all_eles.append(name.encode())

for count in range(0,length['SSH']):
    name = collection_SSH.childNodes[count].localName
    if name == None : continue
    all_eles.append(name.encode())

all_eles = list(set(all_eles))



All_Child = dict()
All_Child['EQ'] = dict()
All_Child['SSH'] = dict() 
for name in all_eles:
    All_Child['EQ'][name] = collection_EQ.getElementsByTagName("cim:"+name)

    All_Child['SSH'][name] = collection_SSH.getElementsByTagName("cim:"+name)


var_WriteStatus.set('All ChildNodes Found!')
Stat_Para_Write = {'bd':1,'anchor':W, 'fg':'black'}
WriteStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_Write, WriteStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.3)


Table_Names = list()
Table_Names.append('BaseVoltage')
Table_Names.append('Substation')
Table_Names.append('VoltageLevel')
Table_Names.append('GeneratingUnit')
Table_Names.append('SynchronousMachine')
Table_Names.append('RegulatingControl')
Table_Names.append('PowerTransformer')
Table_Names.append('EnergyConsumer')
Table_Names.append('PowerTransformerEnd')
Table_Names.append('Breaker')
Table_Names.append('RatioTapChanger')

Needed_Child = dict()
Needed_Child['EQ'] = dict()
Needed_Child['SSH']= dict()

for table_name in Table_Names:
    for key in All_Child['EQ']:
        
        if table_name != key: continue
        Needed_Child['EQ'][key] = All_Child['EQ'][key]

for table_name in Table_Names:
    for key in All_Child['SSH']:
        
        if table_name != key: continue
        Needed_Child['SSH'][key] = All_Child['SSH'][key]





