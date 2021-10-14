import copy
import re
import os
import numpy as np
from scipy.signal import savgol_filter, find_peaks
import pandas as pd

from datetime import datetime, time

import matplotlib.pyplot as plt


def readLoadSeries(filename):
    df = pd.read_excel(filename, index_col=0)
    df = df.sort_index()
    df = np.array(df.iloc[:, 0:2])
    
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


def cutData(x, y, y_smooth, ddy, index):
    cutFlag = False
    if ddy[index] < -0.005:
        x = x[index:]
        y = y[index:]
        y_smooth = y_smooth[index:]
        cutFlag = True
    return x, y, y_smooth, cutFlag


def write(filename, x, y, y_smooth):
    with open(filename, 'w') as f:
        f.write('Time[s],Mass[g],MassSmooth[g]\n')
        for i in range(len(x)):
            f.write('%f,%f,%f\n' % (x[i], y[i], y_smooth[i]))


def processData(filename):
    series = readLoadSeries(filename)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    series = series[:, 5:]
    #print(series[-1])
    #plt.plot(series[0], series[1], c='grey')
    if re.search('降雪', filename) is not None:
        write(os.path.dirname(filename) + '/data.csv',
              series[0], series[1], series[1])
        return
    

    minIndex = np.where(series[1] == np.amin(series[1]))

    x = series[0][:minIndex[0][0]]
    y = series[1][:minIndex[0][0]]
    ax.plot(x, y, c='blue')

    y_smooth = savgol_filter(y, 101, 5)

    dydx = np.gradient(y_smooth, x[1] - x[0])
    dy_smooth = savgol_filter(dydx, 101, 5)
    ddydx = np.gradient(dy_smooth, x[1] - x[0])
    ddy_smooth = savgol_filter(ddydx, 101, 5)

    plistIndex = find_peaks(-1 * ddy_smooth, distance=20)

    plist = []
    for i in plistIndex[0]:
        plist.append(ddy_smooth[i])

    

    indexMin_ddy = plistIndex[0][plist.index(min(plist))]

    x_old = copy.deepcopy(x)
    y_smooth_old = copy.deepcopy(y_smooth)
    x, y, y_smooth, cutFlag = cutData(x, y, y_smooth, ddy_smooth, indexMin_ddy)
    #print(cutFlag)
    ax.plot(x_old, y_smooth_old, c='black')

    ax2 = ax.twinx()
    for i in plistIndex[0]:
        ax2.scatter(x_old[i], ddy_smooth[i])
    ax2.plot(x_old, ddy_smooth, c='green')
    if cutFlag:
        ax2.axvline(x_old[indexMin_ddy], -1, 1, c='red', linestyle='--')
    ax.plot(x, y, c='red')

    plt.savefig(os.path.dirname(filename) + '/res.jpg', dpi=400)
    write(os.path.dirname(filename) + '/data.csv', x, y, y_smooth)
    #plt.show()


def searchXls(dirname):
    dirList = []
    for x in os.walk(dirname):
        for item in os.listdir(x[0]):
            try:
                if item.split('.')[-1] == 'xls' and item[0] != '.':
                    dirList.append(x[0] + '/' + item)
            except IndexError:
                pass

    return dirList


if __name__ == '__main__':
    #filename = '/run/media/smilemax/Data/lzx_wind_tunnel/2 平屋面/平屋面吹雪/L300/7.5mps/7.5mps.xls'
    # processData(filename)

    dirList = searchXls('/run/media/smilemax/Data/lzx_wind_tunnel/')

    for filename in dirList:
        print('Now process ' + filename + '...', end='')
        processData(filename)
        print('done')


    #processData('/run/media/smilemax/Data/lzx_wind_tunnel/2 平屋面/平屋面吹雪/均匀流L500/5.39mps/5.39mps.xls')