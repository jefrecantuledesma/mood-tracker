import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def obtain_data(days: int, sprdshtdir: str) -> None:
    df = pd.read_excel(
        io=sprdshtdir,
        usecols="A:B"
    )

    last_rows=df.tail(days)

    dates=last_rows["Date"].tolist()
    moods=last_rows["Mood"].tolist()

    #tuples = [df.iloc[i].tolist() for i in range(df.shape[0])]

    print(dates, moods)
    return dates, moods

def visualize(dates: tuple, moods: tuple):
    plt.plot(dates, moods, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.grid()
    days = len(dates)
    title = "Your Mood Over the Last " + str(days) + " Days"
    plt.title(title)
    plt.show()


