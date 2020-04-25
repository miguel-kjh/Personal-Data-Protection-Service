from app.main.service.DocumentHandler      import DocumentHandler
from app.main.util.ColumnSelectorDataframe import ColumnSelectorDataFrame
from app.main.util.heuristicMeasures       import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.util.heuristicMeasures       import MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY
from app.main.util.heuristicMeasures       import SAMPLE_DATA_TO_CHOOSE_NAMES

import pandas as pd
from random import sample
import itertools


class DocumentHandlerSpreadsheets(DocumentHandler):
    def __init__(self, path: str, destiny: str = "", anonymizationFunction = None):
        super().__init__(path, destiny=destiny, anonymizationFunction = anonymizationFunction)
        self.selector = ColumnSelectorDataFrame()

    def save(self):
        pass

class DocumentHandlerExcel(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = "", anonymizationFunction=None):
        super().__init__(path, destiny=destiny, anonymizationFunction=anonymizationFunction)
        self.sheets = pd.read_excel(path,sheet_name=None)

    def extractData(self) -> tuple:
        listNames = []
        idCards   = []
        for table in self.sheets:
            for typeColumn in self.selector.getPossibleColumnsNames(self.sheets[table]):
                dfNotNull  = self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()]
                if typeColumn.isName:
                    auxdf = dfNotNull
                    if len(dfNotNull) > MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY:
                        auxdf = sample(list(dfNotNull),round(len(dfNotNull) * SAMPLE_DATA_TO_CHOOSE_NAMES))
                    countOfName = self.selector.columnSearch(auxdf,self.dataSearch.checkNamesInDB)
                    if countOfName / len(auxdf) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames[len(listNames):] = dfNotNull
                else:
                    idCards[len(idCards):] = list(
                        itertools.chain.from_iterable(map(lambda idCards: self.dataSearch.giveIdCards(idCards),dfNotNull))
                    )
        return listNames,idCards

    def documentsProcessing(self):

        if not self.anonymizationFunction:
            return

        for table in self.sheets:
            for typeColumn in self.selector.getPossibleColumnsNames(self.sheets[table]):
                dfNotNull = self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()]
                if typeColumn.isName:
                    auxdf = dfNotNull
                    if len(dfNotNull) > MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY:
                        auxdf = sample(list(dfNotNull),round(len(dfNotNull) * SAMPLE_DATA_TO_CHOOSE_NAMES))
                    countOfName = self.selector.columnSearch(auxdf,self.dataSearch.checkNamesInDB)
                    if countOfName / len(auxdf) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        self.sheets[table][typeColumn.key].replace({str(name): self.anonymizationFunction(str(name)) for name in dfNotNull}, inplace=True)
                else:
                    idCards = list(
                        itertools.chain.from_iterable(map(lambda idCards: self.dataSearch.giveIdCards(idCards),dfNotNull))
                    )
                    self.sheets[table][typeColumn.key].replace({str(idCard): self.anonymizationFunction(str(idCard)) for idCard in idCards}, inplace=True)
        self.save()
    
    def save(self):
        writer = pd.ExcelWriter(self.destiny)
        for sheetName in self.sheets:
            self.sheets[sheetName].to_excel(writer, sheet_name = sheetName, index=False)
        writer.save()

class DocumentHandlerCsv(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = "",anonymizationFunction=None):
        super().__init__(path, destiny=destiny, anonymizationFunction=anonymizationFunction)
        self.df = pd.read_csv(path)

    def extractData(self) -> tuple:
        listNames = []
        idCards   = []
        for typeColumn in self.selector.getPossibleColumnsNames(self.df):
            dfNotNull   = self.df[typeColumn.key][self.df[typeColumn.key].notnull()]
            if typeColumn.isName:
                auxdf = dfNotNull
                if len(dfNotNull) > MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY:
                    auxdf = sample(list(dfNotNull),round(len(dfNotNull) * SAMPLE_DATA_TO_CHOOSE_NAMES))
                countOfName = self.selector.columnSearch(auxdf,self.dataSearch.checkNamesInDB)
                if countOfName / len(auxdf) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                    listNames[len(listNames):] = dfNotNull
            else:
                idCards[len(idCards):] = list(
                    itertools.chain.from_iterable(map(lambda idCards: self.dataSearch.giveIdCards(idCards),dfNotNull))
                )
        return listNames,idCards

    def documentsProcessing(self):
        if not self.anonymizationFunction:
            return

        for typeColumn in self.selector.getPossibleColumnsNames(self.df):
            dfNotNull   = self.df[typeColumn.key][self.df[typeColumn.key].notnull()]
            if typeColumn.isName:
                auxdf = dfNotNull
                if len(dfNotNull) > MAXIMUM_NUMBER_OF_POSSIBLE_NAMES_FOR_A_QUERY:
                    auxdf = sample(list(dfNotNull),round(len(dfNotNull) * SAMPLE_DATA_TO_CHOOSE_NAMES))
                countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                    self.df[typeColumn.key].replace({str(name): self.anonymizationFunction(str(name)) for name in dfNotNull}, inplace=True)
            else:
                idCards = list(
                    itertools.chain.from_iterable(map(lambda idCards: self.dataSearch.giveIdCards(idCards),dfNotNull))
                )
                self.df[typeColumn.key].replace({str(idCard): self.anonymizationFunction(str(idCard)) for idCard in idCards}, inplace=True)
        self.save()


    def save(self):
        self.df.to_csv(self.destiny, index=False)