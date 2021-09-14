import numpy as np
from scipy.signal import savgol_filter
import pandas as pd

from datetime import datetime

import matplotlib.pyplot as plt


def readLoadSeries(filename):
    df = pd.read_excel(filename)
    df = np.array(df.iloc[:, 1:3])
    times = []
    for i in df[:, 0]:
        times.append(datetime.fromisoformat(i))

    deltaTimes = []
    for i in range(len(times)):
        dt = times[i] - times[0]
        deltaTimes.append(dt.seconds + dt.microseconds / 1e6)

    deltaTimes = np.array(deltaTimes)

    series = np.vstack((deltaTimes, df[:, 1]))
    return series


def main():
    filename = './L300/8.0mps/8.0mps.xls'
    series = readLoadSeries(filename)

    #plt.plot(series[0], series[1], c='grey')
    minIndex = np.where(series[1] == np.amin(series[1]))
    y = series[1][:minIndex[0][0]]
    x = series[0][:minIndex[0][0]]

    #plt.plot(x, y, c='grey')

    y_smooth = savgol_filter(y, 101, 5)
    plt.plot(x, y_smooth, c='red')

    deltaY = []
    for i in range(len(y_smooth) - 1):
        deltaY.append(y_smooth[i + 1] - y_smooth[i])

    deltaY_smooth = savgol_filter(deltaY, 101, 5)

    ddY = []
    for i in range(len(deltaY_smooth) - 1):
        ddY.append(deltaY_smooth[i + 1] - deltaY_smooth[i])

    splitNum = 0
    flag = False
    indexMin_deltaY = np.where(deltaY == np.min(deltaY))[0][0]
    indexMax_deltaY = np.where(deltaY == np.min(np.abs(deltaY)))[0][0]
    index_deltaY = (indexMax_deltaY + indexMin_deltaY) // 2
    #plt.plot(x[:-1], deltaY, c='red')

    plt.plot([x[index_deltaY], x[index_deltaY]], [-10000, 10000], c='blue')
    #plt.ylim(ymin=-3, ymax=1)
    plt.ylim(ymin=400, ymax=1000)
    plt.show()


if __name__ == '__main__':
    main()
