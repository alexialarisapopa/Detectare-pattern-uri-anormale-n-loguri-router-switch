import numpy as np
import torch
import json
import os
from sklearn.metrics import accuracy_score, f1_score, classification_report
from model import LogAnomalyModel

# Căi
TEST_PATH = "data/test/test.npz"
MODEL_PATH = "models/trained_model.pt"

def evaluate():
    # 1. Încărcare date test
    data = np.load(TEST_PATH)
    X_test = torch.FloatTensor(data["X"])
    y_test = data["y"]

    # 2. Încărcare model
    model = LogAnomalyModel(input_dim=X_test.shape[1])
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    # 3. Predicție
    with torch.no_grad():
        probs = model(X_test)
        preds = (probs > 0.5).int().numpy().flatten()

    # 4. Calcul metrici
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average='macro')
    
    metrics = {
        "test_accuracy": float(acc),
        "test_f1_macro": float(f1)
    }

    # 5. Salvare JSON
    os.makedirs("results", exist_ok=True)
    with open("results/test_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print("\n--- REZULTATE FINALE TEST ---")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, preds))

if __name__ == "__main__":
    evaluate()