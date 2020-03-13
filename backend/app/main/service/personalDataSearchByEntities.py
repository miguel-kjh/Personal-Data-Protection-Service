from typing import Text
from app.main.service.personalDataSearch import PersonalDataSearch
from app.main.util.fileUtils import isDni

import re

class PersonalDataSearchByEntities(PersonalDataSearch):

    def searchPersonalData(self, text: Text) -> tuple:
        doc = self.nlp(text)
        listNames = [
            {"name": ent.text, "star_char": ent.start_char, "end_char": ent.end_char}
            for ent in doc.ents if ent.label_ == 'PER'
        ]
        listNames = self.selectNames(listNames)
        idCards = [
            {"name": idCard.group(), "star_char": idCard.start(), "end_char": idCard.end()}
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(r'\d{2}.?\d{2}.?\d{2}.?\d{2}\s*\w',text)))
        ]
        # print([(ent.text, ent.label_) for ent in doc.ents])
        # print(listNames)
        # listNames = list(
        #    filter(lambda name: self.checkNameInDB(name['name']), listNames)
        #)
        return (listNames,idCards)
