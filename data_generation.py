import pandas as pd
import numpy as np

# parameters
n = 10000

income = np.random.normal(loc=800, scale=200, size=n)
weights = np.random.randint(1,10000,size=n)
sector = np.random.randint(1,4,size=n)

# save data
df = pd.DataFrame({'income': income, 'weights': weights, 'sector': sector})
df.to_csv('income_data.csv',index=False)
print('Data generated and saved')
