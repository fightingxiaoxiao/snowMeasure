from datetime import datetime, date, time
import binascii

import matplotlib.pyplot as plt


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


times, distances = hexRead('L300/8.5mps/SaveWindows2021_9_12_16-54-07.TXT')

times_align = []
for t in times:
    t = datetime.combine(date.today(), t) - \
        datetime.combine(date.today(), times[0])
    times_align.append(t.seconds + t.microseconds / 1e6)

removeIndex = []
x = []
y = []
for i in range(len(times_align)):
    if distances[i] < 1.8 and distances[i] > 0.6:
        x.append(times_align[i])
        y.append(distances[i])

write('test.csv', x, y)
plt.plot(x, y)

plt.show()
