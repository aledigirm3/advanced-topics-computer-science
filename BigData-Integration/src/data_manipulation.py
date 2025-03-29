import json
import os
import sys
import re
from typing import Dict, Tuple
import paths
from ansi_colors import *


def get_db_dict(filename: str) -> Dict[str, Dict[str, list]]: # -> {database, {table_name, [col1, col2, ...]}}

    db_dict = {}

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for db in data:

        tables_dict = {table: [] for table in db["table_names"]}

        for col in db["column_names_original"]:
            table_index, column_name = col
            if table_index != -1:
                 tables_dict[db["table_names"][table_index]].append(column_name)

        db_dict[db["db_id"]] = tables_dict


    return db_dict


def get_db_dict_mapping(filename: str) -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]]: 
    # -> ( {database, {table_name_original, table_name}}, {database, {table_name, table_name_original}} )

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    original2name_dict = {}
    name2original_dict = {}
        
    for db in data:
        
        databaseID = db["db_id"]
        table_names_original = db["table_names_original"]
        table_names = db["table_names"]
        
        original2name_dict[databaseID] = dict(zip(table_names_original, table_names))
        name2original_dict[databaseID] = dict(zip(table_names, table_names_original))
        
        
    return (original2name_dict, name2original_dict)
    
    
def get_tables_from_SQLquery(sql_query: str) -> list[str]:
    """
    Function to extract table from SQL query.
    
    Args:
        query (str): Query to parse
        
    Returns:
        list: Name of tables taken from query.
    """
    
    # Regex
    table_pattern = re.compile(r'\bFROM\s+(`?\w+`?)(?:\s+AS\s+\w+)?', re.IGNORECASE)
    join_pattern = re.compile(r'\bJOIN\s+(`?\w+`?)(?:\s+AS\s+\w+)?', re.IGNORECASE)
    
    
    tables = set(table_pattern.findall(sql_query))
    tables.update(join_pattern.findall(sql_query))
    
    # Rimuovi i backtick solo se presenti
    clean_tables = {table.strip('`') for table in tables}
    
    return list(clean_tables)


def get_entry_from_llmResponse(filename: str):
    
    with open(filename, "r", encoding="utf-8") as file:
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
    
    return data
    

if __name__ == '__main__':
    
    #query = "SELECT T3.district_id FROM `order` AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id WHERE T1.order_id = 33333"
    #print(get_db_dict_mapping(False))

    db_dict = get_db_dict(paths.DEV + 'dev_tables.json')

    