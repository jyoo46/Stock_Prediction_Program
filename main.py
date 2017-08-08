# FEATURE = [formatted date, open, high, low, close, close adj, volume]

import sys, os.path
sys.path.append(os.path.abspath(os.curdir)+'/func/')

from entity import *

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

print(IT.feature[1])

Apple.plot()
