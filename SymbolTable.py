'''
SymbolTable
A symbol table that keeps a correspondence between symbolic 
labels and numeric addresses.

@author: Kyle June
'''

DEFAULT_SYMBOLS = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}

class SymbolTable(object):
    '''
    Creates a new empty symbol table.
    '''
    def __init__(self):
        table = {}
        table.update(DEFAULT_SYMBOLS)
        self._table = table
    
    '''
    Adds the pair (symbol, address) to the table.
    
    @param: symbol string
    @param: address int
    '''
    def addEntry(self, symbol, address):
        self._table.update({symbol: address})
    
    '''
    Does the symbol table contain the given symbol?
    
    @param: symbol string
    @return: Boolean
    '''
    def contains(self, symbol):
        return symbol in self._table
    
    '''
    Returns the address associated with the symbol.
    
    @param: symbol string
    @return: int
    '''
    def getAddress(self, symbol):
        return self._table.get(symbol)
