import sqlite3 as lite
from typing import Text
from unidecode import unidecode
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import ERROR_RANGE_PERCENTAGE_DB

def normalizeUnicode(string:str) -> str: 
    return unidecode(string)

class NameSearch():
    def __init__(self, errorRange:float=ERROR_RANGE_PERCENTAGE_DB):
        #spacy.prefer_gpu()
        self.nlp = LanguageBuilder().getlanguage()
        self.errorRange = errorRange
        self.conection = spanishNamesDB()
        self.articules = ["DE", "DEL", "EL", "LOS", "TODOS"]

    def checkNameInDB(self,fullName:str) -> bool:
        countWordsInName = 0
        countWordsInDB = 0
        normalizeName = normalizeUnicode(fullName).upper()
        for name in normalizeName.replace('-', ' ').split():
            if name not in self.articules:
                countWordsInName += 1
                name = name.replace('"','')
                try:
                    sentence = "select (select count(*) from surnames where surnames= '%s') OR" \
                                            " (select count(*) from names  where names='%s');" % (name,name)
                    senteceResult = self.conection.query(sentence)
                    countWordsInDB += 1 if senteceResult.fetchone()[0] == 1  else 0
                except lite.OperationalError as identifier:
                    print(identifier)
        return countWordsInName > 0 and countWordsInDB / countWordsInName > self.errorRange

    def isName(self,fullName:str) -> bool:
        with self.nlp.disable_pipes('parser','ner'):
                doc = self.nlp(fullName)
        if 'VERB' in [token.pos_ for token in doc]:
            return True if len(self.searchNames(fullName,processedText=doc)) > 0 and self.searchNames(fullName,processedText=doc)[0]['name'] == fullName else False
        else:
            return self.checkNameInDB(fullName)

    def searchNames(self,text:Text,processedText=None) -> list:
        pass

    def getErrorRange(self) -> float:
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
