from app.main.service.personalDataSearch import PersonalData
from app.main.service.DocumentHandler    import DocumentHandler
from app.main.util.dataPickerInTables    import DataPickerInTables
from app.main.util.fileUtils             import readPdf
from app.main.util.semanticWordLists     import listOfVectorWords
from app.main.util.heuristicMeasures     import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX
from app.main.service.languageBuilder    import LanguageBuilder
import app.main.service.pdf_redactor     as pdf_redactor


from datetime import datetime
from typing   import Text
import re
import itertools
    

class DocumentHandlerPdf(DocumentHandler):

    def __init__(self, path: str, outfile: str = "", anonymizationFunction = None):
        super().__init__(path, outfile=outfile, anonymizationFunction = anonymizationFunction)
        self.options                  = pdf_redactor.RedactorOptions()
        self.options.xmp_filters      = [lambda xml: None]
        self.options.metadata_filters = {
            "Title": [lambda value: value],

            "Producer": [lambda value: value],
            "CreationDate": [lambda value: datetime.utcnow()],

            "DEFAULT": [lambda value: None],
        }

    def getPersonalDataInTables(self, tables:list, listNames:list, idCards: list, lastKey: list, personalData: PersonalData) -> list:
        for table in tables:
            namePicker = DataPickerInTables()
            for index, row in enumerate(table):
                if personalData != PersonalData.idCards and index == 0:
                    lables = list(
                        filter(lambda cell: list(filter(lambda x: LanguageBuilder().semanticSimilarity(cell,x) > MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES,listOfVectorWords)), row)
                    )
                    key = list(map(lambda cell: row.index(cell),lables))
                    if not key:
                        key = lastKey
                        namePicker.addIndexesColumn(key)
                    else:
                        lastKey = key
                        namePicker.addIndexesColumn(key)
                        continue
                
                nameRow = list(filter(lambda cell: namePicker.isColumnName(row.index(cell)), row))
                if personalData != PersonalData.idCards:
                    for cell in nameRow:
                        namePicker.addName(row.index(cell), cell)
                    listNames[len(listNames):] = namePicker.getAllNames(self.dataSearch.checkNamesInDB,MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS)
                
                if personalData != PersonalData.name:
                    idCards[len(idCards):] = list(
                            itertools.chain.from_iterable(
                                map(lambda cell: self.dataSearch.giveIdCards(cell), 
                                filter(lambda cell: cell not in nameRow, row))
                            )
                        )        
        return lastKey    
            

    def getPersonalDataInTexts(self, text: Text, listNames: list, idCards: list, personalData: PersonalData):

        if personalData != PersonalData.idCards:
            textSplit = text.split('\n')
            textWithContext = list(filter(lambda sent: LanguageBuilder().hasContex(sent), textSplit))
            listNames[len(listNames):] = list(
                filter(lambda words: words not in textWithContext and self.dataSearch.isName(words), textSplit)
            )
            listNames[len(listNames):],_ = self.dataSearch.searchPersonalData(' '.join(textWithContext), PersonalData.name)
        if personalData != PersonalData.name:
            _,idCards[len(idCards):] = self.dataSearch.searchPersonalData(' '.join(text), PersonalData.idCards)

    def extractData(self, personalData: PersonalData = PersonalData.all) -> tuple:
        listNames = []
        idCards   = []
        lastKey   = []
        for text,tables in readPdf(self.path):
            lastKey = self.getPersonalDataInTables(tables,listNames,idCards,lastKey,personalData)
            self.getPersonalDataInTexts(text,listNames,idCards,personalData)
        return listNames,idCards

    def documentsProcessing(self, personalData: PersonalData = PersonalData.all):
        def updatePdf(regex:str):
            self.options.content_filters = [
                (
                    re.compile(regex),
                    lambda m: self.anonymizationFunction(m.group())
                )
            ]
            pdf_redactor.redactor(self.options, self.path, self.outfile)
            self.path = self.outfile

        if not self.anonymizationFunction:
            return
        
        maxLength = MAXIMUM_NUMBER_OF_ELEMENTS_IN_A_REGEX
        listNames,idCards = self.extractData(personalData)
        if not listNames and not idCards:
            pdf_redactor.redactor(self.options, self.path, self.outfile)
            return
        listNames = list(set(listNames))
        listNames.sort(
                key     = lambda value: len(value),
                reverse = True
            )
        data = []
        data[len(data):],data[len(data):] = listNames,idCards
        if len(data) > maxLength:
            intial = 0
            for numberRange in range(maxLength,len(data),maxLength):
                updatePdf('|'.join(data[intial:numberRange]))
                intial = numberRange
            updatePdf('|'.join(data[intial:]))
        else:
            updatePdf('|'.join(data))
        
        