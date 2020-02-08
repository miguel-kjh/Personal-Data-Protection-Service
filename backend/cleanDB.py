import sqlite3
import os


class ConnectionFileLog:
    def __init__(self):
        self.connection = sqlite3.connect('app/main/flask_File_main.db')
        self.path = 'storageFiles'

    def deleteFile(self):
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

    def __del__(self):
        print("close")
        self.connection.close()


if __name__ == "__main__":
    ConnectionFileLog().deleteFile()
