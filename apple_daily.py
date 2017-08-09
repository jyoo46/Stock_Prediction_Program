# Regression Model built for Apple's next-day stock price (open)

# FEATURE = [formatted date, open, high, low, close, close adj, volume]

import sys
import os.path
sys.path.append(os.path.abspath(os.curdir) + '/func/')

from entity import *

Apple = Firm("Apple", "AAPL")
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

Firms = [Apple, Adobe, Amazon, Facebook, Google,
         Intel, Microsoft, Nvidia, Qualcomm, Tesla, TI]

suc = fail = 0
pred = []
for idx in range(0, 1256):
    prev = Apple.feature[1][idx]
    temp = -0.25686 + Apple.feature[1][idx] * -0.18745 + Apple.feature[2][idx] * 0.24151 + Apple.feature[4][idx] * 0.94114 + Apple.feature[-1][idx] * -1.86253e-9 + Adobe.feature[4][idx] * 0.02041 + Google.feature[1][idx] * - \
        0.02786 + Google.feature[3][idx] * 0.02511 + Microsoft.feature[-1][idx] * 5.05086e-9 + \
        Qualcomm.feature[3][idx] * -0.10377 + Qualcomm.feature[4][idx] * \
        0.11060 + TI.feature[-1][idx] * 4.045208e-8
    pred.append(temp)
    actual = Apple.feature[1][idx + 1]
    if temp - prev < 0 and actual - prev < 0:
        status = "SUCCESS!"
        suc += 1
    elif temp - prev > 0 and actual - prev > 0:
        status = "SUCCESS!"
        suc += 1
    else:
        status = "MISS"
        fail += 1
    print(status + " Expected: " + str(temp) + ", Actual: " + str(actual))

print("Success: " + str(suc) + ", Fail: " + str(fail))


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.figure(figsize=(20, 10))

plt.plot(Apple.feature[0][1:20], pred[0:19], 'r')
plt.plot(Apple.feature[0][1:20], Apple.feature[1][1:20], 'b')

plt.gcf().autofmt_xdate()
plt.savefig("test.png", linestyle='solid')
