from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.fileUtils import markInHtml,encode
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.heuristicMeasures import MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS
from app.main.util.semanticWordLists import listOfVectorWords
from app.main.util.dataPickerInTables import DataPickerInTables

import re
import pandas as pd
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from enum import Enum,unique

@unique
class TableToken(Enum):
            NONE = 0
            HEAD = 1
            ROW = 2

class TokenHtml:
        def __init__(self,listOfText:list,isTable:TableToken):
            self.text = listOfText
            self.isTable = isTable

class TokenizerHtml:
    def __init__(self, soup:BeautifulSoup):
        self.soup = soup
        self.blacklist = ['[document]', 'noscript', 'header','style',
                     'html', 'meta', 'head', 'input', 'script', 'link', 
                     'lang', 'code','th', 'td']

    def getToken(self) -> TokenHtml:
        def lookForward(lable,nextLable,expectLable:str) -> bool:
            if nextLable.parent.name == expectLable:
                return True
            return False
        
        lableList = list(filter(lambda lable: lable and lable != "\n", self.soup.find_all(text=True)))
        headList = []
        rowList = []
        for index,lable in enumerate(lableList):
            if lable.parent.name not in self.blacklist:
                headList.clear()
                rowList.clear()
                yield TokenHtml([str(lable)],TableToken.NONE)

            elif lable.parent.name == 'th':
                headList.append(str(lable))
                try:
                    if lookForward(lable,lableList[index+1], 'th'):
                        continue
                    yield TokenHtml(headList,TableToken.HEAD)
                except IndexError:
                    yield TokenHtml(headList,TableToken.HEAD)

            elif lable.parent.name == 'td':
                rowList.append(str(lable))
                try:
                    if lookForward(lable,lableList[index+1], 'td') and len(rowList) < len(headList):
                        continue
                    aux = rowList[:]
                    rowList.clear()
                    yield TokenHtml(aux,TableToken.ROW)
                except IndexError:
                    aux = rowList[:]
                    rowList.clear()
                    yield TokenHtml(aux,TableToken.ROW)

class DocumentHandlerHtml(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        with open(self.path, "r", encoding="utf8") as f:
            self.soup = BeautifulSoup(f.read(), "lxml")

    def locateNames(self, sentence):
        newSentence = ''
        index = 0
        for name in re.finditer(self.regexName,sentence):
            newSentence += sentence[index:name.start()] + markInHtml(name.group())
            index = name.end()
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]

        return newSentence

    def encodeNames(self, sentence):
        newSentence = ""
        index = 0
        for name in re.finditer(self.regexName,sentence):
            newSentence += sentence[index:name.start()] + encode(name.group())
            index = name.end()
        if index <= len(sentence) - 1:
            newSentence += sentence[index:]
        
        return newSentence

    def documentsProcessing(self):
        formatter = HTMLFormatter(self.encodeNames)
        listNames,idCards = self.giveListNames()
        listNames = list(set(listNames))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        data = []
        data[len(data):] = listNames
        data[len(data):] = idCards
        self.regexName = "|".join(data)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))
    
    def documentTagger(self):
        formatter = HTMLFormatter(self.locateNames)
        listNames,idCards = self.giveListNames()
        listNames = list(set(listNames))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        data = []
        data[len(data):] = listNames
        data[len(data):] = idCards
        self.regexName = "|".join(data)
        with open(self.destiny, "w") as f:
            f.write(self.soup.prettify(formatter=formatter))

    def giveListNames(self) -> tuple:
        listNames = []
        idCards = []
        picker = DataPickerInTables()
        tokenizer = TokenizerHtml(self.soup)
        for token in tokenizer.getToken():
            if token.isTable == TableToken.NONE:
                names,cards = self.nameSearch.searchPersonalData(token.text[0])
                listNames[len(listNames):] = [name['name'].replace("\n", "") for name in names]
                idCards[len(idCards):] = [card['name'] for card in cards]
                if not picker.isEmpty():
                    listNames[len(listNames):] = picker.getAllNames(MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
                    picker.clear()
            elif token.isTable == TableToken.HEAD:
                keys = list(filter(lambda text: list(
                        filter(lambda x:LanguageBuilder().semanticSimilarity(text,x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                        listOfVectorWords)), token.text))
                if keys:
                    for key in keys:
                        picker.addIndexColumn(token.text.index(key))
            elif token.isTable == TableToken.ROW:
                for index in picker.getIndexesColumn():
                    picker.addName(index,token.text[index])
                    if self.nameSearch.checkNameInDB(token.text[index]):
                        picker.countRealName(index)
                for index,token in enumerate(token.text):
                    if not index in picker.getIndexesColumn() and self.nameSearch.isDni(token):
                        idCards.append(token)
        return listNames,idCards