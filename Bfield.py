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
        if initialValue is None:
            if self.fieldType == INTBASE.INT_DEF:
                self.value = Bconstant(self.BASE,"0")
            elif self.fieldType == INTBASE.BOOL_DEF:
                self.value = Bconstant(self.BASE,"false")
            elif self.fieldType == INTBASE.STRING_DEF:
                self.value = Bconstant(self.BASE, "\"\"") #Empty string
            else:
                theClass = next((c for c in self.BASE.get_BclassList() if c.get_single_name() == self.fieldType), None)
                if theClass is not None:
                    self.value = Bnull(className=theClass.get_name())
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="There is no such class type!")
        elif initialValue == INTBASE.NULL_DEF: # Deal with object scenario
            theClass = next((c for c in self.BASE.get_BclassList() if c.get_single_name() == self.fieldType), None)
            if theClass is not None:
                self.value = Bnull(className=theClass.get_name())
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="There is no such class type!")
            # for c in self.BASE.get_BclassList():
            #     if self.fieldType == c.get_single_name():
            #         self.value = Bnull(className=c.get_name())
            #         break            
           # self.value = Bnull(className=self.fieldType)
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
