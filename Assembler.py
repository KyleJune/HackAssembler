'''
Assembler
Translates HACK assembly into HACK machine code.

@author: Kyle June
'''
import sys
from Parser import Parser
import Code
from SymbolTable import SymbolTable

asmFilename = sys.argv[1]

# This goes through the file and adds the address for each label to the symbol table.
parser = Parser(asmFilename)
symbolTable = SymbolTable()
romAddress = 0
while parser.hasMoreCommands():
    parser.advance()
    if parser.commandType() == 'L_COMMAND':
        symbolTable.addEntry(parser.symbol(), romAddress)
    else:
        romAddress += 1

# This opens the file that will be written to.
hackFilename = asmFilename[:-3] + 'hack'
hackFile = open(hackFilename, 'w')

# This writes the translated code to the hack file.
parser.restart()
ramAddress = 16
while parser.hasMoreCommands():
    parser.advance()
    commandType = parser.commandType()
    if commandType == 'C_COMMAND':
        hackFile.write('111' + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump()) + '\n')
    elif commandType == 'A_COMMAND':
        symbol = parser.symbol()
        try:
            address = int(symbol)
        except:
            if symbolTable.contains(symbol):
                address = symbolTable.getAddress(symbol)
            else:
                address = ramAddress
                # This adds an A command symbol to the symbol table if it's not already in it.
                symbolTable.addEntry(symbol, address)
                ramAddress += 1
        
        hackFile.write(bin(address)[2:].zfill(16) + '\n')

hackFile.close()
