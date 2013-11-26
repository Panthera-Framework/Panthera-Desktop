import argparse

class pantheraArgsParsing:
    description = 'Example app'
    argparse = ""
    
    # here will be args and opts stored
    args = None
    opts = None

    knownArgs = {}    
    
    def __init__ (self, panthera):
        self.argparse = argparse.ArgumentParser(description=self.description)
        
        self.createArgument('--test', self.showHelp, '', 'Display help')
        
    def showHelp(self):
        print("AAAA")
        return ""
        
    def createArgument(self, arg, callback, default="", help=""):
        """
            Add argument to list of known arguments
            
            arg - Argument name eg. --test
            callback - Function to call back if this argument was used
            default - Default value
            help - Help text to display
            
            Returns none
        """
    
        self.argparse.add_argument(arg, default=default, help=help)
        self.knownArgs[arg] = callback
        
    def parse(self):
        self.args = self.argparse.parse_known_args()
        self.opts = self.args[1]
        
        print(self.__dict__['args'])
        
        for arg in self.__dict__['args']:
            print arg
