from typing import Text
from app.main.service.personalDataSearch import PersonalDataSearch
from app.main.util.fileUtils import isDni
from app.main.util.heuristicMeasures import ERROR_RANGE_PERCENTAGE_DB
from app.main.service.languageBuilder import LanguageBuilder

import re
from nltk.tokenize import sent_tokenize



class PersonalDataSearchByRules(PersonalDataSearch):

    def __init__(self, errorRange: float = ERROR_RANGE_PERCENTAGE_DB):
        super().__init__(errorRange=errorRange,namesByRules=True)
        self.label = LanguageBuilder().getLabelNameOfRules()
        

    def searchPersonalData(self, text: Text) -> tuple:
        listNames = []
        idCards   = []
        nextLen   = 0
        with self.nlp.disable_pipes("ner"):
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