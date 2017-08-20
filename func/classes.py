import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

import os.path
parpath = os.path.abspath(os.curdir)

TESTNUM = 1240

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

        self.openT = np.array([])
        self.highT = np.array([])
        self.lowT = np.array([])
        self.closeT = np.array([])
        self.adjT = np.array([])
        self.volumeT = np.array([])

        self.openP = np.array([])
        self.highP = np.array([])
        self.lowP = np.array([])
        self.closeP = np.array([])
        self.adjP = np.array([])
        self.volumeP = np.array([])

        self.readcsv()
        self.prediction = self.createPred()
        self.trend = self.calcTrend()

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

                    self.date = np.append(self.date, row[0])
                    self.open = np.append(self.open, float(row[1]))
                    self.high = np.append(self.high, float(row[2]))
                    self.low = np.append(self.low, float(row[3]))
                    self.close = np.append(self.close, float(row[4]))
                    self.adj = np.append(self.adj, float(row[5]))
                    self.volume = np.append(self.volume, float(row[6]))

        self.dateformatted = np.array(
            [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in self.date])

        self.feature = np.array([self.open, self.high, self.low, self.close, self.adj, self.volume])

    # NOTE: For testing purpose
    def createPred(self):
        for idx in range(0, TESTNUM):
            self.openP = np.append(self.openP, self.open[idx])
            self.highP = np.append(self.highP, self.high[idx])
            self.lowP = np.append(self.lowP, self.low[idx])
            self.closeP = np.append(self.closeP, self.close[idx])
            self.adjP = np.append(self.adjP, self.adj[idx])
            self.volumeP = np.append(self.volumeP, self.volume[idx])

        return np.stack((self.openP, self.highP, self.lowP, self.closeP, self.adjP, self.volumeP))


    def updatePred(self):
        return np.stack((self.openP, self.highP, self.lowP, self.closeP, self.adjP, self.volumeP))


    def addPred(self, fe, var):
        if (fe==0):
            self.openP = np.append(self.openP, var)
        elif (fe==1):
            self.highP = np.append(self.highP, var)
        elif (fe==2):
            self.lowP = np.append(self.lowP, var)
        elif (fe==3):
            self.closeP = np.append(self.closeP, var)
        elif (fe==4):
            self.adjP = np.append(self.adjP, var)
        elif (fe==5):
            self.volumeP = np.append(self.volumeP, var)
            self.prediction = self.updatePred()

        return


    # Analyze daily trend in percentage
    def calcTrend(self):
        self.openT = np.append(self.openT, 0)
        self.highT = np.append(self.highT, 0)
        self.lowT = np.append(self.lowT, 0)
        self.closeT = np.append(self.closeT, 0)
        self.adjT = np.append(self.adjT, 0)
        self.volumeT = np.append(self.volumeT, 0)

        for idx in range(1, TESTNUM):
            self.openT = np.append(self.openT, self.open[idx] - self.open[idx-1])
            self.highT = np.append(self.highT, self.high[idx] - self.high[idx-1])
            self.lowT = np.append(self.lowT, self.low[idx] - self.low[idx-1])
            self.closeT = np.append(self.closeT, self.close[idx] - self.close[idx-1])
            self.adjT = np.append(self.adjT, self.adj[idx] - self.adj[idx-1])
            self.volumeT = np.append(self.volumeT, self.volume[idx] - self.volume[idx-1])

        return np.stack((self.openT, self.highT, self.lowT, self.closeT, self.adjT, self.volumeT))


    def updateTrend(self):
        return np.stack((self.openT, self.highT, self.lowT, self.closeT, self.adjT, self.volumeT))


    def addTrend(self, fe, var):
        if (fe==0):
            self.openT = np.append(self.openT, var)
        elif (fe==1):
            self.highT = np.append(self.highT, var)
        elif (fe==2):
            self.lowT = np.append(self.lowT, var)
        elif (fe==3):
            self.closeT = np.append(self.closeT, var)
        elif (fe==4):
            self.adjT = np.append(self.adjT, var)
        elif (fe==5):
            self.volumeT = np.append(self.volumeT, var)
            self.trend = self.updateTrend()

        return


    def plot(self, fidx, idx, idx2):
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.figure(figsize=(40, 10))
        plt.ticklabel_format(style='sci', useLocale=False)
        plt.plot(self.dateformatted[idx:idx2], self.feature[fidx][idx:idx2], 'r', linestyle='solid')
        plt.plot(self.dateformatted[idx:idx2], self.prediction[fidx][idx:idx2], 'b', linestyle='solid')
        plt.plot(self.dateformatted[0:TESTNUM], self.prediction[fidx][0:TESTNUM], 'g', linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.savefig("test.png")

        return


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

    # Calculate overall industry average of each feature
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

    # TODO: Overall Trend Array (def calcTrend)
