import sqlite3
import os


class ConnectionFileLog:
    """
    Class that establishes a connection to the server's database
    """

    def __init__(self):
        self.connection = sqlite3.connect('app/main/flask_File_main.db')
        self.path = 'storageFiles'

    def deleteFile(self):
        """ 
        Delete the record and allowed files from the database. 
        """

        cursorObj = self.connection.cursor()
        cursorObj.execute("SELECT name from fileLog where isDelete > 0")
        result = cursorObj.fetchall()
        for name in result:
            filename = os.path.join(self.path, name[0])
            print(filename)
            if os.path.exists(filename):
                os.remove(filename)
        cursorObj.execute('DELETE from fileLog where isDelete > 0;')
        self.connection.commit()
        cursorObj.close()

    def updateFile(self):
        """ 
        Updates the record of the files, to allow them to be deleted. 
        """

        cursorObj = self.connection.cursor()
        cursorObj.execute("UPDATE fileLog SET isDelete = 1 where isDelete = 0")
        self.connection.commit()

    def __del__(self):
        """ 
        Delete the database connection.
        """
        
        self.connection.close()


if __name__ == "__main__":
    conn = ConnectionFileLog()
    conn.updateFile()
    conn.deleteFile()
