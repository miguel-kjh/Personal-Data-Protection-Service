import requests
import time
import sys
import statistics


iterations   = 10
listaNames   = 'http://127.0.0.1:5000/search/file/extract-data/json'
encode       = 'http://127.0.0.1:5000/search/file/encode'
tables       = '../backend/app/test/data/tablas/tabla'
text         = '../backend/app/test/data/textos/carta'
web          = '../backend/app/test/data/web/web'

def takeMesure(filename:str, operation:str, nIter:int) -> float:
    messure  = 0
    for _ in range(nIter):
        with open(filename, 'rb') as f:
            st       = time.time()
            requests.post(operation, files={'file': f})
            messure += time.time() - st
    return round(messure/nIter,3)

import pandas as pd
def test_time():
    fileCsvNames = [('times_txt.csv',"%s.txt", text), ('times_docx.csv',"%s.docx", text),('times_pdf.csv',"%s.pdf",text),
    ('times_tables.csv',"%s.xls",tables),('times_web.csv',"%s.html",web)]
    for fileCsvName,operation,filename in fileCsvNames:
        df = {
            "text_1":[],"text_2":[],"text_3":[],"text_4":[],"text_5":[],
            "text_6":[],"text_7":[],"text_8":[],"text_9":[],"text_10":[]
        }
        for index in range(1,iterations+1):
            file  = filename + operation %(index)
            df["text_%i" %index].append(takeMesure(file,listaNames,iterations) * 1000)
            df["text_%i" %index].append(takeMesure(file,encode,iterations) * 1000)
        pd.DataFrame(df, columns=df.keys()).to_csv(fileCsvName, index=False)

def getStatistics(data:list) -> list:
    return [sum(data),  statistics.mean(data),  statistics.stdev(data)]

def getMesure(filename:str, ext:str) -> list:
    nIter = 101
    return [takeMesure("%s%i.%s" %(filename,(iteration % 10)+1,ext),encode,1) for iteration in range(1,nIter)]

def get_time() -> dict:
    
    txt     = getMesure(text,'txt')
    pdf     = getMesure(text,'pdf')
    docx    = getMesure(text,'docx')
    xls     = getMesure(tables,'xls')
    html    = getMesure(web,'html')

    df =  {
        "txt"  : getStatistics(txt),
        "pdf"  : getStatistics(pdf),
        "docx" : getStatistics(docx),
        "xls"  : getStatistics(xls),
        "html" : getStatistics(html),
    }
    pd.DataFrame(df, columns=df.keys()).to_csv('times.csv', index=False)
    return df

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].strip() == 'test_time':
            test_time()
        elif sys.argv[1].strip() == 'get_time':
            print(get_time())
