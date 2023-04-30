class Bclass:
    def __init__(self, code):
        if code[0] != 'class':
            raise SyntaxError("'class' keyword missing")
        if type(code[1]) is str:
            self.name = code[1]
        else:
            raise SyntaxError("Wrong syntax for class name.")
        self.methods = []
        self.fields = []
        self.__get_methods_and_fields(code[2:])
        if(len(self.methods) < 1):
            #TODO: need to find out the right way to repop
            raise TypeError("A class must have at least one method.")
        #TODO: Check fields and methods don't have duplicate names
    
    def __get_methods_and_fields(self,code):
        for x in code:
            if type(x) is not list:
                raise SyntaxError("Wrong syntax for method or field.")
            if x[0] == 'method':
                #TODO: convert x to method object
                self.methods.append(x)
            elif x[0] == 'field':
                self.fields.append(x)
            else:
                raise SyntaxError("Invalid syntax for class definition.")

    def __str__(self):
        return f"class name: {self.name}; # of class methods: {len(self.methods)}; # of class fields: {len(self.fields)} "


















# L = [['class', 'person', ['field', 'name', '""'], ['field', 'age', '0'], ['method', 'init', ['n', 'a'], ['begin', ['set', 'name', 'n'], ['set', 'age', 'a']]], ['method', 'talk', ['to_whom'], ['print', 'name', '" says hello to "', 'to_whom']]], ['class', 'main', ['field', 'p', 'null'], ['method', 'tell_joke', ['to_whom'], ['print', '"Hey "', 'to_whom', '", knock knock!"']], ['method', 'main', [], ['begin', ['call', 'me', 'tell_joke', '"Matt"'], ['set', 'p', ['new', 'person']], ['call', 'p', 'init', '"Siddarth"', '25'], ['call', 'p', 'talk', '"Paul"']]]]]
# code = L[0]
# print(code)
# person = Bclass(code)
# print(person)