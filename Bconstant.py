from intbase import InterpreterBase as INTBASE
from intbase import ErrorType

class Bconstant:
    def __init__(self,BASE,parseString):
        self.BASE = BASE
        self.type = None
        self.value = None
        self.infer_type_and_value(parseString)

    def infer_type_and_value(self,p):
        if p == INTBASE.NULL_DEF:
            self.type = type(None)
            self.value = None
        elif p == INTBASE.TRUE_DEF:
            self.type = type(True)
            self.value = True
        elif p == INTBASE.FALSE_DEF:
            self.type = type(False)
            self.value = False
        elif p.isdigit():
            self.type = type(int(p))
            self.value = int(p)
        elif p[0] == "-" and p[1:].isdigit():
            self.type = type(int(p[1:]))
            self.value = -int(p[1:])        
        elif p[0] == "\"" and p[len(p)-1] == "\"":
            self.type = type("I'm a string")
            self.value = p[1:len(p)-1]
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Unrecognizable constant")