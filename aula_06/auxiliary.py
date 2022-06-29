import pandas as pd

df = pd.read_csv(r'C:\Users\andre\repos\python-zero-ao-ds\datasets\kc_house_data.csv')

# print(df['zipcode'])
#
# print(df.loc[df['zipcode'].isin([98178, 98125]), 'id'])
#
# print(df.dtypes)

print(df.columns)
print(df.dtypes)