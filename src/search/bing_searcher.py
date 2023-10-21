import os
import pprint

import requests

from .searcher import Searcher

class BingSearcher(Searcher):
    def __init__(self):
        self.trusted_sources = ["https://www.nytimes.com",
                                "https://www.washingtonpost.com",
                                "https://www.cnn.com",
                                "https://www.nbcnews.com",
                                "https://www.wsj.com",
                                "https://www.reuters.com",
                                "https://apnews.com",
                                "https://www.bbc.com/news",
                                "https://www.usatoday.com",
                                "https://www.cbsnews.com",
                                "https://www.abcnews.go.com",
                                "https://www.npr.org",
                                "https://www.politico.com",
                                "https://www.foxnews.com",
                                "https://www.bloomberg.com",
                                "https://www.latimes.com",
                                "https://www.chicagotribune.com",
                                "https://www.theguardian.com/us",
                                "https://timesofindia.indiatimes.com",
                                "https://www.thehindu.com",
                                "https://www.ndtv.com",
                                "https://indianexpress.com",
                                "https://www.hindustantimes.com",
                                "https://economictimes.indiatimes.com",
                                "https://www.dnaindia.com",
                                "https://www.news18.com",
                                "https://www.firstpost.com",
                                "https://www.indiatoday.in",
                                "https://www.thequint.com",
                                "https://www.deccanherald.com",
                                "https://www.asianage.com",
                                "https://www.business-standard.com",
                                "https://www.telegraphindia.com",
                                "https://www.financialexpress.com",
                                "https://www.livemint.com",
                                "https://www.outlookindia.com",
                                "https://finance.yahoo.com"
                                ]

    
    def general_search(self, query):
        # Not filtered!!
        # Web search

        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/search"
            # , headers = {'Ocp-Apim-Subscription-Key': os.getenv("BING_KEY")} #type: ignore
            , headers = {'Ocp-Apim-Subscription-Key': "1562b40d25f3455c95346bc10aadc0a7"} #type: ignore
            , params = {
                'q': query
                , 'mkt': 'en-US' # May change this later...
            }
        )
        # print(response.json())
        response = response.json()['webPages']['value']

        response2return = [{k: v for k, v in d.items() if k in ['name','url','snippet']}
    for d in response if any(trusted_url in d.get('url', '') for trusted_url in self.trusted_sources)]
        # print([{k: v for k, v in d.items() if k in ['name','url','snippet']}
    # for d in response])
        # print(response2return)

        if len(response2return) > 0:
            response2return = response2return[0]
        
        return response2return

    def knowledge_graph_search(self, query):

        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/entities"
            , headers = {'Ocp-Apim-Subscription-Key': "1562b40d25f3455c95346bc10aadc0a7"} #type: ignore
            , params = {
                'q': query
                , 'mkt': 'en-US' # May change this later...
            }
        )

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
            , headers = {'Ocp-Apim-Subscription-Key': "1562b40d25f3455c95346bc10aadc0a7"} #type: ignore
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
    general_results = searcher.general_search("Trump wants Postal Service to charge 'much more' for Amazon shipments")
    # news_results = searcher.news_search("Trump wants Postal Service to charge 'much more' for Amazon shipments.")
    # print(pprint.pprint(knowledge_graph_results))
    print(knowledge_graph_results)
    print(general_results)