from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bexpression import Bexp
# from Bconstant import Bconstant
# from Bobject import isObject
from Bconstant import Bconstant
from Bnull import Bnull

class Bstatement:
    #RETURNED = "finish"
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

    def process(self,var_list):
        """
        var_list: (dict) passed in when we call obj_x.run_method("method_name, var_list")
        """
        #BEGIN:
        if self.L[0] == INTBASE.BEGIN_DEF:
            for s in self.L[1:]:
                newStatement = Bstatement(self.BASE,self.OBJ,s)
                result = newStatement.process(var_list)
                if result is not None:
                    return result
        
        # PRINT:
        elif self.L[0] == INTBASE.PRINT_DEF:
            toPrint_str = "" # empty string
            for e in self.L[1:]:
                toPrint = Bexp(self.BASE,self.OBJ,var_list,e).evaluate()
                if toPrint is None:
                    toPrint_str = toPrint_str + "None"
                elif self.isObject(toPrint) and (not isinstance(toPrint, Bnull)):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't print an object")
                elif isinstance(toPrint, Bnull):
                    toPrint_str = toPrint_str + "None"
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
            condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
            if isinstance(condition,bool):
                while condition:
                    newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                    result = newStatement.process(var_list)
                    if result is not None:
                        return result
                    condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the while condition")
        #IF:
        elif self.L[0] == INTBASE.IF_DEF:
            # If there is no else statement
            if len(self.L) == 3:
                condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
                if isinstance(condition,bool):
                    if condition:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                        result = newStatement.process(var_list)
                        if result is not None:
                            return result
                    else:
                        return # The condition is false. Do nothing
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the if condition")
            # If there is a else statement
            elif len(self.L) == 4:
                condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
                if isinstance(condition,bool):
                    if condition:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                        result = newStatement.process(var_list)
                        if result is not None:
                            return result
                    else:
                        newStatement = Bstatement(self.BASE,self.OBJ,self.L[3])
                        result = newStatement.process(var_list)                
                        if result is not None:
                            return result
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the if condition")
            else:
                 self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong if-statement format")
        
        #SET:
        elif self.L[0] == INTBASE.SET_DEF:
            if len(self.L) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong set-statement format")
            exp = self.L[2]
            if isinstance(exp,list) and exp[0] == INTBASE.CALL_DEF:
                expVal = Bstatement(self.BASE,self.OBJ,exp).process(var_list)
            else:
                expVal = Bexp(self.BASE,self.OBJ,var_list,initialList=exp).evaluate() # The value to assign

            toChange = self.L[1]

            theVar = next((f for f in var_list if f.name() == toChange), None)
            if theVar is not None:
                if not self.isObject(expVal): # It's a primitive type
                    const = Bconstant(self.BASE,stringify(expVal))
                    if const.get_type() == theVar.get_type():
                        theVar.change_value(newValue=const)
                    else:
                        self.BASE.error(ErrorType.TYPE_ERROR,description="The value type is not compatible with the variable's type.")
                else: #It's Bobject or Bnull
                    if expVal.get_type() is None:
                        if theVar.get_type() in [INTBASE.INT_DEF,INTBASE.STRING_DEF,INTBASE.BOOL_DEF]:
                            self.BASE.error(ErrorType.TYPE_ERROR,description="Primitive types can't be set to null")
                        expVal.change_type(className=theVar.get_type())
                        theVar.change_value(newValue=expVal)
                    else:
                        if expVal.get_type() == theVar.get_type():
                            theVar.change_value(newValue=expVal)
                        else:
                            self.BASE.error(ErrorType.TYPE_ERROR,description="The value type compatible with the variable's type.")   
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
            theVar = next((f for f in var_list if f.name() == toChange), None)
            if theVar is not None:
                if inputVal.get_type() == theVar.get_type():
                    theVar.change_value(newValue=inputVal)
                else:
                    self.BASE.error(ErrorType.SYNTAX_ERROR,description="The input type is incompatible with the variable type")
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
        
        #CALL
        elif self.L[0] == INTBASE.CALL_DEF:
            if len(self.L) < 2:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong call-statement format")
            objName = self.L[1]


            if isinstance(objName,list): #If it's call or new
                if objName[0] == INTBASE.CALL_DEF:
                    callObj = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=objName).evaluate()
                elif objName[0] == INTBASE.NEW_DEF:
                    callObj = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=objName).evaluate()
            elif objName == "me":
                callObj = self.OBJ
            else:
                for v in var_list:
                    if v.name() == objName:
                        callObj = v.evaluate()
                        break
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to call.") # Not so sure

            if (not self.isObject(callObj)) or isinstance(callObj,Bnull): ## Since Now null type IS AN OBJECT
                self.BASE.error(ErrorType.FAULT_ERROR,description="Using non-object or null to make function call")

            param_list = []
            for e in self.L[3:]:
                exp = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=e).evaluate()
                param_list.append(exp)
            methodName = self.L[2]
            result = callObj.run_method(methodName,param_list)
            return result
        
        #RETURN
        elif self.L[0] == INTBASE.RETURN_DEF:
            if len(self.L) == 1:
                return (None,None) #NOT NONE
            elif len(self.L) == 2:
                exp = self.L[1]
                if isinstance(exp,list) and exp[0] == INTBASE.CALL_DEF:
                    expVal = Bstatement(self.BASE,self.OBJ,exp).process(var_list)
                else:
                    expVal = Bexp(self.BASE,self.OBJ,var_list,initialList=exp).evaluate() # The value to return 
                if self.isObject(expVal):
                    return expVal # return object
                else:
                    # const = Bconstant(self.BASE,stringify(expVal)) # Return Bconstant 
                    return expVal
                    # return const
            else:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong return-statement format")

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
