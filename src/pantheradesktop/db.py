#-*- encoding: utf-8 -*-

__author__ = "Damian Kęska"
__license__ = "LGPLv3"
__maintainer__ = "Damian Kęska"
__copyright__ = "Copyleft by Panthera Desktop Team"

import sys

try:
    import MySQLdb
except ImportError:
    pass
    
try:
    import sqlite3
except ImportError:
    pass
    
try:
    from peewee import *
    import peewee
except ImportError:
    pass

class pantheraDB:
    """
        Database support
    """
    
    panthera = None
    db = None
    cursor = None
    dbType = None

    def __init__(self, panthera):
        """ Initialize connection """
    
        self.panthera = panthera
        
        if not "MySQLdb" in globals() and not "sqlite3" in globals() and not "peewee" in globals():
            self.panthera.logging.output("No MySQL or SQLite3 driver found", "pantheraDB")
            
        # Peewee ORM database
        if self.panthera.config.getKey('databaseType', 'orm') == 'orm':
            if not "peewee" in globals():
                self.panthera.logging.output("Peewee module not found, but orm database type selected", "pantheraDB")
                sys.exit(1)
            
            if self.panthera.config.getKey("databaseSocketType", "sqlite3") == "sqlite3":
                self.db = db = SqliteDatabase(self.panthera.config.getKey('databaseFile', self.panthera.filesDir+"/db.sqlite3"))
                
                class BaseModel(Model):
                    class Meta:
                        database = db
                
                self.BaseModel = BaseModel
                self.dbType = "peewee"
            
        # SQLite3 database
        elif self.panthera.config.getKey('databaseType') == 'sqlite3':
            self.db = sqlite.connect(self.panthera.config.getKey('databaseFile', self.panthera.filesDir+"/db.sqlite3"))
            self.cursor = self.db.cursor()
            self.dbType = "sqlite3"
            
    def query(self, query, values=None):
        """ Execute a raw query """
        
        self.panthera.logging.output(query, "pantheraDB")
    
        if self.dbType == "peewee":
            return self.db.execute_sql(query, values)
            
        elif self.dbType == "sqlite3":
            return pantheraDBSQLite3ResultSet(self.cursor.execute(query, values), self.cursor)
        
class pantheraDBSQLite3ResultSet:
    """ Result set for SQLite3 """

    db = None
    cursor = None

    def __init__(self, cursor, db):
        self.db = db
        self.cursor = cursor
            
        
