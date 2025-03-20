import re
import os
import sys
from data_manipulation import get_db_dict_mapping

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###


if __name__ == '__main__':
    
    original2name, name2original = get_db_dict_mapping(isTrain=False)
    
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
            tables = ", ".join(original2name[db.strip()].values())
            print(f"\n- {db.strip()}: {RED}{tables}{RESET}")
        print("=" * 50)