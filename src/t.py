import json
import os
import pprint

from agent import ContextAgent
from context import Context
from search import News_searcher, GoogleSearcher
from sqlalchemy import create_engine

agent = ContextAgent(os.getenv("OPENAI_API_KEY"))
context = Context()

context.add_message("user", "wut s up")

res = agent.query(context)
print(res)