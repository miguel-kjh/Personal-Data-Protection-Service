from app.test.base import BaseTestCase
from app.main.service.CreateDocumentHandler import getCreatorDocumentHandler
from app.main.service.languageBuilder import LanguageBuilder

import unittest
import json 
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt

pathTables = 'app/test/data/tablas/tabla'
pathTexts  = 'app/test/data/textos/carta'


def saveHeatmap(array:np.array,filename:str):
    plt.close('all')
    heatmap = sns.heatmap(array,cmap="Blues", annot=True,annot_kws={"size": 16})
    figure = heatmap.get_figure()
    figure.savefig(filename, dpi=400)



class TestPerfomanceTables(BaseTestCase):
    
    def test_tables(self):
        iteration = 4
        array     = np.array([[0,0],[0,0]])
        for index in range(1,iteration):
            with open(pathTables + "%s.json" %(index)) as file:
                data = json.load(file)
            creator        = getCreatorDocumentHandler(pathTables + "%s.xls" %(index),'xls')
            dh             = creator.create()
            listNames,_    = dh.giveListNames()
            hits           = 0
            failures       = 0
            falsePositives = 0
            falseNegatives = 0
            df             = pd.read_excel(pathTables + "%s.xls" %(index))
            for name in listNames:
                if name in data["names"]:
                    hits += 1
                else:
                    falsePositives += 1

            for name in data["names"]:
                if name not in listNames:
                    falseNegatives += 1

            for key in df.keys():
                for ele in df[key]:
                    if ele not in listNames:
                        failures += 1

            array[0][0] += hits
            array[0][1] += falseNegatives
            array[1][0] += falsePositives
            array[1][1] += failures
        print(array)
        saveHeatmap(array,'app/test/result/table.png')

class TestPerfomanceTexts(BaseTestCase):
    def test_text(self):
        iteration = 10
        array     = np.array([[0,0],[0,0]])
        for index in range(1,iteration):
            with open(pathTexts + "%s.json" %(index)) as file:
                data = json.load(file)

            creator        = getCreatorDocumentHandler(pathTexts + "%s.txt" %(index),'txt')
            dh             = creator.create()
            listNames,_    = dh.giveListNames()
            hits           = 0
            failures       = 0
            falsePositives = 0
            falseNegatives = 0

            for name in listNames:
                for nameData in data["names"]:
                    if name == nameData:
                        hits += 1
                        break

            for name in listNames:
                if name not in data["names"]:
                    falsePositives += 1

            for name in data["names"]:
                if name not in listNames:
                    falseNegatives += 1
            
            tokens = []
            nlp = LanguageBuilder().getlanguage()
            with open(pathTexts + "%s.txt" %(index), 'r',encoding='utf8') as file:
                for line in file:
                    for phares in sent_tokenize(line.replace('—', ',') ,language='spanish'):
                        tokens[len(tokens):] = nlp(phares)
            
            for token in tokens:
                for ent in listNames:
                    if token not in nlp(ent):
                        failures += 1
                        break

            array[0][0] += hits
            array[0][1] += falseNegatives
            array[1][0] += falsePositives
            array[1][1] += failures
        
        print(array)
        saveHeatmap(array,'app/test/result/text.png')

        


if __name__ == '__main__':
    unittest.main()