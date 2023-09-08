import os
import pprint

import requests

from .searcher import Searcher


class GoogleSearcher(Searcher):
    def __init__(self):
        super().__init__()
        with open('../data/trusted_source/google_search_sources', 'r') as file:
            self.trusted_sources = file.readlines()
        # Remove any newline characters at the end of each line
        self.trusted_sources = [line.strip() for line in self.trusted_sources]
        # print(self.trusted_sources)

    def search(self, query):
        params = {"engine": "google", "q": query, "api_key": os.getenv("SERP_API_KEY")}
        response = requests.get("https://serpapi.com/search", params=params)
        response = response.json()
        # print(response)

        return self.filter_results(response)

    def filter_results(self, response):
        results = []
        # pprint.pprint(response)
        if "answer_box" in response and self.is_valid_source(response["answer_box"]["source"]):
            return {
                "title": response["answer_box"]["title"],
                "link": response["answer_box"]["link"],
                "snippet": response["answer_box"]["snippet"],
                "source": response["answer_box"]["source"]
            }
        for result in response["organic_results"]:
            if self.is_valid_source(result["source"]):
                return {
                    "title": result["title"],
                    "link": result["link"],
                    "snippet": result["snippet"],
                    "source": result["source"]
                }
        return results

    def is_valid_source(self, source):
        if self.trusted_sources.__contains__(source):
            return True
