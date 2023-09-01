import json
import os
import pprint

from agent import StatelessAgent, ContextAgent
from context import Context
from search import News_searcher, GoogleSearcher

if __name__ == "__main__":
    # agent = StatelessAgent(os.getenv("OPENAI_API_KEY"))
    # context = Context()
    # context.add_message("system", "You are a fake news detection expert. You use the Search tool as your primary resource to see if a news is fake or not. You are impartial and only rely on proper sources to judge. You need to figure out whether the following news is fake or not. Provide a JSON object containing the key 'judgement' with either 'Fake', 'Not Fake' or 'Disputed' and another key 'explanation' with the explanation at the very end. Do this for the following news:")
    # # context.add_message("user", """You are a fake news detection expert. You use the Search tool as your primary resource to see if a news is fake or not. You are impartial and only rely on proper sources to judge. You need to figure out whether the following news is fake or not. Provide a JSON object containing the key 'judgement' with either 'Fake', 'Not Fake' or 'Disputed' and another key 'explanation' with the explanation at the very end. Do this for the following news:
    # #
    # # AI is conscious.""")
    # context.add_message("user", """Donald Trump just signed the GOP tax scam into law. Of course, that meant that he invited all of his craven, cruel GOP sycophants down from their perches on Capitol Hill to celebrate in the Rose Garden at the White House. Now, that part is bad enough   celebrating tax cuts for a bunch of rich hedge fund managers and huge corporations at the expense of everyday Americans. Of course, Trump is beside himself with glee, as this represents his first major legislative win since he started squatting in the White House almost a year ago. Thanks to said glee, in true Trumpian style, he gave a free-wheeling address, and a most curious subject came up as Trump was thanking the goons from the Hill. Somehow, Trump veered away from tax cuts, and started talking about the Congressional baseball shooting that happened over the summer.In that shooting, Rep. Steve Scalise, who is also the House Majority Whip, was shot and almost lost his life. Thanks to this tragic and stunning act of political violence, Scalise had a long recovery; in fact he is still in physical therapy. But, of course, vain and looks-obsessed Trump decided that he would congratulate Scalise, not on his survival and on his miraculous recovery, but on the massive amount of weight Scalise lost while he was practically dying. And make no mistake   Scalise is VERY lucky to be alive. According to doctors, when he arrived at the hospital, Scalise was actually, quote, in  imminent risk of death.  Here is the quote, via Twitter:How stunningly tone deaf does one have to be to say something like that? I never thought I d say this about a Republican that I, by all reasonable accounts, absolutely loathe, but I feel sorry for him. I am sorry he got shot, and I am even sorrier that he now has to stand there and listen to that orange buffoon talk about him like that.I am sure that Scalise is a much tougher man than Trump, though. I am equally sure that he also knows that Trump is an international embarrassment and a crazy man who never should have been allowed anywhere near the White House.Featured image via Alex Wong/Getty Images""")
    # response = agent.query(context)
    # print(response)

    searcher = GoogleSearcher()
    # response = searcher.search("Donald Trump GOP tax scam law")

    agent = ContextAgent(os.getenv("OPENAI_API_KEY"))
    context = Context()
    context.add_message("system", "You are a fake news detection expert. You use the Search tool as your primary "
                                  "resource to see if a news is fake or not. You are impartial and only rely on "
                                  "proper sources to judge. You need to figure out whether the following news is fake "
                                  "or not. Provide a JSON object containing the key 'judgement' with either 'Fake', "
                                  "'Not Fake' or 'Disputed' and another key 'explanation' with the explanation at the "
                                  "very end. Do this for the following news:")
    context.add_message("user", "Donald Trump just signed the GOP tax scam into law. Of course, that meant that he "
                                "invited all of his craven, cruel GOP sycophants down from their perches on Capitol "
                                "Hill to celebrate in the Rose Garden at the White House. Now, that part is bad "
                                "enough   celebrating tax cuts for a bunch of rich hedge fund managers and huge "
                                "corporations at the expense of everyday Americans. Of course, Trump is beside "
                                "himself with glee, as this represents his first major legislative win since he "
                                "started squatting in the White House almost a year ago. Thanks to said glee, "
                                "in true Trumpian style, he gave a free-wheeling address, and a most curious subject "
                                "came up as Trump was thanking the goons from the Hill. Somehow, Trump veered away "
                                "from tax cuts, and started talking about the Congressional baseball shooting that "
                                "happened over the summer.In that shooting, Rep. Steve Scalise, who is also the House "
                                "Majority Whip, was shot and almost lost his life. Thanks to this tragic and stunning "
                                "act of political violence, Scalise had a long recovery; in fact he is still in "
                                "physical therapy. But, of course, vain and looks-obsessed Trump decided that he "
                                "would congratulate Scalise, not on his survival and on his miraculous recovery, "
                                "but on the massive amount of weight Scalise lost while he was practically dying. And "
                                "make no mistake   Scalise is VERY lucky to be alive. According to doctors, "
                                "when he arrived at the hospital, Scalise was actually, quote, in  imminent risk of "
                                "death.  Here is the quote, via Twitter:How stunningly tone deaf does one have to be "
                                "to say something like that? I never thought I d say this about a Republican that I, "
                                "by all reasonable accounts, absolutely loathe, but I feel sorry for him. I am sorry "
                                "he got shot, and I am even sorrier that he now has to stand there and listen to that "
                                "orange buffoon talk about him like that.I am sure that Scalise is a much tougher man "
                                "than Trump, though. I am equally sure that he also knows that Trump is an "
                                "international embarrassment and a crazy man who never should have been allowed "
                                "anywhere near the White House.Featured image via Alex Wong/Getty Image")
    # context.add_message("user", "AI is conscious.")
    response = agent.query(context)
    # print(response)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    context.add_message("user", "Give me google search queries you want to search to fact check this news. Give me the queries in json format, where the key is 'queries' and the value is a list of queries.")
    response = agent.query(context)
    # print(response)
    context.add_message("user",
                        "only give me necessary queries.")
    response = agent.query(context)
    response = json.loads(response)
    search_results = {}

    for query in response['queries']:
        print(query)
        result = searcher.search(query)
        search_results[query] = result
    context.add_message("user", search_results.__str__() + "\n now base on these information tell me whether the news "
                                                           "is fake, not fake or disputed. If you are not certain "
                                                           "don't make one-sided conclusion?")
    response = agent.query(context)
    pprint.pprint(context.get_messages())




