from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bconstant import Bconstant
# from Bfield import Bfield
# from Bobject import Bobject
# from Bclass import Bclass
class Bexp:
    RETURNED = "finish"
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

    def isconst(self,thing):
        try:
            const = Bconstant(self.BASE,stringify(thing))
            return True
        except:
            return False

    def isObject(self,thing):
        try:
            const = Bconstant(self.BASE, stringify(thing))
            return False
        except:
            return True

    def evaluate(self):
        if isinstance(self.L, str): # single string (constant/variable)
            s1 = self.L
            return self.eval1(s1)
        elif len(self.L) == 2:
            s1,e1 = self.L
            return self.eval2(s1,e1)
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
                return p.evaluate() # Even parameters need to be evaluated
            # Then check fields
            else:
                fields = self.OBJ.fields
                val = next((f for f in fields if f.name() == s1), (None,None))
                # Use (None,None) to represent "we can't find it" since None might be the value
                if val != (None,None):
                    return val.evaluate()
                else:
                    self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the variable.")

    def eval2(self,s1,e1):
        if s1 == "!":
            e1Val = Bexp(self.BASE,self.OBJ,self.Parameters,e1).evaluate()
            if isinstance(e1Val,bool):
                return not e1Val
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")
        elif s1 == INTBASE.NEW_DEF:
            BclassDefs = self.BASE.BclassList
            for c in BclassDefs:
                # print(type(c))
                if c.get_name() == e1: #NOTE: extremely wirld bug here: changing get_name() to name() won't work
                    return c.instantiate_object()
            self.BASE.error(ErrorType.TYPE_ERROR,description="Can't find the class definition.")
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong unary expression")

    def eval3(self,s1,e1,e2):
        #CASE1: integer arithmetic or string concatenation
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
        
        #CASE2: integer or string comparison, not including == or !=
        comp = isComparison(s1)
        #NOTE: Caveat: string lexicographic order?
        try:
            if comp is not None:
                if type(e1Val) is not type(e2Val):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="The two operands are not compatible.")
                return comp(e1Val, e2Val)
        except:
            self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")
        
        #CASE3: == and !=, integer, string, boolean, or null comparison 
        eqneq = isEqNotEq(s1)
        if eqneq is not None:
            if isinstance(e1Val,int) and isinstance(e2Val,int):
                return eqneq(e1Val,e2Val)
            elif isinstance(e1Val, bool) and isinstance(e2Val, bool):
                 return eqneq(e1Val,e2Val)
            elif isinstance(e1Val,str) and isinstance(e2Val,str):
                return eqneq(e1Val,e2Val)

            #DEAL WITH NULL! (VERY FLAKEY!)
            elif e1Val is None:
                if self.isconst(e2Val):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't compare null with primitive types")
                return eqneq(e1Val,e2Val) # True
            elif e2Val is None:
                if self.isconst(e1Val):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't compare null with primitive types")
                return eqneq(e1Val,e2Val) # True
                
            # elif e1Val == None:
            #     if not isinstance(e2Val,Bobject):
            #         self.BASE.error(ErrorType.TYPE_ERROR,description="The two operands are not compatible.")
            #     else:
            #         return eqneq(e1Val,e2Val)
            # elif e2Val == None:
            #     if not isinstance(e1Val,Bobject):
            #         self.BASE.error(ErrorType.TYPE_ERROR,description="The two operands are not compatible.")
            #     else:
            #         return eqneq(e1Val,e2Val)            
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")

        #CASE4: boolean & and |
        andor = isAndOr(s1)
        if andor is not None:
            if type(e1Val) is bool and type(e2Val) is bool:
                return andor(e1Val, e2Val)
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")

    def evalC(self):
        if len(self.L) < 2:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong call-expression format")
        objName = self.L[1]
        fields = self.OBJ.fields
        theField = next((f for f in fields if f.name() == objName), (None,None))
        if objName in self.Parameters:
            callObj = self.Parameters[objName]
        elif theField != (None,None):
            callObj = theField.evaluate()
        elif objName == "me":
            callObj = self.OBJ
        else:
            self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to call.") # Not so sure
        # Check if it's an object and if it's not null
        if not self.isObject(callObj):
            self.BASE.error(ErrorType.FAULT_ERROR,description="Using non-object or null to make function call")
        param_list = []
        for e in self.L[3:]:
            exp = Bexp(self.BASE,self.OBJ,Parameters=self.Parameters,initialList=e).evaluate()
            param_list.append(exp)
        methodName = self.L[2]
        result = callObj.run_method(methodName,param_list)
        # if result is None or result == Bexp.RETURNED:
        #     self.BASE.error(ErrorType.FAULT_ERROR,description="The call expression doensn't have a return value")
        # else:
        if self.isObject(result):
            return result
        elif result == Bexp.RETURNED:
            return None
        else:
            return result

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
    else:
        return None

def isEqNotEq(s):
    if s == "==":
        return lambda x, y: True if x == y else False
    elif s == "!=":
        return lambda x, y: True if x != y else False
    else:
        return None

def isAndOr(s):
    if s == "&":
        return lambda x, y: x & y
    if s == "|":
        return lambda x, y: x | y
    else:
        return None

def stringify(val):
    if val is None:
        return "null"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, str):
        return '"' + val + '"'
    else: #int case
        return str(val)