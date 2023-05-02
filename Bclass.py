from bparser import *
from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
from Bobject import Bobject

class Bclass:
    def __init__(self, code, BASE):
        """
        self.name: (str) class name
        self.methods: (list) list of method info
        self.fields: (list) list of field info
        """
        self.BASE = BASE
        if code[0] != INTBASE.CLASS_DEF:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Missing 'class' keyword")
        if isinstance(code[1], str): # NOTE: Probably gonna need to use StringWithLineNumber
                                     # SOLVE: use isinstance() will help to check subclass as well
            self.name = code[1]
        else:
            self.BASE.error(ErrorType.SYNTAX_ERROR,description="Missing name for the class")
        self.methods = []
        self.fields = []
        self.__get_methods_and_fields(code[2:])
        
        # Check if there is at least one method in the Bclass definition
        if(len(self.methods) < 1):
            self.BASE.error(ErrorType.TYPE_ERROR,description="A class must have at least one method.")
        
        #TODO: Check fields and methods don't have duplicate names
        #DONE:
        listOfFieldAndMethodNames = [f[1] for f in self.fields] + [m[1] for m in self.methods]
        if len(listOfFieldAndMethodNames) != len(set(listOfFieldAndMethodNames)):
            self.BASE.error(ErrorType.NAME_ERROR,description="Can't have duplicate field or method` names")
    
    def __get_methods_and_fields(self,code):
        for x in code:
            if type(x) is not list:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong syntax for method or field.")
            if x[0] == INTBASE.METHOD_DEF:
                #TODO: convert x to method object
                self.methods.append(x)
            elif x[0] == INTBASE.FIELD_DEF:
                self.fields.append(x)
            else:
                self.BASE.error(ErrorType.SYNTAX_ERROR,description="Invalid syntax for class definition.")

    def instantiate_object(self):
        newClassObject = Bobject(self.BASE,self.name,self.fields,self.methods)
        return newClassObject

    def __str__(self):
        return f"class name: {self.name}; # of class methods: {len(self.methods)}; # of class fields: {len(self.fields)} "


















# L = [['class', 'person', ['field', 'name', '""'], ['field', 'age', '0'], ['method', 'init', ['n', 'a'], ['begin', ['set', 'name', 'n'], ['set', 'age', 'a']]], ['method', 'talk', ['to_whom'], ['print', 'name', '" says hello to "', 'to_whom']]], ['class', 'main', ['field', 'p', 'null'], ['method', 'tell_joke', ['to_whom'], ['print', '"Hey "', 'to_whom', '", knock knock!"']], ['method', 'main', [], ['begin', ['call', 'me', 'tell_joke', '"Matt"'], ['set', 'p', ['new', 'person']], ['call', 'p', 'init', '"Siddarth"', '25'], ['call', 'p', 'talk', '"Paul"']]]]]
# code = L[0]
# print(code)
# person = Bclass(code)
# print(person)