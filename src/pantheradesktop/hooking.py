"""
    Hooking (plugins support) module for Panthera Desktop Framework

"""

class Hooking:
    hooksList = {}
    
    def addOption(self, hookName, func):
        if not hookName in self.hooksList:
            self.hooksList[hookName] = list()
            
        self.hooksList[hookName].append(func)
