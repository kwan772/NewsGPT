import os

from .searcher import Searcher
from newsapi import NewsApiClient

class News_searcher(Searcher):
    def __init__(self):
        super().__init__()
        self.newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

    def search(self, query):
        all_articles = self.newsapi.get_everything(q=query,
                                              language='en',
                                              sort_by='relevancy',
                                              page=2)
        articles = all_articles['articles']
        for art in articles:
            print(art)
        return all_articles