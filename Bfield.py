from Bconstant import Bconstant

class Bfield:
    def __init__(self,BASE,fieldName,initialValue):
        self.BASE = BASE
        self.fieldName = fieldName
        self.value = None # Watch out. This could be an object
        self.__parse_initial_value(initialValue)
    
    def __parse_initial_value(self,initialValue):
        self.value = Bconstant(self.BASE,initialValue)
    
    def name(self):
        return self.fieldName

    # def initial_value(self):
    #     return self.initialValue

    def evaluate(self):
        # Return a tuple: the first entry is its python type; 
        #                 the second entry is the actual value
        if isinstance(self.value, Bconstant):
            return self.value.value # temporary
        else:
            raise NotImplementedError # Need to deal with situations when fields are class objects
