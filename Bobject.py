from intbase import *
from Bfield import Bfield
from Bmethod import Bmethod

class Bobject:
    def __init__(self,BASE,className,fields,methods):
        self.BASE = BASE
        self.classNAME = className
        self.fields = []
        self.methods = []
        self.__add_field(fields)
        self.__add_method(methods)
    
    def __add_method(self,methods):
        for m in methods:
            # Check the format of the method definitions
            if len(m) != 4:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for method in an object")
            if not isinstance(m[1],str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Method doesn't have a string name")
            if not isinstance(m[2],list):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Don't have a parameter list")
            #TODO: check statement format

            newMethodObject = Bmethod(self.BASE,self,m)
            self.methods.append(newMethodObject)

    def __add_field(self,fields):
        for f in fields: 
            # Check the format of the field definitions
            if len(f) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field in an object")
            if not isinstance(f[1], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field name")
            if not isinstance(f[2], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field initial value")
            
            # f has the form: ["field", "<fieldName>", "<initialValue"]
            newFieldObject = Bfield(self.BASE,fieldName=f[1],initialValue=f[2])
            self.fields.append(newFieldObject)
    
    def run_method(self):
        pass

    def evaluate(self):
        return self