from config import *
import matplotlib.pyplot as plt


acc = []
with open(LOG_PATH) as f:
    logs = f.read().split('2018-10')
    for line in logs[1:]:
        if line.split(' ')[4].startswith('----accuracy'):
            acc.append(line.split(' ')[5])
acc = [float(x) for x in acc]
samples = [x*100 for x in range(len(acc))]

plt.plot(samples, acc)
plt.show()
