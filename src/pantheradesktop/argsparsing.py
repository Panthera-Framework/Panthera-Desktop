#-*- encoding: utf-8 -*-

import argparse
import sys

__author__ = "Damian Kęska"
__license__ = "LGPLv3"
__maintainer__ = "Damian Kęska"
__copyright__ = "Copyleft by Panthera Desktop Team"

class pantheraArgsParsing:
    """
        Arguments parsing class for Panthera Desktop Framework
        It's just a simple wrapper to argparse module that supports callbacks
        
    """

    description = 'Example app'
    argparse = ""
    panthera = None
    
    # here will be args and opts stored
    args = None
    opts = None

    knownArgs = {}
    
    
    
    def __init__ (self, panthera):
        """
            Initialize argument parser with Panthera Framework object
            
            panthera - Panthera object
            
        """
    
        self.panthera = panthera
        self.argparse = argparse.ArgumentParser(description=self.description)
        self.createArgument('--version', self.version, '', 'Display help', action='store_true')
        
        
        
    def version(self, value=''):
        """
            Example argument handler, shows application version
            
        """
    
        print(self.panthera.appName + " " +self.panthera.version)
        sys.exit(0)
        
        
        
    def createArgument(self, arg, callback, default="", help="", required=False, dataType=None, action='store', choices=None, type=None, skipArgParse=False):
        """
            Add argument to list of known arguments
            
            arg - Argument name eg. --test
            callback - Function to call back if this argument was used
            default - Default value
            help - Help text to display
            required - Is this a required field?
            skipArgParse - Skip using argparse in this function and use it by your own
            
            Returns none
        """
        
        self.knownArgs[arg] = callback
    
        if not skipArgParse:
            if action == 'store_true' or action == 'store_const' or action == 'store_false':
                return self.argparse.add_argument(arg, default=default, help=help, required=required, action=action)
            
            return self.argparse.add_argument(arg, default=default, help=help, required=required, action=action, choices=choices, type=type)
        
        
        
    def parse(self):
        """
            Run arguments parsing
            
        """
        
        if "addArgs" in dir(self):
            self.addArgs()
        
        self.args = self.argparse.parse_known_args()
        self.opts = self.args[1]
        
        for arg in self.knownArgs:
            if arg in sys.argv:
                self.knownArgs[arg](self.args[0].__dict__[arg.replace('--', '')])
