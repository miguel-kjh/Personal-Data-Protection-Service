from typing import Text
from app.main.service.NameSearch import NameSearch


class NameSearchByEntities(NameSearch):

    def searchNames(self, text: Text, processedText=None) -> list:
        doc = self.nlp(text)
        listNames = [
            (ent.text, ent.start_char, ent.end_char) for ent in doc.ents if ent.label_ == 'PER'
        ]
        # print([(ent.text, ent.label_) for ent in doc.ents])
        # print(listNames)
        listOfDictWithName = []
        for name_complete in listNames:
            if self.checkNameInDB(name_complete[0]):
                listOfDictWithName.append({
                    "name": name_complete[0],
                    "star_char": name_complete[1],
                    "end_char": name_complete[2]
                })
        return listOfDictWithName
