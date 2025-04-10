import torch
import torch.nn.functional as F
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ansi_colors import *



def cosine_similarity(embedding1, embedding2):
    return F.cosine_similarity(embedding1, embedding2, dim=0)


def evaluate(model, dataloader, threshold=0.8, device='cpu'):

    model.eval()
    correct, total = 0, 0
    tp, fp, fn = 0, 0, 0

    with torch.no_grad():
        for emb, emb2, label in dataloader:

            total += 1

            emb1 = emb.to(device)
            emb2 = emb2.to(device)
            label = label.to(device)

            proj1 = model(emb1)
            proj2 = model(emb2)

            similarity = cosine_similarity(proj1, proj2).mean()


            if similarity > threshold:
                if label.item() == 1:
                    correct += 1
                    tp += 1
                else:
                    fp += 1
            else:
                if label.item() == 1:
                    fn += 1
                else:
                    correct += 1

        accuracy = 100 * correct / total
        print(f"\n- {GREEN}Accuracy: {accuracy:.2f}%{RESET}")

        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0

        if (precision + recall) == 0:
            f1_score = 0
        else:
            f1_score = 2 * (precision * recall) / (precision + recall)

        print(f"\n{RED}Performance metrics:{RESET}")
        print(f"\n- {GREEN}Precision: {precision:.2f}{RESET}")
        print(f"\n- {GREEN}Recall: {recall:.2f}{RESET}")
        print(f"\n- {GREEN}F1: {f1_score:.2f}{RESET}\n")


