from datetime import datetime, date, time
import binascii

import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


def hexRead(filename):
    with open(filename, 'rb') as f:
        times = []
        distances = []
        count = 0
        for line in f:
            if count != 0:
                #print(line[1:13].decode('UTF-8'), line[26:31].decode('UTF-8'))
                times.append(time.fromisoformat(line[1:13].decode('UTF-8')))
                distances.append(float(line[26:31].decode('UTF-8')))
            count += 1
    return times, distances


def write(filename, x, y):
    with open(filename, 'w') as f:
        for i in range(len(x)):
            f.write(str(x[i]) + ',' + str(y[i]) + '\n')


path = 'L300/8.5mps/'
files = [f for f in listdir(path) if isfile(join(path, f))]
filename = None
for f in files:
    if f[-4:] == '.TXT':
        filename = path + '/' + f
times, distances = hexRead(filename)

times_align = []
for t in times:
    t = datetime.combine(date.today(), t) - \
        datetime.combine(date.today(), times[0])
    times_align.append(t.seconds + t.microseconds / 1e6)

removeIndex = []
x = []
y = []
for i in range(len(times_align)):
    if distances[i] < 1.136 and distances[i] > 0.6:
        x.append(times_align[i])
        y.append(distances[i])

#plt.plot(x, y)

x_samples, y_samples = [], []
x_tmp, y_tmp = [], []

for i in range(len(x) - 1):
    x_tmp.append(x[i])
    y_tmp.append(y[i])
    if x[i + 1] - x[i] > 2:
        x_samples.append(x_tmp)
        y_samples.append(y_tmp)
        x_tmp, y_tmp = [], []
write(filename[:-4] + '.csv', x, y)
count = 0

for x, y in zip(x_samples, y_samples):
    if count % 2 == 1:
        reversed(x)
        reversed(y)
        start = x[0]
        for i in range(len(x)):
            x[i] = x[i] - start
        #plt.plot(x, y)
    else:
        start = x[0]
        for i in range(len(x)):
            x[i] = x[i] - start
        plt.plot(x, y, label=str(count))
    count += 1

plt.legend()
plt.show()
