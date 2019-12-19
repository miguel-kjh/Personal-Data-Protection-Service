from typing import Text
from NameSearch import NameSearch

def lookForNames(doc) -> list:
    c = []
    articules = ["de", "del","-","el","los","todos"]
    for index,token in enumerate(doc):
        if index == 0 or index == len(doc)-1:
            if token.pos_ == "PROPN":
                c.append(True)
            else:
                c.append(False)
        else:
            if token.pos_ == "PROPN":
                c.append(True)
            else:
                if token.text in articules and len(c) > 0 and c[len(c)-1] == True:
                    c.append(True)
                else:
                    c.append(False)
    #print(c)
    listNames = []
    name = ""
    for index,i in enumerate(c):
        #print(name)
        if i:
            name += doc[index].text + " "
            if index == len(c)-1:
                listNames.append(name[:len(name)-1])
        else:
            if index >= 1 and c[index-1]:
                listNames.append(name[:len(name)-1])
            name = ""
    return listNames


class NameSearchByBruteForce(NameSearch):
    def isName(self,fullName:str) -> bool:
        return True if len(self.searchNames(fullName)) > 0 and self.searchNames(fullName)[0]['name'] == fullName else False
    
    def searchNames(self, text:Text)-> list:
        listOfDictWithName = []
        with self.nlp.disable_pipes('parser','ner'):
            doc = self.nlp(text)
        listNames = lookForNames(doc)
        for nameComplete in listNames:
            if self.checkNameInDB(nameComplete):
                localitation = text.find(nameComplete)
                listOfDictWithName.append({
                        "name":nameComplete,
                        "star_char":text.find(nameComplete),
                        "end_char":localitation + len(nameComplete)
                    })
        return listOfDictWithName