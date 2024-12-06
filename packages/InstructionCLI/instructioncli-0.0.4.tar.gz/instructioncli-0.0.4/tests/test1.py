import os
import sys

# Получаем путь к каталогу src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from InstructionCLI import cli, Instruction, NoInstruction

class RunInstruction(Instruction):  
    def applyParameters(self, parameters : dict):
        print(parameters)
        pass

    def doInstruction(self, expression):
        pass
    
    def nextInstruction(self):
        return NoInstruction()

print(sys.argv)

cli(sys.argv[1:], RunInstruction())