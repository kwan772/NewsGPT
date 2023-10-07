import os

import pandas as pd
from sqlalchemy import create_engine

# Assuming each line in the text file is a separate headline
sample = pd.read_table("../../../data/kaggle/newrecentTrue.txt", header=None, names=['Statement'])


# Define your MySQL connection parameters
USERNAME = "root"
PASSWORD = os.getenv("DB_PASSWORD")
HOST = 'localhost'
PORT = '3306'
DATABASE = 'news_gpt'

# Create a connection to the database
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")


missing_columns = ['Image','Web','Category','Date','Label']
for column in missing_columns:
    sample[column] = None

print(sample)
# Insert the sampled data into your table (assuming you have a table called 'news_samples')
sample.to_sql('IFND_sample', engine, if_exists='append', index=False)
# real_sample.to_sql('news', engine, if_exists='append', index=False)
# Display all columns
pd.set_option('display.max_columns', None)

# Display all rows
pd.set_option('display.max_rows', None)
# display all rows in sample
# print(sample)
