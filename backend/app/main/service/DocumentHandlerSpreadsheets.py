from app.main.service.DocumentHandler import DocumentHandler
from app.main.util.ColumnSelectorDataframe import ColumnSelectorDataFrame
from app.main.util.heuristicMeasures import MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS, MEASURE_TO_COLUMN_KEY_REFERS_TO_NAMES
from app.main.util.fileUtils import encode

import pandas as pd


class DocumentHandlerSpreadsheets(DocumentHandler):
    def __init__(self, path: str, df:pd.DataFrame, destiny: str = ""):
        super().__init__(path, destiny=destiny)
        self.df = df
        self.selector = ColumnSelectorDataFrame()

    def giveListNames(self) -> tuple:
        listNames = []
        for key in self.selector.getPossibleColumnsNames(self.df):
            dfNotNull = self.df[key][self.df[key].notnull()]
            countOfName = self.selector.columnSearch(dfNotNull,self.nameSearch.checkNameInDB)
            if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                listNames[len(listNames):] = dfNotNull
        idCards = []
        for key in self.selector.getPossibleColumnsIdCards(self.df):
            idCards[len(idCards):] = list(
                filter(lambda idCards: self.nameSearch.isDni(idCards),self.df[key][self.df[key].notnull()])
            )
        return listNames,idCards

    def documentsProcessing(self):
        for key in self.selector.getPossibleColumnsNames(self.df):
            dfNotNull = self.df[key][self.df[key].notnull()]
            countOfName = self.selector.columnSearch(dfNotNull,self.nameSearch.checkNameInDB)
            if countOfName / len(dfNotNull) > MEASURE_FOR_TEXTS_WITHOUT_CONTEXTS:
                self.df[key].replace({str(name): encode(str(name)) for name in dfNotNull}, inplace=True)
        for key in self.selector.getPossibleColumnsIdCards(self.df):
            idCards = list(
                filter(lambda idCards: self.nameSearch.isDni(idCards),self.df[key][self.df[key].notnull()])
            )
            self.df[key].replace({str(idCard): encode(str(idCard)) for idCard in idCards}, inplace=True)
        self.save()

    def save(self):
        pass

class DocumentHandlerExcel(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, pd.read_excel(path), destiny=destiny)


    def save(self):
        self.df.to_excel(self.destiny, index=False)

class DocumentHandlerCsv(DocumentHandlerSpreadsheets):

    def __init__(self, path: str, destiny: str = ""):
        super().__init__(path, pd.read_csv(path), destiny=destiny)


    def save(self):
        self.df.to_csv(self.destiny, index=False)