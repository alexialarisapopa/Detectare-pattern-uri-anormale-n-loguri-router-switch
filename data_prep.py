import pandas as pd
import numpy as np
import os
import re
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

RAW_FILE = "data/raw/generated_logs.csv"
PROCESSED_DIR = "data/processed"
TRAIN_DIR = "data/train"
VAL_DIR = "data/validation"
TEST_DIR = "data/test"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

def clean_text(msg):
    msg = re.sub(r"[^a-zA-Z0-9\s\-:]", " ", msg)
    msg = re.sub(r"\s+", " ", msg)
    return msg.lower().strip()

print("[INFO] Loading raw logs...")
df = pd.read_csv(RAW_FILE)

df["clean_message"] = df["message"].apply(clean_text)

vectorizer = HashingVectorizer(
    n_features=2**12,
    alternate_sign=False
)

X_text = vectorizer.transform(df["clean_message"]).toarray()
X_sev = df[["severity"]].values

scaler = StandardScaler()
X_sev_scaled = scaler.fit_transform(X_sev)

X = np.hstack([X_text, X_sev_scaled])
y = df["label"].values

joblib.dump(scaler, "config/scaler.pkl")

print("[INFO] Splitting data (70/15/15)...")
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

np.savez(os.path.join(TRAIN_DIR, "train.npz"), X=X_train, y=y_train)
np.savez(os.path.join(VAL_DIR, "val.npz"), X=X_val, y=y_val)
np.savez(os.path.join(TEST_DIR, "test.npz"), X=X_test, y=y_test)

print("[INFO] Data preparation complete!")
