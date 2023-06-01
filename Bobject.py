from intbase import InterpreterBase as INTBASE
from Bfield import Bfield
from Bmethod import Bmethod
from Bconstant import Bconstant
# from Bexpression import Bexp
from intbase import ErrorType
from Bvariable import BVariable

class Bobject:
    def __init__(self,BASE,className,fields,methods,super_class=None,sub=None):
        """
        super_class: (Bclass) 
        sub: (Bobject) 
        """
        self.BASE = BASE
        self.classNAME = className
        self.fields = []
        self.methods = []
        self.__add_field(fields)
        self.__add_method(methods)
        self.superObj = None
        if super_class is not None:
            self.superObj = super_class.instantiate_object(subObject=self)
        self.subObj = sub
    
    def isObject(self,thing):
        try:
            const = Bconstant(self.BASE, stringify(thing))
            return False
        except:
            return True

    def __add_method(self,methods):
        for m in methods:
            # Check the format of the method definitions
            if len(m) != 5:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for method in an object.")
            if not isinstance(m[2],str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Method doesn't have a string name.")
            if not isinstance(m[3],list):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Don't have a parameter list.")
            if not isinstance(m[1], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Method doesn't have a string type.")
            if not isinstance(m[4],list):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong statement format inside a method.")

            newMethodObject = Bmethod(self.BASE,self,m)
            self.methods.append(newMethodObject)

    def __add_field(self,fields):
        for f in fields: 
            # Check the format of the field definitions
            if len(f) != 4 and len(f) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field in an object")
            if not isinstance(f[1], str):
                 self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field type")
            if not isinstance(f[2], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field name")
            if len(f) == 4:
                if not isinstance(f[3], str):
                    self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field initial value")
                newFieldObject = Bfield(self.BASE,fieldName=f[2],initialValue=f[3],fieldType=f[1])
            else: # Len(f) == 3
                newFieldObject = Bfield(self.BASE,fieldName=f[2],initialValue=None,fieldType=f[1])
            self.fields.append(newFieldObject)
    
    def get_the_most_derived(self):
        obj = self
        while obj.subObj is not None:
            obj = obj.subObj
        return obj

    def run_method(self, method_name, param_list):
        """
        method_name: (str) the name of the method to be called
        param_list: (list) need to be converted to a dict before use (from CALL exp)
                    It could be objects or python primitives
        """
        # Find if such method exists
        theMethod = next((m for m in self.methods if m.name() == method_name), None)
        if theMethod is None:
            if self.superObj is not None:
                result = self.superObj.run_method(method_name,param_list)
                return result
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")
        
        method_param = theMethod.get_parameters()
        # Check if the # of parameters is correct
        if len(param_list) != len(method_param):
            if self.superObj is not None:
                result = self.superObj.run_method(method_name,param_list)
                return result
            else:
                self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")

        var_list = []
        
        ## Add all parameters to the var_list
        for p, mp in zip(param_list, method_param):
            if not self.isObject(p):  
                const = Bconstant(self.BASE,stringify(p))
                if const.get_type() == mp[0]:
                    var_list.append(BVariable(self.BASE, varName=mp[1], initialValue=const, varType=mp[0]))
                else:
                    if self.superObj is not None:
                        result = self.superObj.run_method(method_name,param_list)
                        return result
                    else:
                        self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")
            else:
                if p.get_type() is None: # If the value is a generic null
                    if mp[0] not in [INTBASE.INT_DEF,INTBASE.STRING_DEF,INTBASE.BOOL_DEF]:
                        if not INTBASE.TYPE_CONCAT_CHAR in mp[0]:
                            for c in self.BASE.get_BclassList():
                                if mp[0] == c.get_single_name():
                                    p.change_type(className=c.get_name())                         
                                    break
                        else:
                            p.change_type(className=mp[0])
                        var_list.append(BVariable(self.BASE, varName=mp[1], initialValue=p, varType=mp[0]))
                    else:
                        if self.superObj is not None:
                            result = self.superObj.run_method(method_name,param_list)
                            return result
                        else:
                            self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")
                else: # If it's a non-generic null or an object
                    if isinstance(p.get_type(), list) and mp[0] in p.get_type(): #TODO: Check subclasses #SEEMINGLY DONE
                        var_list.append(BVariable(self.BASE, varName=mp[1], initialValue=p, varType=mp[0]))
                    elif isinstance(p.get_type(), str) and mp[0] == p.get_type():
                        var_list.append(BVariable(self.BASE, varName=mp[1], initialValue=p, varType=mp[0]))
                    else:
                        if self.superObj is not None:
                            result = self.superObj.run_method(method_name,param_list)
                            return result
                        else:
                            self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")

        ## Add all fields to the var_list
        var_list += self.fields
        result = theMethod.execute_statement(var_list)
        return result
    
    def evaluate(self):
        return self

    def get_type(self):
        """
        Return: (list) a list that consists of this object's class name and
                all its superclasses' names.
        """
        return self.classNAME

# def isObject(thing):
#     return isinstance(thing,Bobject)

def stringify(val):
    if val is None:
        return "null"
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, str):
        return '"' + val + '"'
    else: #int case
        return str(val)