import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

import os.path
parpath = os.path.abspath(os.curdir)


class Firm():
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

        self.date = np.array([])
        self.dateformatted = np.array([])

        self.open = np.array([])
        self.high = np.array([])
        self.low = np.array([])
        self.close = np.array([])
        self.adj = np.array([])
        self.volume = np.array([])
        self.feature = []

        self.openT = np.array([])
        self.highT = np.array([])
        self.lowT = np.array([])
        self.closeT = np.array([])
        self.adjT = np.array([])
        self.volumeT = np.array([])
        self.trend = []

        self.readcsv()

    # Read or Update data
    def readcsv(self):
        with open(parpath + '/dataset/' + self.filename + '.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile)
            # Retrive new data
            if not self.date:
                dateidx = 0
                for row in reader:
                    if not dateidx:
                        dateidx = 1
                        continue
                    self.date = np.append(self.date, row[0])
                    self.open = np.append(self.open, float(row[1]))
                    self.high = np.append(self.high, float(row[2]))
                    self.low = np.append(self.low, float(row[3]))
                    self.close = np.append(self.close, float(row[4]))
                    self.adj = np.append(self.adj, float(row[5]))
                    self.volume = np.append(self.volume, float(row[6]))
            # Update existing data
            else:
                for row in reader:
                    if row[0] == self.date[-1]:
                        break
                for row in reader:
                    self.date = np.append(self.date, row[0])
                    self.open = np.append(self.open, float(row[1]))
                    self.high = np.append(self.high, float(row[2]))
                    self.low = np.append(self.low, float(row[3]))
                    self.close = np.append(self.close, float(row[4]))
                    self.adj = np.append(self.adj, float(row[5]))
                    self.volume = np.append(self.volume, float(row[6]))

        self.dateformatted = np.array(
            [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in self.date])

        self.feature = [self.open, self.high,
                        self.low, self.close, self.adj, self.volume]

        return

    def plot(self):
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.figure(figsize=(40, 10))
        plt.ticklabel_format(style='sci', useLocale=False)
        plt.plot(self.feature[0], self.feature[1], 'r')
        plt.gcf().autofmt_xdate()
        plt.savefig("test.png", linestyle='solid')

        return

    def calcTrend(self):
        self.trend = [self.openT, self.highT, self.lowT,
                      self.closeT, self.adjT, self.volumeT]

        for fidx in range(0, len(self.feature)):
            for idx in range(1, len(self.feature[fidx])):
                diff = self.feature[fidx][idx] - self.feature[fidx][idx - 1]
                perdiff = diff / self.feature[fidx][idx]
                self.trend[fidx] = np.append(self.trend[fidx], perdiff)


class Industry():
    def __init__(self, name, array):
        self.name = name
        self.list = array
        self.date = array[0].dateformatted
        self.open = np.array([])
        self.high = np.array([])
        self.low = np.array([])
        self.close = np.array([])
        self.adj = np.array([])
        self.volume = np.array([])
        self.feature = [self.open, self.high, self.low,
                        self.close, self.adj, self.volume]
        self.calcavg()

    def calcavg(self):
        idx = len(self.date)
        num = len(self.list)
        for day in range(0, idx):
            for feat in range(0, len(self.feature)):
                total = 0
                for firm in self.list:
                    total += firm.feature[feat][day]
                self.feature[feat] = np.append(self.feature[feat], total / num)

        return
