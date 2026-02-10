import streamlit as st
import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import os
import re
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from plyer import notification
import winsound
import datetime  # Adăugat pentru a marca timpul salvării

# =====================================================
# 1. DEFINIREA ARHITECTURII RN
# =====================================================
class LogAnomalyModel(nn.Module):
    def __init__(self, input_dim):
        super(LogAnomalyModel, self).__init__()
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
# 2. FUNCȚII HELPER
# =====================================================
def clean_text(msg):
    msg = re.sub(r"[^a-zA-Z0-9\s\-:]", " ", str(msg))
    msg = re.sub(r"\s+", " ", msg)
    return msg.lower().strip()

@st.cache_resource
def load_model(model_path, input_dim):
    if os.path.exists(model_path):
        model = LogAnomalyModel(input_dim=input_dim)
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model
    return None

# =====================================================
# 3. INTERFAȚA STREAMLIT
# =====================================================
st.set_page_config(page_title="SIA - Dashboard Detecție", layout="wide")

st.title("🛡️ SIA: Sistem de Monitorizare și Detecție Anomalii")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurare")
MODEL_PATH = "models/trained_model.pt"
INPUT_DIM = 4097 

# Încărcare model
model = load_model(MODEL_PATH, INPUT_DIM)

if model:
    st.sidebar.success("✅ Model PyTorch încărcat cu succes!")
else:
    st.sidebar.error("❌ Modelul .pt nu a fost găsit!")

# Upload fișier
uploaded_file = st.sidebar.file_uploader("Încarcă loguri noi (CSV)", type="csv")

if uploaded_file is not None and model is not None:
    df = pd.read_csv(uploaded_file)
    
    with st.spinner('Analiză în curs cu Rețeaua Neuronală...'):
        # Preprocesare
        df['clean_message'] = df['message'].apply(clean_text)
        vectorizer = HashingVectorizer(n_features=4096)
        X_text = vectorizer.transform(df['clean_message']).toarray()
        X_input = np.hstack([X_text, df[['severity']].values])
        X_tensor = torch.FloatTensor(X_input)
        
        # Inferență
        with torch.no_grad():
            probs = model(X_tensor)
            df['prediction'] = (probs > 0.5).int().numpy()
            df['confidence'] = probs.numpy()

        # --- SALVARE REZULTATE PE DISC (ETAPA 6) ---
        # Această secțiune forțează actualizarea fișierului cu data de azi
        if not os.path.exists("results"):
            os.makedirs("results")
        df.to_csv("results/predicted_logs_v2.csv", index=False)
        # -------------------------------------------

    # --- METRICI ---
    anomalies_count = int(df['prediction'].sum())
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Loguri", len(df))
    col2.metric("Anomalii Detectate", anomalies_count, delta=f"{(anomalies_count/len(df))*100:.1f}%", delta_color="inverse")
    col3.metric("Status Sistem", "ALERTĂ" if anomalies_count > 0 else "SIGUR", 
              delta="Pericol" if anomalies_count > 0 else "OK")

    # --- ALERTĂ ---
    if anomalies_count > 0:
        st.error(f"⚠️ Atenție! Au fost detectate {anomalies_count} activități suspecte.")
        try:
            winsound.Beep(1000, 400)
            notification.notify(title="SIA Alert", message=f"Detectate {anomalies_count} anomalii!", timeout=5)
        except:
            pass # Previne erori pe sisteme care nu suportă winsound/notifications

    # --- VIZUALIZARE ---
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.write("### 📈 Distribuție Evenimente")
        fig, ax = plt.subplots(figsize=(6, 6))
        labels = ['Normal', 'Anomalie']
        sizes = [len(df) - anomalies_count, anomalies_count]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#5dade2', '#ec7063'])
        st.pyplot(fig)

    with c2:
        st.write("### 🚨 Lista Anomaliilor (Top 10)")
        anomalies_df = df[df['prediction'] == 1].sort_values(by='confidence', ascending=False)
        st.dataframe(anomalies_df[['device', 'message', 'confidence']].head(10), use_container_width=True)

    st.write("### 📋 Toate datele procesate (Salvate în results/predicted_logs_v2.csv)")
    st.dataframe(df[['timestamp', 'device', 'severity', 'message', 'prediction', 'confidence']])

else:
    if model is None:
        st.warning("⚠️ Te rugăm să te asiguri că modelul este antrenat și salvat în folderul models/ înainte de a încărca date.")
    else:
        st.info("👋 Bine ai venit! Te rugăm să încarci un fișier CSV cu loguri din bara laterală pentru a începe monitorizarea.")