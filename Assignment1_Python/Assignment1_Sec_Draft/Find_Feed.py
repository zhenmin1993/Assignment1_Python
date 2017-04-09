from BaseClass import *
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



BaseVoltageTable= Feed_Table_BV(BaseVoltages, cur, conn)
SubstationTable= Feed_Table_SS(Substations, cur, conn)
VoltageLevelTable= Feed_Table_VL(VoltageLevels, cur, conn)
GeneratingUnitTable= Feed_Table_GU(GeneratingUnits, cur, conn)
SynchronousMachineTable= Feed_Table_SYM(SynchronousMachines, cur, conn)
RegulatingControlTable= Feed_Table_RC(RegulatingControls, cur, conn)
PowerTransformerTable= Feed_Table_PT(PowerTransformers, cur, conn)
EnergyConsumerTable= Feed_Table_EC(EnergyConsumers, cur, conn)
PowerTransformerEndTable= Feed_Table_PTE(PowerTransformerEnds, cur, conn)
BreakerTable= Feed_Table_BR(Breakers, cur, conn)
RatioTapChangerTable= Feed_Table_RTC(RatioTapChangers, cur, conn)
ACLineSegmentTable= Feed_Table_ACL(ACLineSegments, cur, conn)

v='varchar(50)'
f = 'float(30)'

BV_name_type = {'nominalValue':f}

SS_name_type = {'name':v, 'region_rdf':v,}

VL_name_type = {'name':f, 'substation_rdf':v,'baseVoltage_rdf':v}
VL_FK_from_to = {'substation_rdf':'Substation', 'baseVoltage_rdf':'BaseVoltage'}

GU_name_type = {'name':v, 'maxP':f,'minP':f, 'equipmentContainer_rdf':v}

SYM_name_type = {'name':v, 'ratedS':f,'P':f,'Q':f,'genUnit_rdf':v ,'regControl_rdf':v , \
                'equipmentContainer_rdf':v, 'baseVoltage_rdf':v}
SYM_FK_from_to = {'genUnit_rdf':'GeneratingUnit', 'regControl_rdf':'RegulatingControl', \
                'baseVoltage_rdf':'BaseVoltage' }

RC_name_type = {'name':v, 'targetValue':f}


PT_name_type = {'name':v, 'equipmentContainer_rdf':v}

EC_name_type = {'name':v, 'P':f,'Q':f,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
EC_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }

PTE_name_type = {'name':v, 'Transformer_r':f,'Transformer_x':f,'Transformer_rdf':v ,\
                'baseVoltage_rdf':v }
PTE_FK_from_to = {'Transformer_rdf':'PowerTransformer','baseVoltage_rdf':'BaseVoltage' }

BR_name_type = {'name':v, 'state':v,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
BR_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }

RTC_name_type = {'name':v, 'step':f}

ACL_name_type = {'name':v, 'ACLineSegment_r':f, 'ACLineSegment_x':f, \
                'ACLineSegment_bch':f, 'ACLineSegment_gch':f,\
                'equipmentContainer_rdf':v}


if New_Table_Choice == 1:
    var_TabCheck.set('Waiting For Table Creating...')
    Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()


    BaseVoltageTable.New_Table_No_FK('BaseVoltage',BV_name_type)
    New_Message = 'Table BaseVoltage Created!'
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SubstationTable.New_Table_No_FK('Substation',SS_name_type)
    New_Message = 'Table Substation Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    VoltageLevelTable.New_Table_Has_FK('VoltageLevel',VL_name_type, VL_FK_from_to)
    New_Message = 'Table VoltageLevel Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    GeneratingUnitTable.New_Table_No_FK('GeneratingUnit',GU_name_type)
    New_Message = 'Table GeneratingUnit Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SynchronousMachineTable.New_Table_Has_FK('SynchronousMachine',SYM_name_type, SYM_FK_from_to)
    New_Message = 'Table SynchronousMachine Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RegulatingControlTable.New_Table_No_FK('RegulatingControl',RC_name_type)
    New_Message = 'Table RegulatingControl Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerTable.New_Table_No_FK('PowerTransformer',PT_name_type)
    New_Message = 'Table PowerTransformer Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    EnergyConsumerTable.New_Table_Has_FK('EnergyConsumer',EC_name_type, EC_FK_from_to)
    New_Message = 'Table EnergyConsumer Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerEndTable.New_Table_Has_FK('PowerTransformerEnd',PTE_name_type, PTE_FK_from_to)
    New_Message = 'Table PowerTransformerEnd Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    BreakerTable.New_Table_Has_FK('Breaker',BR_name_type, BR_FK_from_to)
    New_Message = 'Table Breaker Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RatioTapChangerTable.New_Table_No_FK('RatioTapChanger',RTC_name_type)
    New_Message = 'Table RatioTapChanger Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    ACLineSegmentTable.New_Table_No_FK('ACLineSegment',ACL_name_type)
    New_Message = 'Table ACLineSegment Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    var_TabCheck.set('All Tables Created')
    Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
    win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()
    time.sleep(0.3)



if New_Table_Choice == 0:
    var_TabCheck.set('Waiting For Table Checking...')
    Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()


    BaseVoltageTable.Exist_Table_No_FK('BaseVoltage',BV_name_type)
    New_Message = 'Table BaseVoltage Checked!'
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SubstationTable.Exist_Table_No_FK('Substation',SS_name_type)
    New_Message = 'Table Substation Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    VL_FK_from_to = {'substation_rdf':'Substation', 'baseVoltage_rdf':'BaseVoltage'}
    VoltageLevelTable.Exist_Table_Has_FK('VoltageLevel',VL_name_type, VL_FK_from_to)
    New_Message = 'Table VoltageLevel Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    GeneratingUnitTable.Exist_Table_No_FK('GeneratingUnit',GU_name_type)
    New_Message = 'Table GeneratingUnit Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SynchronousMachineTable.Exist_Table_Has_FK('SynchronousMachine',SYM_name_type, SYM_FK_from_to)
    New_Message = 'Table SynchronousMachine Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RegulatingControlTable.Exist_Table_No_FK('RegulatingControl',RC_name_type)
    New_Message = 'Table RegulatingControl Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerTable.Exist_Table_No_FK('PowerTransformer',PT_name_type)
    New_Message = 'Table PowerTransformer Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    EnergyConsumerTable.Exist_Table_Has_FK('EnergyConsumer',EC_name_type, EC_FK_from_to)
    New_Message = 'Table EnergyConsumer Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerEndTable.Exist_Table_Has_FK('PowerTransformerEnd',PTE_name_type, PTE_FK_from_to)
    New_Message = 'Table PowerTransformerEnd Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    BreakerTable.Exist_Table_Has_FK('Breaker',BR_name_type, BR_FK_from_to)
    New_Message = 'Table Breaker Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RatioTapChangerTable.Exist_Table_No_FK('RatioTapChanger',RTC_name_type)
    New_Message = 'Table RatioTapChanger Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    ACLineSegmentTable.Exist_Table_No_FK('ACLineSegment',ACL_name_type)
    New_Message = 'Table ACLineSegment Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    var_TabCheck.set('All Tables Checked!')
    Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
    win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()
    time.sleep(0.15)
   


var_TabCheck.set('Waiting For Table Writting...')
Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
win.root.update()


BaseVoltageTable.table_write_ID()
BaseVoltageTable.feed_BV("""UPDATE BaseVoltage SET nominalValue=%s
                WHERE rdf = %s """)

New_Message = 'Table BaseVoltage Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



SubstationTable.table_write_ID()
SubstationTable.feed_SS("""UPDATE Substation SET name=%s, region_rdf = %s
                WHERE rdf = %s """)

New_Message = 'Table Substation Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



VoltageLevelTable.table_write_ID()
VoltageLevelTable.feed_VL("""UPDATE VoltageLevel SET name=%s, substation_rdf = %s, baseVoltage_rdf = %s
                WHERE rdf = %s """)
New_Message = 'Table VoltageLevel Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



GeneratingUnitTable.table_write_ID()
GeneratingUnitTable.feed_GU("""UPDATE GeneratingUnit SET name=%s,  maxP = %s, 
    minP = %s, equipmentContainer_rdf = %s WHERE rdf = %s """)

New_Message = 'Table GeneratingUnit Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



SynchronousMachineTable.table_write_ID()
SynchronousMachineTable.feed_SYM("""UPDATE SynchronousMachine SET name=%s,  
    ratedS = %s,genUnit_rdf = %s, regControl_rdf = %s, equipmentContainer_rdf = %s, baseVoltage_rdf = %s WHERE rdf = %s """)

SynchronousMachineTable.SSH_feed_SYM("""UPDATE SynchronousMachine SET P=%s,  
    Q = %s WHERE rdf = %s """)

New_Message = 'Table SynchronousMachine Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



RegulatingControlTable.table_write_ID()
RegulatingControlTable.feed_RC("""UPDATE RegulatingControl SET name=%s WHERE rdf = %s """)

RegulatingControlTable.SSH_feed_RC("""UPDATE RegulatingControl SET targetValue = %s WHERE rdf = %s """)

New_Message = 'Table RegulatingControl Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



PowerTransformerTable.table_write_ID()
PowerTransformerTable.feed_PT("""UPDATE PowerTransformer SET name=%s, equipmentContainer_rdf = %s 
    WHERE rdf = %s """)

New_Message = 'Table PowerTransformer Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



EnergyConsumerTable.table_write_ID()
EnergyConsumerTable.feed_EC("""UPDATE EnergyConsumer SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

EnergyConsumerTable.SSH_feed_EC("""UPDATE EnergyConsumer SET P = %s, Q = %s WHERE rdf = %s """)

New_Message = 'Table EnergyConsumer Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



PowerTransformerEndTable.table_write_ID()
PowerTransformerEndTable.feed_PTE("""UPDATE PowerTransformerEnd SET name=%s, Transformer_r = %s,
    Transformer_x = %s, Transformer_rdf = %s , baseVoltage_rdf = %s WHERE rdf = %s """)

New_Message = 'Table PowerTransformerEnd Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



BreakerTable.table_write_ID()
BreakerTable.feed_BR("""UPDATE Breaker SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

BreakerTable.SSH_feed_BR("""UPDATE Breaker SET state = %s WHERE rdf = %s """)

New_Message = 'Table Breaker Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



RatioTapChangerTable.table_write_ID()
RatioTapChangerTable.feed_RTC("""UPDATE RatioTapChanger SET name=%s  WHERE rdf = %s """)

RatioTapChangerTable.SSH_feed_RTC("""UPDATE RatioTapChanger SET step = %s WHERE rdf = %s """)

New_Message = 'Table RatioTapChanger Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



ACLineSegmentTable.table_write_ID()
ACLineSegmentTable.feed_ACL("""UPDATE ACLineSegment SET name=%s, ACLineSegment_r = %s,
    ACLineSegment_x = %s, ACLineSegment_bch = %s , ACLineSegment_gch = %s, 
        equipmentContainer_rdf = %s WHERE rdf = %s """)


New_Message = 'Table ACLineSegment Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)

New_Message = 'All Table Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)

var_TabCheck.set('All Tables Written Succeeded!')
Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()
time.sleep(0.15)

conn.close()