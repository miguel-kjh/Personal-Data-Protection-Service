import pandas
import statistics
import matplotlib.pyplot as plt
from statistics import mean

list_files = [
    ('times_docx.xls', 'Docx times'),
    ('times_pdf.xls', 'Pdf times'),
    ('times_tables.xls', 'Spreadsheets times'),
    ('times_txt.xls', 'Txt times'),
    ('times_web.xls', 'Web times')
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

def takePlots(xlsfile:str, title:str) -> None:
    df = pandas.read_excel(xlsfile,sheet_name=None)
    for name in df: 
        dfbyWords     = sortData(df[name],3)
        dfbyEntities  = sortData(df[name],2)
        times,words,_ = getExtration(dfbyWords)
        std = statistics.stdev(times)
        plt.suptitle("%s, σ = %.2f ms" %(title,round(std,2)) )
        plt.subplot(211)
        plt.grid(True)
        plt.plot(words, times, 'o-')
        plt.ylabel("Times (ms)")
        plt.xlabel("Words")
        times,_,entities = getExtration(dfbyEntities)
        plt.subplot(212)
        plt.grid(True)
        plt.plot(entities, times, 'o-')
        plt.ylabel("Times (ms)")
        plt.xlabel("Entities")
        plt.subplots_adjust(hspace=0.5)
        plt.savefig('result/%s_%s.png' % (title.replace(" ", "_"), name)) 
        plt.close()


if __name__ == "__main__":
    for file,title in list_files:
        takePlots(file, title)