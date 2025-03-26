import os
import sys
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch

prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *

def get_databases_from_query(model, query: str) -> str:

    # Lista dei database
    database_names = ['debit_card_specializing', 'financial', 'formula_1', 'california_schools',
                    'card_games', 'european_football_2', 'thrombosis_prediction', 'toxicology', 'student_club',
                    'superhero', 'codebase_community']

    # DB embeddings
    db_embeddings = model.encode(database_names)

    # Query embedding
    query_embedding = model.encode([query])

    # Cosine similarity
    similarities = cosine_similarity(query_embedding, db_embeddings)[0]


    # 3 most relevant DB 
    top_indices = np.argsort(similarities)[::-1][:3]
    top_dbs = [(database_names[i]) for i in top_indices]

    databases_string = ", ".join(top_dbs)

    return databases_string
    

if __name__ == '__main__':

    # ======================================MODEL================================================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"{CYAN}{device}{RESET}")
    print(f"Cuda version: {torch.version.cuda}")
    print(f"Torch version: {torch.__version__}\n")

    model = SentenceTransformer('all-MiniLM-L6-v2', device)
    # ===========================================================================================

    if not os.path.exists('../' + paths.LLM_RESPONSE):
        os.makedirs(paths.LLM_RESPONSE)
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} created.")
    else:
        print(f"{CYAN}'{paths.LLM_RESPONSE}'{RESET} already exist.")
    
    filename = "allminiLM_match_databases.txt"

    queries = '../' + paths.DEV + 'dev.json'
    
    with open(queries, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open('../' + paths.LLM_RESPONSE + filename, "a", encoding="utf-8") as file:
        space = "" 

        for query_block in data:

            db_id = query_block["db_id"]
            question = query_block["question"]
            sql = query_block["SQL"]
            response = get_databases_from_query(model, question)
            
            if "question_id" in query_block:
                q_id = query_block["question_id"]
                file.write(f"{space}Qid: {q_id}\n")

            file.write(f"{space}DBid: {db_id}\n")
            file.write(f"{space}QUESTION: {question}\n")
            file.write(f"{space}SQL: {sql}\n")
            file.write(f"{space}llmRESPONSE: {response}\n\n")

            file.flush()
