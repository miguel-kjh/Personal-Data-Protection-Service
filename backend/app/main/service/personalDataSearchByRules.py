from app.main.service.personalDataSearch import PersonalDataSearch, PersonalData
from app.main.util.fileUtils             import isDni
from app.main.service.languageBuilder    import LanguageBuilder
from app.main.util.fileUtils             import replaceUnnecessaryCharacters

from nltk.tokenize import sent_tokenize
from typing        import Text
import re



class PersonalDataSearchByRules(PersonalDataSearch):

    def __init__(self):
        super().__init__()
        self.label = LanguageBuilder().getLabelNameOfRules()
        self.nlp   = LanguageBuilder().getlanguageByRules()

    def _getNames(self, text:Text):
        listNames = []

        for tokenText in sent_tokenize(text.replace('—', ',') ,language='spanish'):
            doc = self.nlp(tokenText)
            listNames[len(listNames):] = self.checkNamesInDB([
                replaceUnnecessaryCharacters(ent.text.strip('\n'))
                for ent in doc.ents
            ])
        
        return listNames
    
    def _getIdCards(self, text:Text):
        return [
            idCard.group()
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(self.regexIdCards,text)))
        ]

    def searchPersonalData(self, text: Text, personalData:PersonalData = PersonalData.all) -> tuple:
        if personalData == PersonalData.name:
            return (self._getNames(text), [])
        elif personalData == PersonalData.idCards:
            return ([], self._getIdCards(text))
        elif personalData == PersonalData.all:
            return (self._getNames(text), self._getIdCards(text))