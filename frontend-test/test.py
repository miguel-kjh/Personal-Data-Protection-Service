import requests
import time

nIter        = 10
listaNames   = 'http://127.0.0.1:5000/search/file/extract-data/json'
encode       = 'http://127.0.0.1:5000/search/file/encode'
tables       = '../backend/app/test/data/tablas/tabla'
text         = '../backend/app/test/data/textos/carta'
web          = '../backend/app/test/data/web/web'

def takeMesure(filename:str, operation:str) -> float:
    messure  = 0
    for _ in range(nIter):
        with open(filename, 'rb') as f:
            st       = time.time()
            requests.post(operation, files={'file': f})
            messure += time.time() - st
    return round(messure/nIter,3)

import pandas as pd
def main():
    fileCsvNames = [('times_txt.csv',"%s.txt", text), ('times_docx.csv',"%s.docx", text),('times_pdf.csv',"%s.pdf",text),
    ('times_tables.csv',"%s.xls",tables),('times_web.csv',"%s.html",web)]
    for fileCsvName,operation,filename in fileCsvNames:
        df = {
            "text_1":[],"text_2":[],"text_3":[],"text_4":[],"text_5":[],
            "text_6":[],"text_7":[],"text_8":[],"text_9":[],"text_10":[]
        }
        for index in range(1,nIter+1):
            file  = filename + operation %(index)
            df["text_%i" %index].append(takeMesure(file,listaNames) * 1000)
            df["text_%i" %index].append(takeMesure(file,encode) * 1000)
        pd.DataFrame(df, columns=df.keys()).to_csv(fileCsvName, index=False)

if __name__ == "__main__":
    main()
