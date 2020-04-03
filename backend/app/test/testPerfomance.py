from app.test.base import BaseTestCase
from app.main.service.CreateDocumentHandler import getCreatorDocumentHandler
from app.main.service.languageBuilder import LanguageBuilder
from app.main.service.DocumentHandlerHtml import TokenizerHtml,TableToken

import unittest
import json 
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

pathTables = 'app/test/data/tablas/tabla'
pathTexts  = 'app/test/data/textos/carta'
pathWeb    = 'app/test/data/web/examples.txt'


def saveHeatmap(array:np.array,filename:str):
    print("\n")
    print(array, "\n")
    plt.close('all')
    heatmap = sns.heatmap(array,cmap="Blues", annot=True,annot_kws={"size": 16})
    figure = heatmap.get_figure()
    figure.savefig(filename, dpi=400)

class ConfidenceMatrixBuilder:
    def __init__(self):
        self.hits                 = 0
        self.failures             = 0
        self.falsePositives       = 0
        self.falseNegatives       = 0
        self.nlp                  = LanguageBuilder().getlanguage()
        self.listOfFalseNegatives = []
        self.listOfFalsePositives = []

    def countHinstInTexts(self, listNames:list, data:list):
        for name in list(set(listNames)):
            countNameInModel = listNames.count(name)
            realCountName    = data.count(name)
            namestokens      = len(self.nlp(name))
            if realCountName == 0:
                self.falsePositives += countNameInModel*namestokens
                self.listOfFalsePositives.append((name,countNameInModel,realCountName))
                continue

            if countNameInModel == realCountName:
                self.hits += countNameInModel*namestokens
            elif countNameInModel < realCountName:
                self.hits += countNameInModel*namestokens
                self.falseNegatives += (realCountName-countNameInModel)*namestokens
                self.listOfFalseNegatives.append((name,countNameInModel,realCountName))
            else:
                print("imposible")

    def countHinstInTables(self,listNames:list, data:list):
        for name in listNames:
            if name in data:
                self.hits += 1
            else:
                self.falsePositives += 1

        for name in data:
            if name not in listNames:
                self.falseNegatives += 1

    def countFailuresInTexts(self, listNames:list, file):
        tokens = []
        for line in file:
            for phares in sent_tokenize(line.replace('—', ',') ,language='spanish'):
                tokens[len(tokens):] = self.nlp(phares)
        
        for token in tokens:
            for ent in listNames:
                if token not in self.nlp(ent):
                    self.failures += 1
                    break

    def countFailuresInWeb(self, listNames:list, tokenizer:TokenizerHtml):
        linguisticTokens = []
        for token in tokenizer.getToken():
            if token.isTable == TableToken.NONE:
                for phares in sent_tokenize(token.text[0].replace('—', ',') ,language='spanish'):
                    linguisticTokens[len(linguisticTokens):] = self.nlp(phares)

        for token in linguisticTokens:
            for ent in listNames:
                if token not in self.nlp(ent):
                    self.failures += 1
                    break
    
    def countFailuresInTables(self, listNames:list, df:pd.DataFrame):
        for key in df.keys():
            for ele in df[key]:
                if ele not in listNames:
                    self.failures += 1

    def getMatrix(self) -> np.array:
        return np.array([
            [self.failures      , self.falseNegatives],
            [self.falsePositives, self.hits]
        ])

    def getListOfFalseNegatives(self):
        return self.listOfFalseNegatives

    def getListOfFalsePositive(self):
        return self.listOfFalsePositives



class TestPerfomanceTables(BaseTestCase):
    
    def test_tables(self):
        iteration = 10
        builder   = ConfidenceMatrixBuilder()
        for index in range(1,iteration):
            with open(pathTables + "%s.json" %(index)) as file:
                data = json.load(file)
            creator        = getCreatorDocumentHandler(pathTables + "%s.xls" %(index),'xls')
            dh             = creator.create()
            listNames,_    = dh.giveListNames()
            df             = pd.read_excel(pathTables + "%s.xls" %(index))

            builder.countHinstInTables(listNames,data['names'])
            builder.countFailuresInTables(listNames,df)

        saveHeatmap(builder.getMatrix(),'app/test/result/table.png')

class TestPerfomanceTexts(BaseTestCase):
    def test_text(self):
        iteration = 10
        builder   = ConfidenceMatrixBuilder()
        for index in range(1,iteration):
            with open(pathTexts + "%s.json" %(index)) as file:
                data = json.load(file)

            creator        = getCreatorDocumentHandler(pathTexts + "%s.txt" %(index),'txt')
            dh             = creator.create()
            listNames,_    = dh.giveListNames()
            
            builder.countHinstInTexts(listNames,data['names'])

            with open(pathTexts + "%s.txt" %(index), 'r',encoding='utf8') as file:
                builder.countFailuresInTexts(listNames,file)    
        
        print(builder.listOfFalsePositives, "\n"  , builder.listOfFalseNegatives)
        saveHeatmap(builder.getMatrix(),'app/test/result/text.png')

class TestPerfomanceWeb(BaseTestCase):
    def test_web(self):
        web       = 'app/test/data/web/web'
        builder   = ConfidenceMatrixBuilder()
        with open(pathWeb, 'r',encoding='utf8') as file:
            for index,url in enumerate(file):
                try:
                    req = requests.get(url)
                except Exception:
                    print("\nWARRNING:", url, "not can get html")
                    break
                creator        = getCreatorDocumentHandler(req.text,'url')
                soup           = BeautifulSoup(req.text, "lxml")
                tokenizer      = TokenizerHtml(soup)
                dh             = creator.create()
                listNames,_    = dh.giveListNames()
                with open(web + "%s.json" %(index+1)) as file:
                    data = json.load(file)

                builder.countHinstInTexts(listNames,data['names'])    
                builder.countFailuresInWeb(listNames,tokenizer)

        print(builder.listOfFalsePositives, "\n"  , builder.listOfFalseNegatives)
        saveHeatmap(builder.getMatrix(),'app/test/result/web.png')

        


if __name__ == '__main__':
    unittest.main()