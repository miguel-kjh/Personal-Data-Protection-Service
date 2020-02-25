from deprecated import deprecated
from app.main.service.DocumentHandler import DocumentHandler
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from app.main.util.fileUtils import markInHtml,encode
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS
from app.main.util.semanticWordLists import listOfVectorWords
from app.main.util.NamePickerInTables import NamePickerInTables

import pandas as pd
import re


@deprecated(version='1.3.1', reason="This class is deprecated")
class DocumentHandlerHtml(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        with open(self.path, "r", encoding="utf8") as f:
            self.soup = BeautifulSoup(f.read(), "lxml")

    def locateNames(self, sentence):
        newSentence = ""
        index = 0
        for name in re.finditer(self.regexData,sentence):
            newSentence += sentence[index:name.start()] + markInHtml(name.group())
            index = name.end()
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]
        return newSentence

    def encodeNames(self, sentence):
        newSentence = ""
        index = 0
        for name in re.finditer(self.regexData,sentence):
            newSentence += sentence[index:name.start()] + encode(name.group())
            index = name.end()
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]
        return newSentence

    def documentsProcessing(self):
        formatter = HTMLFormatter(self.encodeNames)
        listNames = list(set(self.giveListNames()))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        self.regexData = "|".join(listNames)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))
    
    def documentTagger(self):
        formatter = HTMLFormatter(self.locateNames)
        listNames = list(set(self.giveListNames()))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        self.regexData = "|".join(listNames)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))

    def giveListNames(self):
        listNames = []
        indexNameColums = 0
        indexColums = 0
        isTable = True
        blacklist = ['[document]', 'noscript', 'header','style',
                     'html', 'meta', 'head', 'input', 'script', 'link', 
                     'lang', 'code','th', 'td']
        picker = NamePickerInTables()
        for lable in self.soup.find_all(text=True):
            if lable.parent.name not in blacklist:
                listOfMarks = self.nameSearch.searchNames(str(lable))
                listNames[len(listNames):] = [name['name'].replace("\n", "") for name in listOfMarks]
            elif lable.parent.name == 'th':
                if(isTable):
                    #print("Encabezado")
                    isTable = False
                    indexNameColums = 0
                labels = list(
                            filter(lambda x: 
                            LanguageBuilder().semanticSimilarity(str(lable),x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                            listOfVectorWords))
                if labels:
                    picker.addIndexColumn(indexNameColums)
                indexNameColums += 1
                indexColums = 0
                #print(indexNameColums)
            elif lable.parent.name == 'td':
                if(not isTable):
                    isTable = True
                    #print("columnas")
                if indexColums in picker.getIndexesColumn():
                    picker.addName(indexColums,lable)
                    if self.nameSearch.checkNameInDB(lable):
                        picker.countRealName(indexColums)
                indexColums += 1
                #print("Columan donde estamos",indexColums)
                #print("Número de columnas",indexNameColums)
                if indexColums == indexNameColums:
                    indexColums = 0
        listNames[len(listNames):] = picker.getAllNames(MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
        return listNames