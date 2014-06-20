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
        
        # Create some default configuration keys
        self.panthera.config.getKey('databaseHost', 'localhost')
        self.panthera.config.getKey('databasePassword', '')
        self.panthera.config.getKey('databaseUser', 'root')
        self.panthera.config.getKey('databaseDB', 'my-database')
        self.panthera.config.getKey('databaseFile', self.panthera.filesDir+"/db.sqlite3")
        
        
        if not "MySQLdb" in globals() and not "sqlite3" in globals() and not "peewee" in globals():
            self.panthera.logging.output("No MySQL or SQLite3 driver found", "pantheraDB")
            sys.exit(1)
            
        try:
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
                self.db = sqlite3.connect(self.panthera.config.getKey('databaseFile'))
                self.db.row_factory = dict_factory
                self.cursor = self.db.cursor()
                self.dbType = "sqlite3"
                
            elif self.panthera.config.getKey('databaseType') == 'mysql':
                self.db = MySQLdb.connect(
                    host=self.panthera.config.getKey('databaseHost'),
                    user=self.panthera.config.getKey('databaseUser'),
                    passwd=self.panthera.config.getKey('databasePassword'),
                    db=self.panthera.config.getKey('databaseDB')
                )
                
                self.cursor = self.db.cursor()
                self.dbType = "mysql"
                
            self.panthera.logging.output("Connection estabilished using "+self.dbType+" socket", "pantheraDB")
        except Exception as e:
            self.panthera.logging.output("Cannot connect to database: "+str(e), "pantheraDB")
            sys.exit(1)
            
    def query(self, query, values=dict()):
        """ Execute a raw query """
        
        self.panthera.logging.output(query, "pantheraDB")
        
        if self.dbType == "peewee":
            return self.db.execute_sql(query)
            
        elif self.dbType == "sqlite3":
            return pantheraDBSQLite3ResultSet(self.cursor.execute(query), self.cursor)
        
class pantheraDBSQLite3ResultSet:
    """ Result set for SQLite3 """

    db = None
    cursor = None
    lastrowid = None
    indexColumn = None

    def __init__(self, cursor, db):
        self.db = db
        self.cursor = cursor
        self.lastrowid = cursor.lastrowid
        
    def indexColumn(self, columnName):
        """ Column to index by """
    
        self.indexColumn = columnName
        return self
        
    def rowCount(self):
        """ Count affected/selected rows """
    
        rowCount = self.cursor.rowcount
        
        if rowCount < 0:
            rowCount = 0
        
        return rowCount
        
    def fetchAll(self):
        """ Fetch all rows """
    
        f = self.cursor.fetchall()
        
        if self.indexColumn is not None and len(f) > 0 and f[0].has_key(self.indexColumn):
            newArray = dict()
        
            for row in f:
                newArray[row[self.indexColumn]] = row
                
            f = newArray
    
        return f
        
    def fetch(self):
        """ Fetch one row """
    
        return self.cursor.fetchone()
        
def dict_factory(cursor, row):
    """ Dictionary factory for SQLite3 """

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
