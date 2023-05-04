from intbase import *
from Bclass import *
from Bexpression import Bexp
from Bconstant import Bconstant
from Bstatement import Bstatement

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) # call InterpreterBase’s constructor
        self.BclassList = []
    
    def run(self,program):
        Bobjects = []
        # class1 = Bclass(program,self)
        # classObject1 = class1.instantiate_object()
        # for f in classObject1.fields:
        #     t, v = f.evaluate()
        #     n = f.name()
        #     print(f"{n}: type {t}, value: {v}")
        # print("----------------")
        # for m in classObject1.methods:
        #     n = m.name()
        #     s,p = m.test()
        #     print(f"{n}: parameters: {p}, statement: {s}")
        # string = "\"\""
        # c = Bconstant(self,string)
        # print(f"string represents {c.value}, with type {c.type}")
        for c in program:
            self.BclassList.append(Bclass(c,self))
        class1 = Bclass(program[0],self)
        Object1 = class1.instantiate_object()
        p1_val = Bconstant(self,"33345")
        p2_val = Bconstant(self,"\"skrr\"")
        p3_val = Bconstant(self,"false")
        Parameters = {"p1": p1_val, "p2": p2_val, "p3": p3_val}
        # initial = ["!",["!",["!",["!", "ZJX"]]]]
        initial = ['begin', ['begin', ['begin', ['print', 'p1']]]]
        initial = ["if", "false", ["print","123"], ["print", "456"]]
        # initial = ["|", "p1", "p3"]
        # exp = Bexp(self,Object1,Parameters=Parameters,initialList=initial)
        # print(f"This expression evaluates to {exp.evaluate()}, with type: {type(exp.evaluate())}")
        stm = Bstatement(self,Object1,initialList=initial)
        stm.process(Parameters=Parameters)




























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
    # program_source = ""

    file_path = "./codeExample2.brewin"
    program_source = read_file(file_path=file_path)
    # this is how you use our BParser class to parse a valid
    # Brewin program into python list format.
    result, parsed_program = BParser.parse(program_source)
    if result == True:    
        I = Interpreter()
        I.run(parsed_program)
        # print_line_nums(parsed_program[0])
        # print(parsed_program)
    else:
        print('Parsing failed. There must have been a mismatched parenthesis.')

main()
