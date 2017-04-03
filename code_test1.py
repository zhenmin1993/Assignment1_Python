from xml.dom.minidom import parse
import xml.dom.minidom



import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os

host = raw_input('Host name:')
if ( len(host) < 1 ) : 
    host = 'localhost'

user = raw_input('User name:')
if ( len(user) < 1 ) : 
    user = 'root'

passwd = raw_input('Password:')
if ( len(passwd) < 1 ) : 
    passwd = '1993'

db = raw_input('Database Name:')
if ( len(db) < 1 ) : 
    db = '5bus'

port = raw_input('Port:')
if ( len(port) < 1 ) : 
    port = 3306

print 'Connecting to MySQL server'

    
try:

    conn=MySQLdb.connect(host,user,passwd,db,port)
    cur = conn.cursor()

    print 'Connected to MySQL server\n'

except:

    print 'Connection Failed! Please Check!'

execfile('Creating_Table.py')


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



class DataGet(xml.dom.minidom):
    def __init__ (self, TagName_Content, TagName_resource):
        
        self.TagName_Content = TagName_Content
        self.TagName_resource = TagName_resource
        xml.dom.minidom.__init__
        

    def __purify__(self, rdf_str_raw):
        rdf_str = rdf_str_raw.split('#')[1]
        return rdf_str

    def getID(self):
        rdfID = self.getAttribute("rdf:ID")
        return rdfID

    def get_about(self):
        rdf_about = self.getAttribute("rdf:about")
        rdf_about = self.__purify__(rdf_about)
        return rdf_about

    def getContent(self, TagName_Content):
        content = self.getElementsByTagName(self.TagName_Content)[0].childNodes[0].data
        try:
            content = float(content)
            return content
        except:
            return content

    def get_resource(self, TagName_resource):
        find_element = self.getElementsByTagName(self.TagName_resource)[0]
        rdf_resource = find_element.getAttribute("rdf:resource")
        rdf_resource = self.__purify__(rdf_resource) 
        return rdf_resource

    def getName(self):
        name = self.getContent(self, 'cim:IdentifiedObject.name')
        return name



class writeData:
    def __init__(self,cur, conn,command, data):
        self.command = command
        self.data = data
        self.cur = cur
        self.conn = conn

    def writeAttrib(self, command,data, cur):
        table_name = self.localName
        record_name = self.data[1]
        try:  
            cur.execute(self.command, self.data) 
            print 'Table',table_name,'Record %s Attributes Write Into Database Succeed!' % record_name 

        except:
            conn.rollback()
            print 'Table',table_name,'Record %s Attributes Write Into Database Failed!' % record_name 


    def writeOP(self, command, data, cur):
        table_name = self.localName
        try:  
            self.cur.execute(self.command, self.data) 
            print 'Table',table_name,'Operational Data Write Into Database Succeed!' 

        except:
            conn.rollback()
            print 'Table',table_name,'Operational Data Write Into Database Failed!' 








BaseVoltages = dict()
Substations = dict()
VoltageLevels = dict()
GeneratingUnits = dict()
SynchronousMachines = dict()
RegulatingControls = dict()
PowerTransformers = dict()
EnergyConsumers = dict()
PowerTransformerEnds = dict()
Breakers = dict()
RatioTapChangers = dict()


BaseVoltages['EQ'] = Needed_Child['EQ']['BaseVoltage']
Substations['EQ'] = Needed_Child['EQ']['Substation']
VoltageLevels['EQ'] = Needed_Child['EQ']['VoltageLevel']
GeneratingUnits['EQ'] = Needed_Child['EQ']['GeneratingUnit']
SynchronousMachines['EQ'] = Needed_Child['EQ']['SynchronousMachine']
SynchronousMachines['SSH'] = Needed_Child['SSH']['SynchronousMachine']
RegulatingControls['EQ'] = Needed_Child['EQ']['RegulatingControl']
RegulatingControls['SSH'] = Needed_Child['SSH']['RegulatingControl']
PowerTransformers['EQ'] = Needed_Child['EQ']['PowerTransformer']
EnergyConsumers['EQ'] = Needed_Child['EQ']['EnergyConsumer']
EnergyConsumers['SSH'] = Needed_Child['SSH']['EnergyConsumer']
PowerTransformerEnds['EQ'] = Needed_Child['EQ']['PowerTransformerEnd']
Breakers['EQ'] = Needed_Child['EQ']['Breaker']
Breakers['SSH'] = Needed_Child['SSH']['Breaker']
RatioTapChangers['EQ'] = Needed_Child['EQ']['RatioTapChanger']
RatioTapChangers['SSH'] = Needed_Child['SSH']['RatioTapChanger']





for BaseVoltage in BaseVoltages['EQ']:

    BaseVoltageClass = DataGet('', 'cim:BaseVoltage.nominalVoltage')
    rdfID = BaseVoltageClass.getID()
    nominalValue = BaseVoltageClass.getContent(BaseVoltage, 'cim:BaseVoltage.nominalVoltage')
    print rdfID



    if rdfID is None or nominalValue is None : continue
    data =  (rdfID, nominalValue)

    sql = """INSERT IGNORE INTO BaseVoltage(rdf, nominalValue) VALUES (%s, %s)"""






    #rdfID = getID(BaseVoltage)
    #nominalValue = getContent(BaseVoltage, 'cim:BaseVoltage.nominalVoltage')

    
    #if rdfID is None or nominalValue is None : continue
    #data =  (rdfID, nominalValue)

    #sql = """INSERT IGNORE INTO BaseVoltage(rdf, nominalValue) VALUES (%s, %s)"""
    
    #writeAttrib(BaseVoltage, sql,data)
conn.commit()
print ''



for Substation in Substations['EQ']:
    rdfID = getID(Substation)
    name = getName(Substation)
    region_rdf = get_resource(Substation, 'cim:Substation.Region')

    
    if rdfID is None or name is None or region_rdf is None: continue
    data = (rdfID, name, region_rdf)

    sql = """INSERT IGNORE INTO Substation(rdf,name,region_rdf) VALUES (%s, %s, %s)"""
   
    writeAttrib(Substation, sql,data)
conn.commit()
print ''



for VoltageLevel in VoltageLevels['EQ']:
    rdfID = getID(VoltageLevel)
    name = getName(VoltageLevel)

    substation_rdf = get_resource(VoltageLevel, 'cim:VoltageLevel.Substation')

    baseVoltage_rdf = get_resource(VoltageLevel,'cim:VoltageLevel.BaseVoltage')


    if rdfID is None or name is None or substation_rdf is None or baseVoltage_rdf is None: 
        continue
    data = (rdfID, name, substation_rdf , baseVoltage_rdf)

    sql = """INSERT IGNORE INTO VoltageLevel(rdf,name,substation_rdf , baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""

    writeAttrib(VoltageLevel, sql,data)
conn.commit()
print ''



for GeneratingUnit in GeneratingUnits['EQ']:
    rdfID = getID(GeneratingUnit)
    name = getName(GeneratingUnit)

    maxP = getContent(GeneratingUnit, 'cim:GeneratingUnit.maxOperatingP')
    minP = getContent(GeneratingUnit, 'cim:GeneratingUnit.minOperatingP')

    equipmentContainer_rdf = get_resource(GeneratingUnit,'cim:Equipment.EquipmentContainer')

    if rdfID is None or name is None or maxP is None or minP is None or equipmentContainer_rdf is None: 
        continue
    data = (rdfID, name, maxP , minP, equipmentContainer_rdf)

    sql = """INSERT IGNORE INTO GeneratingUnit(rdf,name, maxP, minP , equipmentContainer_rdf) 
        VALUES (%s, %s, %s, %s, %s)"""

    writeAttrib(GeneratingUnit, sql,data)
conn.commit()



for SynchronousMachine in SynchronousMachines['EQ']:
    rdfID = getID(SynchronousMachine)
    name = getName(SynchronousMachine)

    ratedS = getContent(SynchronousMachine,'cim:RotatingMachine.ratedS')

    
    genUnit_rdf = get_resource(SynchronousMachine,'cim:RotatingMachine.GeneratingUnit')
    
    regControl_rdf = get_resource(SynchronousMachine,'cim:RegulatingCondEq.RegulatingControl')
    
    equipmentContainer_rdf = get_resource(SynchronousMachine,'cim:Equipment.EquipmentContainer')

       
    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    

    if rdfID is None or name is None or ratedS is None or genUnit_rdf is None \
        or regControl_rdf is None or equipmentContainer_rdf is None \
            or baseVoltage_rdf is None:  continue
    data = (rdfID, name, ratedS , genUnit_rdf, regControl_rdf, equipmentContainer_rdf, baseVoltage_rdf)

    sql = """INSERT IGNORE INTO SynchronousMachine(rdf,name, ratedS , genUnit_rdf, regControl_rdf, 
        equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    writeAttrib(SynchronousMachine, sql,data)
conn.commit()



for SynchronousMachine in SynchronousMachines['SSH']:
    rdfID = get_about(SynchronousMachine)

    P = getContent(SynchronousMachine,'cim:RotatingMachine.p')
    Q = getContent(SynchronousMachine,'cim:RotatingMachine.q')


    if rdfID is None or P is None or Q is None: continue
    data = (P, Q,rdfID)

    sql = """UPDATE SynchronousMachine SET P=%s, Q=%s 
        WHERE rdf = %s """
    
    writeOP(SynchronousMachine, sql, data) 
conn.commit()
print ''



for RegulatingControl in RegulatingControls['EQ']:
    rdfID = getID(RegulatingControl)
    name = getName(RegulatingControl)
    
    if rdfID is None or name is None: continue
    data =(rdfID, name) 

    sql = """INSERT IGNORE INTO RegulatingControl(rdf,name) 
        VALUES (%s, %s)"""

    writeAttrib(RegulatingControl, sql,data)
conn.commit()


for RegulatingControl in RegulatingControls['SSH']:
    rdfID = get_about(RegulatingControl)
    targetValue =  getContent(RegulatingControl,'cim:RegulatingControl.targetValue')
    
    if rdfID is None or targetValue is None : continue
    data = (targetValue, rdfID)

    sql = """UPDATE RegulatingControl SET targetValue = %s 
        WHERE rdf = %s """
    
    writeOP(RegulatingControl, sql, data) 
conn.commit()
print ''



for PowerTransformer in PowerTransformers['EQ']:
    rdfID = getID(PowerTransformer)
    name = getName(PowerTransformer)

    equipmentContainer_rdf = get_resource(PowerTransformer,'cim:Equipment.EquipmentContainer')
    
    if rdfID is None or name is None or equipmentContainer_rdf is None: continue
    data = (rdfID, name, equipmentContainer_rdf)

    sql = """INSERT IGNORE INTO PowerTransformer(rdf,name, equipmentContainer_rdf) 
        VALUES (%s, %s, %s)"""

    writeAttrib(PowerTransformer, sql,data)

conn.commit()
print ''



for EnergyConsumer in EnergyConsumers['EQ']:
    rdfID = getID(EnergyConsumer)
    name = getName(EnergyConsumer)

    equipmentContainer_rdf = get_resource(EnergyConsumer,'cim:Equipment.EquipmentContainer')


    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    

    if rdfID is None or name is None or equipmentContainer_rdf is None \
        or baseVoltage_rdf is None :  continue
    data = (rdfID, name, equipmentContainer_rdf, baseVoltage_rdf)

    sql = """INSERT IGNORE INTO EnergyConsumer(rdf,name, equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""
    writeAttrib(EnergyConsumer, sql,data)
conn.commit()


for EnergyConsumer in EnergyConsumers['SSH']:
    rdfID = get_about(EnergyConsumer)

    P = getContent(EnergyConsumer,'cim:EnergyConsumer.p')
    Q = getContent(EnergyConsumer,'cim:EnergyConsumer.q')

    if rdfID is None or P is None or Q is None: continue
    data = ( P, Q,  rdfID,)
    
    sql = """UPDATE EnergyConsumer SET P=%s, Q=%s 
        WHERE rdf = %s """
    
    writeOP(EnergyConsumer, sql,data) 
conn.commit()
print ''



for PowerTransformerEnd in PowerTransformerEnds['EQ']:
    rdfID = getID(PowerTransformerEnd)
    name = getName(PowerTransformerEnd)

    Transformer_r = getContent(PowerTransformerEnd,'cim:PowerTransformerEnd.r')

    Transformer_x = getContent(PowerTransformerEnd,'cim:PowerTransformerEnd.x')

    Transformer_rdf = get_resource(PowerTransformerEnd,'cim:PowerTransformerEnd.PowerTransformer')
    
    baseVoltage_rdf = get_resource(PowerTransformerEnd,'cim:TransformerEnd.BaseVoltage')
    
   
    if rdfID is None or name is None or Transformer_r is None or Transformer_x is None \
        or Transformer_rdf is None or baseVoltage_rdf is None :  continue
    data = (rdfID, name,  Transformer_r,  Transformer_x, Transformer_rdf, baseVoltage_rdf)

    sql = """INSERT IGNORE INTO PowerTransformerEnd(rdf,name, Transformer_r,  Transformer_x, 
        Transformer_rdf, baseVoltage_rdf) VALUES (%s, %s, %s, %s, %s, %s)"""
    
    writeAttrib(PowerTransformerEnd, sql,data)
conn.commit()
print ''



for Breaker in Breakers['EQ']:
    rdfID = getID(Breaker)
    name = getName(Breaker)

    equipmentContainer_rdf =  get_resource(Breaker,'cim:Equipment.EquipmentContainer')


    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    
    if rdfID is None or name is None or equipmentContainer_rdf is None \
        or baseVoltage_rdf is None :  continue
    data = (rdfID, name, equipmentContainer_rdf, baseVoltage_rdf)

    sql = """INSERT IGNORE INTO Breaker(rdf,name, equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""

    writeAttrib(Breaker, sql,data)
conn.commit()


for Breaker in Breakers['SSH']:
    rdfID = get_about(Breaker)
    state = getContent(Breaker,'cim:Switch.open')

    if rdfID is None or state is None : continue
    data = (state,rdfID)
    
    sql = """UPDATE Breaker SET state=%s WHERE rdf = %s """
    
    writeOP(Breaker, sql,data)
conn.commit()
print ''



for RatioTapChanger in RatioTapChangers['EQ']:
    rdfID = getID(RatioTapChanger)
    name = getContent(RatioTapChanger,'cim:IdentifiedObject.name')
   
    if rdfID is None or name is None: continue
    data = (rdfID, name)

    sql = """INSERT IGNORE INTO RatioTapChanger(rdf,name) 
        VALUES (%s, %s)"""

    writeAttrib(RatioTapChanger, sql,data)

conn.commit()
print ''



for RatioTapChanger in RatioTapChangers['SSH']:
    rdfID = get_about(RatioTapChanger)

    step = getContent(RatioTapChanger,'cim:TapChanger.step')
    
    if rdfID is None or step is None : continue
    data = (step,rdfID)
    
    sql = """UPDATE RatioTapChanger SET step=%s WHERE rdf = %s """
    
    writeOP(RatioTapChanger, sql,data)
conn.commit()
print ''

conn.close()
