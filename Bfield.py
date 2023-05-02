from Bconstant import Bconstant

class Bfield:
    def __init__(self,BASE,fieldName,initialValue):
        self.BASE = BASE
        self.fieldName = fieldName
        self.initialValue = None
        self.__parse_initial_value(initialValue)
    
    def __parse_initial_value(self,initialValue):
        self.initialValue = Bconstant(self.BASE,initialValue)
    
    def name(self):
        return self.fieldName

    def initial_value(self):
        return self.initialValue

    def evaluate(self):
        return self.initialValue.type, self.initialValue.value