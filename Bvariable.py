from Bconstant import Bconstant
from intbase import InterpreterBase as INTBASE
from intbase import ErrorType

class BVariable:
    def __init__(self,BASE,varName,initialValue,varType):
        """
        The major difference with Bfield is that here initialValue should be 
        a real value, not a string.
        It could be Bconstant, Bobject, or null (with type or not with type)?...
        """
        self.BASE = BASE
        self.varName = varName
        self.value = initialValue
        self.varType = varType # Literal string of the type
    
    def change_value(self,newValue):
        self.value = newValue

    def name(self):
        return self.varName

    def get_type(self):
        return self.varType

    def evaluate(self):
        if isinstance(self.value, Bconstant):
            return self.value.value # primitives
        else:
            return self.value # class objects
