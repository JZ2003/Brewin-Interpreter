from intbase import *
from Bclass import *


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) # call InterpreterBase’s constructor
    
    def run(self,program):
        class1 = Bclass(program,self)
        classObject1 = class1.instantiate_object()
        for f in classObject1.fields:
            t, v = f.evaluate()
            n = f.name()
            print(f"{n}: type {t}, value: {v}")
        # string = "\"\""
        # c = Bconstant(self,string)
        # print(f"string represents {c.value}, with type {c.type}")






























def read_file(file_path):
    """Reads a file of text and returns a list of strings."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

def print_line_nums(parsed_program):
    for item in parsed_program:
        if type(item) is not list:
            print(f'{item} was found on line {item.line_num}')
        else:
            print_line_nums(item)


def main():
    # program_source = ['(class main',
    # ' (method main ()',
    # ' (print "hello world!")',
    # ' ) # end of method',
    # ') # end of class']

    file_path = "./codeExample1.brewin"
    program_source = read_file(file_path=file_path)
    # this is how you use our BParser class to parse a valid
    # Brewin program into python list format.
    result, parsed_program = BParser.parse(program_source)
    if result == True:    
        I = Interpreter()
        I.run(parsed_program[0])
        # print_line_nums(parsed_program[0])
        # print(parsed_program)
    else:
        print('Parsing failed. There must have been a mismatched parenthesis.')

main()
