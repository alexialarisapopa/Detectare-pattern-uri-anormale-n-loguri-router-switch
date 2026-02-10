import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os
import sys

# Adăugăm calea pentru a importa corect model.py din același folder
sys.path.append(os.path.dirname(__file__))
from model import LogAnomalyModel

# Căi relative (Rulează din folderul Proiect_RN)
TRAIN_PATH = "data/train/train.npz"
VAL_PATH = "data/validation/val.npz"

def train_model():
    # 1. Încărcare date
    if not os.path.exists(TRAIN_PATH):
        print("[ERROR] Nu s-au găsit datele .npz. Verifică folderul data/train/")
        return

    train_data = np.load(TRAIN_PATH)
    val_data = np.load(VAL_PATH)

    X_train = torch.FloatTensor(train_data["X"])
    y_train = torch.FloatTensor(train_data["y"]).view(-1, 1)
    X_val = torch.FloatTensor(val_data["X"])
    y_val = torch.FloatTensor(val_data["y"]).view(-1, 1)

    # 2. Inițializare Model
    model = LogAnomalyModel(input_dim=X_train.shape[1])
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 3. Antrenare
    epochs = 20
    batch_size = 32
    print(f"[START] Antrenare pe {len(X_train)} mostre...")

    for epoch in range(epochs):
        model.train()
        # Shuffle la date
        indices = torch.randperm(X_train.size(0))
        
        for i in range(0, X_train.size(0), batch_size):
            idx = indices[i:i+batch_size]
            batch_x, batch_y = X_train[idx], y_train[idx]

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

        # Validare
        model.eval()
        with torch.no_grad():
            val_preds = model(X_val)
            val_loss = criterion(val_preds, y_val)
            acc = ((val_preds > 0.5).float() == y_val).float().mean()
            print(f"Epoca {epoch+1:02d} | Loss: {loss.item():.4f} | Val Loss: {val_loss.item():.4f} | Acc: {acc:.2%}")

    # 4. Salvare
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/trained_model.pt")
    print("\n[SUCCESS] Modelul a fost salvat în models/trained_model.pt")

if __name__ == "__main__":
    train_model()