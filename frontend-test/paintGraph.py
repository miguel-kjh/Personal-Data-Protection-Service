import pandas
import statistics
import plotly.graph_objects as go
import plotly

#plotly.io.orca.config.executable = '/usr/bin/orca'

def getExtration(df:pandas.DataFrame) -> tuple:
    encode = df.iloc[[1]].values
    words  = df.iloc[[3]].values
    return encode[0],words[0]

def sortData(df:pandas.DataFrame) -> pandas.DataFrame:
    transpose = df.T
    transpose = transpose.sort_values(3)
    return transpose.T

if __name__ == "__main__":
    df = pandas.read_csv('times_tables.csv')
    print(df)
    df = sortData(df)
    print(df)
    times,words = getExtration(df)
    std = statistics.stdev(times)
    print(std)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=words,
        y=times,
        name="Anonimization"
    ))

    title = "Spreadsheets times, σ = %.2f ms" %(round(std,2)) 
    fig.update_layout(
        title=title,
        xaxis_title="Word",
        yaxis_title="Times"
    )

    fig.show()



    