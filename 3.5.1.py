import sqlite3
import pandas as pd

connection = sqlite3.connect('currencies.db')
cursor = connection.cursor()
df = pd.read_csv('currencies.csv')
df = df.to_sql('currencies', connection, if_exists='replace', index=False)
connection.commit()
connection.close()


