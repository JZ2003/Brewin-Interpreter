from intbase import InterpreterBase as INTBASE
from intbase import ErrorType

class Bconstant:
    def __init__(self,BASE,parseString):
        self.BASE = BASE
        self.type = None
        self.value = None
        self.__infer_type_and_value(parseString)

    def __infer_type_and_value(self,p):
        # if p == INTBASE.NULL_DEF:
        #     self.type = INTBASE.NULL_DEF
        #     self.value = None
        if p == INTBASE.TRUE_DEF:
            self.type = INTBASE.BOOL_DEF
            self.value = True
        elif p == INTBASE.FALSE_DEF:
            self.type = INTBASE.BOOL_DEF
            self.value = False
        elif p.isdigit():
            self.type = INTBASE.INT_DEF
            self.value = int(p)
        elif p[0] == "-" and p[1:].isdigit():
            self.type = INTBASE.INT_DEF
            self.value = -int(p[1:])        
        elif p[0] == "\"" and p[len(p)-1] == "\"":
            self.type = INTBASE.STRING_DEF
            self.value = p[1:len(p)-1]
        else:
            raise SyntaxError
    
    def get_type(self):
        return self.type

    def evaluate(self):
        return self.value
    
    # def __str__(self):
    #     if self.type is bool and self.value == True:
    #         return INTBASE.TRUE_DEF
    #     elif self.type is bool and self.value == False:
    #         return INTBASE.FALSE_DEF
    #     elif self.type is int:
    #         return self.value
    #     elif isinstance(self.type,str):
    #         return self.value

