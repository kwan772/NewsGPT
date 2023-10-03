import json
import os
import pprint

from agent import StatelessAgent, ContextAgent
from context import Context
from search import News_searcher, GoogleSearcher
from sqlalchemy import create_engine

if __name__ == "__main__":
    # Define your MySQL connection parameters
    USERNAME = "root"
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'news_gpt'
    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    news = []
    offset = 94

    new = {"title": "Senior U.S. Republican senator: 'Let Mr. Mueller do his job'",
           "date": "2017-12-31"}

    searcher = GoogleSearcher()
    agent = ContextAgent(os.getenv("OPENAI_API_KEY"))
    context = Context()

    print(searcher.search("Nehru-Gandhi Family Wasn't Celebrating Birthday When ISRO"))





