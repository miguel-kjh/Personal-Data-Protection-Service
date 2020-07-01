from app.main.service.personalDataSearch import PersonalDataSearch, PersonalData
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

    def _getNames(self, text:Text):
        """
        Gets the names from a text.
        :param text: Text
        :return: list of string
        """

        listNames = []

        for tokenText in sent_tokenize(text.replace('—', ',') ,language='spanish'):
            doc = self.nlp(tokenText)
            listNames[len(listNames):] = self.checkNamesInDB([
                replaceUnnecessaryCharacters(ent.text.strip('\n'))
                for ent in doc.ents if ent.label_ == 'PER'
            ])
        
        return listNames
    
    def _getIdCards(self, text:Text):
        """
        Gets the DNIs from a text.
        :param text: Text
        :return: list of string
        """

        return [
            idCard.group()
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(self.regexIdCards,text)))
        ]

    def searchPersonalData(self, text: Text, personalData:PersonalData = PersonalData.all) -> tuple:
        """
        Obtains personal data from a text.
        :param text: Text
        :param personalData: PersonalData
        :return: tuple(list of string,list of string)
        """

        if personalData == PersonalData.names:
            return (self._getNames(text), [])
        elif personalData == PersonalData.idCards:
            return ([], self._getIdCards(text))
        elif personalData == PersonalData.all:
            return (self._getNames(text), self._getIdCards(text))
