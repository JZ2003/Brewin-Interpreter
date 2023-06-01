from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bobject import Bobject
import copy

# list_keyWord = ["class","method","field","null","begin", "set", "new", "if", "while", "main", "call", "tclass",
#                 "return", "inputs", "inputi", "true", "false","print",""]

class Btemp:
    def __init__(self,code,BASE):
        self.BASE = BASE
        self.super = None # The father (Bclass)
        if code[0] != INTBASE.TEMPLATE_CLASS_DEF:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Missing 'tclass' keyword")
        if isinstance(code[1], str):
            self.name = code[1]
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Missing name for the tclass")
        
        self.param_type = []
        if isinstance(code[2], list) and len(code[2]) >= 1:
            self.param_type = code[2]
        else:
             self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong syntax of parametrized types")
        self.fieldsAndMethods = code[3:]

    def get_name(self):
        return [self.name] #NOTE: This is undertermined yet whether we should return a list

    def get_single_name(self):
        return self.name

    def __type_substitute(self, list, p, f):
        for i in range(len(list)):
            if isinstance(list[i], str):
                list[i] = list[i].replace(p,f)
            else:
                self.__type_substitute(list[i], p, f)
            

    def instantiate_object(self, initString):
        """
        list_paramTypes: (list) list of string literals that specify the formal types of 
            the parametrized type object. 
        """
        list_paramTypes = initString.split(INTBASE.TYPE_CONCAT_CHAR)[1:]
        if len(list_paramTypes) != len(self.param_type):
            self.BASE.error(ErrorType.TYPE_ERROR,description="Wrong number of parametrized types")
        dict_types = {}
        for pt in zip(list_paramTypes,self.param_type):
            dict_types[pt[1]] = pt[0]

        temp_fieldsAndMethods = copy.deepcopy(self.fieldsAndMethods)
        for param, formal in dict_types.items():
            theList = temp_fieldsAndMethods
            self.__type_substitute(theList, param, formal)
        list_fields = []
        list_methods = []
        for x in temp_fieldsAndMethods:
            if not isinstance(x, list):
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format of template method or field")
            if x[0] == INTBASE.FIELD_DEF:
                list_fields.append(x)
            elif x[0] == INTBASE.METHOD_DEF:
                list_methods.append(x)
            else:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong format of template method or field")

        newClassObject = Bobject(BASE=self.BASE,className=initString,fields=list_fields,methods=list_methods,super_class=None,sub=None)
        return newClassObject