import sqlite3 as lite
from typing import Text
from unidecode import unidecode

def normalizeUnicode(string:str) -> str: 
    return unidecode(string)

class NameSearch():
    def __init__(self, nlp,errorRange:float=0.0):
        #spacy.prefer_gpu()
        self.nlp = nlp
        self.errorRange = errorRange
        self.conection = spanishNamesDB()
        self.articules = ["DE", "DEL", "EL", "LOS", "TODOS"]

    def checkNameInDB(self,fullName:str) -> bool:
        countWordsInName = 0
        countWordsInDB = 0
        normalizeName = normalizeUnicode(fullName).upper()
        for name in normalizeName.replace("-", " ").split():
            if name not in self.articules:
                countWordsInName += 1
                try:
                    sentence = "select (select count(*) from surnames where surnames= '"+ name +"') OR" \
                                            " (select count(*) from names  where names='" + name + "');"
                    senteceResult = self.conection.query(sentence)
                    countWordsInDB += 1 if senteceResult.fetchone()[0] == 1  else 0
                except lite.OperationalError as identifier:
                    print(identifier)
        return countWordsInName > 0 and countWordsInDB * 100 / countWordsInName > self.errorRange

    def isName(self,fullName:str) -> bool:
        pass

    def searchNames(self,text:Text) -> list:
        pass

    def getErrorRange(self):
        return self.errorRange

class spanishNamesDB():

    def __init__(self):
        self._db_connection = lite.connect("spanish_names")
        self._db_cur = self._db_connection.cursor()

    def query(self, query:str):
        return self._db_cur.execute(query)

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()
