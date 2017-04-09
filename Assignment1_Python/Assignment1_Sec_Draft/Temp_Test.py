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

