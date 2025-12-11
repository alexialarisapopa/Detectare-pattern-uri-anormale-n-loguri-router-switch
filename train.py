import numpy as np
import tensorflow as tf
import os
from model import build_model

TRAIN = "data/train/train.npz"
VAL = "data/validation/val.npz"

train = np.load(TRAIN)
val = np.load(VAL)

X_train, y_train = train["X"], train["y"]
X_val, y_val = val["X"], val["y"]

model = build_model(X_train.shape[1])

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=32,
    verbose=1
)

os.makedirs("models", exist_ok=True)
model.save("models/trained_model.h5")

np.savetxt("results/training_history.csv",
           np.array(history.history["loss"]))

print("\n[INFO] Training complete!")
