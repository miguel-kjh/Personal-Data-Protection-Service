from app.main.service.DocumentHandler import DocumentHandler
import app.main.service.pdf_redactor as pdf_redactor
from app.main.util.ColumnSelectorDataframe import ColumnSelectorDataFrame
from app.main.util.fileUtils import encode,readPdf
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.service.languageBuilder import LanguageBuilder

from datetime import datetime
import re
import tabula
from typing import Text
    

class DocumentHandlerPdf(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.options = pdf_redactor.RedactorOptions()
        self.options.metadata_filters = {
            "Title": [lambda value: value],

            "Producer": [lambda value: value],
            "CreationDate": [lambda value: datetime.utcnow()],

            "DEFAULT": [lambda value: None],
        }
        self.options.xmp_filters = [lambda xml: None]
        self.selector = ColumnSelectorDataFrame()

    def getPersonalDataInTables(self, listNames:list, idCards: list):
        keyHeap = []
        for table in tabula.read_pdf(self.path, pages="all", multiple_tables=True):
            #table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
            lastKeys = []

            for typeColumn in self.selector.getPossibleColumnsNames(table):
                if typeColumn.isName:
                    dfNotNull = table[typeColumn.key][table[typeColumn.key].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames[len(listNames):] = dfNotNull
                        lastKeys.append(list(table.keys()).index(typeColumn.key))
                else:
                    if self.dataSearch.isDni(typeColumn.key):
                        idCards.append(typeColumn.key)
                    idCards[len(idCards):] = list(
                        filter(lambda idCards: self.dataSearch.isDni(idCards),table[typeColumn.key][table[typeColumn.key].notnull()])
                    )

            if not lastKeys:
                if not keyHeap:continue
                for indexKey in keyHeap[-1]:
                    try:
                        dataKey = list(table.keys())[indexKey]
                    except IndexError:
                        continue
                    dfNotNull = table[dataKey][table[dataKey].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames.append(dataKey)
                        listNames[len(listNames):] = dfNotNull
            else:
                keyHeap.append(lastKeys)

    def getPersonalDataInTexts(self, listNames: list, idCards: list):

        for text in readPdf(self.path):

            if not LanguageBuilder().hasContex(text):
                listNames[len(listNames):] = list(
                    filter(lambda words: words and self.dataSearch.isName(words), map(lambda words: words.strip(), text.split('\n')))
                )
                continue

            names,cards = self.dataSearch.searchPersonalData(text.replace('\n', ' '))
            for name in names:
                listNames.append(name['name'].strip("\n"))
            for card in cards:
                idCards.append(card['name'])

    def giveListNames(self) -> tuple:
        listNames = []
        idCards = []
        self.getPersonalDataInTables(listNames,idCards)
        self.getPersonalDataInTexts(listNames,idCards)
        return listNames,idCards

    def documentsProcessing(self):
        listNames,idCards = self.giveListNames()
        if not listNames and not idCards:
            pdf_redactor.redactor(self.options, self.path, self.destiny)
            return
        listNames = list(set(listNames))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        data = []
        data[len(data):] = listNames
        data[len(data):] = idCards
        regex = '|'.join(data)
        pdf_redactor.redactor(self.options, self.path, self.destiny)
        self.options.content_filters = [
            (
                re.compile(regex),
                lambda m: encode(m.group())
            )
        ]
        pdf_redactor.redactor(self.options, self.path, self.destiny)