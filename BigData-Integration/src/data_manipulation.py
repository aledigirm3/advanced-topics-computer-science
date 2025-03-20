import json
import os
import sys
import re
from typing import Dict, Tuple


### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###

def get_db_dict_mapping(isTrain: bool=True) -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]]: 
    # -> ( {database, {table_name_original, table_name}}, {database, {table_name, table_name_original}} )

    if isTrain:
        tabs = paths.TRAIN + 'train_tables.json'
    else:
        tabs = paths.DEV + 'dev_tables.json'
    with open(tabs, "r", encoding="utf-8") as f:
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
    table_pattern = re.compile(r'\bFROM\s+(\w+)(?:\s+AS\s+\w+)?', re.IGNORECASE)
    join_pattern = re.compile(r'\bJOIN\s+(\w+)(?:\s+AS\s+\w+)?', re.IGNORECASE)
    
    
    tables = set(table_pattern.findall(sql_query))
    tables.update(join_pattern.findall(sql_query))
    
    return list(tables)


if __name__ == '__main__':
    print("aaa")
    