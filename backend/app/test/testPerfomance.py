from app.test.base import BaseTestCase
from app.main.service.CreateDocumentHandler import getCreatorDocumentHandler
from app.main.service.languageBuilder import LanguageBuilder
from app.test.fileVariables import pathTexts,pathTables,pathWeb

import unittest
import json 
import numpy as np
import pandas as pd



class ConfidenceMatrixBuilder:
    def __init__(self):
        self.hits                 = 0
        self.falsePositives       = 0
        self.falseNegatives       = 0
        self.nlp                  = LanguageBuilder().getlanguage()
        self.listOfFalseNegatives = []
        self.listOfFalsePositives = []

    def countHinst(self, listNames:list, data:list):
        for name in list(set(data)):
            countNameInModel = listNames.count(name)
            realCountName    = data.count(name)

            if countNameInModel == realCountName:
                self.hits += countNameInModel
            elif countNameInModel == 0:
                self.falseNegatives += (realCountName-countNameInModel)
                self.listOfFalseNegatives.append((name,countNameInModel,realCountName))
            elif countNameInModel < realCountName:
                self.hits           += realCountName
                self.listOfFalseNegatives.append((name,countNameInModel,realCountName))
            else:
                self.hits           += realCountName
                self.falsePositives += (countNameInModel-realCountName)
                self.listOfFalsePositives.append((name,countNameInModel,realCountName))
        
        for name in list(set(listNames)):
            countNameInModel = listNames.count(name)
            realCountName    = data.count(name)
            if realCountName == 0:
                self.falsePositives += countNameInModel
                self.listOfFalsePositives.append((name,countNameInModel,realCountName))

    def getData(self) -> dict:
        return {
            "hits"           :self.hits, 
            "False Positives":self.falsePositives,
            "False Negatives":self.falseNegatives 
        }
    
    def saveReport(self,filename):
        table = {"NAMES":[], "MATCHES":[], "REAL MARCHES": [], "TYPE": []}
        for name,matches,realMatches in self.listOfFalsePositives:
            table["NAMES"].append(name)
            table["MATCHES"].append(matches)
            table["REAL MARCHES"].append(realMatches)
            table["TYPE"].append("False Positive")

        for name,matches,realMatches in self.listOfFalseNegatives:
            table["NAMES"].append(name)
            table["MATCHES"].append(matches)
            table["REAL MARCHES"].append(realMatches)
            table["TYPE"].append("False Negative")
        
        df = pd.DataFrame(table, columns=table.keys())
        df.to_csv(filename, index=False)

    def getListOfFalseNegatives(self):
        return self.listOfFalseNegatives

    def getListOfFalsePositive(self):
        return self.listOfFalsePositives



class TestPerfomanceTables(BaseTestCase):
    
    def test_tables(self):
        iteration = 11
        builder   = ConfidenceMatrixBuilder()
        print("\n")
        for index in range(1,iteration):
            with open(pathTables + "%s.json" %(index)) as file:
                data = json.load(file)
            creator        = getCreatorDocumentHandler(pathTables + "%s.xls" %(index),'xls')
            dh             = creator.create()
            listNames,_    = dh.extractData()

            builder.countHinst(listNames,data['names'])
            print(pathTables + "%s.xls" %(index), ":", len(listNames), "names")
        print(builder.getData())

        builder.saveReport('app/test/result/tables_report.csv')

class TestPerfomanceTexts(BaseTestCase):
    def test_text(self):
        iteration = 11
        builder   = ConfidenceMatrixBuilder()
        print("\n")
        for index in range(1,iteration):
            with open(pathTexts + "%s.json" %(index)) as file:
                data = json.load(file)

            creator        = getCreatorDocumentHandler(pathTexts + "%s.txt" %(index),'txt')
            dh             = creator.create()
            listNames,_    = dh.extractData()
            print(pathTexts + "%s.txt" %(index), ":", len(listNames), "names")
            builder.countHinst(listNames,data['names'])
        print(builder.getData())
        
        builder.saveReport('app/test/result/text_report.csv')

class TestPerfomanceWeb(BaseTestCase):
    def test_web(self):
        iteration = 11
        builder   = ConfidenceMatrixBuilder()
        print("\n")
        for index in range(1,iteration):
            with open(pathWeb + "%s.json" %(index)) as file:
                data = json.load(file)

            creator        = getCreatorDocumentHandler(pathWeb + "%s.html" %(index),'html')
            dh             = creator.create()
            listNames,_    = dh.extractData()

            builder.countHinst(listNames,data['names'])
            print(pathWeb + "%s.html" %(index), ":", len(listNames), "names")
        print(builder.getData())

        builder.saveReport('app/test/result/web_report.csv')

       


if __name__ == '__main__':
    unittest.main()