from typing import Text
from app.main.service.personalDataSearch import PersonalDataSearch
from app.main.util.fileUtils import isDni

class PersonalDataSearchByEntities(PersonalDataSearch):

    def searchPersonalData(self, text: Text) -> tuple:
        doc = self.nlp(text)
        listNames = [
            {"name": ent.text, "star_char": ent.start_char, "end_char": ent.end_char}
            for ent in doc.ents if ent.label_ == 'PER' and self.checkNameInDB(ent.text)
        ]
        listDNI = [
            {"name": ent.text, "star_char": ent.start_char, "end_char": ent.end_char}
            for ent in doc.ents if ent.label_ in ['BROKEN_DNI','DNI'] and isDni(ent.text)
        ]
        # print([(ent.text, ent.label_) for ent in doc.ents])
        # print(listNames)
        # listNames = list(
        #    filter(lambda name: self.checkNameInDB(name['name']), listNames)
        #)
        return (listNames,listDNI)
