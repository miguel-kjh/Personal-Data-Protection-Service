
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
        self.dataSearch            = PersonalDataSearchByEntities()
        self.anonymizationFunction = anonymizationFunction

    @abstractmethod
    def documentsProcessing(self):
        pass

    def createDataZipFolder(self):
        self._createZip(*self.extractData())

    def createDataJsonFile(self):
        names,idCards = self.extractData()
        data          = {"Names":names,"IdCards":idCards}
        with open(self.outfile,'w') as outfile:
            json.dump(data,outfile)


    @abstractmethod
    def extractData(self) -> tuple:
        pass

    def _saveInZipFile(self, zipf:zipfile.ZipFile, filename:str,nameColum:str, collection:list):
        dataFrame = pd.DataFrame({nameColum:collection})
        export    = dataFrame.to_csv(filename, index=None, header=True)
        if not export:
            zipf.write(filename)
            os.remove(filename)

    def _createZip(self, listNames: list, idCards: list):
        zipf = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        if listNames:
            filename = os.path.join(UPLOAD_FOLDER,"names.csv")
            self._saveInZipFile(zipf,filename,"Names", listNames)
        if idCards:
            filename = os.path.join(UPLOAD_FOLDER,"idCards.csv")
            self._saveInZipFile(zipf,filename,"IdCards", idCards)
