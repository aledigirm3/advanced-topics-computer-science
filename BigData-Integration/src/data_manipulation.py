import json
import os
import sys
import re
from typing import Dict


### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###

def get_db_dict(isTrain: bool=True) -> Dict[str, Dict[str, str]]: # -> {database, {table, [attr1, attr2, ...]}}

    if isTrain:
        tab = paths.TRAIN + 'train_tables.json'
    else:
        tab = paths.DEV + 'dev_tables.json'
    with open(tab, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    db_dict = {}
        
    for db in data:
        
        databaseID = db["db_id"]
        table_names = db["table_names_original"]
        column_names = db["column_names"]
        
        table_attributes = {table: [] for table in table_names}
        
        for table_index, column_name in column_names:
            if table_index != -1:
                table_name = table_names[table_index]
                table_attributes[table_name].append(column_name)
        
        db_dict[databaseID] = table_attributes
        
        
    print(db_dict.keys())
    
    
def get_tables_from_query(sql_query: str) -> list[str]:
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
    