import os

import pandas as pd
from sqlalchemy import create_engine

# Load datasets
fake = pd.read_csv('../../../data/kaggle/Fake.csv')
real = pd.read_csv('../../../data/kaggle/True.csv')

# Randomly sample 50 rows from each dataset
fake_sample = fake.sample(n=100)
real_sample = real.sample(n=100)


# Add the necessary columns based on the dataset
fake_sample['source'] = 'kaggle'
fake_sample['label'] = 'fake'
real_sample['source'] = 'kaggle'
real_sample['label'] = 'real'


# Let's assume the 'title' column exists in the datasets. If not, adjust the name
# Extract only the relevant columns
fake_sample = fake_sample[['source', 'title', 'label', 'date']]
real_sample = real_sample[['source', 'title', 'label', 'date']]


# Define your MySQL connection parameters
USERNAME = "root"
PASSWORD = os.getenv("DB_PASSWORD")
HOST = 'localhost'
PORT = '3306'
DATABASE = 'news_gpt'

# Create a connection to the database
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# Insert the sampled data into your table (assuming you have a table called 'news_samples')
fake_sample.to_sql('news', engine, if_exists='append', index=False)
# real_sample.to_sql('news', engine, if_exists='append', index=False)

