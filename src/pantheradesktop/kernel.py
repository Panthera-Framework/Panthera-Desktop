#-*- encoding: utf-8 -*-

import os
import sys
import atexit
import pantheradesktop.config
import pantheradesktop.hooking
import pantheradesktop.logging
import pantheradesktop.tools as tools

try:
    import pantheradesktop.argsparsing
except Exception:
    pass

try:
    import pantheradesktop.qtgui
except Exception:
    pass

import pantheradesktop.db

try:
    from PySide import QtCore
except ImportError:
    from PyQt4 import QtCore

__author__ = "Damian Kęska"
__license__ = "LGPLv3"
__maintainer__ = "Damian Kęska"
__copyright__ = "Copyleft by Panthera Desktop Team"

class Singleton(object):
    _instance = None
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            
        return class_._instance

class pantheraDesktopApplication(Singleton):
    """
       Panthera Desktop Framework
       
       Main class used to be extended by desktop application, provides base functionality (configuration, database, templating)
       
    """

    config = "" # cofiguration object
    template = "" # gui template object
    argsParser = ""
    app = ""
    __appMain = ""
    
    # application name
    appName = "pantheradesktop-exampleapp"
    version = "0.1"
    
    # directory where to store data eg. ~/.example (will be automaticaly generated in initialize function)
    filesDir = ""
    
    # core classes
    coreClasses = {
        'hooking': pantheradesktop.hooking.pantheraHooking, 
        'logging': pantheradesktop.logging.pantheraLogging, 
        'argsparsing': pantheradesktop.argsparsing.pantheraArgsParsing, 
        'config': pantheradesktop.config.pantheraConfig,
        'gui': pantheradesktop.qtgui.pantheraQTGui, # set to None to disable
        'db': pantheradesktop.db.pantheraDB
    }
    
    def multipleIsFile(self, dirs, fileName):
        for path in dirs:
            if os.path.isfile(path+"/"+fileName):
                return path+"/"+fileName
                
        return False
    
    @classmethod
    def getInstance(c):
        return c.instance
    
    def initialize(self, quiet=False):
        """
            Create required directories, initialize basic objects
            
        """
        
        atexit.register(self.pa_exit)
        self.filesDir = os.path.expanduser("~/."+self.appName)

        # plugins paths
        self.pluginsSearchDirectories = [
            self.filesDir+'/plugins',
            '/usr/share/'+self.appName+'/plugins',
            '/var/lib/'+self.appName+'/plugins'
        ]
        
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
               
        if not os.path.isfile(self.filesDir+"/config.json"):
            try:
                w = open(self.filesDir+"/config.json", "w")
                w.write("{}")
                w.close()
            except Exception as e:
                print("Cannot create "+self.filesDir+"/config.json, please check permissions (details: "+e.strerror+")")
                sys.exit(5)       
        
        # initialize configuration
        self.config = self.coreClasses['config'](self)
        self.config.configPath = self.filesDir+"/config.json"
        
        # initialize database
        if self.coreClasses['db']:
            self.db = self.coreClasses['db'](self)

        # initialize plugins
        self.loadPlugins()

    def loadPlugins(self):
        """
        Load application plugins from directories specified in self.pluginsSearchDirectories
        Only plugins enabled in configuration will be loaded
        :return:
        """

        #for path in self.pluginsSearchDirectories:
        #    print(path)


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
        
        if hasattr(func, '__call__') or "classobj" in str(type(func)):
            self.__appMain = func(self)
            
    def pa_exit(self):
        """ On application exit """
    
        self.hooking.execute('app.pa_exit')
        sys.exit(0)
            
class pantheraClass:
    """ Panthera class """

    panthera = ""

    def __init__(self, panthera):
        """ Initialize object """
    
        self.panthera = panthera
        self.app = panthera
        self.main()
        
    def main(self):
        print("Overwrite me - main()")
    
class pantheraWorker(QtCore.QObject):
    """
        Worker for pantheraWorkThread
    """
    
    finished = QtCore.pyqtSignal()
    dataReady = QtCore.pyqtSignal(list, dict)
    job = None
    jobArgs = None
    thread = None
    
    def setJob(self, job, args='', thread=''):
        self.job = job
        self.jobArgs = args
        self.thread = thread
    
    """
        Run callable function inside of thread
    """

    def run(self):
        if self.job:
            if self.jobArgs:
                self.job(self.jobArgs, self.thread)
            else:
                self.job(thread=self.thread)
        else:
            print("Warning: pantheraWorker job was not set")
            
        self.finished.emit()
            
class pantheraWorkThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

     # this class is solely needed for these two methods, there
     # appears to be a bug in PyQt 4.6 that requires you to
     # explicitly call run and start from the subclass in order
     # to get the thread to actually start an event loop

    def start(self):
        QtCore.QThread.start(self)

    def run(self):
        QtCore.QThread.run(self)
        
def createThread(callable, args='', autostart=True):
    """ Create a Worker and Thread and connect them """
    
    appThread = pantheradesktop.kernel.pantheraWorkThread()
    appWorker = pantheradesktop.kernel.pantheraWorker()
    appWorker.setJob(callable, args, appThread)
    appWorker.moveToThread(appThread)
    appWorker.finished.connect(appThread.terminate)
    appThread.started.connect(appWorker.run)
    
    if autostart:
        appThread.start()
    
    return appThread, appWorker
