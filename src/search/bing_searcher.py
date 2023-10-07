import os
import pprint

import requests

from .searcher import Searcher

class BingSearcher(Searcher):
    
    def general_search(self, query):
        # Not filtered!!
        # Web search

        print(query)
        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/search"
            , headers = {'Ocp-Apim-Subscription-Key': os.getenv("BING_KEY")} #type: ignore
            , params = {
                'q': query
                , 'mkt': 'en-US' # May change this later...
            }
        )
        print(response.json())
        response = response.json()['webPages']['value']
    
        response2return = [{k: v for k, v in d.items() if k in ['name','url','snippet']} for d in response]
        
        return response2return

    def knowledge_graph_search(self, query):

        print(query)
        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/entities"
            , headers = {'Ocp-Apim-Subscription-Key': os.getenv("BING_KEY")} #type: ignore
            , params = {
                'q': query
                , 'mkt': 'en-US' # May change this later...
            }
        )

        print(response.json())
        response = response.json()['entities']['value']

        
        entities = []
        
        if len(response) >= 1:
            for entity in response:
                entities.append({
                    "Type": "Most likely match" if entity['entityPresentationInfo']['entityScenario'] == 'DominantEntity' else "Potential match"
                    , "Name": entity['name']
                    , "description": entity["description"]
                })
        
        return entities

        
    def news_search(self, query):
        # Only returns news descriptions :(
        
        
        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/news/search"
            , headers = {'Ocp-Apim-Subscription-Key': os.getenv("BING_KEY")} #type: ignore
            , params = {
                'q': query
                , 'mkt': 'en-US' # May change this later...
            }
        )
        
        news = response.json()['value']
        cleaned_news = []
        
        for article in news:
            cleaned_news.append({
                "source_name": article['provider'][0]['name']
                , "headline": article['name']
                , "description": article['description']
                , "url": article['url']
            })
        
        return cleaned_news

    def search(self, query):
        pass
        
        
if __name__ == "__main__":
    searcher = BingSearcher()

    knowledge_graph_results = searcher.knowledge_graph_search("Donald Trump age")
    general_results = searcher.general_search("Trump wants Postal Service to charge 'much more' for Amazon shipments.")
    # news_results = searcher.news_search("Trump wants Postal Service to charge 'much more' for Amazon shipments.")
    print(pprint.pprint(knowledge_graph_results))