from app.main.service.DocumentHandler import DocumentHandler
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import tabula
import app.main.service.pdf_redactor as pdf_redactor
from app.main.util.ColumnSelectorDataframe import ColumnSelectorDataFrame
from app.main.util.fileUtils import encode
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.service.languageBuilder import LanguageBuilder

from datetime import datetime
import re
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
                    except IndexError as identifier:
                        print(identifier)
                        continue
                    dfNotNull = table[dataKey][table[dataKey].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.nameSearch.checkNameInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames.append(dataKey)
                        listNames[len(listNames):] = dfNotNull
            else:
                keyHeap.append(lastKeys)

    def getPersonalDataInTexts(self, listNames: list):
        fp = open(self.path, 'rb')
        parser = PDFParser(fp)
        fp.close()
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    #for text in lt_obj.get_text().split("\n"):
                    text = lt_obj.get_text()
                    if text:
                        self.buffer.add(text)
                        #print(text)
                        #print("--------------------------")
                        #doc = self.nameSearch.searchNames(text)
                        #for entity in doc:
                            #listNames.append(entity['name'].strip("\n"))
        for text in self.buffer:
            print(text)
            print("--------------------------")
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