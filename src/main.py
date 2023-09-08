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
    offset = 94
    with engine.connect() as connection:
        result = connection.execute(f'SELECT * FROM news limit 300 offset {offset}')

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

        # context.add_message("user", "The news title is: Republican Senator Gets Dragged For Going After Robert Mueller. "
        #                             "Give me google search queries you want to search to fact check this news. Give me "
        #                             "the queries in json format, where the key is 'queries' and the value is a list of "
        #                             "queries.")
        # context.add_message("assistant", '{"queries":["Republican Senator Gets Dragged For Going After Robert Mueller."]}')
        # context.add_message("user", """{"Republican Senator gets dragged for going after robert mueller." :
        # {
        # "title": "Republicans Take Their Shot at Mueller—And Narrowly Miss",
        # "link": "https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/",
        # "snippet": "Former Special Counsel Robert Mueller (center) faced attacks from Representatives John Ratcliffe (left) and Louie Gohmert (right).",
        # "source": "The Atlantic"
        # }
        # }
        # Base on the google searches, tell me whether the news title is fake or real or disputed.
        # """)
        # context.add_message("assistant", """{"judgement":"Fake", "explanation": "No trusted news source has mentioned
        # that republican senator was dragged for going after robert mueller. Base on the fact source from The Atlantic,
        # Robert Mueller did face attacks from Representatives John Ratcliffe and Louie Gohmert but there is no mentions
        # about getting dragged. More information about this can be found here
        # https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/"}""")
        #
        # context.add_message("user", "The news title is: Trump wants Postal Service to charge 'much more' for Amazon "
        #                             "shipments. "
        #                             "Give me google search queries you want to search to fact check this news. Give me "
        #                             "the queries in json format, where the key is 'queries' and the value is a list of "
        #                             "queries.")
        # context.add_message("assistant", """{"queries":["Trump wants Postal Service to charge 'much more' for Amazon shipments."]}""")
        # context.add_message("user", """{"Trump wants Postal Service to charge 'much more' for Amazon shipments" :
        #     {
        #     "title": "Trump wants Postal Service to charge 'much more' for ...",
        #     "link": "https://www.reuters.com/article/us-usa-trump-amazon-com/trump-wants-postal-service-to-charge-much-more-for-amazon-shipments-idUSKBN1EN15O",
        #     "snippet": "President Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon , picking another fight ...",
        #     "source": "Reuters"
        #     }
        #     }
        #     Base on the google searches, tell me whether the news title is fake or real or disputed.
        #     """)
        # context.add_message("assistant", """{"judgement":"True", "explanation": "Reuters has mentioned that President
        # Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon. Hence
        # the news is true and more information can be found here
        # https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/"}""")
        #
        # context.add_message("user", f"{new['title']}"
        #                             ". Give me google search queries you want to search to fact check this news. Give me "
        #                             "the queries in json format, where the key is 'queries' and the value is a list of "
        #                             "queries. Do not return newlines and double quotes in the string should be "
        #                               "replace by single quotes.")
        # response = agent.query(context)
        # print(response)
        # response = json.loads(response.replace("\n", " ").replace("\r", ""))
        # search_results = {}
        #
        # for query in response['queries']:
        #     print(query)
        #     result = searcher.search(query + f" {new['date']}")
        #     search_results[query] = result
        # context.add_message("user", search_results.__str__() +
        #                             "\nBase on the google searches, tell me whether the news title is fake or real or disputed.")
        context.add_message("user", f"{new['title']}")
        response = agent.query(context)
        print(response)

        final_response = json.loads(response.replace("\n", " ").replace("\r", ""))
        judgement = final_response['judgement']
        explanation = final_response['explanation']

        with engine.connect() as connection:
            escaped_content = context.get_messages().__str__().replace("'", "").replace('%', '%%')
            escaped_explanation = explanation.replace("'", "").replace('%', '%%')
            connection.execute(
                f"UPDATE news SET base_gpt_label = '{judgement}', base_model_explanation = '{escaped_explanation}' WHERE id = {new['id']}")

        print(final_response)
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





