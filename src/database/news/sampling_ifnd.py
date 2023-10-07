import os
from sqlalchemy import create_engine
import pandas as pd

# Define your MySQL connection parameters
USERNAME = "root"
PASSWORD = os.getenv("DB_PASSWORD")
HOST = 'localhost'
PORT = '3306'
DATABASE = 'news_gpt'

# Create a connection to the database
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

df = pd.read_sql("SELECT * FROM IFND where date > '2021-10-01'", engine)

fake_news = df[df['Label'] == 'Fake'].sample(200)

# Write the DataFrame to a new table named "selected_data"
fake_news.to_sql('IFND_sample', engine, if_exists='replace', index=False)
