import spacy
from spacy.pipeline import EntityRuler
import sqlite3 as lite
from unidecode import unidecode
from typing import Text

def normalizeUnicode(string:str) -> str: 
    return unidecode(string)

class SearcherNamesTexts():
    
    def __init__(self, nlp,errorRange:float=0.0):
        #spacy.prefer_gpu()
        self.nlp = nlp
        self.errorRange = errorRange
        self.conection = spanishNamesDB()
        pattern = [
            {'POS': 'PROPN', 'OP': '+'},
            {'TEXT': {'REGEX': 'de|el|del|-'}, 'OP': '?'},
            {'POS': 'PROPN', 'OP': '?'}
        ]
        ruler = EntityRuler(self.nlp)
        patterns = [{"label": "PER", "pattern": pattern}]
        ruler.add_patterns(patterns)

    def checkNameInDB(self,fullName:str) -> bool:
        countWordsInName = 0
        countWordsInDB = 0
        normalizeName = normalizeUnicode(fullName).upper()
        for name in normalizeName.replace("-", " ").split():
            if name not in ["DE", "DEL", "EL", "LA"]:
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
        doc = self.nlp(fullName)
        return True if len(doc.ents) == 1 and doc.ents[0].text == fullName and self.checkNameInDB(fullName) else False


    def searchNames(self,text:Text) -> list:
        doc = self.nlp(text)
        listNames = [
            (ent.text,ent.start_char,ent.end_char) for ent in doc.ents if ent.label_ == "PER"
            ]
        listOfDictWithName = []
        for name_complete in listNames:
            if self.checkNameInDB(name_complete[0]):
                listOfDictWithName.append({
                    "name":name_complete[0],
                    "star_char":name_complete[1],
                    "end_char":name_complete[2]
                    })
        return listOfDictWithName

    def getErrorRange(self) -> float:
        return self.errorRange

    def setErrorRange(self, error_range:float):
        self.errorRange = error_range

class spanishNamesDB():

    def __init__(self):
        self._db_connection = lite.connect("spanish_names")
        self._db_cur = self._db_connection.cursor()

    def query(self, query:str):
        return self._db_cur.execute(query)

    def __del__(self):
        self._db_connection.close()


import spacy
if __name__ == "__main__":
    s = SearcherNamesTexts(spacy.load("es_core_news_sm"))
    print(s.searchNames("DELETE FROM SURNAME;"))