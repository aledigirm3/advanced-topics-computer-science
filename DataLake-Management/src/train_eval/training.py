import torch


def train(model, loss_fn, dataloader, num_epochs, device='cpu'):

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for emb1, emb2, label in dataloader:

            emb1 = emb1.to(device)
            emb2 = emb2.to(device)
            label = label.to(device)

            optimizer.zero_grad()

            proj1 = model(emb1)
            proj2 = model(emb2)

            loss = loss_fn(proj1, proj2, label)
            total_loss += loss.item()

            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {total_loss/len(dataloader)}")