
# NewGPT

This repository includes the implemenation of a news detection system leverage LLM and web searches from trusted sources. 




## Running Experiments

The following section contains the steps needed to run the experiments. This may vary on different IDEs or operating systems. Pleaase contact us through email if any issues are encountered. 

Install Packages
```bash
  pip install -r requirements.txt
```
Note: you may need to install additional packages required from these libraries.

Set up Database

1. Download mySQL database management system.
2. Create a new table named "**news_gpt**"
3. Import SQL database dump at **data->database_dump->news-gpt-2023-10-21.sql**

 


Set up API keys

1. Get openai API keys at https://openai.com/product
2. Get Bing Search API keys at https://www.microsoft.com/en-us/bing/apis/bing-web-search-api 
This step also involves setting up Azure Virtual Machine for the API acess. 

Set up Environment Variables in .env file
```
DB_PASSWORD=<your databse password>
OPENAI_API_KEY=<your openai API key>
BING_KEY=<your bing search API key>
```

To run experiments:

1. One Search NewsGPT
Run **src->t.py**, results will be inserted into the SQL database. 

2. Multi-search NewsGPT
Run comment out line 72-73 in **src->searcher->bing_searcher**, then run **src->t.py**, results will be inserted into the SQL database. 

3. Base GPT model
Run **src->base_gpt.py**, results will be inserted into the SQL database. 

To run the models on different dataset, please adjust the SQL query to select from differnt data tables accordingly at line 24 in **src->t.py** or line 21 in **src->base_gpt.py**.