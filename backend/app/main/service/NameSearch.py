import sqlite3 as lite
from abc import ABC, abstractmethod
from typing import Text
from unidecode import unidecode
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import ERROR_RANGE_PERCENTAGE_DB


def normalizeUnicode(string: str) -> str:
    return unidecode(string)


class NameSearch(ABC):
    def __init__(self, errorRange: float = ERROR_RANGE_PERCENTAGE_DB):
        # spacy.prefer_gpu()
        self.nlp = LanguageBuilder().getlanguage()
        self.errorRange = errorRange
        self.connection = SpanishNamesDB()
        self.keywords = ["DE", "DEL", "EL", "LOS", "TODOS"]

    def checkNameInDB(self, fullName: str) -> bool:
        countWordsInName = 0
        countWordsInDB = 0
        normalizeName = normalizeUnicode(fullName).upper()
        for name in normalizeName.replace('-', ' ').split():
            if name not in self.keywords:
                countWordsInName += 1
                try:
                    sentence = "select (select count(*) from surnames where surnames= '%s') OR" \
                               " (select count(*) from names  where names='%s');" % (name, name)
                    senteceResult = self.connection.query(sentence)
                    countWordsInDB += 1 if senteceResult.fetchone()[0] == 1 else 0
                except lite.OperationalError as identifier:
                    print(identifier)
        return countWordsInName > 0 and countWordsInDB / countWordsInName > self.errorRange

    def isName(self, fullName: str) -> bool:
        doc = self.nlp(fullName)
        if 'VERB' in [token.pos_ for token in doc]:
            return True if len(self.searchNames(fullName, processedText=doc)) > 0 and \
                           self.searchNames(fullName, processedText=doc)[0]['name'] == fullName else False
        else:
            return self.checkNameInDB(fullName)

    @abstractmethod
    def searchNames(self, text: Text, processedText=None) -> list:
        pass


class SpanishNamesDB:

    def __init__(self):
        self.connection = lite.connect("spanish_names")
        self.cursor = self.connection.cursor()

    def query(self, query: str):
        return self.cursor.execute(query)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
