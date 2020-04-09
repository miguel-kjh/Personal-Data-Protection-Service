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
from typing import Text

class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.document = docx.Document(self.path)

    def documentsProcessing(self):
        def updateDocx(regex:str, text:Text) -> Text:
            regexName = re.compile(regex)
            return regexName.sub(lambda match: encode(match.group()), text)
        data              = []
        maxLength         = 4000
        listNames,idCards = self.giveListNames()
        listNames = list(set(listNames))
        listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
        data[len(data):],data[len(data):] = listNames,idCards
        regex = '|'.join(data)
        regexName = re.compile(regex)
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if len(data) > maxLength:
                    intial = 0
                    for numberRange in range(maxLength,len(data),maxLength):
                        block.text = updateDocx('|'.join(data[intial:numberRange]), block.text)
                        intial     = numberRange
                    block.text = updateDocx('|'.join(data[intial:]), block.text)
                else:
                    block.text = regexName.sub(lambda match: encode(match.group()), block.text)
            elif isinstance(block, Table):
                for row in block.rows:
                    for cell in row.cells:
                        if len(data) > maxLength:
                            intial = 0
                            for numberRange in range(maxLength,len(data),maxLength):
                                cell.text = updateDocx('|'.join(data[intial:numberRange]), cell.text)
                                intial = numberRange
                            cell.text = updateDocx('|'.join(data[intial:]), cell.text)
                        else:
                            cell.text = regexName.sub(lambda match: encode(match.group()), cell.text)

            else:
                continue
        self.document.save(self.destiny)

    def giveListNames(self) -> tuple:
        lastKey    = []
        listNames  = []
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
                namePicker = DataPickerInTables()
                for index, row in enumerate(block.rows):
                    rowText = [cell.text for cell in row.cells]
                    if index == 0:
                        lables = list(
                            filter(lambda cell: list(filter(lambda x: LanguageBuilder().semanticSimilarity(cell,x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,listOfVectorWords)), rowText)
                        )
                        key = list(map(lambda cell: rowText.index(cell),lables))
                        if not key:
                            key = lastKey
                            namePicker.addIndexesColumn(key)
                        else:
                            lastKey = key
                            namePicker.addIndexesColumn(key)
                            continue

                    nameRow = list(filter(lambda cell: namePicker.isColumnName(rowText.index(cell)), rowText))
                    for cell in nameRow:
                        namePicker.addName(rowText.index(cell), cell)

                    listIdCard[len(listIdCard):] = list(filter(lambda cell: self.dataSearch.isDni(cell), filter(lambda cell: cell not in nameRow, rowText)))
                    
                listNames[len(listNames):] = namePicker.getAllNames(self.dataSearch.checkNamesInDB,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
            else:
                continue
        return listNames,listIdCard