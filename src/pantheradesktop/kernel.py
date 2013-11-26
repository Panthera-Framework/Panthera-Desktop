import os
import sys
import pantheradesktop.config
import pantheradesktop.hooking
import pantheradesktop.logging
import pantheradesktop.argsparsing

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
    
    # directory where to store data eg. ~/.example (will be automaticaly generated in initialize function)
    filesDir = ""
    
    # core classes
    coreClasses = {'hooking': pantheradesktop.hooking.pantheraHooking, 'logging': pantheradesktop.logging.pantheraLogging, 'argsparsing': pantheradesktop.argsparsing.pantheraArgsParsing, 'config': pantheradesktop.config.pantheraConfig}
    
    
    
    def initialize(self):
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
        self.logging = self.coreClasses['logging'](self)
        self.logging.output('Initializing application', 'pantheraDesktopApplication')
               
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
                
        # initialize args parser
        self.argsParser = self.coreClasses['argsparsing'](self)
        self.argsParser.parse()
        
        self.hooking.execute('app.mainloop')
                
                
                
