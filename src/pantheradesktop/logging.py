import inspect
from time import strftime, localtime
import time

class pantheraLogging:
    logging = True
    silent = False
    session = ""
    panthera = ""
    lastLogTime = 0
    
    
    
    def initializeTimer(self):
        """
            Initialize timer for benchmarking custom code blocks
        """
    
        self.lastLogTime = time.time()
    
    
    
    def convertMessage(self, message, stackPosition):
        """
            Format a message
            
            message - message
            stackPosition - function name on stack
            
            Returns string
        """
    
        diff = "-"
    
        if self.lastLogTime > 0:
            diff = time.time()-self.lastLogTime
    
        return "["+str(time.time())+", "+str(diff)+"] "+stackPosition+": "+message
        
        
    
    def __init__ (self, panthera):
        """ 
            Constructor, takes panthera object as argument 
        """
    
        self.panthera = panthera
        
        

    def output(self, message, group='', savetoLogs=True, execHook=True, skipDate=False):
        """ 
            Outputs to log file and to console 
        """
        
        if self.logging == False:
            return False
            
        if not skipDate:
            message = self.convertMessage(message, inspect.stack()[1][3])
            
        if self.silent == False:
            print(message)
            
        self.session += message + "\n"
