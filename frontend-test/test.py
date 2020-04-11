import requests
import time

nIter        = 10
listaNames   = 'http://127.0.0.1:5000/search/file/extract-data/json'
encode       = 'http://127.0.0.1:5000/search/file/encode'
tables       = '../backend/app/test/data/tablas/tabla'
txt          = '../backend/app/test/data/textos/carta'
web          = '../backend/app/test/data/web/web'
tosave       = '../backend/app/test/result/times.csv'

def takeMesure(filename:str, strjoin:str, operation:str) -> float:
    result = 0
    for index in range(1,nIter):
        messure = 0
        file    = filename + strjoin %(index)
        for _ in range(nIter):
            with open(file, 'rb') as f:
                st = time.time()
                r = requests.post(operation, files={'file': f})
                messure += time.time() - st
        result += messure/nIter
    return result/nIter

import pandas as pd
def main():
    df = {"txt": [],"docx": [], "pdf": [], "excel/csv": [], "web": []}
    df["excel/csv"].append(takeMesure(tables,"%s.xls",encode))
    df["excel/csv"].append(takeMesure(tables,"%s.xls",listaNames))

    df["txt"].append(takeMesure(txt,"%s.txt",encode))
    df["txt"].append(takeMesure(txt,"%s.txt",listaNames))

    df["docx"].append(takeMesure(txt,"%s.docx",encode))
    df["docx"].append(takeMesure(txt,"%s.docx",listaNames))

    df["pdf"].append(takeMesure(txt,"%s.pdf",encode))
    df["pdf"].append(takeMesure(txt,"%s.pdf",listaNames))

    df["web"].append(takeMesure(web,"%s.html",encode))
    df["web"].append(takeMesure(web,"%s.html",listaNames))

    pd.DataFrame(df, columns=df.keys()).to_csv(tosave, index=False)

if __name__ == "__main__":
    main()
