from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.fileUtils import encode
from app.main.service.languageBuilder import LanguageBuilder

from typing import Text
import re

class DocumentHandlerTxt(DocumentHandler):

    def modifyLine(self, line: str, data: list) -> str:
        if not data:
            return line
        newLine = ""
        index   = 0
        for ent in data:
            newLine += line[index:ent['star_char']] + encode(ent['name'])
            index    = ent['end_char']
        if index <= len(line) - 1:
            newLine += line[index:]
        return newLine

    def documentsProcessing(self):
        def updateTxt(regex:str, text:Text) -> Text:
            regexName = re.compile(regex)
            return regexName.sub(lambda match: encode(match.group()), text)

        with open(self.path, 'r', encoding='utf8') as file, open(self.destiny, 'w',encoding='utf8') as destiny:
            data              = []
            fileText          = str(file.read())
            maxLength         = 4000
            listNames,idCards = self.giveListNames()
            listNames = list(set(listNames))
            listNames.sort(
                    key=lambda value: len(value),
                    reverse=True
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
            destiny.write(fileText)
                

                

    def giveListNames(self) -> tuple:
        listNames = []
        idCards   = []
        with open(self.path, 'r',encoding='utf8') as file:
            for line in file:
                line = line[0:len(line)-1]
                if LanguageBuilder().hasContex(line):
                    data                       = self.dataSearch.searchPersonalData(line)
                    listNames[len(listNames):] = [name['name'] for name in data[0]]
                    idCards[len(idCards):]     = [idCard['name'] for idCard in data[1]]
                elif self.dataSearch.isName(line):
                    listNames.append(line)
        return listNames,idCards