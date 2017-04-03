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
