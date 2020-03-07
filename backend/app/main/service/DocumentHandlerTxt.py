from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.fileUtils import encode
from app.main.service.languageBuilder import LanguageBuilder

class DocumentHandlerTxt(DocumentHandler):

    def modifyLine(self, line: str, data: list) -> str:
        if not data:
            return line
        newLine = ""
        index = 0
        for ent in data:
            newLine += line[index:ent['star_char']] + encode(ent['name'])
            index = ent['end_char']
        if index <= len(line) - 1:
            newLine += line[index:]
        return newLine

    def documentsProcessing(self):
        with open(self.path, 'r', encoding='utf8') as file, open(self.destiny, 'w',encoding='utf8') as destiny:
            for line in file:

                if LanguageBuilder().hasContex(line):
                    data = []
                    data[len(data):] = self.dataSearch.searchPersonalData(line)[0]
                    data[len(data):] = self.dataSearch.searchPersonalData(line)[1]
                    destiny.writelines(self.modifyLine(line, data))
                    continue

                if self.dataSearch.checkNameInDB(line):
                    line = encode(line)

                _,idCards = self.dataSearch.searchPersonalData(line)
                destiny.writelines(self.modifyLine(line, idCards))

                

    def giveListNames(self) -> tuple:
        listNames = []
        idCards = []
        with open(self.path, 'r',encoding='utf8') as file:
            for line in file:
                if LanguageBuilder().hasContex(line):
                    listNames[len(listNames):] = [name['name'] for name in self.dataSearch.searchPersonalData(line)[0]]
                    idCards[len(idCards):]     = [idCard['name'] for idCard in self.dataSearch.searchPersonalData(line)[1]]
                    continue

                if self.dataSearch.checkNameInDB(line):
                    listNames.append(line[0:len(line) - 1])
                    continue

                idCards[len(idCards):] = [idCard['name'] for idCard in self.dataSearch.searchPersonalData(line)[1]]
        return listNames,idCards