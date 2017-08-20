# FEATURE = [open, high, low, close, close adj, volume]

import sys
import os.path
sys.path.append(os.path.abspath(os.curdir) + '/func/')

from classes import *
from regmodel import *

Apple     = Firm("Apple", "AAPL")
Adobe     = Firm("Adobe", "ADBE")
Amazon    = Firm("Amazon", "AMZN")
Facebook  = Firm("Facebook", "FB")
Google    = Firm("Google", "GOOG")
Intel     = Firm("Intel", "INTC")
Microsoft = Firm("Microsoft", "MSFT")
Nvidia    = Firm("Nvidia", "NVDA")
Qualcomm  = Firm("Qualcomm", "QCOM")
Tesla     = Firm("Tesla", "TSLA")
TI        = Firm("TI", "TXN")

Firms     = [Apple, Adobe, Amazon, Facebook, Google, Intel, Microsoft, Nvidia, Qualcomm, Tesla, TI]

IT        = Industry("IT", Firms)

models = []
for fidx in range(0, len(Firms)):
    temp = []
    for vidx in range(0, len(Firms[fidx].feature)):
        model = regModel(Firms, fidx, vidx)
        temp.append(model)
    models.append(temp)


print(models[0][0].summary())
predNext(Firms, models)
Apple.plot(0, 0, 1256)

# x = np.array([])
# x2 = np.array([])
# y = np.array([])
#
# for idx in range(1000, 1256):
#     print(Apple.prediction[0][idx] - Apple.feature[0][idx], idx-1000)
    # x = np.append(x, idx-1000)
    # x2 = np.append(x2, (idx-1000)**2)
    # y = np.append(y, Apple.prediction[0][idx] - Apple.feature[0][idx])

# # Firms[0].plot(0, 0, 1256)
# x = np.vstack((x, x2))
# x = sm.add_constant(x.T)
# res = sm.OLS(y, x).fit()
# print(res.summary())
