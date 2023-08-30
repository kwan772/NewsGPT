from abc import ABC, abstractmethod


class Searcher(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def search(self, query):
        pass
