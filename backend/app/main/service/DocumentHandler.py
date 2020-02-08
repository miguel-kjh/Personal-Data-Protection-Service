import re
from datetime import datetime

import pandas as pd

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import app.main.service.pdf_redactor as pdf_redactor

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from app.main.util.fileUtils import encode, itemIterator, markInHtml
from app.main.service.NameSearchByEntities import NameSearchByEntities
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.semanticWordLists import listOfVectorWords
from app.main.service.NamePickerInTables import NamePickerInTables


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


# TODO? optimize
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

    def giveListNames(self) -> list:
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
        listNames = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    for text in lt_obj.get_text().split("\n"):
                        if text != '':
                            doc = self.nameSearch.searchNames(text)
                            for e in doc:
                                listNames.append(e['name'].strip("\n"))
        return list(set(listNames))

    def documentsProcessing(self):
        listNames = self.giveListNames()
        # print(listNames[:])
        if len(listNames) > 0:
            listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
            self.options.content_filters = [
                (
                    re.compile(listNames[0]),
                    lambda m: encode(listNames[0]).upper()
                )
            ]
            pdf_redactor.redactor(self.options, self.path, self.destiny)
            for name in listNames[1:]:
                self.options.content_filters = [
                    (
                        re.compile(name),
                        lambda m: encode(name).upper()
                    )
                ]
                pdf_redactor.redactor(self.options, self.destiny, self.destiny)


class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.document = docx.Document(self.path)

    def getNameOfTable(self, table: Table) -> NamePickerInTables:
        picker = NamePickerInTables()
        isLables = True
        for row in table.rows:
            for index, cell in enumerate(row.cells):
                for paragraph in cell.paragraphs:
                    if isLables:
                        listOfWordSemantics = list(
                            filter(lambda x: LanguageBuilder().semanticSimilarity(str(paragraph.text),
                                                                                  x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                                   listOfVectorWords))
                        if listOfWordSemantics != []:
                            picker.addIndexColumn(index)
                    else:
                        if picker.isColumnName(index) and bool(paragraph.text.strip()):
                            picker.addName(index, paragraph.text)
                            if self.nameSearch.isName(paragraph.text): picker.countRealName(index)
            isLables = False
        return picker

    def documentsProcessing(self):
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                listNames = self.nameSearch.searchNames(block.text)
                for name in listNames:
                    regexName = re.compile(name['name'])
                    text = regexName.sub(encode(name['name']), block.text)
                    block.text = text
            elif isinstance(block, Table):
                picker = self.getNameOfTable(block)
                if picker:
                    for row in block.rows[1:]:
                        for index, cell in enumerate(row.cells):
                            if picker.isRealColumName(index, MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS):
                                for paragraph in cell.paragraphs:
                                    paragraph.text = encode(paragraph.text)
            else:
                continue
        self.document.save(self.destiny)

    def giveListNames(self) -> list:
        doc = docx.Document(self.path)
        listNames = []
        for block in itemIterator(doc):
            if isinstance(block, Paragraph):
                listOfMarks = self.nameSearch.searchNames(block.text)
                if listOfMarks != []:
                    listNames[len(listNames):] = [name['name'] for name in listOfMarks]
            elif isinstance(block, Table):
                listNames[len(listNames):] = self.getNameOfTable(block).getAllNames(MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
            else:
                continue
        return listNames


class DocumentHandlerExcel(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.df = pd.read_excel(path)

    def getPossibleColumnsNames(self):
        for key, typeColumn in zip(self.df.keys(), self.df.dtypes):
            if typeColumn == object:
                listOfWordSemantics = list(
                    filter(
                        lambda x: LanguageBuilder().semanticSimilarity(key, x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                        listOfVectorWords))
                if listOfWordSemantics != []:
                    yield key

    def documentsProcessing(self):
        for key in self.getPossibleColumnsNames():
            #print(key)
            dfNotNull = self.df[key][self.df[key].notnull()]
            countOfName = sum(list(map(lambda x: self.nameSearch.isName(str(x)), dfNotNull)))
            if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                self.df[key].replace({str(name): encode(str(name)) for name in dfNotNull}, inplace=True)
        self.df.to_excel(self.destiny, index=False)

    def giveListNames(self) -> list:
        listNames = []
        for key in self.getPossibleColumnsNames():
            #print(key)
            dfNotNull = self.df[key][self.df[key].notnull()]
            countOfName = sum(list(map(lambda x: self.nameSearch.isName(str(x)), dfNotNull)))
            if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                listNames[len(listNames):] = dfNotNull
        return listNames


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
        print(sentence)
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
                # print(lable)
                listOfMarks = self.nameSearch.searchNames(str(lable))
                listNames[len(listNames):] = [name['name'].replace("\n", "") for name in listOfMarks]
        return listNames


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
