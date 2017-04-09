from xml.dom.minidom import parse
import xml.dom.minidom
from Tkinter import *

import xml.etree.ElementTree as ET
import MySQLdb

import sys
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
ACLineSegments = dict()


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
ACLineSegments['EQ'] = Needed_Child['EQ']['ACLineSegment']


print 'Creating New Tables'

v='varchar(50)'
f = 'float(30)'

BaseVoltageTable= Feed_Table_BV(BaseVoltages, cur, conn)

BV_name_type = {'nominalValue':f}
BaseVoltageTable.New_Table_No_FK('BaseVoltage',BV_name_type)

print 'Table BaseVoltage created\n'

var_TabCheck.set('Tables BaseVoltage Created')
Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'black'}
TabCheckStructStatus = {'row':9, 'sticky':N+E+S+W, 'columnspan':3}
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()
time.sleep(0.1)


SubstationTable= Feed_Table_SS(Substations, cur, conn)

SS_name_type = {'name':v, 'region_rdf':v,}
SubstationTable.New_Table_No_FK('BaseVoltage',SS_name_type)

print 'Table Substation created\n'

var_TabCheck.set('Table Substation Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



VoltageLevelTable= Feed_Table_VL(VoltageLevels, cur, conn)

VL_name_type = {'name':f, 'substation_rdf':v,'baseVoltage_rdf':v}
VL_FK_from_to = {'substation_rdf':'Substation', 'baseVoltage_rdf':'BaseVoltage'}
VoltageLevelTable.New_Table_Has_FK('VoltageLevel',VL_name_type, VL_FK_from_to)

print 'Table VoltageLevel created\n'

var_TabCheck.set('Table VoltageLevel Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



GeneratingUnitTable= Feed_Table_GU(GeneratingUnits, cur, conn)

GU_name_type = {'name':v, 'maxP':f,'minP':f, 'equipmentContainer_rdf':v}
GeneratingUnitTable.New_Table_No_FK('GeneratingUnit',GU_name_type)

print 'Table GeneratingUnit created\n'

var_TabCheck.set('Table GeneratingUnit Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



SynchronousMachineTable= Feed_Table_SYM(SynchronousMachines, cur, conn)

SYM_name_type = {'name':v, 'ratedS':f,'P':f,'Q':f,'genUnit_rdf':v ,'regControl_rdf':v , \
            'equipmentContainer_rdf':v, 'baseVoltage_rdf':v}

SYM_FK_from_to = {'genUnit_rdf':'GeneratingUnit', 'regControl_rdf':'RegulatingControl', \
                'baseVoltage_rdf':'BaseVoltage' }

SynchronousMachineTable.New_Table_Has_FK('SynchronousMachine',SYM_name_type, SYM_FK_from_to)

print 'Table SynchronousMachine created\n'

var_TabCheck.set('Table SynchronousMachine Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



RegulatingControlTable= Feed_Table_RC(RegulatingControls, cur, conn)

RC_name_type = {'name':v, 'targetValue':f}
RegulatingControlTable.New_Table_No_FK('RegulatingControl',RC_name_type)


print 'Table RegulatingControl created\n'

var_TabCheck.set('Table RegulatingControl Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



PowerTransformerTable= Feed_Table_PT(PowerTransformers, cur, conn)

PT_name_type = {'name':v, 'equipmentContainer_rdf':v}
PowerTransformerTable.New_Table_No_FK('PowerTransformer',PT_name_type)

print 'Table PowerTransformer created\n'

var_TabCheck.set('Table PowerTransformer Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



EnergyConsumerTable= Feed_Table_EC(EnergyConsumers, cur, conn)

EC_name_type = {'name':v, 'P':f,'Q':f,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
EC_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }
EnergyConsumerTable.New_Table_Has_FK('EnergyConsumer',EC_name_type, EC_FK_from_to)

print 'Table EnergyConsumer created\n'

var_TabCheck.set('Table EnergyConsumer Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



PowerTransformerEndTable= Feed_Table_PTE(PowerTransformerEnds, cur, conn)

PTE_name_type = {'name':v, 'Transformer_r':f,'Transformer_x':f,'Transformer_rdf':v ,'baseVoltage_rdf':v }
PTE_FK_from_to = {'Transformer_rdf':'PowerTransformer','baseVoltage_rdf':'BaseVoltage' }
PowerTransformerEndTable.New_Table_Has_FK('PowerTransformerEnd',PTE_name_type, PTE_FK_from_to)

print 'Table PowerTransformerEnd created\n'

var_TabCheck.set('Table PowerTransformerEnd Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()



BreakerTable= Feed_Table_BR(Breakers, cur, conn)


BR_name_type = {'name':v, 'state':v,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
BR_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }
BreakerTable.New_Table_Has_FK('Breaker',BR_name_type, BR_FK_from_to)

print 'Table Breaker created\n'

var_TabCheck.set('Table Breaker Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()




RatioTapChangerTable= Feed_Table_RTC(RatioTapChangers, cur, conn)

RTC_name_type = {'name':v, 'step':f}
RatioTapChangerTable.New_Table_No_FK('RatioTapChanger',RTC_name_type)

print 'Table RatioTapChanger created\n'

var_TabCheck.set('Table RatioTapChanger Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()




ACLineSegmentTable= Feed_Table_ACL(ACLineSegments, cur, conn)

ACL_name_type = {'name':v, 'ACLineSegment_r':f, 'ACLineSegment_x':f, \
                    'ACLineSegment_bch':f, 'ACLineSegment_gch':f,\
                    'equipmentContainer_rdf':v}
ACLineSegmentTable.New_Table_No_FK('ACLineSegment',ACL_name_type)

print 'Table ACLineSegment created\n'

var_TabCheck.set('Table ACLineSegment Created')
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()

