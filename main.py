# FEATURE = [open, high, low, close, close adj, volume]

import sys
import os.path
sys.path.append(os.path.abspath(os.curdir) + '/func/')

from entity import *
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

pred      = predNext(Firms, models)

print(pred)

Firms[0].plot(0, 0, 1000)
