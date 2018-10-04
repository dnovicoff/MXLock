"""
File: Domain.py
Purpose:
Copywrite: Sendwell 2013
"""

class DomainMX(object):
    
    def setID(self,ID):
        self.uid = ID
        
    def getID(self):
        return self.uid
    
    def setMachine(self,machine):
        self.machine = machine
        
    def getMachine(self):
        return self.machine
    
    def setPriority(self,priority):
        self.priority = priority
        
    def getPriority(self):
        return self.priority
    
    def setAddress(self,address):
        self.address = address
        
    def getAddress(self):
        return self.address
    
    def setType(self,rType):
        self.type = rType
        
    def getType(self):
        return self.type

    def toString(self):
        return "ID\t%s\nMachine\t%s\nPriority\t%s\nAddress\t%s\n" % (self.getID(),self.getMachine(),self.getPriority(),self.getAddress())
    
    def __init__(self,uid,machine="",priority=0,address="0.0.0.0",rType=None):
        self.uid = uid
        self.machine = machine
        self.priority = priority
        self.address = address
        self.type = rType
        
        
        