import os
from agent import ContextAgent
from context import Context
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
    offset = 150
    with engine.connect() as connection:
        result = connection.execute(f'SELECT * FROM IFND_sample Limit 100000 offset {offset}')

        # Append rows to the 'news' list
        for row in result:
            news.append(dict(row))  # Converting each row to dictionary for better readability

    for new in news:
        hasException = True
        while hasException:
            try:
                agent = ContextAgent(os.getenv("OPENAI_API_KEY"))
                context = Context()
                # few shot learning
                context.add_message("system", "You are a fake news detection expert. You use the Search tools as your primary "
                                              "resource to see if a news title is fake or not. You are impartial and only rely on "
                                              "proper sources to judge. You need to figure out whether the following news is fake "
                                              "or not. Provide a JSON object containing the key 'judgement' with either 'Fake', "
                                              "'Not Fake' or 'Disputed' and another key 'explanation' with the explanation at "
                                              "the "
                                              "very end. Do not return newlines and double quotes in the string should be "
                                              "replace by single quotes. Verify the following news: ")
                context.add_message("user", new['Statement'])

                # res = agent.query_with_functions(context)
                res = agent.query(context)
                # print(context)
                final_response = json.loads(res.replace("\n", " ").replace("\r", ""))
                judgement = final_response['judgement']
                explanation = final_response['explanation']

                with engine.connect() as connection:
                    escaped_content = context.get_messages().__str__().replace("'", "").replace('%', '%%')
                    escaped_explanation = explanation.replace("'", "").replace('%', '%%')
                    connection.execute(
                        f"UPDATE IFND_sample SET _model_label = '{judgement}', _model_explanation = '{escaped_explanation}', _model_response='{escaped_content}' WHERE id = {new['id']}")
                hasException = False
                offset += 1
                print(f"{offset} rows processed")


            except Exception as e:
                hasException = True
                print(e)
