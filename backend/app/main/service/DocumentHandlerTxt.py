from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.fileUtils import encode

class DocumentHandlerTxt(DocumentHandler):

    def modifyLine(self, line: str, data: list) -> str:
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
                data = []
                data[len(data):] = self.nameSearch.searchPersonalData(line)[0]
                data[len(data):] = self.nameSearch.searchPersonalData(line)[1]
                destiny.writelines(self.modifyLine(line, data))

    def giveListNames(self) -> tuple:
        listNames = []
        idCards = []
        with open(self.path, 'r',encoding='utf8') as file:
            for line in file:
                listNames[len(listNames):] = [name['name'] for name in self.nameSearch.searchPersonalData(line)[0]]
                idCards[len(idCards):] = [idCard['name'] for idCard in self.nameSearch.searchPersonalData(line)[1]]
        return listNames,idCards