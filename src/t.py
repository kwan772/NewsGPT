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
    offset = 169
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
                                              "replace by single quotes.")

                context.add_message("user",
                                    "The following is a few examples that shows you what I expect: The news title is: Trump wants Postal Service to charge 'much more' for Amazon "
                                    "shipments. "
                                    "Give me bing search queries you want to search to fact check this news. Give me "
                                    "the queries in json format, where the key is 'queries' and the value is a list of "
                                    "queries.")
                context.add_message("user", """[{'name': "Trump wants Postal Service to charge 'much more' for Amazon shipments ...", 'url': 'https://www.reuters.com/article/us-usa-trump-amazon-com-idUSKBN1EN15O', 'snippet': 'SEATTLE/WASHINGTON (Reuters) - President Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon AMZN.O, picking another fight with...'}, {'name': "Trump wants Postal Service to charge 'much more' for Amazon shipments", 'url': 'https://finance.yahoo.com/news/trump-targets-amazon-call-postal-hike-prices-131847748--finance.html', 'snippet': 'By Eric M. Johnson and Makini Brice SEATTLE/WASHINGTON (Reuters) - President Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon...'}, {'name': "Trump wants Postal Service to charge 'much more' for Amazon shipments", 'url': 'https://finance.yahoo.com/news/trump-wants-postal-charge-much-001720396.html', 'snippet': 'SEATTLE/WASHINGTON (Reuters) - President Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon (AMZN.O), picking another fight...'}]
        
                        Base on the bing searches, tell me whether the news title is fake or real or disputed.
                        """)
                context.add_message("assistant", """{"judgement":"True", "explanation": "Reuters has mentioned that President
                    Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon. Hence
                    the news is true and more information can be found here
                    https://www.reuters.com/article/us-usa-trump-amazon-com-idUSKBN1EN15O"}""")

                context.add_message("assistant", """{"judgement":"True", "explanation": "Reuters has mentioned that President
                    Donald Trump called on the U.S. Postal Service on Friday to charge "much more" to ship packages for Amazon. Hence
                    the news is true and more information can be found here
                    https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/"}""")
                context.add_message('user',
                                    'The news title is: US lawmakers press White House for tougher enforcement of China chip rules. '
                                    "Give me bing search queries you want to search to fact check this news. Give me "
                                    "the queries in json format, where the key is 'queries' and the value is a list of "
                                    "queries.")
                context.add_message("user", """
                        [{
                        "name": "US lawmakers press White House for tougher enforcement of China chip rules.",
                        "url": "https://www.reuters.com/technology/us-lawmakers-press-white-house-tougher-enforcement-china-chip-rules-2023-10-06/",
                        "snippet": "Two senior Republican lawmakers in the U.S. House of Representatives on Friday pressed ...",
        
                        }
                        }]
                        Base on the bing searches, tell me whether the news title is fake or real or disputed.
                        """)
                context.add_message("assistant", """{"judgement":"True", "explanation": "US lawmakers press White House for tougher enforcement of China chip rules. Hence
                    the news is true and more information can be found here
                    https://www.reuters.com/technology/us-lawmakers-press-white-house-tougher-enforcement-china-chip-rules-2023-10-06/"}""")

                context.add_message("user",
                                    "The news title is: Republican Senator Gets Dragged For Going After Robert Mueller. "
                                    "Give me google search queries you want to search to fact check this news. Give me "
                                    "the queries in json format, where the key is 'queries' and the value is a list of "
                                    "queries.")
                context.add_message("user", """
                        [{
                        "name": "Republicans Take Their Shot at Mueller—And Narrowly Miss",
                        "url": "https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/",
                        "snippet": "Former Special Counsel Robert Mueller (center) faced attacks from Representatives John Ratcliffe (left) and Louie Gohmert (right).",
                        }
                        }]
                        Base on the google searches, tell me whether the news title is fake or real or disputed.
                        """)
                context.add_message("assistant", """{"judgement":"Fake", "explanation": "No trusted news source has mentioned
                        that republican senator was dragged for going after robert mueller. Base on the fact source from The Atlantic,
                        Robert Mueller did face attacks from Representatives John Ratcliffe and Louie Gohmert but there is no mentions
                        about getting dragged. More information about this can be found here
                        https://www.theatlantic.com/politics/archive/2019/07/mueller-hearing-republicans-attack/594613/"}""")

                context.add_message('user',
                                    "The news title is: Commander Biden Gnaws Washington Monument Down To Slobber-Covered Stub")
                context.add_message("user", """[
                        {
                        "name": "Commander Biden Gnaws Washington Monument Down To Slobber-Covered Stub",
                        "url": "https://www.theonion.com/commander-biden-gnaws-washington-monument-down-to-slobb-1850903577",
                        "snippet": "WASHINGTON—Noting that there was no excuse for the first dog’s most recent instance of bad behavior, the White House confirmed Thursday that Commander Biden had gnawed the Washington Monument down to a slobber-covered stub.",
                        }
                        ]
                        Base on the bing searches, tell me whether the news title is fake or real or disputed.
                        """)

                context.add_message("assistant", """{"judgement":"Fake", "explanation": "No trusted news source has mentioned that Joe Biden's dog bite the monument. However, BBC give some information on the dog biting incident
    
    
                        https://www.bbc.com/news/world-us-canada-67015811"}""")
                context.add_message('user',
                                    "The news title is: Is BJP's Shivraj Singh Chouhan going to take on Digvijay Singh in Bhopal?")
                context.add_message('assistant',
                                    """{"queries":["Is BJP's Shivraj Singh Chouhan going to take on Digvijay Singh in Bhopal?"]}""")
                context.add_message("user", """[
                        {
                        "name": "Is BJP's Shivraj Singh Chouhan going to take on Digvijay Singh in Bhopal?",
                        "url": "https://www.indiatoday.in/fact-check/story/fact-check-is-shivraj-singh-chouhan-going-to-take-on-digvijay-singh-in-bhopal-1490983-2019-04-01 ",
                        "snippet": "The candidate list viral on social media with Shivraj Singh Chouhan's name is doctored.",
                        }
                        ]
                        Base on the bing searches, tell me whether the news title is fake or real or disputed.
                        """)
                context.add_message("assistant", """{"judgement":"Fake", "explanation": "According to the fact-checking article from India Today, 
                                        the claim that BJP has fielded Shivraj Singh Chouhan to take on Digvijay Singh in Bhopal is false. 
                                        The BJP has not yet declared Shivraj Singh Chouhans seat for the Lok Sabha polls. 
                                        The candidate list viral on social media with Chouhans name is doctored. Hence this is fake.
                                        For more information, please refer to the article here: 
                                        https://www.indiatoday.in/fact-check/story/fact-check-is-shivraj-singh-chouhan-going-to-take-on-digvijay-singh-in-bhopal-1490983-2019-04-01""")
                context.add_message("user",'Nancy Pelosi accuses interim House speaker of ordering her to give up office in Capitol')
                context.add_message('assistant',
                                    """{"queries": "Pelosi accuses interim House speaker of ordering her to give up office in Capitol"}""")
                context.add_message("user", """[
                        {
                        "name": "Interim House Speaker 'evicts' two senior Democrats from Capitol",
                        "url": "https://www.bbc.com/news/world-us-canada-67005444 ",
                        "snippet": "Nancy Pelosi and her long-time deputy Steny Hoyer have been ordered to leave their workspaces in the US Capitol by acting House Speaker Patrick McHenry.",
                        }
                        ]
                        Base on the bing searches, tell me whether the news title is fake or real or disputed.
                        """)
                context.add_message("assistant", """{"judgement":"True", "explanation": "According to BBC, 
                                        Nancy Pelosi and her long-time deputy Steny Hoyer have been ordered to leave their workspaces in the US Capitol by acting House Speaker Patrick McHenry. Hence this is True.
                                        For more information, please refer to the article here: 
                                        https://www.bbc.com/news/world-us-canada-67005444""")




                context.add_message("user", "Now, verify the following news: " + new['Statement'])

                res = agent.query_with_functions(context)
                # print(res)
                # res = agent.query(context)
                # print(context)
                final_response = json.loads(res.replace("\n", " ").replace("\r", ""))
                judgement = final_response['judgement']
                explanation = final_response['explanation']

                with engine.connect() as connection:
                    escaped_content = context.get_messages().__str__().replace("'", "").replace('%', '%%')
                    escaped_explanation = explanation.replace("'", "").replace('%', '%%')
                    r = connection.execute(
                        f"UPDATE IFND_sample SET few_shot_model_label = '{judgement}', few_shot_model_explanation = '{escaped_explanation}', few_shot_model_response='{escaped_content}' WHERE id = {new['id']}")
                # print(r)
                hasException = False
                offset += 1
                print(f"{offset} rows processed")
                # print(context)


            except Exception as e:
                hasException = True
                print(e)



