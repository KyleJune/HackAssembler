'''
Parser
Encapsulates access to the input code. Reads an assembly language command, parses it, and 
provides convenient access to the command's components (fields and symbols). In addition, 
removes all white space and comments.

@author: Kyle June
'''
import re

RE_JUNK = re.compile('(^\s+|\s*(//.*)?$)')
A_COMMAND = re.compile('^@(.*)')
C_COMMAND = re.compile('^(?:([^=]+)=)?([^;\(\)]+)(?:;(.*))?$')
L_COMMAND = re.compile('^\((.*)\)$')

class Parser(object):
    '''
    Opens the input file/stream and gets ready to 
    parse it.
    
    @param: filename string The name of the asm file to be parsed.
    '''
    def __init__(self, filename):
        self._filename = filename
        self._file = open(filename, 'r')
        self._line = None
        self._done = False
        self._command = None
        self._commandType = None
        self._commandMatch = None
    
    '''
    Are there more commands in the input?
    
    @return: Boolean
    '''
    def hasMoreCommands(self):
        if self._done:
            return False
        
        line = self._file.readline()
        if line == '':
            self._file.close()
            self._line = None
            self._done = True
            return False
        
        line = RE_JUNK.sub('', line)
        if line == '':
            return self.hasMoreCommands()
        else:
            self._line = line
            return True
    
    '''
    Reads the next command from the input and 
    makes it the current command. Should be called 
    only if hasMoreCommands() is true. Initially 
    there is no current command.
    '''
    def advance(self):
        self._command = self._line
        self._commandType = None
        self._commandMatch = None
    
    '''
    Returns the type of the current command:
    - A_COMMAND for @xxx where xxx is either a 
      symbol or a decimal number
    - C_COMMAND for dest=comp;jump
    - L_COMMAND (actually, pseudo-command) for 
      (xxx) where xxx is a symbol.
    
    @return: string
    '''
    def commandType(self):
        command = self._command
        commandType = None
        match = A_COMMAND.match(command)
        if match:
            commandType = 'A_COMMAND'
        else:
            match = C_COMMAND.match(command)
            if match:
                commandType = 'C_COMMAND'
            else:
                match = L_COMMAND.match(command)
                if match:
                    commandType = 'L_COMMAND'
        
        self._commandType = commandType
        self._commandMatch = match
        return commandType
    
    '''
    Returns the symbol or decimal xxx of the 
    current command @xxx or (xxx). Should be 
    called only when commandType() is 
    A_COMMAND or L_COMMAND.
    
    @return: string
    '''
    def symbol(self):
        return self._commandMatch.group(1)
    
    '''
    Returns the dest mnemonic in the current 
    C-command (8 possibilities). Should be called 
    only when commandType() is C_COMMAND.
    
    @return: string
    '''
    def dest(self):
        return self._commandMatch.group(1)
    
    '''
    Returns the comp mnemonic in the current 
    C-command (28 possibilities). Should be called 
    only when commandType() is C_COMMAND.
    
    @return: string
    '''
    def comp(self):
        return self._commandMatch.group(2)
    
    '''
    Returns the jump mnemonic in the current 
    C-command (8 possibilities). Should be called 
    only when commandType() is C_COMMAND.
    
    @return: string
    '''
    def jump(self):
        return self._commandMatch.group(3)
    
    '''
    This restarts the parser by re-opening the asm file.
    '''
    def restart(self):
        if not self._done:
            self._file.close()
        self.__init__(self._filename)
