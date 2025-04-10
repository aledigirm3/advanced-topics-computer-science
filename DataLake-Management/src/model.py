import torch
import torch.nn as nn
import torch.nn.functional as F

class ProjectionMLP(nn.Module):
    def __init__(self, embedding_dim=768, hidden_dim=256, output_dim=128):
        super(ProjectionMLP, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        x = self.fc(x)
        return F.normalize(x, dim=1)
        

# Contrastive Loss
class ContrastiveLoss(nn.Module):
    def __init__(self, margin=0.2):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, emb1, emb2, label):
        cosine_sim = F.cosine_similarity(emb1, emb2)

        positive_loss = label * (1 - cosine_sim)**2
        negative_loss = (1 - label) * F.relu(cosine_sim - self.margin)**2

        loss = positive_loss + negative_loss
        return loss.mean()
