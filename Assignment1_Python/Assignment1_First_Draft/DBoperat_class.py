from xml.dom.minidom import parse
import xml.dom.minidom

from BaseClass import *

import MySQLdb

import sys
import os





#A inhereted from class Base_Feed_Table to fill in the table created
class Feed_Table_BV(Base_Feed_Table):

    def feed_BV(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        nominalValues = self.get_content_normal('nominalVoltage', 'EQ')
        #self.sql_update = sql_update
        for iter in range(len(rdfIDs)):
            data  = (nominalValues[iter], rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_SS(Base_Feed_Table):            

    def feed_SS(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        names = self.get_name()
        region_rdfs = self.get_rdf_normal('Region')
        #self.sql_update = sql_update
        
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , region_rdfs[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''



class Feed_Table_VL(Base_Feed_Table):

    def feed_VL(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        names = self.get_name()
        substation_rdfs = self.get_rdf_normal('Substation')
        baseVoltage_rdfs = self.get_rdf_normal('BaseVoltage')
        #self.sql_update = sql_update
        
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , substation_rdfs[iter], baseVoltage_rdfs[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_GU(Base_Feed_Table):

    def feed_GU(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        maxPs = list()
        minPs = list()
        equipmentContainer_rdfs = list()
        names = self.get_name()
        maxPs = self.get_content_normal('maxOperatingP', 'EQ')
        minPs = self.get_content_normal('minOperatingP', 'EQ')
        equipmentContainer_rdfs = self.get_equipcontain_rdf()
        #self.sql_update = sql_update
        
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , maxPs[iter], minPs[iter], equipmentContainer_rdfs[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_SYM(Base_Feed_Table):


    def get_ratedS_sym(self):
        ratedSs = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                ratedS_temp = item.getContent('cim:RotatingMachine.ratedS')
                ratedSs.append(ratedS_temp)
            except:
                print "no ratedS in this element"
        return ratedSs

    def get_genUnit_rdf_sym(self):
        genUnit_rdfs = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                genUnit_rdf_temp = item.get_resource('cim:RotatingMachine.GeneratingUnit')
                genUnit_rdfs.append(genUnit_rdf_temp)
            except:
                print "no genUnit_rdf in this element"
        return genUnit_rdfs


    def get_regControl_rdf_sym(self):
        get_regControls = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                get_regControl_temp = item.get_resource('cim:RegulatingCondEq.RegulatingControl')
                get_regControls.append(get_regControl_temp)
            except:
                print "no get_regControl in this element"
        return get_regControls


    def feed_SYM(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        ratedSs = list()
        genUnit_rdfs = list()
        regControl_rdfs = list()
        equipmentContainer_rdfs = list()

        names = self.get_name()
        ratedSs = self.get_ratedS_sym()
        genUnit_rdfs = self.get_genUnit_rdf_sym()
        regControl_rdfs = self.get_regControl_rdf_sym()
        
        equipmentContainer_rdfs = self.get_equipcontain_rdf()
        
        for iter in range(len(rdfIDs)):
            baseVoltage_rdf = self.fetch_baseVoltage_rdf(equipmentContainer_rdfs[iter])
            data  = (names[iter] , ratedSs[iter], genUnit_rdfs[iter], regControl_rdfs[iter], \
                equipmentContainer_rdfs[iter], baseVoltage_rdf,rdfIDs[iter])

            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''

    def get_P_sym(self):
        Ps = list()
        all_element_table = self.struct('SSH')
        for item in all_element_table:
            try:
                P_temp = item.getContent('cim:RotatingMachine.p')
                Ps.append(P_temp)
            except:
                print "no P in this element"
        return Ps

    def get_Q_sym(self):
        Qs = list()
        all_element_table = self.struct('SSH')
        for item in all_element_table:
            try:
                Q_temp = item.getContent('cim:RotatingMachine.q')
                Qs.append(Q_temp)
            except:
                print "no Q in this element"
        return Qs


    def SSH_feed_SYM(self,sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_SSH()
        Ps = list()
        Qs = list()
        Ps = self.get_P_sym()
        Qs = self.get_Q_sym()
        
        for iter in range(len(rdfIDs)):
            data  = (Ps[iter] , Qs[iter], rdfIDs[iter])

            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_RC(Base_Feed_Table):

    def feed_RC(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        names = list()
        names = self.get_name()
                
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''

    def SSH_feed_RC(self,sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_SSH()

        targetValues = list()
        targetValues = self.get_content_normal('targetValue', 'SSH')
        
        for iter in range(len(rdfIDs)):
            data  = (targetValues[iter], rdfIDs[iter])

            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_PT(Base_Feed_Table):

    def feed_PT(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()

        equipmentContainer_rdfs = list()
        names = self.get_name()
        equipmentContainer_rdfs = self.get_equipcontain_rdf()
      
        
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , equipmentContainer_rdfs[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


class Feed_Table_EC(Base_Feed_Table):

    def feed_EC(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        equipmentContainer_rdfs = list()
        names = self.get_name()

        equipmentContainer_rdfs = self.get_equipcontain_rdf()
        
        for iter in range(len(rdfIDs)):
            baseVoltage_rdf = self.fetch_baseVoltage_rdf(equipmentContainer_rdfs[iter])
            data  = (names[iter] , equipmentContainer_rdfs[iter] , baseVoltage_rdf, rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''

    def SSH_feed_EC(self,sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_SSH()

        Ps = list()
        Ps = self.get_content_normal('p', 'SSH')

        Qs = list()
        Qs = self.get_content_normal('q', 'SSH')       
        
        for iter in range(len(rdfIDs)):

            data  = (Ps[iter], Qs[iter], rdfIDs[iter])

            self.table_update_normal(sql_update, data)

        self.conn.commit()

        print ''




class Feed_Table_PTE(Base_Feed_Table):

    def get_baseVoltage_rdf_pte(self):
        get_baseVoltages = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                get_baseVoltage_temp = item.get_resource('cim:TransformerEnd.BaseVoltage')
                get_baseVoltages.append(get_baseVoltage_temp)
            except:
                print "no baseVoltage_rdf in this element"
        return get_baseVoltages       



    def feed_PTE(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()

        names = self.get_name()

        Transformer_rs = list()
        Transformer_rs = self.get_content_normal('r', 'EQ')
        
        Transformer_xs = list()
        Transformer_xs = self.get_content_normal('x', 'EQ')

        Transformer_rdfs = list()
        Transformer_rdfs = self.get_rdf_normal('PowerTransformer')

        baseVoltage_rdfs = list()
        baseVoltage_rdfs = self.get_baseVoltage_rdf_pte()


        for iter in range(len(rdfIDs)):

            data  = (names[iter] , Transformer_rs[iter] , Transformer_xs[iter],  Transformer_rdfs[iter] , \
                baseVoltage_rdfs[iter], rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''



class Feed_Table_BR(Base_Feed_Table):

    def feed_BR(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        equipmentContainer_rdfs = list()
        names = self.get_name()

        equipmentContainer_rdfs = self.get_equipcontain_rdf()
        
        for iter in range(len(rdfIDs)):
            baseVoltage_rdf = self.fetch_baseVoltage_rdf(equipmentContainer_rdfs[iter])
            data  = (names[iter] , equipmentContainer_rdfs[iter] , baseVoltage_rdf, rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''


    def get_state_br(self):
        states = list()
        all_element_table = self.struct('SSH')
        for item in all_element_table:
            try:
                state_temp = item.getContent('cim:Switch.open')
                states.append(state_temp)
            except:
                print "no state in this element"
        return states


    def SSH_feed_BR(self,sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_SSH()

        states = list()
        states = self.get_state_br()       
        
        for iter in range(len(rdfIDs)):

            data  = (states[iter], rdfIDs[iter])

            self.table_update_normal(sql_update, data)

        self.conn.commit()

        print ''


class Feed_Table_RTC(Base_Feed_Table):

    def feed_RTC(self, sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()

        names = self.get_name()
        
        for iter in range(len(rdfIDs)):
            data  = (names[iter] , rdfIDs[iter])
            self.table_update_normal(sql_update, data)
        self.conn.commit()

        print ''

    def get_step_rtc(self):
        steps = list()
        all_element_table = self.struct('SSH')
        for item in all_element_table:
            try:
                step_temp = item.getContent('cim:TapChanger.step')
                steps.append(step_temp)
            except:
                print "no step in this element"
        return steps


    def SSH_feed_RTC(self,sql_update):
        rdfIDs = list()
        rdfIDs = self.get_IDs_SSH()

        steps = list()
        steps = self.get_step_rtc()    
        
        for iter in range(len(rdfIDs)):

            data  = (steps[iter], rdfIDs[iter])

            self.table_update_normal(sql_update, data)

        self.conn.commit()

        print ''