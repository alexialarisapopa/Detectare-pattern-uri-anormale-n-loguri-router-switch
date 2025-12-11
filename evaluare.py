import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, classification_report

TEST = "data/test/test.npz"
MODEL = "models/trained_model.h5"

test = np.load(TEST)
X_test, y_test = test["X"], test["y"]

model = tf.keras.models.load_model(MODEL)

pred_probs = model.predict(X_test)
preds = (pred_probs > 0.5).astype(int)

print("Accuracy:", accuracy_score(y_test, preds))
print("F1-score:", f1_score(y_test, preds))
print("\nClassification Report:\n", classification_report(y_test, preds))
