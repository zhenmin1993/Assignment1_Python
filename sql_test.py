import xml.etree.ElementTree as ET
import MySQLdb


conn=MySQLdb.connect(host='localhost',user='root',passwd='1993',db='5bus',port=3306)
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.execute('SET FOREIGN_KEY_CHECKS = 0')
cur.execute('DROP TABLE IF EXISTS BaseVoltage')
cur.execute('DROP TABLE IF EXISTS Substation')
cur.execute('DROP TABLE IF EXISTS VoltageLevel')
cur.execute('DROP TABLE IF EXISTS GeneratingUnit')
cur.execute('DROP TABLE IF EXISTS SynchronousMachine')
cur.execute('DROP TABLE IF EXISTS RegulatingControl')
cur.execute('DROP TABLE IF EXISTS PowerTransformer')
cur.execute('DROP TABLE IF EXISTS EnergyConsumer')
cur.execute('DROP TABLE IF EXISTS PowerTransformerEnd')
cur.execute('DROP TABLE IF EXISTS Breaker')
cur.execute('DROP TABLE IF EXISTS RatioTapChanger')

#

cur.execute("""CREATE TABLE BaseVoltage(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    nominalValue float(20))""")

cur.execute("""CREATE TABLE Substation(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    region_rdf varchar(50))""")

cur.execute("""CREATE TABLE VoltageLevel(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name float(20), 
    substation_rdf varchar(50),      
    baseVoltage_rdf varchar(50), 
    FOREIGN KEY (substation_rdf) REFERENCES Substation(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

cur.execute("""CREATE TABLE GeneratingUnit(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    maxP float(20), 
    minP float(20), 
    equipmentContainer_rdf varchar(50) )""")

cur.execute("""CREATE TABLE SynchronousMachine(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    ratedS float(20) , 
    P float(30), 
    Q float(30), 
    genUnit_rdf varchar(50), 
    regControl_rdf varchar(50), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (genUnit_rdf) REFERENCES GeneratingUnit(rdf) ON DELETE SET NULL,
    FOREIGN KEY (regControl_rdf) REFERENCES RegulatingControl(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

cur.execute("""CREATE TABLE RegulatingControl(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    targetValue float(20) )""")

cur.execute("""CREATE TABLE PowerTransformer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    equipmentContainer_rdf varchar(50) )""")

cur.execute("""CREATE TABLE EnergyConsumer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    P float(30), 
    Q float(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

cur.execute("""CREATE TABLE PowerTransformerEnd(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    Transformer_r float(30), 
    Transformer_x float(30), 
    Transformer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (Transformer_rdf) REFERENCES PowerTransformer(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

cur.execute("""CREATE TABLE Breaker(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    state varchar(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

cur.execute("""CREATE TABLE RatioTapChanger(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    step float(10) )""")






fname1 = raw_input('Enter file name EQ: ')
if ( len(fname1) < 1 ) : fname1 = 'microgrid_EQ.xml'

fname2 = raw_input('Enter file name SSH: ')
if ( len(fname2) < 1 ) : fname2 = 'microgrid_SSH.xml'


cim = '{http://iec.ch/TC57/2013/CIM-schema-cim16#}'
entsoe = '{http://entsoe.eu/CIM/SchemaExtension/3/1#}'
md= '{http://iec.ch/TC57/61970-552/ModelDescription/1#}'
rdf='{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'

tree1 = ET.parse(fname1)
root1 = tree1.getroot()

tree2 = ET.parse(fname2)
root2 = tree2.getroot()

def purify(rdf_str_raw):
    rdf_str = rdf_str_raw.split('#')[1]
    return rdf_str

for BaseVoltage in root1.findall(cim+'BaseVoltage'):
    rdfID = BaseVoltage.attrib[rdf+'ID']
    nominalValue = BaseVoltage.find(cim+'BaseVoltage.nominalVoltage').text
    nominalValue = float(nominalValue)

    if rdfID is None or nominalValue is None : continue
    print rdfID, nominalValue

    sql = """INSERT IGNORE INTO BaseVoltage(rdf, nominalValue) VALUES (%s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, nominalValue))
  
        conn.commit()
    except:

        conn.rollback()




for Substation in root1.findall(cim+'Substation'):
    rdfID = Substation.attrib[rdf+'ID']
    name = Substation.find(cim+'IdentifiedObject.name').text
    region_rdf = Substation.find(cim+'Substation.Region').attrib[rdf+'resource']
    region_rdf = purify(region_rdf)

    if rdfID is None or name is None or region_rdf is None: continue
    print rdfID, name, region_rdf

    sql = """INSERT IGNORE INTO Substation(rdf,name,region_rdf) VALUES (%s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name,region_rdf))
  
        conn.commit()
    except:

        conn.rollback()

for VoltageLevel in root1.findall(cim+'VoltageLevel'):
    rdfID = VoltageLevel.attrib[rdf+'ID']
    name = VoltageLevel.find(cim+'IdentifiedObject.name').text
    name = float(name)
    substation_rdf = VoltageLevel.find(cim+'VoltageLevel.Substation').attrib[rdf+'resource']
    substation_rdf = purify(substation_rdf)

    baseVoltage_rdf = VoltageLevel.find(cim+'VoltageLevel.BaseVoltage').attrib[rdf+'resource']
    baseVoltage_rdf = purify(baseVoltage_rdf)


    if rdfID is None or name is None or substation_rdf is None or baseVoltage_rdf is None: 
        continue
    print rdfID, name, substation_rdf , baseVoltage_rdf

    sql = """INSERT IGNORE INTO VoltageLevel(rdf,name,substation_rdf , baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, substation_rdf , baseVoltage_rdf))
  
        conn.commit()
    except:

        conn.rollback()

for GeneratingUnit in root1.findall(cim+'GeneratingUnit'):
    rdfID = GeneratingUnit.attrib[rdf+'ID']
    name = GeneratingUnit.find(cim+'IdentifiedObject.name').text
    maxP = GeneratingUnit.find(cim+'GeneratingUnit.maxOperatingP').text
    minP = GeneratingUnit.find(cim+'GeneratingUnit.minOperatingP').text
    maxP = float(maxP)
    minP = float(minP)
    equipmentContainer_rdf = GeneratingUnit.find(cim+'Equipment.EquipmentContainer').attrib[rdf+'resource']
    equipmentContainer_rdf = purify(equipmentContainer_rdf)
    

    if rdfID is None or name is None or maxP is None or minP is None or equipmentContainer_rdf is None: 
        continue
    print rdfID, name, maxP , minP, equipmentContainer_rdf

    sql = """INSERT IGNORE INTO GeneratingUnit(rdf,name, maxP, minP , equipmentContainer_rdf) 
        VALUES (%s, %s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, maxP , minP, equipmentContainer_rdf))
  
        conn.commit()
    except:

        conn.rollback()   

for SynchronousMachine in root1.findall(cim+'SynchronousMachine'):
    rdfID = SynchronousMachine.attrib[rdf+'ID']
    name = SynchronousMachine.find(cim+'IdentifiedObject.name').text
    ratedS = SynchronousMachine.find(cim+'RotatingMachine.ratedS').text
    ratedS = float(ratedS)
    
    genUnit_rdf = SynchronousMachine.find(cim+'RotatingMachine.GeneratingUnit').attrib[rdf+'resource']
    genUnit_rdf = purify(genUnit_rdf)
    regControl_rdf = SynchronousMachine.find(cim+'RegulatingCondEq.RegulatingControl').\
        attrib[rdf+'resource']
    regControl_rdf = purify(regControl_rdf)
    equipmentContainer_rdf = SynchronousMachine.find(cim+'Equipment.EquipmentContainer').\
        attrib[rdf+'resource']
    equipmentContainer_rdf = purify(equipmentContainer_rdf)
       
    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    



    if rdfID is None or name is None or ratedS is None or genUnit_rdf is None \
        or regControl_rdf is None or equipmentContainer_rdf is None \
            or baseVoltage_rdf is None:  continue
    print rdfID, name, ratedS , genUnit_rdf, regControl_rdf, equipmentContainer_rdf, baseVoltage_rdf

    sql = """INSERT IGNORE INTO SynchronousMachine(rdf,name, ratedS , genUnit_rdf, regControl_rdf, 
        equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, ratedS , genUnit_rdf, regControl_rdf, \
            equipmentContainer_rdf, baseVoltage_rdf))
        conn.commit()

    except:

        conn.rollback() 


for SynchronousMachine in root2.findall(cim+'SynchronousMachine'):
    rdfID = SynchronousMachine.attrib[rdf+'about']
    P = SynchronousMachine.find(cim+'RotatingMachine.p').text
    Q = SynchronousMachine.find(cim+'RotatingMachine.q').text
    P = float(P)
    Q = float(Q)

    rdfID = purify(rdfID)

    if rdfID is None or P is None or Q is None: continue
    print rdfID, P, Q

    sql = """UPDATE SynchronousMachine SET P=%s, Q=%s 
        WHERE rdf = %s """
    
    try:
        cur.execute(sql,(P,Q,rdfID))
        conn.commit() 

    except: 

        conn.rollback()



for RegulatingControl in root1.findall(cim+'RegulatingControl'):
    rdfID = RegulatingControl.attrib[rdf+'ID']
    name = RegulatingControl.find(cim+'IdentifiedObject.name').text
    
    if rdfID is None or name is None: continue
    print rdfID, name

    sql = """INSERT IGNORE INTO RegulatingControl(rdf,name) 
        VALUES (%s, %s)"""

    try:
        cur.execute(sql,(rdfID, name))
        conn.commit() 

    except: 

        conn.rollback()



for RegulatingControl in root2.findall(cim+'RegulatingControl'):
    rdfID = RegulatingControl.attrib[rdf+'about']
    targetValue = RegulatingControl.find(cim+'RegulatingControl.targetValue').text
    targetValue = float(targetValue)
    rdfID = purify(rdfID)

    if rdfID is None or targetValue is None : continue
    print rdfID, targetValue

    sql = """UPDATE RegulatingControl SET targetValue = %s 
        WHERE rdf = %s """
    
    try:
        cur.execute(sql,(targetValue,rdfID))
        conn.commit() 

    except: 

        conn.rollback()


for PowerTransformer in root1.findall(cim+'PowerTransformer'):
    rdfID = PowerTransformer.attrib[rdf+'ID']
    name = PowerTransformer.find(cim+'IdentifiedObject.name').text
    equipmentContainer_rdf = PowerTransformer.find(cim+'Equipment.EquipmentContainer').attrib[rdf+'resource']
    
    if rdfID is None or name is None or equipmentContainer_rdf is None: continue
    print rdfID, name, equipmentContainer_rdf

    sql = """INSERT IGNORE INTO PowerTransformer(rdf,name, equipmentContainer_rdf) 
        VALUES (%s, %s, %s)"""

    try:
        cur.execute(sql,(rdfID, name, equipmentContainer_rdf))
        conn.commit() 

    except: 

        conn.rollback()

for EnergyConsumer in root1.findall(cim+'EnergyConsumer'):
    rdfID = EnergyConsumer.attrib[rdf+'ID']
    name = EnergyConsumer.find(cim+'IdentifiedObject.name').text

    equipmentContainer_rdf = EnergyConsumer.find(cim+'Equipment.EquipmentContainer').attrib[rdf+'resource']
    equipmentContainer_rdf = purify(equipmentContainer_rdf)

    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    

    if rdfID is None or name is None or equipmentContainer_rdf is None \
        or baseVoltage_rdf is None :  continue
    print rdfID, name, equipmentContainer_rdf, baseVoltage_rdf

    sql = """INSERT IGNORE INTO EnergyConsumer(rdf,name, equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, equipmentContainer_rdf, baseVoltage_rdf))
        conn.commit()

    except:

        conn.rollback() 

for EnergyConsumer in root2.findall(cim+'EnergyConsumer'):
    rdfID = EnergyConsumer.attrib[rdf+'about']
    P = EnergyConsumer.find(cim+'EnergyConsumer.p').text
    Q = EnergyConsumer.find(cim+'EnergyConsumer.q').text
    P = float(P)
    Q = float(Q)
    rdfID = purify(rdfID)

    if rdfID is None or P is None or Q is None: continue
    print rdfID, P, Q
    
    sql = """UPDATE EnergyConsumer SET P=%s, Q=%s 
        WHERE rdf = %s """
    
    try:
        cur.execute(sql,(P,Q,rdfID))
        conn.commit() 

    except: 

        conn.rollback()


for PowerTransformerEnd in root1.findall(cim+'PowerTransformerEnd'):
    rdfID = PowerTransformerEnd.attrib[rdf+'ID']
    name = PowerTransformerEnd.find(cim+'IdentifiedObject.name').text
    Transformer_r = PowerTransformerEnd.find(cim+'PowerTransformerEnd.r').text
    Transformer_r = float(Transformer_r)

    Transformer_x = PowerTransformerEnd.find(cim+'PowerTransformerEnd.x').text
    Transformer_x = float(Transformer_x)


    Transformer_rdf = PowerTransformerEnd.find(cim+'PowerTransformerEnd.PowerTransformer').\
        attrib[rdf+'resource']
    Transformer_rdf = purify(Transformer_rdf)

    baseVoltage_rdf = PowerTransformerEnd.find(cim+'TransformerEnd.BaseVoltage').attrib[rdf+'resource']
    baseVoltage_rdf = purify(baseVoltage_rdf)

    
    if rdfID is None or name is None or Transformer_r is None or Transformer_x is None \
        or Transformer_rdf is None or baseVoltage_rdf is None :  continue
    print rdfID, name,  Transformer_r,  Transformer_x, Transformer_rdf, baseVoltage_rdf

    sql = """INSERT IGNORE INTO PowerTransformerEnd(rdf,name, Transformer_r,  Transformer_x, 
        Transformer_rdf, baseVoltage_rdf) VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, Transformer_r,  Transformer_x, Transformer_rdf, baseVoltage_rdf))
        conn.commit()

    except:

        conn.rollback()


for Breaker in root1.findall(cim+'Breaker'):
    rdfID = Breaker.attrib[rdf+'ID']
    name = Breaker.find(cim+'IdentifiedObject.name').text

    equipmentContainer_rdf = Breaker.find(cim+'Equipment.EquipmentContainer').attrib[rdf+'resource']
    equipmentContainer_rdf = purify(equipmentContainer_rdf)

    sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
    cur.execute(sql_voltage, (equipmentContainer_rdf))
    baseVoltage_rdf = cur.fetchone()[0]
    

    if rdfID is None or name is None or equipmentContainer_rdf is None \
        or baseVoltage_rdf is None :  continue
    print rdfID, name, equipmentContainer_rdf, baseVoltage_rdf

    sql = """INSERT IGNORE INTO Breaker(rdf,name, equipmentContainer_rdf, baseVoltage_rdf) 
        VALUES (%s, %s, %s, %s)"""
    try:
   
        cur.execute(sql, (rdfID, name, equipmentContainer_rdf, baseVoltage_rdf))
        conn.commit()

    except:

        conn.rollback() 

for Breaker in root2.findall(cim+'Breaker'):
    rdfID = Breaker.attrib[rdf+'about']
    state = Breaker.find(cim+'Switch.open').text

    rdfID = purify(rdfID)

    if rdfID is None or state is None : continue
    print rdfID, state
    
    sql = """UPDATE Breaker SET state=%s WHERE rdf = %s """
    
    try:
        cur.execute(sql,(state,rdfID))
        conn.commit() 

    except: 

        conn.rollback()

for RatioTapChanger in root1.findall(cim+'RatioTapChanger'):
    rdfID = RatioTapChanger.attrib[rdf+'ID']
    name = RatioTapChanger.find(cim+'IdentifiedObject.name').text

    
    if rdfID is None or name is None: continue
    print rdfID, name

    sql = """INSERT IGNORE INTO RatioTapChanger(rdf,name) 
        VALUES (%s, %s)"""

    try:
        cur.execute(sql,(rdfID, name))
        conn.commit() 

    except: 

        conn.rollback()

for RatioTapChanger in root2.findall(cim+'RatioTapChanger'):
    rdfID = RatioTapChanger.attrib[rdf+'about']
    rdfID = purify(rdfID)

    step = RatioTapChanger.find(cim+'TapChanger.step').text
    step = float(step)
    

    if rdfID is None or step is None : continue
    print rdfID, step
    
    sql = """UPDATE RatioTapChanger SET step=%s WHERE rdf = %s """
    
    try:
        cur.execute(sql,(step,rdfID))
        conn.commit() 

    except: 

        conn.rollback()

conn.close()
