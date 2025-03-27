import re
import os
import sys

prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
from llm import query_groq
from data_manipulation import get_db_dict_mapping, get_entry_from_llmResponse
from examples import findTables_example1DEV, findTables_example2DEV, findTables_example3DEV
import paths
from ansi_colors import *


def get_tables_from_query(query: str, db1: str, db2: str, db3: str) -> str:

    """
    Function to extract relevant tables from natural language query.
    
    Args:
        query (str): Natural language query.
        db1 (str): database 1 with associated tables
        db2 (str): database 2 with associated tables
        db2 (str): database 3 with associated tables
        
    Returns:
        str: relevant tables.
    """

    system_prompt = """(forget the previous answers) You are an agent in the field of big data integration. 
    Given a natural language query and three databases with their respective tables, your task is to determine which tables 
    (from ONLY single database) are necessary to satisfy the query. Ensure that all selected tables are 
    relevant and sufficient to retrieve the required information.
    (answer only with database and relevant tables)
    

    ---
    Example 1: """ + findTables_example1DEV.__str__() + """
    ---
    Example 2: """ + findTables_example2DEV.__str__() + """
    ---
    Example 3: """ + findTables_example3DEV.__str__() + """
    
    (The provided examples select only the necessary tables for a possible SQL query to satisfy the natural language query)
    """

    content = f"""identify the necessary tables from a single database to satisfy the query: {query}
                [DATABASES]
                {db1}
                {db2}
                {db3}"""


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
    
    if not os.path.exists('../' + paths.LLM_RESPONSE):
        os.makedirs(paths.LLM_RESPONSE)
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} created.")
    else:
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} already exist.")

    
    original2name, name2original = get_db_dict_mapping(f"../{paths.DEV}dev_tables.json")
    
    filename = "../" + paths.LLM_RESPONSE + "match_databases.txt"
    data = get_entry_from_llmResponse(filename)
    
    filename = "match_tables.txt"
    with open('../' + paths.LLM_RESPONSE + filename, "a", encoding="utf-8") as file:
        for qid, entry in data.items():
            db1= ""
            db2 = ""
            db3 = ""
            
            databases = entry["llmRESPONSE"].split(",")
            for db in databases:
                tables = ", ".join(original2name[db.strip()].values())
                if db1 == "":
                    db1 = f"{db.strip()}: {tables}"
                elif db2 == "":
                    db2 = f"{db.strip()}: {tables}"
                else:
                    db3 = f"{db.strip()}: {tables}"
                
            response = get_tables_from_query(entry['QUESTION'], db1, db2, db3)
            
            file.write(f"Qid: {qid}\n")
            file.write(f"DBid: {entry['DBid']}\n")
            file.write(f"QUESTION: {entry['QUESTION']}\n")
            file.write(f"SQL: {entry['SQL']}\n")
            file.write(f"llmRESPONSE: {response}\n\n")

            file.flush()