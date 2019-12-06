import sqlite3
import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConnectionFileLog(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect('fileLog.db',check_same_thread=False)
    
    def insertFileLog(self, filename:str, path:str,delete:bool,typeFile:str) -> bool:
        cursorObj = self.connection.cursor()
        try:
            cursorObj.execute('INSERT INTO fileLog(name,path,isDelete,type) VALUES(?, ?, ?, ?)', (filename,path,delete,typeFile))
            self.connection.commit()
            cursorObj.close()
            return True
        except Exception as identifier:
            print(identifier)
            self.connection.commit()
            cursorObj.close()
            return False

    def updateDelete(self, name:str):
        cursorObj = self.connection.cursor()
        cursorObj.execute('UPDATE fileLog set isDelete=1 where name="'+name+'";')
        self.connection.commit()
        cursorObj.close()

    def deleteFile(self):
        cursorObj = self.connection.cursor()
        cursorObj.execute("SELECT path,name from fileLog where isdelete > 0")
        result = cursorObj.fetchall()
        for path,name in result:
            print(path + "/" + name)
            if os.path.exists(path + "/" + name):
                os.remove(path + "/" + name)
        cursorObj.execute('DELETE from fileLog where isdelete > 0;')
        self.connection.commit()
        cursorObj.close()
        
    def __del__(self):
        print("close")
        self.connection.close()