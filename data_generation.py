import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import seaborn as sns

# parameters
n = 10000

income = np.random.normal(loc=800, scale=200, size=n)
weights = np.random.randint(1,10000,size=n)
sector = np.random.randint(1,7,size=n)
print(sum(weights))

# plot
# sns.kdeplot(income, weights=weights)

# save data
df = pd.DataFrame({'income': income, 'weights': weights, 'sector': sector})
df.to_csv('income_data.csv',index=False)
print('Data generated and saved')
