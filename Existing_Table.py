import xml.dom.minidom
from Tkinter import *
import tkMessageBox



import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os


print 'Tables checking, if not exist, creat new table'

cur.execute("""CREATE TABLE IF NOT EXISTS BaseVoltage(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    nominalValue float(20))""")

print 'Table BaseVoltage created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS Substation(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    region_rdf varchar(50))""")

print 'Table Substation created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS VoltageLevel(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name float(20), 
    substation_rdf varchar(50),      
    baseVoltage_rdf varchar(50), 
    FOREIGN KEY (substation_rdf) REFERENCES Substation(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table VoltageLevel created\n'


cur.execute("""CREATE TABLE IF NOT EXISTS GeneratingUnit(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    maxP float(20), 
    minP float(20), 
    equipmentContainer_rdf varchar(50) )""")

print 'Table GeneratingUnit created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS SynchronousMachine(
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

cur.execute("""CREATE TABLE IF NOT EXISTS RegulatingControl(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    targetValue float(20) )""")

print 'Table RegulatingControl created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS PowerTransformer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    equipmentContainer_rdf varchar(50) )""")

print 'Table PowerTransformer created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS EnergyConsumer(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    P float(30), 
    Q float(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table EnergyConsumer created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS PowerTransformerEnd(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    Transformer_r float(30), 
    Transformer_x float(30), 
    Transformer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (Transformer_rdf) REFERENCES PowerTransformer(rdf) ON DELETE SET NULL,
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table PowerTransformerEnd created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS Breaker(
    rdf varchar(50) NOT NULL PRIMARY KEY,
    name varchar(20), 
    state varchar(30), 
    equipmentContainer_rdf varchar(50), 
    baseVoltage_rdf varchar(50),
    FOREIGN KEY (baseVoltage_rdf) REFERENCES BaseVoltage(rdf) ON DELETE SET NULL)""")

print 'Table Breaker created\n'

cur.execute("""CREATE TABLE IF NOT EXISTS RatioTapChanger(
    rdf varchar(50) NOT NULL PRIMARY KEY ,
    name varchar(20), 
    step float(10) )""")

print 'Table RatioTapChanger created\n'