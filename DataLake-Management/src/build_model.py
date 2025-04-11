import pickle
import torch
import paths
import numpy as np
from model import ProjectionMLP, ContrastiveLoss
from train_eval.training import train
from train_eval.evaluation import evaluate
from torch.utils.data import TensorDataset, DataLoader
from ansi_colors import *

# ===========================================================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"{CYAN}{device}{RESET}")
print(f"Cuda version: {torch.version.cuda}")
print(f"Torch version: {torch.__version__}\n")
# ===========================================================================================

def load_dataset(filename: str, batch_size: int, shuffle: bool=True):
    
    with open(paths.DATASET + filename, "rb") as f:
        pairs, labels = pickle.load(f)


    embeddings1 = np.array([emb1 for emb1, _ in pairs], dtype=np.float32)
    embeddings2 = np.array([emb2 for _, emb2 in pairs], dtype=np.float32)

    embeddings1 = torch.tensor(embeddings1, dtype=torch.float32)
    embeddings2 = torch.tensor(embeddings2, dtype=torch.float32)
    labels = torch.tensor(labels, dtype=torch.float32)

    print(embeddings1.shape)
    input_dim = embeddings1.shape[1]

    dataset = TensorDataset(embeddings1, embeddings2, labels)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    return dataloader, input_dim


if __name__ == '__main__':

    #=======hyperparameters=========
    batch_size = 16 
    num_epochs = 10
    threshold = 0.4
    #===============================

    filename = 'train_pairs_dataset.pkl'
    dataloader, input_dim = load_dataset(filename, batch_size)

    model = ProjectionMLP(embedding_dim=input_dim)
    contrastive_loss = ContrastiveLoss()

    model = model.to(device)
    print(f"{CYAN}{model}{RESET}")


    print(f"{GREEN}TRAINING...{RESET}")
    train(model, contrastive_loss, dataloader, num_epochs, device)
    
    print(f"{GREEN}EVALUATION...{RESET}")
    filename = 'test_pairs_dataset.pkl'
    dataloader, input_dim = load_dataset(filename, batch_size=1, shuffle=False)
    evaluate(model, dataloader, threshold, device)

