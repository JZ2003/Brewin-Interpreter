from intbase import InterpreterBase, ErrorType
from Bclass import *
from Bexpression import Bexp
from Bconstant import Bconstant
from Bstatement import Bstatement

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) # call InterpreterBase’s constructor
        self.BclassList = []
    
    def run(self,program):
        result, parsed_program = BParser.parse(program)
        # parsed_program = program
        for c in parsed_program:
            self.BclassList.append(Bclass(c,self))
        # Check dup in class definitions
        className_list = [c.get_name() for c in self.BclassList]
        if len(className_list) != len(set(className_list)):
            self.error(ErrorType.TYPE_ERROR, description="Duplicate class definitions!")
        mainClass = next((c for c in self.BclassList if c.get_name() == INTBASE.MAIN_CLASS_DEF), (None,None))
        if mainClass == (None,None):
            self.error(ErrorType.FAULT_ERROR, description="No main class!")
        mainObj = mainClass.instantiate_object()
        mainObj.run_method("main", [])
























# def read_file(file_path):
#     """Reads a file of text and returns a list of strings."""
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         lines = [line.strip() for line in lines]
#         return lines

# def print_line_nums(parsed_program):
#     for item in parsed_program:
#         if type(item) is not list:
#             print(f'{item} was found on line {item.line_num}')
#         else:
#             print_line_nums(item)


# def main():
#     # program_source = ['(class main',
#     # ' (method main ()',
#     # ' (print "hello world!")',
#     # ' ) # end of method',
#     # ') # end of class']
#     # program_source = ""

#     file_path = "./codeExample3.brewin"
#     program_source = read_file(file_path=file_path)
#     # this is how you use our BParser class to parse a valid
#     # Brewin program into python list format.
#     result, parsed_program = BParser.parse(program_source)
#     if result == True:    
#         I = Interpreter()
#         I.run(parsed_program)
#         # print_line_nums(parsed_program[0])
#         # print(parsed_program)
#     else:
#         print('Parsing failed. There must have been a mismatched parenthesis.')

# main()
