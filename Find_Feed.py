from xml.dom.minidom import parse
import xml.dom.minidom



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
    rdfID = getID(BaseVoltage)
    nominalValue = getContent(BaseVoltage, 'cim:BaseVoltage.nominalVoltage')

    
    if rdfID is None or nominalValue is None : continue
    data =  (rdfID, nominalValue)

    sql = """INSERT IGNORE INTO BaseVoltage(rdf, nominalValue) VALUES (%s, %s)"""
    
    writeAttrib(BaseVoltage, sql,data)
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