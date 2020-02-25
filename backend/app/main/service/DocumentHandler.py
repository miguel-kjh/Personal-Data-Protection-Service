
import pandas as pd
from app.main.service.NameSearchByEntities import NameSearchByEntities


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
