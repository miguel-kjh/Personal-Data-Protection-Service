from app.main.util.fileUtils import encode, itemIterator
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.service.languageBuilder import LanguageBuilder
from app.main.util.semanticWordLists import listOfVectorWords
from app.main.util.NamePickerInTables import NamePickerInTables
from app.main.service.DocumentHandler import DocumentHandler

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

import re

class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.document = docx.Document(self.path)

    def getPickerData(self, table: Table) -> NamePickerInTables:
        picker = NamePickerInTables()
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
                            picker.addIndexColumn(index)
                    else:
                        if picker.isColumnName(index) and paragraph.text.strip():
                            picker.addName(index, paragraph.text)
                            if self.nameSearch.checkNameInDB(paragraph.text): picker.countRealName(index)
            isLabels = False
        return picker

    def definePicker(self, table: Table, picker: NamePickerInTables):
        for row in table.rows:
            for index, cell in enumerate(row.cells):
                if picker.isColumnName(index):
                    for paragraph in cell.paragraphs:
                        if paragraph.text.strip():
                            picker.addName(index, paragraph.text)
                            if self.nameSearch.checkNameInDB(paragraph.text): picker.countRealName(index)

    def documentsProcessing(self):
        LastIndexesColumn = []
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if LanguageBuilder().hasContex(block.text):
                    listNames = self.nameSearch.searchNames(block.text)
                    for name in listNames:
                        regexName = re.compile(name['name'])
                        text = regexName.sub(encode(name['name']), block.text)
                        block.text = text
                elif self.nameSearch.isName(block.text):
                    regexName = re.compile(block.text.strip())
                    text = regexName.sub(encode(block.text.strip()), block.text)
                    block.text = text
            elif isinstance(block, Table):
                picker = self.getPickerData(block)
                if picker.getIndexesColumn():
                    LastIndexesColumn = picker.getIndexesColumn()
                    initialRow = 1
                elif LastIndexesColumn:
                    picker.addIndexesColumn(LastIndexesColumn)
                    self.definePicker(block, picker)
                    initialRow = 0
                else:
                    continue
                for row in block.rows[initialRow:]:
                    for index, cell in enumerate(row.cells):
                        if picker.isRealColumName(index, MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS):
                            for paragraph in cell.paragraphs:
                                paragraph.text = encode(paragraph.text)
            else:
                continue
        self.document.save(self.destiny)

    def giveListNames(self) -> list:
        LastIndexesColumn = []
        listNames = []
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if LanguageBuilder().hasContex(block.text):
                    listOfMarks = self.nameSearch.searchNames(block.text)
                    if listOfMarks != []:
                        listNames[len(listNames):] = [name['name'] for name in listOfMarks]
                elif self.nameSearch.isName(block.text):
                    listNames.append(block.text.strip())
            elif isinstance(block, Table):
                picker = self.getPickerData(block)
                if picker.getIndexesColumn():
                    LastIndexesColumn = picker.getIndexesColumn()
                elif LastIndexesColumn:
                    picker.addIndexesColumn(LastIndexesColumn)
                    self.definePicker(block, picker)
                else: 
                    continue
                listNames[len(listNames):] = picker.getAllNames(MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
            else:
                continue
        return listNames