import statsmodels.api as sm
import numpy as np
import math

TESTNUM = 1240
ESTITV = 1

# Build multiple linear regression model of given firm(yidx) by
def regModel(Firms, yidx, fidx):
    for i in range(0, len(Firms)):
        for j in range(0, len(Firms[i].feature)):
            if i == 0 and j == 0:
                xdom = Firms[i].feature[j][0:TESTNUM]
            else:
                xdom = np.vstack((xdom, Firms[i].feature[j][0:TESTNUM]))

        for j in range(0, len(Firms[i].trend)):
            xdom = np.vstack((xdom, Firms[i].trend[j][0:TESTNUM]))

    xdom = sm.add_constant(xdom.T)

    res = sm.OLS(Firms[yidx].feature[fidx][ESTITV:TESTNUM+ESTITV], xdom).fit()

    return res


# def predNext(Firms, model):
#     prediction = []
#
#     for i in range(0, len(Firms[0].feature[0][1:])):
#         total = 0
#         for fi in range(0, len(Firms)):
#             for fe in range(0, len(Firms[fi].feature)):
#                 if (model.pvalues[0] < 0.05):
#                     total += model.params[0]
#                 if (model.pvalues[6 * fi + fe + 1] < 0.05):
#                     total += Firms[fi].feature[fe][i] * model.params[6 * fi + fe + 1]
#         prediction.append(total)
#
#     return prediction

def predNext(Firms, models):
    for idx in range(TESTNUM, len(Firms[0].feature[0])):
        for fidx in range(0, len(Firms)):
            pred = []
            for midx in range(0, 6):
                pred.append(models[fidx][midx].params[0])

                for fi in range(0, len(Firms)):
                    for fe in range(0, len(Firms[fi].feature)):
                        pred[midx] += Firms[fi].prediction[fe][idx-ESTITV] * models[fidx][midx].params[6 * fi + fe + 1]


            for midx in range(6, 12):
                for fi in range(0, len(Firms)):
                    for fe in range(0, len(Firms[fi].trend)):
                        pred[midx-6] += Firms[fi].trend[fe][idx-ESTITV] * models[fidx][midx-6].params[(6 * fi + fe + 1) + 66]

                Firms[fidx].addPred(midx-6, pred[midx-6])

            for midx in range(0, 6):
                Firms[fidx].addTrend(midx, Firms[fidx].prediction[midx][-1] - Firms[fidx].prediction[midx][-2])

    return


def calcError(Firms, prediction, firmidx, featidx):
    totalerr = 0
    for i in range(0, len(prediction)):
        real = Firms[firmidx].feature[featidx][i + 1]
        pred = prediction[i]
        error = math.fabs(real - pred) / real
        totalerr += error

    return totalerr / len(prediction)

def checkTrendPrediction(Firms, prediction, firmidx, featidx):
    suc = fail = 0
    for i in range(1, len(prediction)):
        real = Firms[firmidx].feature[featidx][i + 1]
        real_p = Firms[firmidx].feature[featidx][i]
        pred = prediction[i]
        pred_p = prediction[i - 1]

        if ((real - real_p) > 0 and (pred - pred_p) > 0) or ((real - real_p) < 0 and (pred - pred_p) < 0):
            suc += 1
        else:
            fail += 1

    return suc, fail
