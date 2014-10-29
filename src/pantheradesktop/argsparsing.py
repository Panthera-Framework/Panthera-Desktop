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
    app = None
    
    # here will be args and opts stored
    args = None
    opts = None

    # plugins management
    _enablePluginsManagement = True

    knownArgs = {}
    
    
    
    def __init__ (self, panthera):
        """
            Initialize argument parser with Panthera Framework object
            
            panthera - Panthera object
            
        """
    
        self.panthera = panthera
        self.app = panthera
        self.argparse = argparse.ArgumentParser(description=self.description)
        self.createArgument('--version', self.version, 'Display help', action='store_true', required=False)

        if self._enablePluginsManagement:
            self.createArgument('--plugins', self.pluginsList, 'Display plugins list', action='store_true', required=False)
            self.createArgument('--enablePlugin', self.pluginsEnable, 'Enable plugin', required=False)
            self.createArgument('--disablePlugin', self.pluginsDisable, 'Enable plugin', required=False)

    def pluginsEnable(self, pluginName='', enable=True):
        """
        Enable a plugin
        :param pluginName:
        :param enable:
        :return:
        """

        self.app.loadPlugins()

        if not pluginName in self.app.pluginsAvailable:
            print("Cannot toggle plugin: "+str(pluginName)+", file not found")
            sys.exit(1)

        self.app.togglePlugin(pluginName, enable)
        sys.exit(0)

    def pluginsDisable(self, pluginName):
        """
        Disable a plugin
        :param pluginName:
        :return:
        """

        return self.pluginsEnable(pluginName, False)

    def pluginsList(self, opt=''):
        """
        List all plugins (enabled and disabled)
        :param opt:
        :return:
        """

        self.app.loadPlugins()

        print("Application is looking for plugins in those directories: ")

        for directory in self.app.pluginsSearchDirectories:
            print(directory)

        print("\n")

        if self.app.pluginsAvailable:
            print("Available plugins: ")

            for plugin in self.app.pluginsAvailable:
                if plugin in self.app._plugins:
                    print("[x] "+plugin)
                else:
                    print("[ ] "+plugin)

            print("\nx - enabled")
        else:
            print("No plugins available\n")

        sys.exit(0)
        
    def version(self, value=''):
        """
            Example argument handler, shows application version
            
        """
    
        print(self.panthera.appName + " " +self.panthera.version)
        sys.exit(0)
        
        
        
    def createArgument(self, arg, callback, default="", help="", required=False, dataType=None, action='store', choices=None, type=None, skipArgParse=False, short=None):
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
        argsString = 'arg, default=default, help=help, required=required, action=action'

        if not skipArgParse:
            if not action == 'store_true' and not action == 'store_const' and not action == 'store_false':
                argsString += ', choices=choices, type=type'

            if short is not None:
                argsString = 'short, '+argsString

            eval('self.argparse.add_argument('+argsString+')')

        
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
