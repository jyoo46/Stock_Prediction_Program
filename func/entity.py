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
        self.date = np.array([])
        self.dateformatted = np.array([])
        self.p_open = np.array([])
        self.p_high = np.array([])
        self.p_low = np.array([])
        self.p_close = np.array([])
        self.p_adj = np.array([])
        self.volume = np.array([])
        self.filename = filename
        self.readcsv()

    # Read or Update data
    def readcsv(self):
        with open(parpath+'/dataset/'+self.filename+'.csv', 'rb') as csvfile:
            reader=csv.reader(csvfile)
            # Retrive new data
            if not self.date:
                dateidx = 0
                for row in reader:
                    if not dateidx:
                        dateidx = 1
                        continue
                    self.date = np.append(self.date,row[0])
                    self.p_open = np.append(self.p_open,float(row[1]))
                    self.p_high = np.append(self.p_high,float(row[2]))
                    self.p_low = np.append(self.p_low,float(row[3]))
                    self.p_close= np.append(self.p_close,float(row[4]))
                    self.p_adj = np.append(self.p_adj,float(row[5]))
                    self.volume = np.append(self.volume,float(row[6]))
            # Update existing data
            else:
                for row in reader:
                    if row[0] == self.date[-1]:
                        break
                for row in reader:
                    self.date = np.append(self.date,row[0])
                    self.p_open = np.append(self.p_open,float(row[1]))
                    self.p_high = np.append(self.p_high,float(row[2]))
                    self.p_low = np.append(self.p_low,float(row[3]))
                    self.p_close= np.append(self.p_close,float(row[4]))
                    self.p_adj = np.append(self.p_adj,float(row[5]))
                    self.volume = np.append(self.volume,float(row[6]))

        self.dateformatted = np.array([dt.datetime.strptime(d,'%Y-%m-%d').date() for d in self.date])
        self.feature = [self.dateformatted, self.p_open, self.p_high, self.p_low, self.p_close, self.p_adj, self.volume]

        return

    def plot(self):
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.figure(figsize=(40,10))
        # plt.xlabel("Date(YYYY-MM-DD)")
        # plt.ylabel("Dollars ($)")
        plt.ticklabel_format(style='sci', useLocale=False)
        plt.plot(self.feature[0], self.feature[1], 'r')
        plt.gcf().autofmt_xdate()
        plt.savefig("test.png", linestyle='solid')

        return


class Industry():
    def __init__(self, name, array):
        self.name = name
        self.list = array
        self.date = array[0].feature[0]
        self.p_open = np.array([])
        self.p_high = np.array([])
        self.p_low = np.array([])
        self.p_close = np.array([])
        self.p_adj = np.array([])
        self.volume = np.array([])
        self.feature = [self.date, self.p_open, self.p_high, self.p_low, self.p_close, self.p_adj, self.volume]
        self.calcavg()

    def calcavg(self):
        idx = len(self.date)
        num = len(self.list)
        for day in range (0, idx):
            for feat in range (1, 7):
                total = 0
                for firm in self.list:
                    total += firm.feature[feat][day]
                self.feature[feat] = np.append(self.feature[feat], total/num)

        return
