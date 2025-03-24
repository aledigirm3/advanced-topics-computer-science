import re
import os
import sys
from llm import query_groq
from data_manipulation import get_db_dict_mapping
from examples import findTables_example1DEV, findTables_example2DEV, findTables_example3DEV

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###


def get_tables_from_query(query: str) -> str:

    """
    Function to extract relevant tables from natural language query.
    
    Args:
        query (str): Natural language query.
        databases (str): databases with associated tables
        
    Returns:
        str: relevant tables.
    """

    system_prompt = """(forget the previous answers) PROMPT ENG.

    ---
    Example 1: """ + findTables_example1DEV + """
    ---
    Example 2: """ + findTables_example2DEV + """
    ---
    Example 3: """ + findTables_example3DEV + """
    
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
    
    original2name, name2original = get_db_dict_mapping(isTrain=False)
    print(original2name['student_club'].values())
    sys.exit(0)
    
    with open(paths.LLM_RESPONSE + "match_databases.txt", "r", encoding="utf-8") as file:
        text = file.read()

    pattern = re.findall(
        r"Qid: (\d+)\nDBid: ([^\n]+)\nQUESTION: ([^\n]+)\nSQL: ([^\n]+)\nllmRESPONSE: ([^\n]+)", 
        text
    )
    data = {
        int(qid): {
            "DBid": dbid.strip(),
            "QUESTION": question.strip(),
            "SQL": sql.strip(),
            "llmRESPONSE": llmresp.strip(),
        }
        for qid, dbid, question, sql, llmresp in pattern
    }

    for qid, entry in data.items():
        print(f" Qid: {CYAN}{qid}{RESET}")
        print(f"DBid: {CYAN}{entry['DBid']}{RESET}")
        print(f"QUESTION: {CYAN}{entry['QUESTION']}{RESET}")
        print(f"SQL: {CYAN}{entry['SQL']}{RESET}")
        print(f"llmRESPONSE: {CYAN}{entry['llmRESPONSE']}{RESET}")
        
        databases = entry["llmRESPONSE"].split(",")
        for db in databases:
            tables = ", ".join(original2name[db.strip()].keys())
            print(f"\n- {db.strip()}: {RED}{tables}{RESET}")
        print("=" * 50)