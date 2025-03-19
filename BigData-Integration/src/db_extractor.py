import os
import sys
import json
from llm import query_groq
from examples import findDB_example1DEV, findDB_example2DEV, findDB_example3DEV

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###


def get_databases_from_query(query: str) -> str:

    """
    Function to extract the top 3 most relevant databases from query.
    
    Args:
        query (str): Natural language query.
        
    Returns:
        str: top 3 most relevant databases (separated by comma).
    """

    system_prompt = """(forget the previous answers) You are an agent in the field of big data integration. 
    Given a natural language query, identify the top 3 most relevant databases from the following list. 
    (RESPOND ONLY WITH THE NAMES OF THE DATABASES)

    - DATABASES: ['debit_card_specializing', 'financial', 'formula_1', 'california_schools',
                  'card_games', 'european_football_2', 'thrombosis_prediction', 'toxicology', 'student_club',
                  'superhero', 'codebase_community']

    ---
    Example 1: """ + findDB_example1DEV.__str__() + """
    ---
    Example 2: """ + findDB_example2DEV.__str__() + """
    ---
    Example 3: """ + findDB_example3DEV.__str__() + """
    
    """

    content = f"Provide me the 3 most relevant databases based on this QUERY: {query}"


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
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} created.")
    else:
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} already exist.")
    
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
            response = get_databases_from_query(question)
            
            if "question_id" in query_block:
                q_id = query_block["question_id"]
                file.write(f"{space}Qid: {q_id}\n")

            file.write(f"{space}DBid: {db_id}\n")
            file.write(f"{space}QUESTION: {question}\n")
            file.write(f"{space}SQL: {question}\n")
            file.write(f"{space}llmRESPONSE: {response}\n\n")

            file.flush()
