
from app.main.service.personalDataSearch            import PersonalData
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
    def documentsProcessing(self, personalData: PersonalData = PersonalData.all):
        """  
        Processes the personal data of a document and modifies the content of the document.
        :param personalData: PersonalData
        """

        pass

    def createDataCsvFile(self, personalData: PersonalData = PersonalData.all):
        """
        Creates a csv file with the data
        :param personalData: PersonalData
        """

        self._createCsv(*self.extractData(personalData))

    def createDataJsonFile(self, personalData: PersonalData = PersonalData.all):
        """
        Creates a json file with the data
        :param personalData: PersonalData
        """

        names,idCards = self.extractData(personalData)
        data = {"Names":names,"IdCards":idCards}
        with open(self.outfile,'w') as outfile:
            json.dump(data,outfile)


    @abstractmethod
    def extractData(self, personalData: PersonalData = PersonalData.all) -> tuple:
        """  
        Extracts personal data from a document.
        :param personalData: PersonalData
        :return: tuple(names, DNIs)
        """
        
        pass

    def _createCsv(self, listNames: list, idCards: list):
        """  
        Private method to create a dataFrame with the data 
        :param listNames: list of strings
        :param idCards: list of strings
        """

        if len(listNames) < len(idCards):
            listNames[len(listNames):] = [None]*(len(idCards)-len(listNames))
        elif len(listNames) > len(idCards):
            idCards[len(idCards):] = [None]*(len(listNames)-len(idCards))
            
        filename  = os.path.join(UPLOAD_FOLDER,self.outfile)
        dataFrame = pd.DataFrame({"Names":listNames, "Dni": idCards})
        dataFrame.to_csv(filename, index=None, header=True)
