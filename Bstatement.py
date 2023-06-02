from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bexpression import Bexp
# from Bconstant import Bconstant
# from Bobject import isObject
from Bconstant import Bconstant
from Bnull import Bnull
from Bvariable import BVariable

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
        #LET:
        if self.L[0] == INTBASE.LET_DEF:
            locVarList = []
            for v in self.L[1]:
                if len(v) == 3:
                    type,name,initVal = v
                elif len(v) == 2:
                    type,name = v
                    initVal = None
                else:
                    self.BASE.error(ErrorType.SYNTAX_ERROR_ERROR,description="Wrong Syntax for local variables")
                
                #NOTE: Need to change to include template case
                if INTBASE.TYPE_CONCAT_CHAR not in type:
                    if type not in self.BASE.get_allTypeNames():
                        self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid local variable type.")
                else:
                    if type.split(INTBASE.TYPE_CONCAT_CHAR)[0] not in self.BASE.get_allTypeNames():
                        self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid local variable type.")
                
                if initVal is None or initVal == INTBASE.NULL_DEF:
                    if type == INTBASE.INT_DEF:
                        valObj = Bconstant(self.BASE, "0")
                    elif type == INTBASE.STRING_DEF:
                        valObj = Bconstant(self.BASE, "\"\"")
                    elif type == INTBASE.BOOL_DEF:
                        valObj = Bconstant(self.BASE, "false")
                    else:
                        if INTBASE.TYPE_CONCAT_CHAR not in type:
                            theClass = next((c for c in self.BASE.get_BclassList() if c.get_single_name() == type), None)
                            if theClass is not None:
                                valObj = Bnull(className=theClass.get_name())
                            else:
                                self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid local variable type.")
                        else:
                            plainTempType = type.split(INTBASE.TYPE_CONCAT_CHAR)[0]
                            theTemplate = next((t for t in self.BASE.get_BtempList() if t.get_single_name() == plainTempType), None)
                            if theTemplate is not None:
                                valObj = Bnull(className=type)
                            else:
                                self.BASE.error(ErrorType.TYPE_ERROR,description=f"Invalid local variable type.")
                else:  # Primitive scenario
                    valObj = Bconstant(self.BASE,initVal) 
                    # check to do initial type checking:
                    if valObj.get_type() != type:
                        self.BASE.error(ErrorType.TYPE_ERROR,description="Local variable initial value is of wrong type")
                newLocVar = BVariable(self.BASE, varName=name, initialValue=valObj,varType=type)
                locVarList.append(newLocVar)
            # CHECK duplicate local variables
            locVarNameSet = set([i.name() for i in locVarList])
            if len(locVarNameSet) != len(locVarList):
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't have local variables of the same name.")
            for s in self.L[2:]:
                newStatement = Bstatement(self.BASE, self.OBJ, s)
                result = newStatement.process(var_list=locVarList+var_list)
                if result is not None:
                    return result

        #BEGIN:
        elif self.L[0] == INTBASE.BEGIN_DEF:
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
                if isinstance(toPrint,tuple) and toPrint[1] is not None:
                    return toPrint
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
            if isinstance(condition,tuple) and condition[1] is not None:
                return condition           
            if isinstance(condition,bool):
                while condition:
                    newStatement = Bstatement(self.BASE,self.OBJ,self.L[2])
                    result = newStatement.process(var_list)
                    if result is not None:
                        return result
                    condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
                    if isinstance(condition,tuple) and condition[1] is not None:
                        return condition                 
            else:
                self.BASE.error(ErrorType.TYPE_ERROR,description="Use a non-boolean type as the while condition")
        #IF:
        elif self.L[0] == INTBASE.IF_DEF:
            # If there is no else statement
            if len(self.L) == 3:
                condition = Bexp(self.BASE,self.OBJ,var_list,self.L[1]).evaluate()
                if isinstance(condition,tuple) and condition[1] is not None:
                    return condition               
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
                if isinstance(condition,tuple) and condition[1] is not None:
                    return condition                      
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
            expVal = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=exp).evaluate()
            if isinstance(expVal,tuple) and expVal[1] is not None:
                return expVal      
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
                        if '@' not in theVar.get_type():
                            for c in self.BASE.get_BclassList():
                                if theVar.get_type() == c.get_single_name():
                                    expVal.change_type(className=c.get_name())
                                    break
                        else:
                            for t in self.BASE.getBtempList():
                                if theVar.get_type().split('@')[0] == t.get_single_name():
                                    expVal.change_type(className=theVar.get_type())
                        theVar.change_value(newValue=expVal)
                    else:
                        if isinstance(expVal.get_type(),list):
                            if theVar.get_type() in expVal.get_type():
                                theVar.change_value(newValue=expVal)
                            else:
                                self.BASE.error(ErrorType.TYPE_ERROR,description="The value type incompatible with the variable's type.")   
                        else:
                             if theVar.get_type() == expVal.get_type():
                                theVar.change_value(newValue=expVal)
                             else:
                                self.BASE.error(ErrorType.TYPE_ERROR,description="The value type incompatible with the variable's type.")
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
            
        
        #INPUTI & INPUTS
        elif self.L[0] == INTBASE.INPUT_INT_DEF or self.L[0] == INTBASE.INPUT_STRING_DEF:
            if len(self.L) != 2:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong input-statement format")
            input = self.BASE.get_input() # get input with python string format
            if input.isdigit() or (input[0] == "-" and input[1:].isdigit()): #inputi case
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
                    self.BASE.error(ErrorType.TYPE_ERROR,description="The input type is incompatible with the variable type.")
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
        
        #CALL
        elif self.L[0] == INTBASE.CALL_DEF:
            if len(self.L) < 2:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong call-statement format")
            objName = self.L[1]

            # print(f"The objName is {objName}")
            if isinstance(objName,list): #If it's call or new
                callObj = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=objName).evaluate()
                if isinstance(callObj,tuple) and callObj[1] is not None:
                    return callObj      

            elif objName == INTBASE.ME_DEF:
                callObj = self.OBJ.get_the_most_derived()
            
            elif objName == INTBASE.SUPER_DEF:
                if self.OBJ.superObj is not None:
                    callObj = self.OBJ.superObj
                else:
                    self.BASE.error(ErrorType.NAME_ERROR,description="Can't find such a method from the super object.")
            
            else:
                callObj = next((v for v in var_list if v.name() == objName), None)
                if callObj is None:
                    self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to call.") # Not so sure
                else:
                    callObj = callObj.evaluate()
            if (not self.isObject(callObj)) or isinstance(callObj,Bnull): ## Since Now null type IS AN OBJECT
                self.BASE.error(ErrorType.FAULT_ERROR,description="Using non-object or null to make function call")

            param_list = []
            for e in self.L[3:]:
                exp = Bexp(self.BASE,self.OBJ,varList=var_list,initialList=e).evaluate()
                if isinstance(exp,tuple) and exp[1] is not None:
                    return exp      
                param_list.append(exp)
            methodName = self.L[2]
            # print(f"Now it's object {callObj.classNAME}, with a parameter of len {len(param_list)}")
            result = callObj.run_method(methodName,param_list)
            return result
        
        #RETURN
        elif self.L[0] == INTBASE.RETURN_DEF:
            if len(self.L) == 1:
                return (None,None) #NOT NONE, but should immediately return.
            elif len(self.L) == 2:
                exp = self.L[1]

                if exp == INTBASE.ME_DEF:
                    return self.OBJ
                else:
                    expVal = Bexp(self.BASE,self.OBJ,var_list,initialList=exp).evaluate()
                    if isinstance(expVal,tuple) and expVal[1] is not None:
                        return expVal                          
                    return expVal
            else:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong return-statement format")

        #Try
        elif self.L[0] == INTBASE.TRY_DEF:
            if len(self.L) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong try-statement format")
            mainStm = Bstatement(BASE=self.BASE,OBJ=self.OBJ,initialList=self.L[1])
            mainResult = mainStm.process(var_list=var_list)
    
            if mainResult is not None:
                if isinstance(mainResult,tuple) and mainResult[1] is not None: # We catch a throw
                    catchStm = Bstatement(BASE=self.BASE,OBJ=self.OBJ,initialList=self.L[2])
                    # Add the exception variable
                    excString = Bconstant(BASE=self.BASE,parseString=stringify(mainResult[1]))
                    exception = BVariable(BASE=self.BASE,varName=INTBASE.EXCEPTION_VARIABLE_DEF,initialValue=excString,varType=excString.get_type())
                    if exception.get_type() != INTBASE.STRING_DEF:
                        self.BASE.error(ErrorType.TYPE_ERROR,description="Something shit busted!")
                    catchResult = catchStm.process(var_list=[exception]+var_list)
                    if catchResult is not None:
                        return catchResult
                else: # Just a normal return 
                    return mainResult
            

        #Throw
        elif self.L[0] == INTBASE.THROW_DEF:
            if len(self.L) != 2: 
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong throw-statement format")
            exp = self.L[1]
            excVal = Bexp(self.BASE,self.OBJ,var_list,initialList=exp).evaluate() #TODO: CHECK THIS EVALUATIONNNNNNNNN
            if isinstance(excVal,tuple) and excVal[1] is not None:
                return excVal      
            if not isinstance(excVal,str):
                self.BASE.error(ErrorType.TYPE_ERROR,description="Exception can only be string type!")
            return (None,excVal)
            



        else:
            raise RuntimeError

        

def stringify(val):
    if val is None:
        return "null"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, str):
        return '"' + val + '"'
    else: #int case
        return str(val)
