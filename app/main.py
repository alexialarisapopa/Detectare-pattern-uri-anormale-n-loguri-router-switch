import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import os
import re
from sklearn.feature_extraction.text import HashingVectorizer
from plyer import notification
import winsound

# =====================================================
# 1. DEFINIREA ARHITECTURII RN (Identică cu train.py)
# =====================================================
class LogAnomalyModel(nn.Module):
    def __init__(self, input_dim):
        super(LogAnomalyModel, self).__init__()
        # Folosim nn.Sequential pentru a corespunde exact cu structura salvată
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

# =====================================================
# 2. CONFIGURARE CĂI (Relative la rădăcina proiectului)
# =====================================================
INPUT_FILE = "data/raw/generated_logs.csv"
MODEL_PATH = "models/trained_model.pt"
OUTPUT_FILE = "data/processed/predicted_logs_v2.csv"

def clean_text(msg):
    msg = re.sub(r"[^a-zA-Z0-9\s\-:]", " ", str(msg))
    msg = re.sub(r"\s+", " ", msg)
    return msg.lower().strip()

# =====================================================
# 3. LOGICA PRINCIPALĂ (STATE MACHINE)
# =====================================================
def run_sia_inference():
    print("\n--- [SIA] Sistem de Monitorizare Activ (Etapa 5) ---")
    
    # Verificare existență fișiere
    if not os.path.exists(MODEL_PATH):
        print(f"[EROARE] Nu am găsit modelul la {MODEL_PATH}. Rulează train.py mai întâi!")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"[EROARE] Nu am găsit fișierul de intrare la {INPUT_FILE}")
        return

    # STARE: ACQUIRE DATA
    df = pd.read_csv(INPUT_FILE)
    print(f"[INFO] Se analizează {len(df)} mesaje de log...")

    # STARE: PREPROCESS
    df['clean_message'] = df['message'].apply(clean_text)
    
    # CORECOARE DIMENSIUNE: Schimbăm n_features la 4096 pentru a corespunde modelului antrenat
    # 4096 (text) + 1 (severity) = 4097 (dimensiunea cerută de modelul tău)
    vectorizer = HashingVectorizer(n_features=4096)
    X_text = vectorizer.transform(df['clean_message']).toarray()
    
    # Combinăm textul vectorizat cu severitatea
    X_input = np.hstack([X_text, df[['severity']].values])
    X_tensor = torch.FloatTensor(X_input)

    # STARE: RN_INFERENCE
    # Inițializăm modelul cu dimensiunea corectă (4097)
    model = LogAnomalyModel(input_dim=X_input.shape[1])
    
    # Încărcăm "creierul" antrenat
    try:
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        print("[SUCCESS] Modelul PyTorch a fost încărcat corect.")
    except RuntimeError as e:
        print(f"[EROARE CRITICĂ] Dimensiunea datelor nu se potrivește: {e}")
        return

    with torch.no_grad():
        probs = model(X_tensor)
        # Predicție binară (0 sau 1)
        df['prediction'] = (probs > 0.5).int().numpy()
        df['confidence'] = probs.numpy()

    # STARE: THRESHOLD CHECK & ALERT
    anomalies = df[df['prediction'] == 1]
    
    if not anomalies.empty:
        print(f"\n[ALERTA] Detectate {len(anomalies)} posibile atacuri/anomalii!")
        
        # Notificare vizuală în Windows
        try:
            notification.notify(
                title='SIA: Anomalii Detectate',
                message=f'S-au identificat {len(anomalies)} evenimente suspecte în loguri.',
                timeout=7
            )
        except:
            print("[INFO] Notificarea vizuală nu a putut fi afișată.")
        
        # Semnal sonor (BEEP)
        winsound.Beep(1000, 400)
        
        # Afișăm primele 5 anomalii găsite pentru verificare
        print("\nPrimele anomalii identificate:")
        print(anomalies[['device', 'message', 'confidence']].head())

    # SALVARE REZULTATE
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[INFO] Rezultate salvate în: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_sia_inference()