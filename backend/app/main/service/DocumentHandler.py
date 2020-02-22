
import pandas as pd


from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from app.main.service.NameSearchByEntities import NameSearchByEntities
from app.main.util.fileUtils import markInHtml,encode


class DocumentHandler:

    def __init__(self, path: str, destiny: str = ""):
        self.path = path
        self.destiny = destiny
        self.nameSearch = NameSearchByEntities()

    def documentsProcessing(self):
        pass

    # def documentTagger(self):
    # pass

    def createFileOfName(self):
        self.createCsv(self.giveListNames())

    def giveListNames(self) -> list:
        pass

    def createCsv(self, listNames: list):
        dataFrame = pd.DataFrame(listNames, columns=['Names'])
        export_csv = dataFrame.to_csv(self.destiny, index=None, header=True)
        print(export_csv)

from deprecated import deprecated

@deprecated(version='1.3.1', reason="This class is deprecated")
class DocumentHandlerHtml(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        with open(self.path, "r", encoding="utf8") as f:
            self.soup = BeautifulSoup(f.read(), "lxml")

    def locateNames(self, sentence):
        listNames = self.nameSearch.searchNames(str(sentence))
        if listNames is []:
            return sentence
        newSentence = ""
        index = 0
        for name in listNames:
            newSentence += sentence[index:name['star_char']] + markInHtml(name['name'])
            index = name['end_char']
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]
        return newSentence

    def encodeNames(self, sentence):
        listNames = self.nameSearch.searchNames(str(sentence))
        if listNames is []:
            return sentence
        newSentence = ""
        index = 0
        for name in listNames:
            newSentence += sentence[index:name['star_char']] + encode(name['name'])
            index = name['end_char']
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]
        return newSentence

    def documentsProcessing(self):
        formatter = HTMLFormatter(self.encodeNames)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))
    
    def documentTagger(self):
        formatter = HTMLFormatter(self.locateNames)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))

    def giveListNames(self):
        listNames = []
        blacklist = ['[document]', 'noscript', 'header',
                     'html', 'meta', 'head', 'input', 'script', 'link', 'lang']
        for lable in self.soup.stripped_strings:
            if lable not in blacklist:
                print(lable)
                listOfMarks = self.nameSearch.searchNames(str(lable))
                listNames[len(listNames):] = [name['name'].replace("\n", "") for name in listOfMarks]
        return listNames
