# FEATURE = [formatted date, open, high, low, close, close adj, volume]

import sys, os.path, math
sys.path.append(os.path.abspath(os.curdir)+'/func/')

from entity import *

import pandas as pd
import statsmodels.api as sm
# from statsmodels.formula.api import ols
Apple = Firm("Apple","AAPL")
Adobe = Firm("Adobe", "ADBE")
Amazon = Firm("Amazon", "AMZN")
Facebook = Firm("Facebook", "FB")
Google = Firm("Google", "GOOG")
Intel = Firm("Intel", "INTC")
Microsoft = Firm("Microsoft", "MSFT")
Nvidia = Firm("Nvidia", "NVDA")
Qualcomm = Firm("Qualcomm", "QCOM")
Tesla = Firm("Tesla", "TSLA")
TI = Firm("TI", "TXN")

Firms = [Apple, Adobe, Amazon, Facebook, Google, Intel, Microsoft, Nvidia, Qualcomm, Tesla, TI]

IT = Industry("IT", Firms)

for i in range(0, len(Firms)):
    for j in range(1, len(Firms[i].feature)):
        if i==0 and j==1:
            xdom = Firms[i].feature[j][0:-1]
        else:
            xdom = np.vstack((xdom, Firms[i].feature[j][0:-1]))

xdom = sm.add_constant(xdom.T)


xdom = xdom.tolist()
ydom = Apple.feature[1][1:].tolist()
var = sm.OLS(ydom, xdom)
model = var.fit()

# res = sm.OLS(Apple.feature[1][1:], xdom).fit()
print(model.summary())

print(model.params)

pred = []

for i in range(0, 1256):
    total = 0
    for fi in range(0, len(Firms)):
        for fe in range(1, len(Firms[fi].feature)):
            total += Firms[fi].feature[fe][i] * model.params[6*fi + (fe-1) + 1]
    pred.append(total)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.figure(figsize=(20,10))

plt.plot(Apple.feature[0][1:], pred, 'r')
plt.plot(Apple.feature[0][1:], Apple.feature[1][1:], 'b')

plt.gcf().autofmt_xdate()
plt.savefig("test.png", linestyle='solid')


for i in range(0, len(pred)):
    print(Apple.feature[1][i+1], pred[i])
