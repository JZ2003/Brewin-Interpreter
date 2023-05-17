from Bconstant import Bconstant
from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bnull import Bnull

class Bfield:
    def __init__(self,BASE,fieldName,initialValue,fieldType):
        self.BASE = BASE
        self.fieldName = fieldName
        self.value = None # Watch out. This could be an object
        if fieldType not in self.BASE.get_allTypeNames():
            self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid field type.")
        self.fieldType = fieldType # Literal string of the type
        self.__parse_initial_value(initialValue)
    
    def __parse_initial_value(self,initialValue):
        if initialValue == INTBASE.NULL_DEF: # Deal with object scenario
            self.value = Bnull(className=self.fieldType)
        else:  # Primitive scenario
            self.value = Bconstant(self.BASE,initialValue) 
            # check to do initial type checking:
            if self.value.get_type() != self.fieldType:
                self.BASE.error(ErrorType.TYPE_ERROR,description="Field initial value is of wrong type")
    
    def change_value(self,newValue):
        self.value = newValue

    def name(self):
        return self.fieldName

    def get_type(self):
        return self.fieldType

    def evaluate(self):
        if isinstance(self.value, Bconstant):
            return self.value.value # temporary
        else:
            return self.value # Need to deal with situations when fields are class objects
