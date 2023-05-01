from intbase import *
from Bfield import Bfield

class Bobject:
    def __init__(self,BASE,className,fields,method):
        self.BASE = BASE
        self.classNAME = className
        self.fields = []
        self.methods = []
        self.add_field(fields)
    
    def add_method(self):
        pass

    def add_field(self,fields):
        for f in fields:
            newFieldObject = Bfield(self.BASE,fieldName=f[1],initialValue=f[2])
            self.fields.append(newFieldObject)
        

    def run_method(self):
        pass
