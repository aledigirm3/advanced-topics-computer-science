import os
import sys
import json
from llm import query_groq
from examples import findDB_example1, findDB_example2, findDB_example3

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###


def get_db_from_query(query: str) -> str:

    """
    Function to extract the top 10 most relevant databases from query.
    
    Args:
        query (str): Natural language query.
        
    Returns:
        str: top 10 most relevant databases (separated by comma).
    """

    system_prompt = """(forget the previous answers) You are an agent in the field of big data integration. 
    Given a natural language query, identify the top 10 most relevant databases from the following list. 
    (RESPOND ONLY WITH THE NAMEs OF THE DATABASES)

    - DATABASES: ['european_football_1', 'sales_in_weather', 'craftbeer', 'soccer_2016', 'restaurant',
    'movie', 'olympics', 'language_corpus', 'app_store', 'sales', 'video_games', 'image_and_language',
    'software_company', 'authors', 'movies_4', 'social_media', 'human_resources', 'regional_sales',
    'computer_student', 'works_cycles', 'food_inspection_2', 'citeseer', 'bike_share_1', 'law_episode',
    'cs_semester', 'legislator', 'world', 'cookbook', 'university', 'books', 'shipping', 'food_inspection',
    'movie_platform', 'shakespeare', 'book_publishing_company', 'car_retails', 'mental_health_survey',
    'hockey', 'music_platform_2', 'address', 'menu', 'professional_basketball', 'cars', 'synthea',
    'genes', 'retails', 'talkingdata', 'beer_factory', 'chicago_crime', 'mondial_geo', 'student_loan',
    'codebase_comments', 'retail_world', 'music_tracker', 'disney', 'college_completion', 'ice_hockey_draft',
    'world_development_indicators', 'airline', 'retail_complains', 'trains', 'public_review_platform',
    'donor', 'coinmarketcap', 'simpson_episodes', 'movie_3', 'shooting', 'superstore', 'movielens']

    ---
    Example 1: """ + findDB_example1.__str__() + """
    ---
    Example 2: """ + findDB_example2.__str__() + """
    ---
    Example 3: """ + findDB_example3.__str__() + """
    
    """

    content = f"Provide me the 10 most relevant databases based on this QUERY: {query}"


    return query_groq(messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": content
        }
    ])


if __name__ == '__main__':

    if not os.path.exists(paths.LLM_RESPONSE):
        os.makedirs(paths.LLM_RESPONSE)
        print(f"'{paths.LLM_RESPONSE}' created.")
    else:
        print(f"'{paths.LLM_RESPONSE}' already exist.")
    
    filename = "match_databases.txt"

    queries = paths.TRAIN + 'train.json'
    
    with open(queries, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(paths.LLM_RESPONSE + filename, "a", encoding="utf-8") as file:
        space = "" 

        for query_block in data:

            db_id = query_block["db_id"]
            question = query_block["question"]
            sql = query_block["SQL"]
            response = get_db_from_query(question)


            file.write(f"{space}DBid: {db_id}\n")
            file.write(f"{space}QUESTION: {question}\n")
            file.write(f"{space}SQL: {question}\n")
            file.write(f"{space}llmRESPONSE: {response}\n\n")

            file.flush()
