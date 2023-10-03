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
    offset = 0
    with engine.connect() as connection:
        result = connection.execute(f'SELECT * FROM news where label="fake" limit 300 offset {offset}')

        # Append rows to the 'news' list
        for row in result:
            news.append(dict(row))  # Converting each row to dictionary for better readability

    for new in news:
        searcher = GoogleSearcher()
        agent = ContextAgent(os.getenv("OPENAI_API_KEY"))
        context = Context()

        # few shot learning
        context.add_message("system", "You are a fake news detection expert. You use the Search tool as your primary "
                                      "resource to see if a news title is fake or not. You are impartial and only rely on "
                                      "proper sources to judge. You need to figure out whether the following news is fake "
                                      "or not. Provide a JSON object containing the key 'judgement' with either 'Fake', "
                                      "'Not Fake' or 'Disputed' and another key 'explanation' with the explanation at "
                                      "the "
                                      "very end. Do not return newlines and double quotes in the string should be "
                                      "replace by single quotes. Verify the following news: ")

        context.add_message("user", f"{new['title']}")
        response = agent.query(context)

        final_response = json.loads(response.replace("\n", " ").replace("\r", ""))
        judgement = final_response['judgement']
        explanation = final_response['explanation']

        # print(new['title'])
        print(final_response)
        print("@@@@@@")

        with engine.connect() as connection:
            escaped_content = context.get_messages().__str__().replace("'", "").replace('%', '%%')
            escaped_explanation = explanation.replace("'", "").replace('%', '%%')
            connection.execute(
                f"UPDATE news SET base_gpt_label = '{judgement}', base_model_explanation = '{escaped_explanation}' WHERE id = {new['id']}")

        print(context)
        offset += 1
        print(f"{offset} rows processed")



    # # context.add_message("user", "AI is conscious.")
    # response = agent.query(context)
    # # print(response)
    # # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # context.add_message("user", "Give me google search queries you want to search to fact check this news. Give me "
    #                             "the queries in json format, where the key is 'queries' and the value is a list of "
    #                             "queries.")
    # response = agent.query(context)
    # # print(response)
    # context.add_message("user",
    #                     "only give me necessary queries.")
    # response = agent.query(context)
    # response = json.loads(response)
    # search_results = {}
    #
    # for query in response['queries']:
    #     print(query)
    #     result = searcher.search(query)
    #     search_results[query] = result
    # context.add_message("user", search_results.__str__() + "\n now base on these information tell me whether the news "
    #                                                        "is fake, not fake or disputed. If you are not certain "
    #                                                        "don't make one-sided conclusion?")





