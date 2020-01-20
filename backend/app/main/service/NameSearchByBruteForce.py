from typing import Text
from app.main.service.NameSearch import NameSearch

def lookForNames(doc) -> list:
    c = []
    articules = ["de", "del","-","el","los","todos"]
    for token in doc:
        if token.i == 0 or token.i == len(doc)-1:
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
    count = 0
    isFirstWordOfName = True
    for index,i in enumerate(c):
        if i:
            if isFirstWordOfName:
                isFirstWordOfName = False
                count = doc[index].idx #the first character index    
            name += doc[index].text + " "
            if index == len(c)-1:
                listNames.append(
                    (
                        name[:len(name)-1],
                        count,
                        count+len(name)-1
                    )
                )
        else:
            if index >= 1 and c[index-1]:
                listNames.append(
                    (
                        name[:len(name)-1],
                        count,
                        count+len(name)-1
                    )
                )
            name = ""
            isFirstWordOfName = True
    return listNames


class NameSearchByBruteForce(NameSearch):
    
    def searchNames(self, text:Text, processedText=None)-> list:
        listOfDictWithName = []
        with self.nlp.disable_pipes('parser','ner'): 
            doc = self.nlp(text)
        tabuList = [ ent.text for ent in doc.ents if ent.label_ in ["NORP", "GPE"]]
        listNames = lookForNames(doc)
        for nameComplete in listNames:
            if self.checkNameInDB(nameComplete[0]) and nameComplete not in tabuList:
                listOfDictWithName.append({
                        "name":nameComplete[0],
                        "star_char":nameComplete[1],
                        "end_char":nameComplete[2]
                    })
        return listOfDictWithName
