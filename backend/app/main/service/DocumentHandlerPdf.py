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
from collections.abc import Iterable, Iterator


class BufferIterator(Iterator):
    def __init__(self,buffer:list):
        self.buffer = buffer
        self.position = 0

    def __next__(self) -> Text:
        try:
            text = self.buffer[self.position]
            if not text['row']:
                self.position += 1
                return text['text']
            count = 1
            for nextText in self.buffer[self.position:]:
                if not nextText['row']:
                    break
                count += 1
            if count >= 3:
                self.position += count
                text = self.buffer[self.position]
        except IndexError:
            raise StopIteration
        self.position += 1
        return text['text']

class BufferReaderPdf(Iterable):
    def __init__(self):
        self.bufferText = []

    def add(self, text:Text) -> bool:
        self.bufferText.append(
            {
                'text':text,
                'row': not LanguageBuilder().hasContex(text)
            }
        )

    def __iter__(self) -> BufferIterator:
        return BufferIterator(self.bufferText)
    

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
        self.buffer = BufferReaderPdf()

    def getPersonalDataInTables(self, listNames:list):
        keyHeap = []
        for table in tabula.read_pdf(self.path, pages="all", multiple_tables=True):
            #table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
            lastKeys = []

            for key in self.selector.getPossibleColumnsNames(table):
                dfNotNull = table[key][table[key].notnull()]
                countOfName = self.selector.columnSearch(dfNotNull,self.nameSearch.checkNameInDB)
                if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                    listNames[len(listNames):] = dfNotNull
                    lastKeys.append(list(table.keys()).index(key))
            if not lastKeys:
                if not keyHeap:continue
                for indexKey in keyHeap[-1]:
                    try:
                        dataKey = list(table.keys())[indexKey]
                    except IndexError:
                        continue
                    dfNotNull = table[dataKey][table[dataKey].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.nameSearch.checkNameInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames.append(dataKey)
                        listNames[len(listNames):] = dfNotNull
            else:
                keyHeap.append(lastKeys)

    def getPersonalDataInTexts(self, listNames: list):
        
        for text in readPdf(self.path):
            self.buffer.add(text)

        for text in self.buffer:
            doc = self.nameSearch.searchNames(text)
            for entity in doc:
                listNames.append(entity['name'].strip("\n"))

    def giveListNames(self) -> list:
        listNames = []
        self.getPersonalDataInTables(listNames)
        self.getPersonalDataInTexts(listNames)
        return listNames

    def documentsProcessing(self):
        listNames = list(set(self.giveListNames()))
        if not listNames:
            pdf_redactor.redactor(self.options, self.path, self.destiny)
            return
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        regex = '|'.join(listNames)
        pdf_redactor.redactor(self.options, self.path, self.destiny)
        self.options.content_filters = [
            (
                re.compile(regex),
                lambda m: encode(m.group())
            )
        ]
        pdf_redactor.redactor(self.options, self.path, self.destiny)