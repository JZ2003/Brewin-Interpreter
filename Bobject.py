# from intbase import *``
from Bfield import Bfield
from Bmethod import Bmethod
from Bconstant import Bconstant
# from Bexpression import Bexp
from intbase import ErrorType
class Bobject:
    def __init__(self,BASE,className,fields,methods):
        self.BASE = BASE
        self.classNAME = className
        self.fields = []
        self.methods = []
        self.__add_field(fields)
        self.__add_method(methods)
    
    def __add_method(self,methods):
        for m in methods:
            # Check the format of the method definitions
            if len(m) != 4:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for method in an object")
            if not isinstance(m[1],str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Method doesn't have a string name")
            if not isinstance(m[2],list):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Don't have a parameter list")
            #TODO: check statement format

            newMethodObject = Bmethod(self.BASE,self,m)
            self.methods.append(newMethodObject)

    def __add_field(self,fields):
        for f in fields: 
            # Check the format of the field definitions
            if len(f) != 3:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field in an object")
            if not isinstance(f[1], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field name")
            if not isinstance(f[2], str):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format for field initial value")
            
            # f has the form: ["field", "<fieldName>", "<initialValue"]
            newFieldObject = Bfield(self.BASE,fieldName=f[1],initialValue=f[2])
            self.fields.append(newFieldObject)
    
    def run_method(self, method_name, param_list):
        """
        method_name: (str) the name of the method to be called
        param_list: (list) need to be converted to a dict before use (from CALL exp)
                    It could be objects or python primitives
        """
        # Find if such method exists
        theMethod = next((m for m in self.methods if m.name() == method_name), (None,None))
        if theMethod == (None,None):
            self.BASE.error(ErrorType.NAME_ERROR,description="Calling an undefined method.")
        method_param = theMethod.get_parameters()
        # Check if the # of parameters is correct
        if len(param_list) != len(method_param):
            self.BASE.error(ErrorType.TYPE_ERROR,description="Calling a method with wrong number of parameters.")
        # param_evaluated = []
        # for p in param_list:
        #     if isinstance(p,list):
        #         exp = Bexp(self.BASE,self,)
        param_dict = {}
        for p, mp in zip(param_list, method_param):
            try:  
                const = Bconstant(self.BASE,stringify(p))
                param_dict[mp] = const
            except:
                if isinstance(p,Bobject):
                    param_dict[mp] = p
                else:
                    self.BASE.error(ErrorType.SYNTAX_ERROR,description="Passing in wrong format of parameters.")
        
        result = theMethod.execute_statement(param_dict)
        return result
    
    def evaluate(self):
        return self

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