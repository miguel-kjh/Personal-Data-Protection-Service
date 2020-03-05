from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import ERROR_RANGE_PERCENTAGE_DB
from app.main.util.fileUtils import isDni

import sqlite3 as lite
import re
from abc import ABC, abstractmethod
from typing import Text
from unidecode import unidecode


def normalizeUnicode(string: str) -> str:
    return unidecode(string)


class PersonalDataSearch(ABC):
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
        for name in normalizeName.replace('-', ' ').replace(',','').split():
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
        pattern = re.compile(r'\d')
        if pattern.search(fullName):
            return False
        
        return self.checkNameInDB(fullName)

    def isDni(self, idCards: str) -> bool:
        with self.nlp.disable_pipes("ner"):
            doc = self.nlp(idCards)
        return len(doc.ents) == 1 and str(doc.ents[0]) == idCards and isDni(idCards)

    @abstractmethod
    def searchPersonalData(self, text: Text) -> tuple:
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
