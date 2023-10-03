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

df = pd.read_sql("SELECT * FROM IFND", engine)


categories = ["COVID-19", "VIOLENCE", "ELECTION", "GOVERNMENT", "POLITICS", "TRAD"]
selected_rows = []

for category in categories:
    print(category)
    fake_news = df[(df['Category'] == category) & (df['Label'] == 'Fake')].sample(50)
    real_news = df[(df['Category'] == category) & (df['Label'] == 'TRUE')].sample(50)
    selected_rows.extend([fake_news, real_news])

new_df = pd.concat(selected_rows, ignore_index=True)

# Write the DataFrame to a new table named "selected_data"
new_df.to_sql('IFND_sample', engine, if_exists='replace', index=False)
