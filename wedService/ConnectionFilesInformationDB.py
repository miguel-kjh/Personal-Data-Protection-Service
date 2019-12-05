import sqlite3

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConnectionFilesInformation(metaclass=Singleton):
    def __init__(self):
        #check_same_thread=False
        self.connection = sqlite3.connect('filesInformation.db')
        self.cursorObj = self.connection.cursor()
    
    def insertDataFiles(self, filename:str, path:str,delete:bool,typeFile:str):
        try:
            self.cursorObj.execute('INSERT INTO filesInformation(name,path,isDelete,type) VALUES(?, ?, ?, ?)', (filename,path,delete,typeFile))
            sentence = 'select max(id) from filesInformation where name="'+ filename +'";'
            self.cursorObj.execute(sentence)
            obj = self.cursorObj.fetchall()[0]
            self.connection.commit()
            return obj[0]
        except Exception as identifier:
            print(identifier)
            return False

    def sql_update_rate_null(self, row):
        self.cursorObj.execute('UPDATE rate set fail=null, success=NULL where conversation="'+row+'";')
        self.connection.commit()

    def sql_delete_table(self,name:str):
        self.sql_update_rate_null(name)
        self.cursorObj.execute("DELETE FROM "+name+";")
        self.connection.commit()

    def sql_insert_rate(self,fail,success,name):
        self.cursorObj.execute('UPDATE rate set fail=?, success=? where conversation="'+name+'";', (fail,success))
        self.connection.commit()

    def __del__(self):
        print("close")
        self.connection.close()