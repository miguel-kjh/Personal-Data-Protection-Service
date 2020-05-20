from app.main.util.fileUtils           import itemIterator
from app.main.util.heuristicMeasures   import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES, MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX
from app.main.service.languageBuilder  import LanguageBuilder
from app.main.util.semanticWordLists   import listOfVectorWords
from app.main.util.dataPickerInTables  import DataPickerInTables
from app.main.service.DocumentHandler  import DocumentHandler

import docx
from docx.text.paragraph import Paragraph
from docx.table          import Table

import re
import itertools
from typing import Text


class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path: str, outfile: str = "", anonymizationFunction = None):
        super().__init__(path, outfile=outfile, anonymizationFunction=anonymizationFunction)
        self.document = docx.Document(self.path)

    def documentsProcessing(self):
        def updateDocx(regex:str, text:Text) -> Text:
            regexName = re.compile(regex)
            return regexName.sub(lambda match: self.anonymizationFunction(match.group()), text)

        if not self.anonymizationFunction:
            return
            
        data              = []
        maxLength         = MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX
        listNames,idCards = self.extractData()
        listNames         = list(set(listNames))
        listNames.sort(
                key     = lambda value: len(value),
                reverse = True
            )
        data[len(data):],data[len(data):] = listNames,idCards
        theExpressionShouldBeTrodden      = True

        if len(data) <= maxLength:
            theExpressionShouldBeTrodden = False
            regex     = '|'.join(data)
            regexName = re.compile(regex)

        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if theExpressionShouldBeTrodden:
                    intial = 0
                    for numberRange in range(maxLength,len(data),maxLength):
                        block.text = updateDocx('|'.join(data[intial:numberRange]), block.text)
                        intial     = numberRange
                    block.text = updateDocx('|'.join(data[intial:]), block.text)
                else:
                    block.text = regexName.sub(lambda match: self.anonymizationFunction(match.group()), block.text)
            elif isinstance(block, Table):
                for row in block.rows:
                    for cell in row.cells:
                        if theExpressionShouldBeTrodden:
                            intial = 0
                            for numberRange in range(maxLength,len(data),maxLength):
                                cell.text = updateDocx('|'.join(data[intial:numberRange]), cell.text)
                                intial = numberRange
                            cell.text = updateDocx('|'.join(data[intial:]), cell.text)
                        else:
                            cell.text = regexName.sub(lambda match: self.anonymizationFunction(match.group()), cell.text)

            else:
                continue
        self.document.save(self.outfile)

    def extractData(self) -> tuple:
        lastKey    = []
        listNames  = []
        listIdCard = []
        for block in itemIterator(self.document):
            if isinstance(block, Paragraph):
                if LanguageBuilder().hasContex(block.text):
                    listNames[len(listNames):],listIdCard[len(listIdCard):] = self.dataSearch.searchPersonalData(block.text)
                elif self.dataSearch.isName(block.text):
                    listNames.append(block.text.strip())
                else:
                    _,listIdCard[len(listIdCard):] = self.dataSearch.searchPersonalData(block.text)
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

                    listIdCard[len(listIdCard):] = list(
                        itertools.chain.from_iterable(
                            map(lambda cell: self.dataSearch.giveIdCards(cell), 
                            filter(lambda cell: cell not in nameRow, rowText))
                        )
                    )
                    
                listNames[len(listNames):] = namePicker.getAllNames(self.dataSearch.checkNamesInDB,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
            else:
                continue
        return listNames,listIdCard