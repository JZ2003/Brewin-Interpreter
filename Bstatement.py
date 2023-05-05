from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bexpression import Bexp
# from Bconstant import Bconstant
from Bobject import Bobject
from Bconstant import Bconstant
class Bstatement:
    def __init__(self,BASE,OBJ,initialList):
        self.BASE = BASE
        self.OBJ = OBJ
        self.L = initialList

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
            for e in self.L[1:]:
                toPrint = Bexp(self.BASE,self.OBJ,Parameters,e).evaluate()
                if isinstance(toPrint,Bobject):
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't print an object")
                elif toPrint is None:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Can't print a null")
                elif toPrint is True:
                    self.BASE.output("true")
                elif toPrint is False:
                    self.BASE.output("false")
                elif isinstance(toPrint,int):
                    self.BASE.output(toPrint)
                elif isinstance(toPrint,str):
                    self.BASE.output(toPrint)
                else:
                    self.BASE.error(ErrorType.TYPE_ERROR,description="Something goes wrong when printing")
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
                if isinstance(expVal, Bobject): # object type
                    Parameters[toChange] = expVal
                else: # primitive type
                    const = Bconstant(self.BASE,stringify(expVal))
                    Parameters[toChange] = const
            # If it is a field
            elif theField != (None,None):
                if isinstance(expVal, Bobject): # object type
                    theField.change_value(expVal)
                else: # primitive type
                    theField.change_value(stringify(expVal))
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Can't find the parameter or field to set.")
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
