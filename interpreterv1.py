from intbase import *

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) # call InterpreterBase’s constructor
    
    def run(self,program):
        pass































def read_file(file_path):
    """Reads a file of text and returns a list of strings."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines




def main():
    # program_source = ['(class main',
    # ' (method main ()',
    # ' (print "hello world!")',
    # ' ) # end of method',
    # ') # end of class']

    file_path = "./codeExample2.brewin"
    program_source = read_file(file_path=file_path)
    # this is how you use our BParser class to parse a valid
    # Brewin program into python list format.
    result, parsed_program = BParser.parse(program_source)
    if result == True:
        print(parsed_program)
    else:
        print('Parsing failed. There must have been a mismatched parenthesis.')

main()

L = [['class', 'person', ['field', 'name', '""'], ['field', 'age', '0'], ['method', 'init', ['n', 'a'], ['begin', ['set', 'name', 'n'], ['set', 'age', 'a']]], ['method', 'talk', ['to_whom'], ['print', 'name', '" says hello to "', 'to_whom']]], ['class', 'main', ['field', 'p', 'null'], ['method', 'tell_joke', ['to_whom'], ['print', '"Hey "', 'to_whom', '", knock knock!"']], ['method', 'main', [], ['begin', ['call', 'me', 'tell_joke', '"Matt"'], ['set', 'p', ['new', 'person']], ['call', 'p', 'init', '"Siddarth"', '25'], ['call', 'p', 'talk', '"Paul"']]]]]
print(len(L[1]))