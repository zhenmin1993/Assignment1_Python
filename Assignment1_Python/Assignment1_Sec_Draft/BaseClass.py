from xml.dom.minidom import parse
import xml.dom.minidom



import xml.etree.ElementTree as ET
import MySQLdb

import sys
import os


#*******This class is to define the basic functions for recors processing
class info_parse():
    def __init__(self,element):
        self.element = element

#Function to take away the "#" symbol so that easier to find the primary key
    def purify(self,str_in):
        rdf_str = str_in.split('#')[1]
        return rdf_str


        
#Function to take the rdfID of one element in EQ file
    def getID(self):
        rdfID = self.element.getAttribute("rdf:ID")
        return rdfID

#Function to take the rdfID of one element in SSH file
    def get_about(self):
        rdf_about = self.element.getAttribute("rdf:about")
        rdf_about = self.purify(rdf_about)
        return rdf_about

#Function to extract the data stored in one record, transmit to float if it is a number
    def getContent(self,  TagName):
        content = self.element.getElementsByTagName(TagName)[0].childNodes[0].data
        try:
            content = float(content)
            return content
        except:
            return content

#Function to extract the foreign key
    def get_resource(self, TagName):
        find_element = self.element.getElementsByTagName(TagName)[0]
        rdf_resource = find_element.getAttribute("rdf:resource")
        rdf_resource = self.purify(rdf_resource) 
        return rdf_resource

#Function to extract the name of the object
    def getName(self):
        name = self.getContent('cim:IdentifiedObject.name')
        return name



#A basic class to get rdfID both from EQ file and SSH file
class Base_Get_Records(info_parse):
    def __init__(self,all_element):
        self.all_element = all_element

#find all the elements (ChildNodes) in the file you choose(type of file can be EQ or SSH)
    def struct(self, type):
    
        all_element_table = list()
        for element in self.all_element[type]:

            self.table_name = element.localName.encode()
            #extract the name of the node and use as table name
            element_table = info_parse(element) 
            #make every element a info_parse instance so it will have the above functions
            all_element_table.append(element_table)
            #put all the element instance in all_element_table
        return all_element_table

    def get_IDs_EQ(self):
        rdfIDs_EQ = list()
        all_element_table = list()
        all_element_table = self.struct('EQ')
        #use the above struct function to construct a type EQ element table
        for item in all_element_table:
            try:
                rdfID_temp = item.getID()
                rdfIDs_EQ.append(rdfID_temp)
                #get rdfIDs and store them into list
                
            except:
                print "can't find rdfID"
        return rdfIDs_EQ


    def get_IDs_SSH(self):
        rdfIDs_SSH = list()
        all_element_table = list()
        all_element_table = self.struct('SSH')
        #use the above struct function to construct a type SSH element table
        for item in all_element_table:
            try:
                rdfID_temp = item.get_about()
                rdfIDs_SSH.append(rdfID_temp)
                #get rdfIDs and store them into list
                
            except:
                print "can't find rdfID"
        return rdfIDs_SSH


class Create_Table(Base_Get_Records):
    def __init__(self, cur,conn):
        self.cur = cur
        self.conn = conn

    def New_Table_No_FK(self, tab_title,name_type):
        try:
            self.cur.execute('SET FOREIGN_KEY_CHECKS = 0')
            self.cur.execute('DROP TABLE IF EXISTS' + ' '+tab_title)
            sql_newTab = str()
            sql_newTab = 'CREATE TABLE '+ tab_title + ' (rdf varchar(50) NOT NULL PRIMARY KEY '
            for key,value in name_type.items():
                sql_newTab = sql_newTab + ','+ key + ' '+ value
            sql_newTab = sql_newTab + ')'
            self.cur.execute(sql_newTab)
            print 'Table' + tab_title + 'Created!\n'

        except:
            print 'Table' + tab_title + 'Creation Failed!\n'

    def New_Table_Has_FK(self, tab_title,name_type, FK_from_to):
        try:
            self.cur.execute('SET FOREIGN_KEY_CHECKS = 0')
            self.cur.execute('DROP TABLE IF EXISTS' + ' '+tab_title)
            sql_newTab = str()
            sql_newTab = 'CREATE TABLE '+ tab_title + ' (rdf varchar(50) NOT NULL PRIMARY KEY '
            for key,value in name_type.items():
                sql_newTab = sql_newTab + ','+ key + ' '+ value

            for key,value in FK_from_to.items():
                sql_newTab = sql_newTab + ',' + 'FOREIGN KEY (' + key + ') REFERENCES ' \
                    + value + '(rdf) ON DELETE SET NULL'
            sql_newTab = sql_newTab + ')'
            self.cur.execute(sql_newTab)
            print 'Table ' + tab_title + ' Created!\n'
        except:
            print 'Table ' + tab_title + ' Creation Failed!\n'

    def Exist_Table_No_FK(self, tab_title,name_type):
        try:
            self.cur.execute('CREATE TABLE IF NOT EXISTS  '+tab_title)
            sql_newTab = str()
            sql_newTab = 'CREATE TABLE '+ tab_title + ' (rdf varchar(50) NOT NULL PRIMARY KEY '
            for key,value in name_type.items():
                sql_newTab = sql_newTab + ','+ key + ' '+ value
            sql_newTab = sql_newTab + ')'
            self.cur.execute(sql_newTab)
            print ' Table ' + tab_title + ' Checked!\n'
        except:
            print 'Table ' + tab_title + ' Check Failed!\n'

    def Exist_Table_Has_FK(self, tab_title,name_type, FK_from_to):
        try:
            self.cur.execute('CREATE TABLE IF NOT EXISTS  '+tab_title)
            sql_newTab = str()
            sql_newTab = 'CREATE TABLE '+ tab_title + ' (rdf varchar(50) NOT NULL PRIMARY KEY '
            for key,value in name_type.items():
                sql_newTab = sql_newTab + ','+ key + ' '+ value

            for key,value in FK_from_to.items():
                sql_newTab = sql_newTab + ',' + 'FOREIGN KEY (' + key + ') REFERENCES ' \
                    + value + '(rdf) ON DELETE SET NULL'
            sql_newTab = sql_newTab + ')'
            self.cur.execute(sql_newTab)
            print ' Table ' + tab_title + ' Checked!\n'
        except:
            print ' Table ' + tab_title + ' Check Failed!\n'








#A basic class to fill in the table created
#class Base_Feed_Table(Base_Get_Records):
class Base_Feed_Table(Create_Table):
    def __init__(self,all_element, cur, conn):
        self.all_element = all_element
        self.cur = cur
        self.conn = conn

#Write the primary keys(rdfID) in the table
    def table_write_ID(self):
        rdfIDs = list()
        rdfIDs = self.get_IDs_EQ()
        for iter in range(len(rdfIDs)):
            rdfID = rdfIDs[iter]

            if rdfID is None: print 'the record is empty!'
            data = (rdfID,)
            try: 
                self.sql_insert = "INSERT IGNORE INTO "+ self.table_name+"(rdf) VALUES (%s)" 
                self.cur.execute(self.sql_insert, data) 
                print 'Table',self.table_name,'ID Write Into Database Succeed!'

            except:
                self.conn.rollback()
                print 'Table',self.table_name,'ID Attribute Write Into Database Failed!'
        self.conn.commit()


#insert the other tag data into the table where rdfID equals
    def table_update_normal(self, sql_update,data):
        self.sql_update = sql_update        
        try:  
            self.cur.execute(self.sql_update, data)
            print 'Table',self.table_name,'Record Attribute Write Into Database Succeed!'

        except:
            self.conn.rollback()
            print 'Table',self.table_name,'One Record Attribute Write Into Database Failed!'

#get the name of the element
    def get_name(self):
        names = list()
        #region_rdfs = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                name_temp = item.getName()
                names.append(name_temp)
            except:
                print "no name in this element"
        return names

#Get the foreign keys of one element (here use normal because there are some special cases)
    def get_rdf_normal(self, rdf_name):
        rdf_lst = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                rdf_temp = item.get_resource('cim:'+self.table_name+'.'+rdf_name)
                rdf_lst.append(rdf_temp)
            except:
                print "no', rdf_name ,'rdf in this element"
        return rdf_lst

#get equipment container rdf
    def get_equipcontain_rdf(self):
        rdf_lst = list()
        all_element_table = self.struct('EQ')
        for item in all_element_table:
            try:
                rdf_temp = item.get_resource('cim:Equipment.EquipmentContainer')
                rdf_lst.append(rdf_temp)
            except:
                print "no EquipmentContainer_rdf in this element"
        return rdf_lst
        
#Get the content of the element
    def get_content_normal(self, content_name, type):
        content_lst = list()
        all_element_table = self.struct(type)
        for item in all_element_table:
            try:
                content_temp = item.getContent('cim:'+self.table_name+'.'+content_name)
                content_lst.append(content_temp)
            except:
                print "no', content_name ,'in this element"
        return content_lst

#getting baseVoltage rdf by making association with euipmentContainer_rdf
    def fetch_baseVoltage_rdf(self, equipmentContainer_rdf):
        sql_voltage = """SELECT baseVoltage_rdf FROM VoltageLevel WHERE rdf = %s """
        self.cur.execute(sql_voltage, (equipmentContainer_rdf,))
        baseVoltage_rdf = self.cur.fetchone()[0]
        return baseVoltage_rdf


