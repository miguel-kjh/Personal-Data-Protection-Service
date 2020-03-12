from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.ColumnSelectorDataframe import ColumnSelectorDataFrame
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.util.fileUtils import encode

import pandas as pd


class DocumentHandlerSpreadsheets(DocumentHandler):
    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.selector = ColumnSelectorDataFrame()

    def save(self):
        pass

class DocumentHandlerExcel(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.sheets = pd.read_excel(path,sheet_name=None)

    def giveListNames(self) -> tuple:
        listNames = []
        idCards   = []
        for table in self.sheets:
            for typeColumn in self.selector.getPossibleColumnsNames(self.sheets[table]):
                if typeColumn.isName:
                    dfNotNull = self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        listNames[len(listNames):] = dfNotNull
                else:
                    idCards[len(idCards):] = list(
                        filter(lambda idCards: self.dataSearch.isDni(idCards),self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()])
                    )
        return listNames,idCards

    def documentsProcessing(self):
        for table in self.sheets:
            for typeColumn in self.selector.getPossibleColumnsNames(self.sheets[table]):
                if typeColumn.isName:
                    dfNotNull = self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()]
                    countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                    if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                        self.sheets[table][typeColumn.key].replace({str(name): encode(str(name)) for name in dfNotNull}, inplace=True)
                else:
                    idCards = list(
                        filter(lambda idCards: self.dataSearch.isDni(idCards),self.sheets[table][typeColumn.key][self.sheets[table][typeColumn.key].notnull()])
                    )
                    self.sheets[table][typeColumn.key].replace({str(idCard): encode(str(idCard)) for idCard in idCards}, inplace=True)
        self.save()
    
    def save(self):
        writer = pd.ExcelWriter(self.destiny)
        for sheetName in self.sheets:
            self.sheets[sheetName].to_excel(writer, sheet_name = sheetName, index=False)
        writer.save()

class DocumentHandlerCsv(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.df = pd.read_csv(path)

    def giveListNames(self) -> tuple:
        listNames = []
        idCards   = []
        for typeColumn in self.selector.getPossibleColumnsNames(self.df):
            if typeColumn.isName:
                dfNotNull = self.df[typeColumn.key][self.df[typeColumn.key].notnull()]
                countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                    listNames[len(listNames):] = dfNotNull
            else:
                idCards[len(idCards):] = list(
                    filter(lambda idCards: self.dataSearch.isDni(idCards),self.df[typeColumn.key][self.df[typeColumn.key].notnull()])
                )
        return listNames,idCards

    def documentsProcessing(self):
        for typeColumn in self.selector.getPossibleColumnsNames(self.df):
            if typeColumn.isName:
                dfNotNull = self.df[typeColumn.key][self.df[typeColumn.key].notnull()]
                countOfName = self.selector.columnSearch(dfNotNull,self.dataSearch.checkNamesInDB)
                if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                    self.df[typeColumn.key].replace({str(name): encode(str(name)) for name in dfNotNull}, inplace=True)
            else:
                idCards = list(
                    filter(lambda idCards: self.dataSearch.isDni(idCards),self.df[typeColumn.key][self.df[typeColumn.key].notnull()])
                )
                self.df[typeColumn.key].replace({str(idCard): encode(str(idCard)) for idCard in idCards}, inplace=True)
        self.save()


    def save(self):
        self.df.to_csv(self.destiny, index=False)