import sqlite3 as lite
from typing import Text
from utils import normalizeUnicode,generatorNames

class SearcherNamesTexts():
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

    def setErrorRange(self):
        return self.errorRange
    

class SearcherNamesLikeEntities(SearcherNamesTexts):
    def isName(self,fullName:str) -> bool:
        doc = self.nlp(fullName)
        return True if len(doc.ents) == 1 and doc.ents[0].text == fullName and self.checkNameInDB(fullName) else False

    def searchNames(self,text:Text) -> list:
        doc = self.nlp(text)
        listNames = [
            (ent.text,ent.start_char,ent.end_char) for ent in doc.ents if ent.label_ == "PER"
            ]
        #print([(token.text, token.pos_, token.dep_) for token in doc])
        #print(listNames)
        listOfDictWithName = []
        for name_complete in listNames:
            if self.checkNameInDB(name_complete[0]):
                listOfDictWithName.append({
                        "name":name_complete[0],
                        "star_char":name_complete[1],
                        "end_char":name_complete[2]
                    })
        return listOfDictWithName

class SearcherNamesProcedure(SearcherNamesTexts):

    def isName(self,fullName:str) -> bool:
        return True if len(self.searchNames(fullName)) > 0 and self.searchNames(fullName)[0]['name'] == fullName else False
    
    def searchNames(self, text:Text)-> list:
        listOfDictWithName = []
        for token in generatorNames(self.nlp,text):
            wordsName = [i[1].text for i in token]
            nameComplete = " ".join(wordsName)
            if self.checkNameInDB(nameComplete):
                listOfDictWithName.append({
                        "name":nameComplete,
                        "star_char":text.find(wordsName[0]),
                        "end_char":text.find(wordsName[-1]) + len(wordsName[-1])
                    })
        return listOfDictWithName

    

class spanishNamesDB():

    def __init__(self):
        self._db_connection = lite.connect("spanish_names")
        self._db_cur = self._db_connection.cursor()

    def query(self, query:str):
        return self._db_cur.execute(query)

    def __del__(self):
        self._db_connection.close()

from languageBuilder import languageBuilder
if __name__ == "__main__":
    nlp = languageBuilder().getlanguage()
    s = SearcherNamesProcedure(nlp)
    #print("Nombres finales 1", s.searchNames("CAROLINA BENITEZ del ROSARIO y juez Daniel Rosas"))
    #print("Nombres finales 2", s.searchNames("Noelia Real Giménez"))
    #print("Nombres finales 3", s.searchNames("La señorita Maria Baute"))
    #print("Nombres finales 3", s.searchNames("La señorita Maria Baute"))
    #print("Nombres finales 4", s.searchNames("Miguel de Montes de Oca estuvo aquí hace dos minutos"))
    print("Nombres finales 5", s.searchNames("Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea: "
                + "Laura Vega, "
                + "Juan Sebastian Ramírez y "
                + "Joseph Stetter."))
