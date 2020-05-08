import pandas
import statistics
import matplotlib.pyplot as plt
from statistics import mean
import math

list_files = [
    ('times_docx.xls', 'Docx'),
    ('times_pdf.xls', 'Pdf'),
    ('times_tables.xls', 'Spreadsheets'),
    ('times_txt.xls', 'Txt'),
    ('times_web.xls', 'Web')
]

def getExtration(df:pandas.DataFrame) -> tuple:
    encode   = df.iloc[[1]].values
    words    = df.iloc[[3]].values
    entities = df.iloc[[2]].values
    return encode[0],words[0],entities[0]

def sortData(df:pandas.DataFrame, value:int) -> pandas.DataFrame:
    transpose = df.T
    transpose = transpose.sort_values(value)
    return transpose.T

def average(x):
       assert len(x) > 0
       return float(sum(x)) / len(x)

def pearson_def(x, y):
       assert len(x) == len(y)
       n = len(x)
       assert n > 0
       avg_x = average(x)
       avg_y = average(y)
       diffprod = 0
       xdiff2 = 0
       ydiff2 = 0
       for idx in range(n):
           xdiff = x[idx] - avg_x
           ydiff = y[idx] - avg_y
           diffprod += xdiff * ydiff
           xdiff2 += xdiff * xdiff
           ydiff2 += ydiff * ydiff

       return diffprod / math.sqrt(xdiff2 * ydiff2)

def takePlots(xlsfile:str, title:str) -> None:
    df = pandas.read_excel(xlsfile,sheet_name=None)
    for name in df: 
        dfbyWords     = sortData(df[name],3)
        #dfbyEntities  = sortData(df[name],2)
        times,words,entities = getExtration(dfbyWords)
        print(pearson_def(times,entities))
        std_times    = statistics.stdev(times)
        std_entities = statistics.stdev(entities)
        plt.suptitle(title)
        plt.subplot(211)
        plt.grid(True)
        plt.title("%s times, σ = %.2f ms" %(title,round(std_times,2)) )
        plt.plot(words, times, 'o-')
        plt.ylabel("Times (ms)")
        plt.xlabel("Words")
        #times,_,entities = getExtration(dfbyEntities)
        plt.subplot(212)
        plt.grid(True)
        plt.title("%s Entities, σ = %.2f" %(title,round(std_entities,2)) )
        plt.plot(words, entities, 'o-')
        plt.ylabel("Entities")
        plt.xlabel("Words")
        plt.subplots_adjust(hspace=0.5)
        plt.savefig('result/%s_%s.png' % (title.replace(" ", "_"), name)) 
        plt.close()


if __name__ == "__main__":
    for file,title in list_files:
        takePlots(file, title)