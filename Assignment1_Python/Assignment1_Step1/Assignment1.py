from xml.dom.minidom import parse
import xml.dom.minidom



import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os


while True:
    print 'Enter file name EQ (this file should contain equipment attributes)'
    fname_EQ = raw_input('File EQ name ("EXT" to quit):')
    
    if ( len(fname_EQ) < 1 ) : 
        fname_EQ = 'microgrid_EQ.xml'
        
    print '\nEnter file name SSH (this file should contain equipment attributes)'
    fname_SSH = raw_input('File SSH name ("EXT" to quit):')
    
    if ( len(fname_SSH) < 1 ) : 
        fname_SSH = 'microgrid_SSH.xml'
        
    if fname_EQ == 'EXT' and fname_SSH != 'EXT':
        print '\nPlease give me correct file name then' 
        continue
    if fname_EQ == 'EXT' and fname_SSH == 'EXT' : 
        identify = 3
        break
    identify = 0
    try:
        DOMTree_EQ = xml.dom.minidom.parse(fname_EQ)
        collection_EQ = DOMTree_EQ.documentElement
        print '\nEQ data read success\n'
    except:
        identify = 1
        print '\nWrong EQ file name or file does not exist!'

    if identify == 1: continue
    try:
        DOMTree_SSH = xml.dom.minidom.parse(fname_SSH)
        collection_SSH = DOMTree_SSH.documentElement
        print 'SSH data read success\n'
        
        break

    except:
        identify = 2
        print 'Wrong SSH file name or file does not exist!\n'

if identify == 3: sys.exit()



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
    #print type(name), 'EQ'
    All_Child['SSH'][name] = collection_SSH.getElementsByTagName("cim:"+name)
    #print name, 'SSH'

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





execfile("Creating_Table.py")
execfile("myfun.py")
execfile("Find_Feed.py")

