from app.test.base import BaseTestCase
from app.main.service.CreateDocumentHandler import getCreatorDocumentHandler
from app.main.service.languageBuilder import LanguageBuilder
from app.test.fileVariables import pathTexts,pathTables,pathWeb,pathTimes
from app.main.service.personalDataSearchByEntities  import PersonalDataSearchByEntities
from app.main.service.personalDataSearchByRules     import PersonalDataSearchByRules


from nltk.tokenize import word_tokenize
import unittest
import json 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import re,string
import itertools
import time


class ConfidenceMatrixBuilder:
    def __init__(self):
        self.hits                 = 0
        self.falsePositives       = 0
        self.falseNegatives       = 0
        self.nlp                  = LanguageBuilder().getlanguage()
        self.listOfFalseNegatives = []
        self.listOfFalsePositives = []

    def countHinst(self, listNames:list, data:list, filename:str):
        listNames = list(map(lambda name: name.replace('\n',''),listNames))
        for name in list(set(data)):
            countNameInModel = listNames.count(name)
            realCountName    = data.count(name)

            if countNameInModel == realCountName:
                self.hits += countNameInModel
            elif countNameInModel == 0:
                self.falseNegatives += (realCountName-countNameInModel)
                self.listOfFalseNegatives.append((name,countNameInModel,realCountName,filename))
            elif countNameInModel < realCountName:
                self.hits           += realCountName
                self.listOfFalseNegatives.append((name,countNameInModel,realCountName,filename))
            else:
                self.hits           += realCountName
                self.falsePositives += (countNameInModel-realCountName)
                self.listOfFalsePositives.append((name,countNameInModel,realCountName,filename))
        
        for name in list(set(listNames)):
            countNameInModel = listNames.count(name)
            realCountName    = data.count(name)
            if realCountName == 0:
                self.falsePositives += countNameInModel
                self.listOfFalsePositives.append((name,countNameInModel,realCountName, filename))

    def getData(self) -> dict:
        return {
            "hits"           :self.hits, 
            "False Positives":self.falsePositives,
            "False Negatives":self.falseNegatives 
        }

    def _buildGarph(self, df:pd.DataFrame, yname, filename):
        block = df[(df["TYPE"] == 'False Negative') & (df["MATCHES"] == 0)].groupby('FILE').groups
        block = {k:len(v) for k,v in block.items()}
        plt.subplots_adjust(hspace=0.5)

        plt.subplot(211)
        plt.bar(block.keys(), block.values(), align='center', alpha=0.5)
        plt.ylabel(yname)
        plt.title('False Negative')

        block = df[df["TYPE"] == 'False Positive'].groupby('FILE').groups
        block = {k:len(v) for k,v in block.items()}

        plt.subplot(212)
        plt.bar(block.keys(), block.values(), align='center', alpha=0.5)
        plt.ylabel(yname)
        plt.title('False Positive')

        plt.savefig(filename)
        plt.close()
    
    def saveReport(self,csvfile, imgfile):
        table = {"NAMES":[], "MATCHES":[], "REAL MARCHES": [], "TYPE": [], "FILE":[]}
        for name,matches,realMatches,file in self.listOfFalsePositives:
            table["NAMES"].append(name)
            table["MATCHES"].append(matches)
            table["REAL MARCHES"].append(realMatches)
            table["TYPE"].append("False Positive")
            table["FILE"].append(file)

        for name,matches,realMatches,file in self.listOfFalseNegatives:
            table["NAMES"].append(name)
            table["MATCHES"].append(matches)
            table["REAL MARCHES"].append(realMatches)
            table["TYPE"].append("False Negative")
            table["FILE"].append(file)
        
        df = pd.DataFrame(table, columns=table.keys())
        df.to_csv(csvfile, index=False)
        self._buildGarph(df,'count',imgfile)


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

            builder.countHinst(listNames,data['names'],"tables%s" %(index))
            #print(pathTables + "%s.xls" %(index), ":", len(listNames), "names")
        print(builder.getData())

        builder.saveReport('app/test/result/tables_report.csv', 'app/test/result/tables_report.jpg')

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
            #print(pathTexts + "%s.txt" %(index), ":", len(listNames), "names")
            builder.countHinst(listNames,data['names'],"text%s" %(index))
        print(builder.getData())
        
        builder.saveReport('app/test/result/text_report.csv','app/test/result/text_report.jpg')

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

            builder.countHinst(listNames,data['names'], "web%s" %(index))
            #print(pathWeb + "%s.html" %(index), ":", len(listNames), "names")
        print(builder.getData())

        builder.saveReport('app/test/result/web_report.csv','app/test/result/web_report.jpg')

def test_time_of_Model():
    entModel   = PersonalDataSearchByEntities()
    rulesModel = PersonalDataSearchByRules()
    def getMesures(text:str) -> list:
        st = time.time()
        data = entModel.searchPersonalData(text)
        ent_times = time.time()-st
        ent_len   = len(data[0]) + len(data[1])

        st = time.time()
        data = rulesModel.searchPersonalData(text)
        rules_times = time.time()-st
        rules_len   = len(data[0]) + len(data[1])

        return [ent_times,ent_len,rules_times,rules_len, len(word_tokenize(text))]
        
    with open(pathTimes, "r", encoding='latin-1') as file:
        texts = file.read()
    texts = re.sub('<.*>','lineSplit',texts)

    texts = re.sub('ENDOFARTICLE.','',texts)

    punctuationNoPeriod = "[" + re.sub("\.","",string.punctuation) + "]"
    texts = re.sub(punctuationNoPeriod, "", texts)

    list_texts = texts.split('lineSplit')
    mesures = np.array(
                list(filter(lambda row: row[1]*row[3]*row[4] != 0,
                    map(lambda text: getMesures(text),
                        list_texts
                        )
                    )
                )
            )
    df = pd.DataFrame(mesures)
    df.to_excel('app/test/result/times_output.xlsx')

class TestOfTimesModel(BaseTestCase):
    def test_time_of_Model(self):
        #test_time_of_Model()
        pass


       


if __name__ == '__main__':
    unittest.main()