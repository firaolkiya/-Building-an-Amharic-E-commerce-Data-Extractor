import pandas as pd

df = pd.read_csv('data/telegram_data.csv')
df['Date'] = pd.to_datetime(df['Date'])


print(len(df))
print(df.head())