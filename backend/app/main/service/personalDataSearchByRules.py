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
        nextLen   = 0

        for tokenText in sent_tokenize(text.replace('—', ',') ,language='spanish'):
            doc = self.nlp(tokenText)
            listNames[len(listNames):] = self.selectNames([
                {"name": ent.text, "star_char": ent.start_char+nextLen, "end_char": ent.end_char+nextLen}
                for ent in doc.ents if ent.label_ == self.label
            ])
            nextLen += len(tokenText) + 1
        
        idCards = [
            {"name": idCard.group(), "star_char": idCard.start(), "end_char": idCard.end()}
            for idCard in list(filter(lambda x: isDni(x.group()) , re.finditer(self.regexIdCards,text)))
        ]
        
        return (listNames,idCards)