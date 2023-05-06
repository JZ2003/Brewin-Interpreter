from intbase import InterpreterBase as INTBASE
from intbase import ErrorType
# from Bconstant import Bconstant
# from Bexpression import Bexp
from Bstatement import Bstatement
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
    
    def get_parameters(self):
        return self.parameters

    def get_statement(self):
        return self.statement
    
    def __parse_name_and_statement(self,l):
        pass
        self.methodName = l[1]
        self.parameters = l[2]
        self.statement = l[3] #TODO: instantiate a real statement

    def execute_statement(self,Parameters):
        # evaluate the statement with parameters and OBJ fields
        """
        Parameters: (dict) get parameters from the object call_method function
        """

        # if len(self.parameters) != len(Parameters):
        #     self.BASE.error(ErrorType.TYPE_ERROR,description="Wrong number of parameters")
        # Prmt_evaluated = [Bexp(self.BASE) for p in Parameters]

        stm = Bstatement(self.BASE,self.OBJ,self.statement)
        result = stm.process(Parameters=Parameters)
        return result

    def test(self):
        return self.statement, self.parameters
