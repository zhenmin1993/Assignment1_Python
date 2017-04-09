from xml.dom.minidom import parse
import xml.dom.minidom
from Tkinter import *

import xml.etree.ElementTree as ET
import MySQLdb

import sys







# Make some fresh tables
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


print 'Creating New Tables'

cur.execute("""CREATE TABLE BaseVoltage(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    nominalValue float(20))""")

print 'Table BaseVoltage created\n'

cur.execute("""CREATE TABLE Substation(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    region_rdf varchar(50))""")

print 'Table Substation created\n'

cur.execute("""CREATE TABLE VoltageLevel(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name float(20), 
    substation_rdf varchar(50),      
    baseVoltage_rdf varchar(50), 
    FOREIGN KEY (substation_rdf) REFERENCES Substation(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table VoltageLevel created\n'


cur.execute("""CREATE TABLE GeneratingUnit(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    maxP float(20), 
    minP float(20), 
    equipmentContainer_rdf varchar(50) )""")

print 'Table GeneratingUnit created\n'

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

print 'Table SynchronousMachine created\n'

cur.execute("""CREATE TABLE RegulatingControl(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    targetValue float(20) )""")

print 'Table RegulatingControl created\n'

cur.execute("""CREATE TABLE PowerTransformer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    equipmentContainer_rdf varchar(50) )""")

print 'Table PowerTransformer created\n'

cur.execute("""CREATE TABLE EnergyConsumer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    P float(30), 
    Q float(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table EnergyConsumer created\n'

cur.execute("""CREATE TABLE PowerTransformerEnd(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    Transformer_r float(30), 
    Transformer_x float(30), 
    Transformer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (Transformer_rdf) REFERENCES PowerTransformer(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table PowerTransformerEnd created\n'

cur.execute("""CREATE TABLE Breaker(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    state varchar(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table Breaker created\n'

cur.execute("""CREATE TABLE RatioTapChanger(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    step float(10) )""")

print 'Table RatioTapChanger created\n'



