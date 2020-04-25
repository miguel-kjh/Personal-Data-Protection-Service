import pandas
import statistics
import matplotlib.pyplot as plt

def getExtration(df:pandas.DataFrame) -> tuple:
    times = df.iloc[[1]].values
    words = df.iloc[[3]].values
    return times[0],words[0]

def sortData(df:pandas.DataFrame) -> pandas.DataFrame:
    transpose = df.T
    transpose = transpose.sort_values(3)
    return transpose.T

if __name__ == "__main__":
    df = pandas.read_csv('times_web.csv')
    print(df)
    df = sortData(df)
    print(df)
    times,words = getExtration(df)
    times.sort()
    print(times, words)
    print(statistics.stdev(times))
    plt.plot(words,times)
    plt.show()

    