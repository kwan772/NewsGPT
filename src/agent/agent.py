from abc import ABC, abstractmethod
# from langchain import LLMMathChain, OpenAI, SerpAPIWrapper
# from langchain.agents import initialize_agent, Tool
# from langchain.agents import AgentType
# from langchain.chat_models import ChatOpenAI
import openai


class Agent(ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__()
        # llm = ChatOpenAI(openai_api_key= self.api_key, temperature=0, model="gpt-3.5-turbo")
        # self.agent = initialize_agent([], llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
        self.gpt_config = {
            "engine": "gpt-3.5-turbo-16k"
        }
        self.model = "gpt-3.5-turbo-16k"


    @abstractmethod
    def query(self, context):
        pass
