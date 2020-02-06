from typing import Text
from app.main.service.NameSearch import NameSearch

def cleanHeadAndTailOfList(listTokens:list):
    for token in reversed(listTokens):
        if token.pos_ == "PROPN": break
        listTokens.remove(token)
    for token in listTokens:
        if token.pos_ == "PROPN": break
        listTokens.remove(token)

def generatorNames(doc, text:Text):
    articules = ["de", "del","-","el","los","todos"]
    listTokens = [token for token in doc if token.pos_ == 'PROPN' or token.text.lower() in articules]
    cleanHeadAndTailOfList(listTokens)
    if listTokens == []: return listTokens
    names = [listTokens[0]]
    count = names[0].idx
    if len(listTokens) == 1 and names[0].pos_ == 'PROPN':
        yield (names,count,count+len(names[0].text))
    else:
        countNames = 0
        for token in listTokens[1:]:
            if token.i == names[countNames].i + 1:
                names.append(token)
                if listTokens[-1] == token:
                    if names[0].pos_ == 'PROPN' and names[-1].pos_ == names[0].pos_:
                        yield (
                            names, 
                            count, 
                            count+sum([ len(n.text) for n in names])+len(names)-1
                        )
                    break    
                countNames += 1
            else:
                if names[0].pos_ == 'PROPN' and names[-1].pos_ == names[0].pos_:
                    yield (
                        names,
                        count,
                        count+sum([ len(n.text) for n in names])+len(names)-1
                    )
                names = []
                names.append(token)
                countNames = 0
                count = token.idx


class NameSearchByGenerator(NameSearch):

    
    def searchNames(self, text:Text, processedText=None)-> list:
        listOfDictWithName = []
        if processedText==None:
            doc = self.nlp(text)
        else:
            doc = processedText
        for token in generatorNames(doc,text):
            wordsName = [i.text for i in token[0]]
            nameComplete = " ".join(wordsName)
            if self.checkNameInDB(nameComplete):
                listOfDictWithName.append({
                        "name":nameComplete,
                        "star_char":token[1],
                        "end_char":token[2]
                    })
        return listOfDictWithName
