
class Bmethod:
    def __init__(self,BASE,OBJ,initialList):
        self.BASE = BASE
        self.OBJ = OBJ # The object it belongs to; used to access field variables and "ME".
        self.methodName = None
        self.statement = None
        self.parameters = []
        self.__parse_name_and_statement(initialList)
    
    def name(self):
        return self.methodName
    
    def __parse_name_and_statement(self,l):
        pass
        self.methodName = l[1]
        self.parameters = l[2]
        self.statement = l[3] #TODO: instantiate a real statement

    def execute_statement(self):
        # evaluate the statement with parameters and OBJ fields
        pass

    def test(self):
        return self.statement, self.parameters