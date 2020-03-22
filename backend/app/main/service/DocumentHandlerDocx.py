from app.main.util.fileUtils import encode, itemIterator
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.semanticWordLists import listOfVectorWords
from app.main.util.dataPickerInTables import DataPickerInTables
from app.main.service.DocumentHandler import DocumentHandler

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

import re

class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.document = docx.Document(self.path)

    def _getPickerData(self, table: Table) -> DataPickerInTables:
        namePicker = DataPickerInTables()
        idCardsPicker = DataPickerInTables()
        isLabels = True
        for row in table.rows:
            for index, cell in enumerate(row.cells):
                for paragraph in cell.paragraphs:
                    if isLabels:
                        labels = list(
                            filter(lambda x: LanguageBuilder().semanticSimilarity(str(paragraph.text),
                                                                                  x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,
                                   listOfVectorWords))
                        if labels:
                            namePicker.addIndexColumn(index)
                        else:
                            idCardsPicker.addIndexColumn(index)
                    else:
                        if namePicker.isColumnName(index) and paragraph.text.strip():
                            namePicker.addName(index, paragraph.text)
            isLabels = False
        return namePicker

    def _defineNamePicker(self, table: Table, picker: DataPickerInTables):
        for row in table.rows:
            for index, cell in enumerate(row.cells):
                if picker.isColumnName(index):
                    for paragraph in cell.paragraphs:
                        if paragraph.text.strip():
                            picker.addName(index, paragraph.text)
    
    def getIdCards(self,table: Table, picker: DataPickerInTables) -> list:
        idCards = []
        for row in table.rows:
            for index, cell in enumerate(row.cells):
                if not picker.isColumnName(index):
                    for paragraph in cell.paragraphs:
                        if self.dataSearch.isDni(paragraph.text):
                            idCards.append(paragraph.text)
        return idCards

    def documentsProcessing(self):
        LastIndexesColumn = []
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if LanguageBuilder().hasContex(block.text):
                    listNames,listIdCards = self.dataSearch.searchPersonalData(block.text)
                    for name in listNames:
                        regexName = re.compile(name['name'])
                        text = regexName.sub(encode(name['name']), block.text)
                        block.text = text
                    for idCard in listIdCards:
                        regexName = re.compile(idCard['name'])
                        text = regexName.sub(encode(idCard['name']), block.text)
                        block.text = text
                elif self.dataSearch.isName(block.text):
                    regexName = re.compile(block.text.strip())
                    text = regexName.sub(encode(block.text.strip()), block.text)
                    block.text = text
                else:
                    _,listIdCards = self.dataSearch.searchPersonalData(block.text)
                    for idCard in listIdCards:
                        regexName = re.compile(idCard['name'])
                        text = regexName.sub(encode(idCard['name']), block.text)
                        block.text = text
            elif isinstance(block, Table):
                picker = self._getPickerData(block)
                if picker.getIndexesColumn():
                    LastIndexesColumn = picker.getIndexesColumn()
                    initialRow = 1
                elif LastIndexesColumn:
                    picker.addIndexesColumn(LastIndexesColumn)
                    self._defineNamePicker(block, picker)
                    initialRow = 0
                else:
                    continue
                for row in block.rows[initialRow:]:
                    for index, cell in enumerate(row.cells):
                        if picker.isRealColumName(self.dataSearch.checkNamesInDB, index, MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS):
                            for paragraph in cell.paragraphs:
                                paragraph.text = encode(paragraph.text)
                        else:
                            for paragraph in cell.paragraphs:
                                if self.dataSearch.isDni(paragraph.text):
                                    paragraph.text = encode(paragraph.text)
            else:
                continue
        self.document.save(self.destiny)

    def giveListNames(self) -> tuple:
        LastIndexesColumn = []
        listNames = []
        listIdCard = []
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if LanguageBuilder().hasContex(block.text):
                    names,idCards = self.dataSearch.searchPersonalData(block.text)
                    if names:
                        listNames[len(listNames):]   = [name['name'] for name in names]
                    if idCards:
                        listIdCard[len(listIdCard):] = [idCard['name'] for idCard in idCards]
                elif self.dataSearch.isName(block.text):
                    listNames.append(block.text.strip())
                else:
                    _,idCards = self.dataSearch.searchPersonalData(block.text)
                    if idCards:
                        listIdCard[len(listIdCard):] = [idCard['name'] for idCard in idCards]
            elif isinstance(block, Table):
                picker = self._getPickerData(block)
                if picker.getIndexesColumn():
                    LastIndexesColumn = picker.getIndexesColumn()
                elif LastIndexesColumn:
                    picker.addIndexesColumn(LastIndexesColumn)
                    self._defineNamePicker(block, picker)
                else: 
                    continue
                listNames[len(listNames):] = picker.getAllNames(self.dataSearch.checkNamesInDB,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
                listIdCard[len(listIdCard):] = self.getIdCards(block,picker)
            else:
                continue
        return listNames,listIdCard