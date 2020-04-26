import pandas
import statistics
import plotly.graph_objects as go

def getExtration(df:pandas.DataFrame) -> tuple:
    encode = df.iloc[[1]].values
    extr   = df.iloc[[0]].values
    words  = df.iloc[[3]].values
    return encode[0],extr[0],words[0]

def sortData(df:pandas.DataFrame) -> pandas.DataFrame:
    transpose = df.T
    transpose = transpose.sort_values(3)
    return transpose.T

if __name__ == "__main__":
    df = pandas.read_csv('times_web.csv')
    print(df)
    df = sortData(df)
    print(df)
    encode,extr,words = getExtration(df)
    #print(statistics.stdev(times))
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=words,
        y=encode,
        name="Anonimization"
    ))


    fig.add_trace(go.Scatter(
        x=words,
        y=extr,
        name="Extraction"
    ))

    fig.update_layout(
        title="Web times",
        xaxis_title="Word",
        yaxis_title="Times"
    )

    fig.show()

    