import re
import sys
from data_manipulation import get_db_dict_mapping, get_tables_from_SQLquery, get_entry_from_llmResponse
import paths
from ansi_colors import *


def database_match_eval(filename: str):

    data = get_entry_from_llmResponse(filename)

    correct_pred = 0
    total_entry = 0

    for qid, entry in data.items():
        entry_list = entry['llmRESPONSE'].split(", ")
        if entry['DBid'] in entry_list:
            correct_pred += 1

        total_entry += 1

    print(f"{GREEN}ACCURACY (db match): {RESET}{correct_pred/total_entry}")



def table_match_eval(filename: str):
    
    original2name, name2original = get_db_dict_mapping(paths.DEV + 'dev_tables.json')
    
    data = get_entry_from_llmResponse(filename)
    
    tp = 0
    fp = 0
    fn = 0
    
    
    for qid, entry in data.items():
        truth_tables = get_tables_from_SQLquery(entry['SQL'])
        
        database, _, result = entry['llmRESPONSE'].partition(":")
        
        database = database.strip()
        
        predicted_tables_list = result.split(",")
        predicted_tables = [item.strip() for item in predicted_tables_list]
        
        for table in predicted_tables:
            
            if name2original[database][table] in truth_tables:

                tp += 1
                truth_tables.remove(name2original[database][table])
            else:
                fp += 1
                
        fn += len(truth_tables)
            
        
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"{GREEN}PRECISION: {RESET}{precision:.2f}")
    print(f"{GREEN}RECALL: {RESET}{recall:.2f}")
    print(f"{GREEN}F1-score: {RESET}{f1_score:.2f}")
    
def att_table_match_eval(filename: str):
    
    original2name, name2original = get_db_dict_mapping(paths.DEV + 'dev_tables.json')
    
    data = get_entry_from_llmResponse(filename, withAttributes=True)
    
    table_tp = 0
    table_fp = 0
    table_fn = 0
    
    att_tp = 0
    att_fp = 0
    att_fn = 0
    
    n_ist = 0
    
    for qid, entry in data.items():
        n_ist += 1
        print(f"{RED}{qid}{RESET}")
        truth_tables = get_tables_from_SQLquery(entry['SQL'])
        truth_attributes = entry['attributes'].split(",")
        truth_attributes =[item.strip() for item in truth_attributes]
        
        database, _, result = entry['llmRESPONSE'].partition(":")
        
        database = database.strip()
        
        predicted_att_tables_list = re.findall(r'\b[\w\s\-]+\s*\(.*?\)', result)
        predicted_att_tables = [item.strip() for item in predicted_att_tables_list]
        
        for att_table_str in predicted_att_tables:
            
            att_table = re.match(r'\s*([\w\s\-]+)\s*\((.*?)\)', att_table_str)
            table = att_table.group(1)
            attributes = [att.strip() for att in att_table.group(2).split(',')]
            
            if name2original[database][table] in truth_tables:

                table_tp += 1
                truth_tables.remove(name2original[database][table])
            else:
                table_fp += 1
                
            for att in attributes:
                if att in truth_attributes:
                    att_tp += 1
                    truth_attributes.remove(att)
                else:
                    att_fp += 1
                    
        table_fn += len(truth_tables)
        att_fn += len(truth_attributes)
            

    precision = table_tp / (table_tp + table_fp) if (table_tp + table_fp) > 0 else 0
    recall = table_tp / (table_tp + table_fn) if (table_tp + table_fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"{CYAN}*===Table evaluation===*{RESET}")
    print(f"{GREEN}PRECISION: {RESET}{precision:.2f}")
    print(f"{GREEN}RECALL: {RESET}{recall:.2f}")
    print(f"{GREEN}F1-score: {RESET}{f1_score:.2f}")
    print('\n')
    precision = att_tp / (att_tp + att_fp) if (att_tp + att_fp) > 0 else 0
    recall = att_tp / (att_tp + att_fn) if (att_tp + att_fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"{CYAN}*===Attributes evaluation===*{RESET}")
    print(f"{GREEN}PRECISION: {RESET}{precision:.2f}")
    print(f"{GREEN}RECALL: {RESET}{recall:.2f}")
    print(f"{GREEN}F1-score: {RESET}{f1_score:.2f}")
    print(n_ist)


if __name__ == '__main__':

    filename = paths.LLM_RESPONSE + "att_match_tables.txt"

    att_table_match_eval(filename)