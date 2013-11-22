import json

class pantheraConfig:
    """
        Panthera Desktop Configuration
        
        Simple json based key-value storage
        
    """

    panthera = ""
    memory = {}
    configPath = ""
    configurationChanged = False
    
    def __init__(self, panthera):
        self.panthera = panthera
    
    def loadConfig(self):
        """
            Load configuration from JSON file to memory
            
        """
    
        t = open(self.configPath, "rb")
        
        try:
            memory = json.loads(t.read())
        except Exception as e:
            print("Cannot parse configuration file, "+e.strerror)
            sys.exit(5) # errno.EIO = 5
            
        t.close()
        
    
        
    def getKey(self, key, defaultValue=None):
        """
            Get configuration key
        
            key - name
            defaultValue - default value to set if key does not exists yet
        
        """
    
        if not memory:
            self.loadConfig();
    
        if key in self.memory:
            return self.memory[key]
            
        # if key does not exists in key-value database yet, create it with default value
        if defaultValue is not None:
            self.setKey(key, defaultValue)

        return defaultValue
            
    """
        Set configuration key
        
        key - name
        value - value
        
    """
            
    def setKey(self, key, value):
        if type(key) is not str:
            return False
            
        if type(value) is module or type(value) == object:
            return False
    
        self.configurationChanged = True
        self.memory[key] = value
        
    """
        Save configuration right back to json file
        
    """
        
    def save():
        if self.configurationChanged:
            w = open(self.configPath, "wb")
            w.write(json.dumps(self.memory))
            w.close()
        
        
    
    
