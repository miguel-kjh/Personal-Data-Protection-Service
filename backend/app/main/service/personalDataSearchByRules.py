from app.main.service.personalDataSearch import PersonalDataSearch
from app.main.util.fileUtils             import isDni
from app.main.service.languageBuilder    import LanguageBuilder

from nltk.tokenize import sent_tokenize
from typing        import Text
import re



class PersonalDataSearchByRules(PersonalDataSearch):

    def __init__(self):
        super().__init__()
        self.label = LanguageBuilder().getLabelNameOfRules()
        self.nlp   = LanguageBuilder().getlanguageByRules()

    def searchPersonalData(self, text: Text) -> tuple:
        listNames = []
        idCards   = []

        for tokenText in sent_tokenize(text.replace('—', ',') ,language='spanish'):
            doc = self.nlp(tokenText)
            listNames[len(listNames):] = self.checkNamesInDB([
                ent.text for ent in doc.ents
            ])
        
        idCards = [
            idCard.group()
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(self.regexIdCards,text)))
        ]
        
        return (listNames,idCards)