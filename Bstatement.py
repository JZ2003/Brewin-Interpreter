from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bexpression import Bexp
# from Bconstant import Bconstant
# from Bobject import isObject
from Bconstant import Bconstant


class Bstatement:
    def __init__(self,BASE,OBJ,initialList):
        self.BASE = BASE
        self.OBJ = OBJ
        self.L = initialList

    def isObject(self,thing):
        try:
            const = Bconstant(self.BASE, stringify(thing))
            return False
        except:
            return True

    def process(self,Parameters):
        """
        Parameters: (dict) passed in when we call obj_x.run_method("method_name, Parameters")
        """
        #BEGIN:
        if self.L[0] == INTBASE.BEGIN_DEF:
            for s in self.L[1:]:
                newStatement = Bstatement(self.BASE,self.OBJ,s)
                newStatement.process(Parameters)
        
        # PRINT:
        elif self.L[0] == INTBASE.PRINT_DEF:
            toPrint_str = "" # empty string
            for e in self.L[1:]:
                toPrint = Bexp(self.BASE,self.OBJ,Parameters,e).evaluate()
                if self.isObject(toPrint):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't print an object")
                elif toPrint is None:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't print a null")
                elif toPrint is True:
                    toPrint_str = toPrint_str + "true"
                elif toPrint is False:
                    toPrint_str = toPrint_str + "false"
                elif isinstance(toPrint,int):
                    toPrint_str = toPrint_str + str(toPrint)
                elif isinstance(toPrint,str):
                    toPrint_str = toPrint_str + toPrint
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Something goes wrong when printing")
            self.BASE.output(toPrint_str)
        # WHILE:
        elif self.L[0] == INTBASE.WHILE_DEF:
            condition = Bexp(self.BASE,self.OBJ,Parameters,self.L[1]).evaluate()
            if isinstance(condition,bool):
                while condition:
                    newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                    newStatement.process(Parameters)
                    condition = Bexp(self.BASE,self.OBJ,Parameters,self.L[1]).evaluate()
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the while condition")
        #IF:
        elif self.L[0] == INTBASE.IF_DEF:
            # If there is no else statement
            if len(self.L) == 3:
                condition = Bexp(self.BASE,self.OBJ,Parameters,self.L[1]).evaluate()
                if isinstance(condition,bool):
                    if condition:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                        newStatement.process(Parameters)
                    else:
                        return # The condition if false. Do nothing
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the if condition")
            # If there is a else statement
            elif len(self.L) == 4:
                condition = Bexp(self.BASE,self.OBJ,Parameters,self.L[1]).evaluate()
                if isinstance(condition,bool):
                    if condition:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                        newStatement.process(Parameters)
                    else:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[3])
                        newStatement.process(Parameters)                
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the if condition")
            else:
                 self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong if-statement format")
        
        #SET:
        elif self.L[0] == INTBASE.SET_DEF:
            if len(self.L) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong set-statement format")
            exp = self.L[2]
            expVal = Bexp(self.BASE,self.OBJ,Parameters,initialList=exp).evaluate() # The value to assign
            toChange = self.L[1]
            fields = self.OBJ.fields
            theField = next((f for f in fields if f.name() == toChange), (None,None))
            # If it is a parameter
            if toChange in Parameters:
                if self.isObject(expVal): # object type
                    Parameters[toChange] = expVal
                else: # primitive type
                    const = Bconstant(self.BASE,stringify(expVal))
                    Parameters[toChange] = const
            # If it is a field
            elif theField != (None,None):
                if self.isObject(expVal): # object type
                    theField.change_value(expVal)
                else: # primitive type
                    const = Bconstant(self.BASE,stringify(expVal))
                    theField.change_value(const)
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
        
        #INPUTI & INPUTS
        elif self.L[0] == INTBASE.INPUT_INT_DEF or self.L[0] == INTBASE.INPUT_STRING_DEF:
            if len(self.L) != 2:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong input-statement format")
            input = self.BASE.get_input() # get input with python string format
            if input.isdigit(): #inputi case
                inputVal = Bconstant(self.BASE,input)
            else: #inputs case
                inputVal = Bconstant(self.BASE, '"' + input + '"') #NOTE: to denote a Bstring, 
                                                                        #we need another pair of quotes
            toChange = self.L[1] 
            fields = self.OBJ.fields
            theField = next((f for f in fields if f.name() == toChange), (None,None))
            # If it is a parameter
            if toChange in Parameters:
                    Parameters[toChange] = inputVal
            # If it is a field
            elif theField != (None,None):
                    theField.change_value(inputVal)
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
        
        #CALL
        elif self.L[0] == INTBASE.CALL_DEF:
            if len(self.L) < 2:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong call-statement format")
            objName = self.L[1]
            fields = self.OBJ.fields
            theField = next((f for f in fields if f.name() == objName), (None,None))
            if objName in Parameters:
                callObj = Parameters[objName]
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
                exp = Bexp(self.BASE,self.OBJ,Parameters=Parameters,initialList=e).evaluate()
                param_list.append(exp)
            methodName = self.L[2]
            callObj.run_method(methodName,param_list)


        else:
            raise NotImplementedError

        

def stringify(val):
    if val is None:
        return "null"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, str):
        return '"' + val + '"'
    else: #int case
        return str(val)
