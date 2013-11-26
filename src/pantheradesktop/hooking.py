"""
    Hooking (plugins support) module for Panthera Desktop Framework

"""

class pantheraHooking:
    hooksList = {}
    
    def addOption(self, hookName, func, priority=99):
        """
            Connect method to a hooking slot
            
            hookName - hooking slot name
            func - function address
            priority - 0-99 priority number (lowest = higher priority)
            
            Returns bool
        """
        
        if priority > 99 or priority < 0:
            raise Exception('Priority should be in range of 0 to 99')
            return False

        # create array if there is no any hooked function yet
        if not hookName in self.hooksList:
            self.hooksList[hookName] = {}
            
        self.hooksList[hookName][priority+'_'+func.__str__] = func
        
        return True
        
        
    def execute(self, hookName, data=''):
        """
            Execute all functions on selected slot
            
            hookName - hooking slot name
            data - data to pass
            
            Returns data
        """
    
        if not hookName in self.hooksList:
            return data
            
        for func in sorted(self.hooksList[hookName]):
            data = func(data)
            
        return data
        
    def hookExists(self, hookName):
        """
            Check if hooking slot exists
            
            hookName - hooking slot name
            
            Returns bool
        """
    
        return hookName in self.hooksList
        
    def removeOption(self, func, hookName=None):
        """
            Remove an option from hooking slot
            
            func - function
            hookName - hooking slot name
            
            Returns bool
        """
    
        return isConnected(func, hookName, True)
        
    def isConnected(self, func, hookName=None, removeHook=False):
    
        """
            Check if selected function is connected to selected or any hook slot
            
            func - function
            hookName - optional hooking slot
            
            Returns bool
        """
        
        for name in self.hooksList:
        
            if hookName is not None:
                if not self.hookExists(hookName):
                    return False
            
                name = self.hooksList[hookName]
        
            for hook in name:
                if hook == func:
                    if removeHook:
                        del self.hooksList[hookName]
                
                    return True
    
            if hookName is not None:
                return False
