import sys
import os
import time
import datetime
from config import *
import matplotlib.pyplot as plt


def log(msg, log_path, start=None):
    def get_progress_time(s):
        h = s // 3600
        s = s % 3600
        m = s // 60
        s = s % 60
        return (h, m, s)

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if start:
        delta_time = get_progress_time(int(time.time() - start))
        ts = str(delta_time[0]) + 'h' + str(delta_time[1]) + 'm' + str(delta_time[2]) + 's'
        log_msg = '{} training:{} {}'.format(time_now, ts, msg)
    else:
        log_msg = '{} {}'.format(time_now, msg)

    with open(log_path, 'a') as f:
        f.write(log_msg + '\n')
    sys.stdout.write(log_msg + '\n')


def draw_train_acc():
    files = []
    for f in os.listdir(os.path.dirname(LOG_PATH)):
        if f != os.path.basename(LOG_PATH) and f.split('.')[0] == os.path.basename(LOG_PATH).split('.')[0]:
            files.append(f)
    files.sort()
    acc = []
    with open(os.path.join(os.path.dirname(LOG_PATH), files[-1])) as f:
        for line in f.readlines():
            data = line.split(' ')[4]
            if data.startswith('----accuracy'):
                acc.append(data.split(':')[1])
    acc = [float(x) for x in acc]
    samples = [x * 100 for x in range(len(acc))]
    plt.plot(samples, acc)
    plt.show()


if __name__ == '__main__':
    draw_train_acc()
