#-*- encoding: utf-8 -*-

import os
import sys
import pantheradesktop.config
import pantheradesktop.hooking
import pantheradesktop.logging
import pantheradesktop.argsparsing
import pantheradesktop.qtgui

__author__ = "Damian Kęska"
__license__ = "LGPLv3"
__maintainer__ = "Damian Kęska"
__copyright__ = "Copyleft by Panthera Desktop Team"

class pantheraDesktopApplication:
    """
       Panthera Desktop Framework
       
       Main class used to be extended by desktop application, provides base functionality (configuration, database, templating)
       
    """

    config = "" # cofiguration object
    template = "" # gui template object
    argsParser = ""
    
    # application name
    appName = "example"
    version = "0.1"
    
    # directory where to store data eg. ~/.example (will be automaticaly generated in initialize function)
    filesDir = ""
    
    # core classes
    coreClasses = {
        'hooking': pantheradesktop.hooking.pantheraHooking, 
        'logging': pantheradesktop.logging.pantheraLogging, 
        'argsparsing': pantheradesktop.argsparsing.pantheraArgsParsing, 
        'config': pantheradesktop.config.pantheraConfig,
        'gui': pantheradesktop.qtgui.pantheraQTGui # set to None to disable
    }
    
    def multipleIsFile(self, dirs, fileName):
        for path in dirs:
            if os.path.isfile(path+"/"+fileName):
                return path+"/"+fileName
                
        return False
    
    
    def initialize(self, quiet=False):
        """
            Create required directories, initialize basic objects
            
        """
        
        self.filesDir = os.path.expanduser("~/."+self.appName)
        
        # create user's data directory if missing
        if not os.path.isdir(self.filesDir):
            try:
                os.mkdir(self.filesDir)
            except Exception as e:
                print("Cannot create "+self.filesDir+" directory, please check permissions (details: "+e.strerror+")")
                sys.exit(5)

        self.hooking = self.coreClasses['hooking']()
        self.logging = self.coreClasses['logging'](self, quiet)
        
        # plugins support: action before configuration load
        self.hooking.execute('app.beforeConfigLoad')
               
        # initialize configuration
        self.config = self.coreClasses['config'](self)
        
        if not os.path.isfile(self.filesDir+"/config.json"):
            try:
                w = open(self.filesDir+"/config.json", "w")
                w.write("{}")
                w.close()
            except Exception as e:
                print("Cannot create "+self.filesDir+"/config.json, please check permissions (details: "+e.strerror+")")
                sys.exit(5)

    def main(self, func=None):
        """ Main function """
        
        # initialize args parser
        self.argsParser = self.coreClasses['argsparsing'](self)
        self.argsParser.parse()
    
        self.logging.output('Initializing application mainloop', 'pantheraDesktopApplication')
        
        # graphical user interface (if avaliable)
        if "gui" in self.coreClasses:
            if self.coreClasses['gui']:
                self.gui = self.coreClasses['gui'](self)
        
        # plugins support: mainloop
        self.hooking.execute('app.mainloop')
        
        if hasattr(func, '__call__'):
            func(self)
            
class pantheraClass:
    """ Panthera class """

    panthera = ""

    def __init__(self, panthera):
        """ Initialize object """
    
        self.panthera = panthera
        self.main()
        
    def main(self):
        print("Overwrite me - main()")
                
                
