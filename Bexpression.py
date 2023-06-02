from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bconstant import Bconstant
from Bnull import Bnull
# from Bfield import Bfield
# from Bobject import Bobject
# from Bclass import Bclass
class Bexp:
    RETURNED = "finish"
    def __init__(self,BASE,OBJ,varList,initialList):
        """
        BASE: the interpreter pointer
        OBJ: the OBJ pointer of the object in which the expression is called (fields)
        Parameters: dictionary of parameters with values (From statement)
        initialList: the list representation used to contruct this expression
        """
        self.BASE = BASE
        self.OBJ = OBJ
        self.varList = varList
        self.L = initialList # Might be a list or a single string

    def isconst(self,thing):
        try:
            const = Bconstant(self.BASE,stringify(thing))
            return True
        except:
            return False

    def isObject(self,thing): # Test and see if it's Bnull or Bobject
        try:
            const = Bconstant(self.BASE, stringify(thing))
            return False
        except:
            return True

    def evaluate(self):
        """
        RETURN: Python primitive/Bobject instances/Bnull instances
        """
        if isinstance(self.L, str): # single string (constant/variable)
            s1 = self.L
            return self.eval1(s1)
        elif self.L[0] == INTBASE.CALL_DEF:
            return self.evalC()        
        elif len(self.L) == 2:
            s1,e1 = self.L
            return self.eval2(s1,e1)
        elif len(self.L) == 3:
            s1, e1, e2 = self.L
            return self.eval3(s1,e1,e2)
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
            if s1 == INTBASE.NULL_DEF:
                return Bnull() # If it's 'null' literal, then it evaluates to be a generic null.
            # Then, the next possibility is that s1 refers to a variable(fields/locals/params)
            for v in self.varList:
                if v.name() == s1:
                    return v.evaluate() # A python primitive/Bobject/Bnull
            self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the variable.")

    def eval2(self,s1,e1):
        if s1 == "!":
            e1Val = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=e1).evaluate()
            if isinstance(e1Val,tuple) and e1Val[1] is not None:
                return e1Val                  
            if isinstance(e1Val,bool):
                return not e1Val
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")
        elif s1 == INTBASE.NEW_DEF:
            if not INTBASE.TYPE_CONCAT_CHAR in e1:
                BclassDefs = self.BASE.get_BclassList()
                for c in BclassDefs:
                    if c.get_single_name() == e1:
                        return c.instantiate_object()
                self.BASE.error(ErrorType.TYPE_ERROR,description="Can't find the class definition.")
            else: # A template type
                BtempDefs = self.BASE.get_BtempList()
                plainTempType = e1.split(INTBASE.TYPE_CONCAT_CHAR)[0]
                for t in BtempDefs:
                    if t.get_single_name() == plainTempType:
                        return t.instantiate_object(initString=e1)
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong unary expression")

    def eval3(self,s1,e1,e2):
        #CASE1: integer arithmetic or string concatenation
        e1Val = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=e1).evaluate()
        if isinstance(e1Val,tuple) and e1Val[1] is not None:
            return e1Val          
        e2Val = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=e2).evaluate()
        if isinstance(e2Val,tuple) and e2Val[1] is not None:
            return e2Val          
        op = isPlus(s1)
        if op is not None:
            if type(e1Val) is str and type(e2Val) is str:
                return op(e1Val,e2Val)
            elif type(e1Val) is int and type(e2Val) is int:
                return op(e1Val,e2Val)
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The operations are not compatible with the operands.")

        op = isArithmetic(s1)
        if op is not None:
            if type(e1Val) is int and type(e2Val) is int:
                return op(e1Val,e2Val)
            else:
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
        
        #CASE3: == and !=, integer, string, boolean 
        eqneq = isEqNotEq(s1)
        if eqneq is not None:
            if type(e1Val) is int and type(e2Val) is int:
                return eqneq(e1Val,e2Val)
            elif isinstance(e1Val, bool) and isinstance(e2Val, bool):
                 return eqneq(e1Val,e2Val)
            elif isinstance(e1Val,str) and isinstance(e2Val,str):
                return eqneq(e1Val,e2Val)

        #CASE3.5: null and object comparison
        eqneq = objEqNotEq(s1)
        if eqneq is not None:
            if self.isconst(e1Val) or self.isconst(e2Val):
                self.BASE.error(ErrorType.TYPE_ERROR,description="Can't compare primitive types with null or objects")
            elif e1Val.get_type() is None or e2Val.get_type() is None: # At least one of them is a generic null
                if isinstance(e1Val,Bnull) and isinstance(e2Val,Bnull):
                    return eqneq(True)
                else:
                    return eqneq(False)
            elif not set(e1Val.get_type()).issubset(set(e2Val.get_type())) and not set(e2Val.get_type()).issubset(set(e1Val.get_type())):
                self.BASE.error(ErrorType.TYPE_ERROR,description="Can't compare two things of different types")
            elif isinstance(e1Val,Bnull) and isinstance(e2Val,Bnull):
                return eqneq(True)
            else:
                return eqneq(e1Val is e2Val) # Object reference comparison or one null one object of the same type

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
        if isinstance(objName,list): #If it's call or new
            callObj = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=objName).evaluate()
            if isinstance(callObj,tuple) and callObj[1] is not None:
                return callObj  

            # if objName[0] == INTBASE.CALL_DEF:
            #     callObj = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=objName).evaluate()
            # elif objName[0] == INTBASE.NEW_DEF:
            #     callObj = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=objName).evaluate()
        elif objName == INTBASE.ME_DEF:
            callObj = self.OBJ.get_the_most_derived()
        elif objName == INTBASE.SUPER_DEF:
            if self.OBJ.superObj is not None:
                callObj = self.OBJ.superObj
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find such a method from the super object.")
        else:
            callObj = next((v for v in self.varList if v.name() == objName), None)
            if callObj is None:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to call.") # Not so sure
            else:
                callObj = callObj.evaluate()

        if (not self.isObject(callObj)) or isinstance(callObj,Bnull): ## Since Now null type IS AN OBJECT
            self.BASE.error(ErrorType.FAULT_ERROR,description="Using non-object or null to make function call")
        
        param_list = []
        for e in self.L[3:]:
            exp = Bexp(self.BASE,self.OBJ,varList=self.varList,initialList=e).evaluate()
            if isinstance(exp,tuple) and exp[1] is not None:
                return exp              
            param_list.append(exp)
        methodName = self.L[2]
        result = callObj.run_method(methodName,param_list)
        # if result is None or result == Bexp.RETURNED:
        #     self.BASE.error(ErrorType.FAULT_ERROR,description="The call expression doensn't have a return value")
        # else:

        return result


        # if self.isObject(result):
        #     return result
        # elif result == (None,None):
        #     return None
        # else:
        #     return result

def isPlus(s):
    if s == "+":
        return lambda x,y: x + y
    else:
        return None

def isArithmetic(s):
    if s == "-":
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

def objEqNotEq(s):
    if s == "==":
        return lambda x: x
    elif s == "!=":
        return lambda x: not x
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