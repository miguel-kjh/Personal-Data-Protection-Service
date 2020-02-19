from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.fileUtils import encode

class DocumentHandlerTxt(DocumentHandler):

    def modifyLine(self, line: str, listNames: list) -> str:
        newLine = ""
        index = 0
        for name in listNames:
            newLine += line[index:name['star_char']] + encode(name['name'])
            index = name['end_char']
        if index <= len(line) - 1:
            newLine += line[index:]
        return newLine

    def documentsProcessing(self):
        with open(self.path, 'r') as file, open(self.destiny, 'w') as destiny:
            for line in file:
                listNames = self.nameSearch.searchNames(line)
                destiny.writelines(self.modifyLine(line, listNames))

    def giveListNames(self) -> list:
        listNames = []
        with open(self.path, 'r') as file:
            for line in file:
                listNames[len(listNames):] = [name['name'] for name in self.nameSearch.searchNames(line)]
        return listNames