from app.main.service.personalDataSearch import PersonalData
from app.main.service.DocumentHandler    import DocumentHandler
from app.main.service.languageBuilder    import LanguageBuilder
from app.main.util.heuristicMeasures     import MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX

from typing import Text
import re

class DocumentHandlerTxt(DocumentHandler):

    def documentsProcessing(self, personalData: PersonalData = PersonalData.all):
        def updateTxt(regex:str, text:Text) -> Text:
            regexName = re.compile(regex)
            return regexName.sub(lambda match: self.anonymizationFunction(match.group()), text)

        if not self.anonymizationFunction:
            return

        with open(self.path, 'r', encoding='utf8') as file, open(self.outfile, 'w',encoding='utf8') as outfile:
            data              = []
            fileText          = str(file.read())
            maxLength         = MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX
            listNames,idCards = self.extractData(personalData)
            listNames = list(set(listNames))
            listNames.sort(
                    key     = lambda value: len(value),
                    reverse = True
                )
            data[len(data):],data[len(data):] = listNames,idCards
            if len(data) > maxLength:
                intial = 0
                for numberRange in range(maxLength,len(data),maxLength):
                    fileText   = updateTxt('|'.join(data[intial:numberRange]), fileText)
                    intial     = numberRange
                fileText = updateTxt('|'.join(data[intial:]), fileText)
            else:
                fileText = updateTxt('|'.join(data), fileText)
            outfile.write(fileText)
                

                

    def extractData(self, personalData: PersonalData = PersonalData.all) -> tuple:
        listNames = []
        idCards   = []
        with open(self.path, 'r',encoding='utf8') as file:
            for line in file:
                line = line[0:len(line)-1]
                if LanguageBuilder().hasContex(line):
                    listNames[len(listNames):],idCards[len(idCards):] = self.dataSearch.searchPersonalData(line,personalData)
                elif personalData != PersonalData.idCards and self.dataSearch.isName(line):
                    listNames.append(line)
        return listNames,idCards