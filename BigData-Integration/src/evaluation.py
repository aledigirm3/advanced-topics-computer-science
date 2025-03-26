import os
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
    
    original2name, name2original = get_db_dict_mapping(isTrain=False)
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


if __name__ == '__main__':

    filename = "allminiLM_match_databases.txt"

    database_match_eval(filename)