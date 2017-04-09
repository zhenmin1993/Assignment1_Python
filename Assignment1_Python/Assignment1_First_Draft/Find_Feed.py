from xml.dom.minidom import parse
import xml.dom.minidom


from DBoperat_class import *

import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os
import time




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




BaseVoltageTable= Feed_Table_BV(BaseVoltages, cur, conn)

BaseVoltageTable.table_write_ID("""INSERT IGNORE INTO BaseVoltage(rdf) VALUES (%s)""")
BaseVoltageTable.feed_BV("""UPDATE BaseVoltage SET nominalValue=%s
                WHERE rdf = %s """)

var_WriteStatus.set('Table BaseVoltage Writen Succeed!')
Stat_Para_Write = {'bd':1,'anchor':W, 'fg':'black'}
WriteStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


SubstationTable= Feed_Table_SS(Substations, cur, conn)

SubstationTable.table_write_ID("""INSERT IGNORE INTO Substation(rdf) VALUES (%s)""")
SubstationTable.feed_SS("""UPDATE Substation SET name=%s, region_rdf = %s
                WHERE rdf = %s """)

var_WriteStatus.set('Table Substation Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


VoltageLevelTable= Feed_Table_VL(VoltageLevels, cur, conn)

VoltageLevelTable.table_write_ID("""INSERT IGNORE INTO VoltageLevel(rdf) VALUES (%s)""")
VoltageLevelTable.feed_VL("""UPDATE VoltageLevel SET name=%s, substation_rdf = %s, baseVoltage_rdf = %s
                WHERE rdf = %s """)

var_WriteStatus.set('Table VoltageLevel Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


GeneratingUnitTable= Feed_Table_GU(GeneratingUnits, cur, conn)

GeneratingUnitTable.table_write_ID("""INSERT IGNORE INTO GeneratingUnit(rdf) VALUES (%s)""")
GeneratingUnitTable.feed_GU("""UPDATE GeneratingUnit SET name=%s,  maxP = %s, minP = %s, 
    equipmentContainer_rdf = %s WHERE rdf = %s """)

var_WriteStatus.set('Table GeneratingUnit Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)



SynchronousMachineTable= Feed_Table_SYM(SynchronousMachines, cur, conn)

SynchronousMachineTable.table_write_ID("""INSERT IGNORE INTO SynchronousMachine(rdf) VALUES (%s)""")
SynchronousMachineTable.feed_SYM("""UPDATE SynchronousMachine SET name=%s,  ratedS = %s,
    genUnit_rdf = %s, regControl_rdf = %s, equipmentContainer_rdf = %s, baseVoltage_rdf = %s WHERE rdf = %s """)

SynchronousMachineTable.SSH_feed_SYM("""UPDATE SynchronousMachine SET P=%s,  Q = %s WHERE rdf = %s """)

var_WriteStatus.set('Table SynchronousMachine Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


RegulatingControlTable= Feed_Table_RC(RegulatingControls, cur, conn)

RegulatingControlTable.table_write_ID("""INSERT IGNORE INTO RegulatingControl(rdf) VALUES (%s)""")
RegulatingControlTable.feed_RC("""UPDATE RegulatingControl SET name=%s WHERE rdf = %s """)

RegulatingControlTable.SSH_feed_RC("""UPDATE RegulatingControl SET targetValue = %s WHERE rdf = %s """)

var_WriteStatus.set('Table RegulatingControl Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


PowerTransformerTable= Feed_Table_PT(PowerTransformers, cur, conn)

PowerTransformerTable.table_write_ID("""INSERT IGNORE INTO PowerTransformer(rdf) VALUES (%s)""")
PowerTransformerTable.feed_PT("""UPDATE PowerTransformer SET name=%s, equipmentContainer_rdf = %s 
    WHERE rdf = %s """)

var_WriteStatus.set('Table PowerTransformer Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


EnergyConsumerTable= Feed_Table_EC(EnergyConsumers, cur, conn)

EnergyConsumerTable.table_write_ID("""INSERT IGNORE INTO EnergyConsumer(rdf) VALUES (%s)""")
EnergyConsumerTable.feed_EC("""UPDATE EnergyConsumer SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

EnergyConsumerTable.SSH_feed_EC("""UPDATE EnergyConsumer SET P = %s, Q = %s WHERE rdf = %s """)

var_WriteStatus.set('Table EnergyConsumer Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


PowerTransformerEndTable= Feed_Table_PTE(PowerTransformerEnds, cur, conn)

PowerTransformerEndTable.table_write_ID("""INSERT IGNORE INTO PowerTransformerEnd(rdf) VALUES (%s)""")
PowerTransformerEndTable.feed_PTE("""UPDATE PowerTransformerEnd SET name=%s, Transformer_r = %s,
    Transformer_x = %s, Transformer_rdf = %s , baseVoltage_rdf = %s WHERE rdf = %s """)

var_WriteStatus.set('Table PowerTransformerEnd Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


BreakerTable= Feed_Table_BR(Breakers, cur, conn)

BreakerTable.table_write_ID("""INSERT IGNORE INTO Breaker(rdf) VALUES (%s)""")
BreakerTable.feed_BR("""UPDATE Breaker SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

BreakerTable.SSH_feed_BR("""UPDATE Breaker SET state = %s WHERE rdf = %s """)

var_WriteStatus.set('Table Breaker Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)


RatioTapChangerTable= Feed_Table_RTC(RatioTapChangers, cur, conn)

RatioTapChangerTable.table_write_ID("""INSERT IGNORE INTO RatioTapChanger(rdf) VALUES (%s)""")
RatioTapChangerTable.feed_RTC("""UPDATE RatioTapChanger SET name=%s  WHERE rdf = %s """)

RatioTapChangerTable.SSH_feed_RTC("""UPDATE RatioTapChanger SET step = %s WHERE rdf = %s """)

var_WriteStatus.set('Table RatioTapChanger Writen Succeed!')
win.AddStatus(Stat_Para_Write, TotStructStatus, var_WriteStatus.get())
win.root.update()
time.sleep(0.2)

conn.close()