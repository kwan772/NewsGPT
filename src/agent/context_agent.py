import openai
from agent import Agent
from src.context import Context

class ContextAgent(Agent):
    def __init__(self, api_key):
        super().__init__(api_key)

    def query(self, context):
        self.context = context
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model = self.model,
            messages=self.context.get_messages()
        )
        # print(self.context.get_messages())
        self.context.add_message("assistant", response["choices"][0]["message"]['content'])
        # print(response["choices"][0]["message"]['content'])
        return response["choices"][0]["message"]['content']

        # response = self.agent.run(prompt)
        # return response

