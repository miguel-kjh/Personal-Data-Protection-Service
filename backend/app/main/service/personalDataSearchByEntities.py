from app.main.service.personalDataSearch import PersonalDataSearch
from app.main.util.fileUtils             import isDni
from app.main.service.languageBuilder    import LanguageBuilder
from app.main.util.fileUtils             import replaceUnnecessaryCharacters

from nltk.tokenize import sent_tokenize
from typing        import Text
import re



class PersonalDataSearchByEntities(PersonalDataSearch):

    def __init__(self):
        super().__init__()
        self.nlp = LanguageBuilder().getlanguage()

    def searchPersonalData(self, text: Text) -> tuple:
        listNames = []

        for tokenText in sent_tokenize(text.replace('—', ',') ,language='spanish'):
            doc = self.nlp(tokenText)
            listNames[len(listNames):] = self.checkNamesInDB([
                replaceUnnecessaryCharacters(ent.text.strip('\n'))
                for ent in doc.ents if ent.label_ == 'PER'
            ])
        
        idCards = [
            idCard.group()
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(self.regexIdCards,text)))
        ]

        return (listNames,idCards)
