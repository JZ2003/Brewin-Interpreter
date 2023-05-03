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
            s1, e1, e2 = self.L
            return self.eval3(s1,e1,e2)
        elif self.L[0] == INTBASE.CALL_DEF:
            return self.evalC()
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong expression syntax")
    
    #The base case in evaluate() where there's only a string to eval
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
                    self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the variable.")

    def eval2(self):
        pass

    def eval3(self,s1,e1,e2):
        op = isArithmetic(s1)
        e1Val = Bexp(self.BASE,self.OBJ,self.Parameters,e1).evaluate()
        e2Val = Bexp(self.BASE,self.OBJ,self.Parameters,e2).evaluate()
        try:
            if op is not None:
                if type(e1Val) is not type(e2Val):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="The two operands are not compatible.")
                return op(e1Val,e2Val)
        except TypeError:
            self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")
        
        comp = isComparison(s1)
        #NOTE: Caveat: string lexicographic order?
        try:
            if comp is not None:
                if type(e1Val) is not type(e2Val):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="The two operands are not compatible.")
                return comp(e1Val, e2Val)
        except:
            raise self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")
        


    def evalC(self):
        pass


def isArithmetic(s):
    if s == "+":
        return lambda x, y: x + y 
    elif s == "-":
        return lambda x, y: x - y
    elif s == "*":
        return lambda x, y: x * y
    elif s == "/":
        return lambda x, y: x // y
    elif s == "%":
        return lambda x, y: x % y      
    else:
        return None      

def isComparison(s):
    if s == ">":
        return lambda x, y: True if x > y else False
    elif s == ">=":
        return lambda x, y: True if x >= y else False
    elif s == "<":
        return lambda x, y: True if x < y else False
    elif s == "<=":
        return lambda x, y: True if x <= y else False
    elif s == "==":
        return lambda x, y: True if x == y else False
    elif s == "!=":
        return lambda x, y: True if x != y else False
    else:
        return None

        