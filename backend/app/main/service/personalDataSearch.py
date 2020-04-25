from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures  import ERROR_RANGE_PERCENTAGE_DB
from app.main.util.fileUtils          import isDni,normalizeUnicode,generateWordsAsString

from abc       import ABC, abstractmethod
from typing    import Text
from itertools import chain
import sqlite3 as lite
import re

class PersonalDataSearch(ABC):
    def __init__(self):
        self.keywords     = ["DE", "DEL", "EL", "LOS", "TODOS", "Y"]
        self.errorRange   = ERROR_RANGE_PERCENTAGE_DB
        self.connection   = SpanishNamesDB()
        self.regexIdCards = r'\d{2}([\.-]?|\s*)\d{2}([\.-]?|\s*)\d{2}([\.-]?|\s*)\d{2}\s*\w'

    def _convertName(self,name:str) -> list:
        normalizeName = normalizeUnicode(str(name)).upper()
        words         = list(
            filter(
                lambda n: n not in self.keywords, normalizeName.replace('-', ' ').replace(',','').replace('\'','').split()
                )
            )
        return words

    def _checkNameInSubset(self,name:list, nameSubset:list) -> bool:
        if not name: return False
        namesFound = list(filter(lambda n: n in nameSubset, name))
        return len(namesFound)/len(name) > self.errorRange


    def checkNamesInDB(self, names:list) -> list:
        listNames = list(map(lambda x: self._convertName(x), names))
        words     = list(chain.from_iterable(listNames))
        if not words: return []
        nameSubset = []
        
        for strName in generateWordsAsString(list(set(words))):
            try:
                sentence                     = "select distinct names from names where names in %s;" % (strName)
                senteceResult                = self.connection.query(sentence)
                nameSubset[len(nameSubset):] = [queryResult[0] for queryResult in senteceResult.fetchall()]
                sentence                     = "select distinct surnames from surnames where surnames in %s;" % (strName)
                senteceResult                = self.connection.query(sentence)
                nameSubset[len(nameSubset):] = [queryResult[0] for queryResult in senteceResult.fetchall()]
            except lite.OperationalError as identifier:
                print(identifier)

        finalNames = list(
            filter(
                lambda name: self._checkNameInSubset(name,nameSubset), listNames
            )
        )
        return [names[listNames.index(strName)] for strName in finalNames]

    def checkNameInDB(self, fullName: str) -> bool:
        countWordsInName = 0
        countWordsInDB   = 0
        normalizeName    = normalizeUnicode(fullName).upper()

        for name in normalizeName.replace('-', ' ').replace(',','').split():
            if name not in self.keywords:
                countWordsInName += 1
                try:
                    sentence        = "select (select count(*) from surnames where surnames= '%s') OR" \
                                      " (select count(*) from names  where names='%s');" % (name, name)
                    senteceResult   = self.connection.query(sentence)
                    countWordsInDB += 1 if senteceResult.fetchone()[0] == 1 else 0
                except lite.OperationalError as identifier:
                    print(identifier)

        return countWordsInName > 0 and countWordsInDB / countWordsInName > self.errorRange

    def isName(self, fullName: str) -> bool:
        pattern = re.compile(r'\d')
        if pattern.search(fullName):
            return False
        
        return self.checkNameInDB(fullName)

    def selectNames(self, names: list) -> list:
        selectedNames = self.checkNamesInDB([name['name'] for name in names])
        return list(
            filter(
                lambda name: name['name'] in selectedNames,names
            )
        )

    def giveIdCards(self, string: str) -> list:
        match = map(
                lambda x: x.group(), re.finditer(self.regexIdCards,str(string))
            )
        return list(filter(lambda idCard: isDni(idCard), match))

    @abstractmethod
    def searchPersonalData(self, text: Text) -> tuple:
        pass


class SpanishNamesDB:

    def __init__(self):
        self.connection = lite.connect("spanish_names")
        self.cursor     = self.connection.cursor()

    def query(self, query: str):
        return self.cursor.execute(query)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
