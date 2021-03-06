import matplotlib
import pandas as pd
import seaborn as sns
import numpy as np

#  Load the data from ``jester-data-1.csv'',
df = pd.read_csv('https://raw.githubusercontent.com/albanda/CE888/master/lab4-recommender/jester-data-1.csv')
print(df)

arr = df.values

# Check the dataset description to figure out which value you should replace with NaNs (the cells for which we don't have a rating). This is the test set.

ratedArr = df.replace(99, np.NaN)

#There's a column you need to remove because it doesn't contain ratings. Check the description of the dataset and figure out which one. Then drop it.

ratedArr = ratedArr.drop('74', axis=1)
print(ratedArr)


rated = np.where(arr!=99)
print(len(rated[0]), rated[1].shape)


def replace(orig, percentage=0.1):
  """
  Replaces 'percentage'% of the original values in 'orig' with 99's
  :param orig: original data array
  :param percentage: percentage of values to replace (0<percentage<1)
  """
  new_data = orig.copy()
  arrIsNaN = np.isnan(new_data)
  rated = np.where(arrIsNaN==False)
  n_rated = len(rated[0])
  idx = np.random.choice(n_rated, size=int(percentage*n_rated), replace=False)
  new_data[rated[0][idx], rated[1][idx]] = 99
  return new_data, (rated[0][idx], rated[1][idx])

#remove first column because it's the number how many users rated.
