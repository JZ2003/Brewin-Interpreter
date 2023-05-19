from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bconstant import Bconstant
# from Bexpression import Bexp
from Bstatement import Bstatement
from Bnull import Bnull

class Bmethod:
    def __init__(self,BASE,OBJ,initialList):
        self.BASE = BASE
        self.OBJ = OBJ # The object it belongs to; used to access field variables and "ME".
        self.methodName = None
        self.statement = None
        self.parameters = [] # A list of tuples recording type, name of parameters
        self.methodType = None # None if it's void
        self.__parse_name_and_statement(initialList)
    
    def isObject(self,thing):
        try:
            const = Bconstant(self.BASE, stringify(thing))
            return False
        except:
            return True
    
    def name(self):
        return self.methodName
    
    def get_parameters(self):
        return self.parameters

    def get_statement(self):
        return self.statement
    
    def __parse_name_and_statement(self,l):
        self.methodName = l[2]
        if l[1] == INTBASE.VOID_DEF:
            #print("haha")
            self.methodType = None # If it's void
        elif l[1] in self.BASE.get_allTypeNames():
            self.methodType = l[1] # If it's non-void
        else:
            self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid return type for the method {self.methodName}.")
        self.parameters = []
        for i in l[3]:
            if i[0] not in self.BASE.get_allTypeNames():
                self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid param type for the method {self.methodName}.")
            else:
                self.parameters.append((i[0],i[1]))  # i[0] is the type; i[1] is the name
        self.statement = l[4] 

    def execute_statement(self,var_list):
        # evaluate the statement with parameters and OBJ fields
        """
        var_list: (list)parameters+fields from the object call_method function
        """

        # if len(self.parameters) != len(Parameters):
        #     self.BASE.error(ErrorType.TYPE_ERROR,description="Wrong number of parameters")
        # Prmt_evaluated = [Bexp(self.BASE) for p in Parameters]

        stm = Bstatement(self.BASE,self.OBJ,self.statement)
        result = stm.process(var_list = var_list)

        if result is None or result == (None,None): #Return nothing
            # print(self.methodType)
            if self.methodType is None: #If it's void type
                return None
            else:
                if self.methodType == INTBASE.INT_DEF:
                    return 0
                elif self.methodType == INTBASE.BOOL_DEF:
                    return False
                elif self.methodType == INTBASE.STRING_DEF:
                    return ""
                else:
                    for c in self.BASE.get_BclassList():
                        if self.methodType == c.get_single_name():
                            return Bnull(className=c.get_name())
                    raise NotImplementedError
        if not self.isObject(result): # It's a primitive type
            const = Bconstant(self.BASE,stringify(result))
            #print(const.evaluate(), self.methodType,self.methodName)
            #print(const)
            if const.get_type() == self.methodType:
                return result
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="The value type is not compatible with the method return type.")
        else: #It's Bobject or Bnull
            if result.get_type() is None: # Generic null case
                if self.methodType in [INTBASE.INT_DEF,INTBASE.STRING_DEF,INTBASE.BOOL_DEF]:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Null can't be returned as a primitive type")
                for c in self.BASE.get_BclassList():
                    if self.methodType == c.get_single_name():
                        result.change_type(className=c.get_name())
                        break    
                return result
            else:
                if self.methodType in result.get_type():
                    return result
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="The value type is not compatible with the method return type.")   

    # def test(self):
    #     return self.statement, self.parameters

def stringify(val):
    if val is None:
        return "null"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, str):
        return '"' + val + '"'
    else: #int case
        return str(val)