import pantheradesktop.config
import pantheradesktop.hooking

"""
   Panthera Desktop Framework
   
   Main class used to be extended by desktop application, provides base functionality (configuration, database, templating)
   
"""

class pantheraDesktopApplication:
    config = "" # cofiguration object
    template = "" # gui template object
    
    # application name
    appName = "example"
    
    # directory where to store data eg. ~/.example (will be automaticaly generated in initialize function)
    filesDir = ""
    
    """
        Create required directories, initialize basic objects
        
    """
    
    def initialize():
        self.filesDir = os.path.expanduser("~/."+appName)
        
        # create user's data directory if missing
        if not os.path.isdir(self.filesDir):
            try:
                os.mkdir(self.filesDir)
            except Exception as e:
                print("Cannot create "+self.filesDir+" directory, please check permissions (details: "+e.strerror+")")
                sys.exit(5)
            
        # initialize configuration
        self.config = pantheradesktop.config.pantheraConfig(self)
        
        if not os.path.isfile(self.filesDir+"/config.json"):
            try:
                w = open(self.filesDir+"/config.json", "r")
                w.write("{}")
                w.close()
            except Exception as e:
                print("Cannot create "+self.filesDir+"/config.json, please check permissions (details: "+e.strerror+")")
                sys.exit(5)
                
                
                
                
                
