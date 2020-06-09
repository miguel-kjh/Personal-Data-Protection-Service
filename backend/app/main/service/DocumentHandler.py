
from app.main.service.personalDataSearchByEntities  import PersonalDataSearchByEntities
from app.main.service.personalDataSearchByRules     import PersonalDataSearchByRules
from app.main.util.envNames                         import UPLOAD_FOLDER


import pandas as pd
import os
import zipfile
import json

from abc import ABC, abstractmethod


class DocumentHandler(ABC):

    def __init__(self, path: str, outfile: str = "", anonymizationFunction = None):
        self.path                  = path
        self.outfile               = outfile
        self.dataSearch            = PersonalDataSearchByRules()
        self.anonymizationFunction = anonymizationFunction

    @abstractmethod
    def documentsProcessing(self):
        pass

    def createDataCsvFile(self):
        self._createCsv(*self.extractData())

    def createDataJsonFile(self):
        names,idCards = self.extractData()
        data          = {"Names":names,"IdCards":idCards}
        with open(self.outfile,'w') as outfile:
            json.dump(data,outfile)


    @abstractmethod
    def extractData(self) -> tuple:
        pass

    def _createCsv(self, listNames: list, idCards: list):
        if len(listNames) < len(idCards):
            listNames[len(listNames):] = [None]*(len(idCards)-len(listNames))
        elif len(listNames) > len(idCards):
            idCards[len(idCards):] = [None]*(len(listNames)-len(idCards))
            
        filename = os.path.join(UPLOAD_FOLDER,self.outfile)
        dataFrame = pd.DataFrame({"Names":listNames, "Dni": idCards})
        dataFrame.to_csv(filename, index=None, header=True)
