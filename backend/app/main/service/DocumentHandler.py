
import pandas as pd
from app.main.service.personalDataSearchByEntities import PersonalDataSearchByEntities


class DocumentHandler:

    def __init__(self, path: str, destiny: str = ""):
        self.path = path
        self.destiny = destiny
        self.nameSearch = PersonalDataSearchByEntities()

    def documentsProcessing(self):
        pass

    # def documentTagger(self):
    # pass

    def createFileOfName(self):
        self.createCsv(*self.giveListNames())

    def giveListNames(self) -> tuple:
        pass

    def createCsv(self, listNames: list, idCards: list):
        dataFrame = pd.DataFrame({"Names":listNames, "idCards":idCards}, columns=['Names'])
        export_csv = dataFrame.to_csv(self.destiny, index=None, header=True)
        print(export_csv)
