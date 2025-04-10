import os
import paths
import itertools
import pandas as pd
from embedder import Embedder
import pickle
from ansi_colors import *

def remove_tables(dir: str, startWith: str):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.startswith(startWith):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"{RED}{file_path} removed{RESET}")

def prepare_data():
    remove_tables(paths.TABLES.TRAIN.value, 'test_')
    remove_tables(paths.TABLES.TEST.value, 'training_')


def create_positive_pairs(dir: str, embedder: Embedder):
    print(f"- {CYAN}Creating positive pairs (embeddings)...{RESET}")
    pairs_dataset = []
    labels = []
    for root, dirs, files in os.walk(dir):
        if root == dir:
            continue

        # Possible pairs
        pairs = list(itertools.combinations(files, 2))

        for (file1, file2) in pairs:
            #print(f"({root}/{file1}, {root}/{file2})")
            emb1, emb2 = embed_pair(root + '/' + file1, root +'/' + file2, embedder)
            pairs_dataset.append((emb1, emb2))
            labels.append(1)

    print(f"{GREEN}All files completed{RESET}\n")
    return pairs_dataset, labels



def create_negative_pairs(dir: str, embedder: Embedder):
    
    print(f"- {CYAN}Creating negative pairs (embeddings)...{RESET}")
    folders = sorted([os.path.join(dir, d) for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))])

    pairs_dataset = []
    labels = []

    for i in range(len(folders) - 1):
        dir1 = folders[i]
        dir2 = folders[i + 1]

        # Files for each folder
        files1 = [(folders[i], f) for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))]
        files2 = [(folders[i + 1], f) for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))]

        # Generate possible pairs from dir1 and dir2
        pairs = list(itertools.product(files1, files2))

        #print(f"\nPairs from {os.path.basename(dir1)} and {os.path.basename(dir2)}:")
        for (dir_a, file_a), (dir_b, file_b) in pairs:
            emb1, emb2 = embed_pair(dir_a + '/' + file_a, dir_b + '/' + file_b, embedder)
            pairs_dataset.append((emb1, emb2))
            labels.append(0)
    
    print(f"{GREEN}All files completed{RESET}\n")
    return pairs_dataset, labels



def embed_pair(table1: str, table2: str, embedder: Embedder):
    df1 = pd.read_csv(table1, dtype=str)
    df1 = df1.drop(df1.columns[0], axis=1)
    df2 = pd.read_csv(table2, dtype=str)
    df2 = df2.drop(df2.columns[0], axis=1)
    

    result1 = ""
    result2 = ""

    # Takes the first 10 lines
    for col in df1.columns:
        result1 += f'{col}:\n'
        result1 += ', '.join(map(str, df1[col].head(10).to_list()))
        result1 += '\n'

    for col in df2.columns:
        result2 += f'{col}:\n'
        result2 += ', '.join(map(str, df2[col].head(10).to_list()))
        result2 += '\n'

    embed1 = embedder.get_sentence_embedding(result1)
    embed2 = embedder.get_sentence_embedding(result2)

    return embed1, embed2

if __name__ == '__main__':

    prepare_data()
    
    os.makedirs(paths.DATASET, exist_ok=True)
    embedder = Embedder()

    # TRAIN DATASET
    print(f"==={CYAN}TRAIN{RESET}===")
    positive_pairs, positive_labels = create_positive_pairs(paths.TABLES.TRAIN.value, embedder)
    negative_pairs, negative_labels = create_negative_pairs(paths.TABLES.TRAIN.value, embedder)
    pairs = positive_pairs + negative_pairs
    labels = positive_labels + negative_labels
    with open(paths.DATASET + 'train_pairs_dataset.pkl', 'wb') as f:
        pickle.dump((pairs, labels), f)


    # TEST DATASET
    print(f"==={CYAN}TEST{RESET}===")
    positive_pairs, positive_labels = create_positive_pairs(paths.TABLES.TEST.value, embedder)
    negative_pairs, negative_labels = create_negative_pairs(paths.TABLES.TEST.value, embedder)
    pairs = positive_pairs + negative_pairs
    labels = positive_labels + negative_labels
    with open(paths.DATASET + 'test_pairs_dataset.pkl', 'wb') as f:
        pickle.dump((pairs, labels), f)
