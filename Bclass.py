from bparser import *
from intbase import ErrorType


def get_line_nums(parsed_program):
    for item in parsed_program:
        if type(item) is not list:
            return item.line_num
        else:
            return get_line_nums(item)

class Bclass:
    def __init__(self, code, BASE):
        if code[0] != 'class':
            BASE.error(ErrorType.SYNTAX_ERROR,description="Missing 'class' keyword")
        if isinstance(code[1], str): # NOTE: Probably gonna need to use StringWithLineNumber
                                     # SOLVE: use isinstance() will help to check subclass as well
            self.name = code[1]
        else:
            BASE.error(ErrorType.SYNTAX_ERROR,description="Missing name for the class")
        self.methods = []
        self.fields = []
        self.__get_methods_and_fields(code[2:], BASE)
        if(len(self.methods) < 1):
            #TODO: need to find out the right way to repop
            BASE.error(ErrorType.TYPE_ERROR,description="A class must have at least one method.")
        #TODO: Check fields and methods don't have duplicate names
    
    def __get_methods_and_fields(self,code,BASE):
        for x in code:
            if type(x) is not list:
                BASE.error(ErrorType.SYNTAX_ERROR,description="Wrong syntax for method or field.")
            if x[0] == 'method':
                #TODO: convert x to method object
                self.methods.append(x)
            elif x[0] == 'field':
                self.fields.append(x)
            else:
                BASE.error(ErrorType.SYNTAX_ERROR,description="Invalid syntax for class definition.")

    def __str__(self):
        return f"class name: {self.name}; # of class methods: {len(self.methods)}; # of class fields: {len(self.fields)} "


















# L = [['class', 'person', ['field', 'name', '""'], ['field', 'age', '0'], ['method', 'init', ['n', 'a'], ['begin', ['set', 'name', 'n'], ['set', 'age', 'a']]], ['method', 'talk', ['to_whom'], ['print', 'name', '" says hello to "', 'to_whom']]], ['class', 'main', ['field', 'p', 'null'], ['method', 'tell_joke', ['to_whom'], ['print', '"Hey "', 'to_whom', '", knock knock!"']], ['method', 'main', [], ['begin', ['call', 'me', 'tell_joke', '"Matt"'], ['set', 'p', ['new', 'person']], ['call', 'p', 'init', '"Siddarth"', '25'], ['call', 'p', 'talk', '"Paul"']]]]]
# code = L[0]
# print(code)
# person = Bclass(code)
# print(person)