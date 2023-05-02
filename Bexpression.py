from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bconstant import Bconstant
from Bfield import Bfield
class Bexp:
    def __init__(self,BASE,OBJ,Parameters,initialList):
        """
        BASE: the interpreter pointer
        OBJ: the OBJ pointer of the object in which the expression is called (fields)
        Parameters: dictionary of parameters with values (From statement)
        initialList: the list representation used to contruct this expression
        """
        self.BASE = BASE
        self.OBJ = OBJ
        self.Parameters = Parameters
        self.L = initialList # Might be a list or a single string
        pass

    def evaluate(self):
        if isinstance(self.L, str): # single string (constant/variable)
            s1 = self.L
            return self.eval1(s1)
        elif len(self.L) == 2:
            return self.eval2()
        elif len(self.L) == 3:
            return self.eval3()
        elif self.L[0] == INTBASE.CALL_DEF:
            return self.evalC()
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong expression syntax")
    
    def eval1(self,s1):
        # Check if it's a constant
        try:
            # If it is
            constant = Bconstant(self.BASE,s1)
            return constant.evaluate()
        except SyntaxError:
            # Else, check if it's variable or parameters
            # Check parameters first
            if s1 in self.Parameters:
                p = self.Parameters[s1]
                return p.evaluate() # Even parameters need to be 
            # Then check fields
            else:
                fields = self.OBJ.fields
                val = next((f for f in fields if f.name() == s1), (None,None))
                # Use (None,None) to represent "we can't find it" since None might be the value
                if val != (None,None):
                    return val.evaluate()
                else:
                    self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the variable")

    def eval2(self):
        pass

    def eval3(self):
        pass

    def evalC(self):
        pass