import numpy as np
import statsmodels.api as sm
Y = [1,3,4,5,2,3,4]
X = range(1,8)
print(X)
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results = model.fit()
print(results.params)
results.tvalues
print(Y)
print(X)
print(results.t_test([1, 0]))
print(results.f_test(np.identity(2)))