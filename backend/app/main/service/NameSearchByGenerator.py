from typing import Text
from app.main.service.NameSearch import NameSearch

def cleanHeadAndTailOfList(listTokens:list):
    for token in reversed(listTokens):
        if token[1].pos_ == "PROPN": break
        listTokens.remove(token)
    for token in listTokens:
        if token[1].pos_ == "PROPN": break
        listTokens.remove(token)

def generatorNames(nlp, text:Text):
    with nlp.disable_pipes('parser','ner'):
        doc = nlp(text)
        articules = ["de", "del","-","el","los","todos"]
        listTokens = [(index,token) for index,token in enumerate(doc) if token.pos_ == 'PROPN' or token.text.lower() in articules]
        cleanHeadAndTailOfList(listTokens)
        if listTokens == []: return listTokens
        names = [listTokens[0]]
        if len(listTokens) == 1 and names[0][1].pos_ == 'PROPN':
            yield names
        else:
            countNames = 0
            for token in listTokens[1:]:
                if token[0] == names[countNames][0] + 1:
                    names.append(token)
                    if listTokens[-1] == token:
                        if names[0][1].pos_ == 'PROPN' and names[-1][1].pos_ == names[0][1].pos_:
                            yield names
                        break    
                    countNames += 1
                else:
                    if names[0][1].pos_ == 'PROPN' and names[-1][1].pos_ == names[0][1].pos_:
                        yield names
                    names = []
                    names.append(token)
                    countNames = 0


class NameSearchByGenerator(NameSearch):

    def isName(self,fullName:str) -> bool:
        return True if len(self.searchNames(fullName)) > 0 and self.searchNames(fullName)[0]['name'] == fullName else False
    
    def searchNames(self, text:Text)-> list:
        listOfDictWithName = []
        for token in generatorNames(self.nlp,text):
            wordsName = [i[1].text for i in token]
            nameComplete = " ".join(wordsName)
            if self.checkNameInDB(nameComplete):
                localitation = text.find(nameComplete)
                listOfDictWithName.append({
                        "name":nameComplete,
                        "star_char":text.find(nameComplete),
                        "end_char":localitation + len(nameComplete)
                    })
        return listOfDictWithName
