import os

import pandas as pd
from sqlalchemy import create_engine

# Load datasets
sample = pd.read_csv('../../../data/kaggle/IFND.csv', encoding='ISO-8859-1')


# Define your MySQL connection parameters
USERNAME = "root"
PASSWORD = os.getenv("DB_PASSWORD")
HOST = 'localhost'
PORT = '3306'
DATABASE = 'news_gpt'

# Create a connection to the database
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

sample['Date'] = pd.to_datetime(sample['Date'], errors='coerce')
sample = sample.dropna(subset=['Date'])

# Insert the sampled data into your table (assuming you have a table called 'news_samples')
sample.to_sql('IFND', engine, if_exists='append', index=False)
# real_sample.to_sql('news', engine, if_exists='append', index=False)
# Display all columns
pd.set_option('display.max_columns', None)

# Display all rows
pd.set_option('display.max_rows', None)
# display all rows in sample
# print(sample)
