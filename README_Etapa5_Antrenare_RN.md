# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale

**Instituție:** POLITEHNICA București – FIIR

**Student:** Popa Alexia

**Link Repository GitHub:** (https://github.com/alexialarisapopa/Detectare-pattern-uri-anormale-n-loguri-router-switch)

**Data predării:** 18.12.2025

---

## 1. Scopul Etapei 5

Această etapă corespunde punctului **6. Configurarea și antrenarea modelului RN** din lista de 9 etape. Obiectivul principal este antrenarea efectivă a modelului MLP (Multi-Layer Perceptron) definit anterior pe dataset-ul de loguri, evaluarea performanței obținute și integrarea modelului antrenat în aplicația de monitorizare.

---

## 2. PREREQUISITE – Verificare Etapa 4

Înainte de antrenare, am confirmat existența următoarelor elemente din etapa anterioară:

* **State Machine** definit și documentat în folderul `docs/`.
* **Contribuție originală de 40%** (20.000 de loguri generate propriu) în `data/generated/`.
* **Cele 3 module funcționale**: Data Logging (Modul 1), Arhitectură RN (Modul 2) și Interfață Streamlit (Modul 3).

---

## 3. Pregătire Date pentru Antrenare

Am refăcut preprocesarea completă pe dataset-ul combinat (30.000 loguri publice + 20.000 loguri originale):

* **Split Stratificat**: 70% Train (35.000 samples), 15% Validation (7.500 samples), 15% Test (7.500 samples).
* **Parametri**: Am utilizat `random_state=42` pentru reproducibilitate și `HashingVectorizer` cu 4096 de caracteristici.

---

## 4. Hiperparametri și Justificări (Nivel 1)

* **Learning rate: 0.001** - Valoare standard pentru Adam optimizer, asigurând o convergență stabilă pe datele de tip text.
* **Batch size: 32** - Oferă un echilibru între stabilitatea gradientului și memoria utilizată pentru cele 50.000 de mostre.
* **Number of epochs: 20** - Numărul de iterații necesar pentru ca modelul să atingă performanța maximă fără overfitting.
* **Optimizer: Adam** - Algoritm adaptiv eficient pentru rețele neuronale ce procesează date sparse.
* **Loss function: BCELoss** - Utilizată pentru clasificarea binară (Normal vs. Anomalie).
* **Activation functions**: **ReLU** în straturile ascunse (pentru non-linearitate) și **Sigmoid** la ieșire (pentru calcularea probabilității).

---

## 5. Analiză Erori în Context Industrial (Nivel 2)

### A. Analiza claselor cu dificultăți

Deși modelul prezintă o acuratețe de aproape 100%, erori pot apărea la logurile de mentenanță care generează mesaje similare cu atacurile de tip Denial of Service (volum mare de date într-un timp scurt).

### B. Caracteristici cauzatoare de erori

Mesajele foarte scurte sau generice (ex: "System updated") pot fi interpretate eronat dacă în setul de antrenare au fost asociate accidental cu activități suspecte.

### C. Implicații industriale

* **False Negatives (Atac ratat)**: Reprezintă riscul cel mai mare, putând duce la oprirea producției.
* **False Positives (Alarmă falsă)**: Sunt mai puțin critice, necesitând doar o verificare manuală rapidă din partea operatorului.
* **Prioritate**: Minimizarea cazurilor în care atacurile reale sunt ignorate.

### D. Măsuri corective propuse

1. Introducerea de augmentări (zgomot în text) pentru a face modelul mai robust.
2. Implementarea unui "Learning Rate Scheduler" pentru a rafina antrenarea în ultimele epoci.
3. Colectarea și re-etichetarea manuală a cazurilor unde modelul a fost nesigur (scoruri de confidence apropiate de 0.5).

---

## 6. Verificare Consistență cu State Machine

Interfața actualizată respectă fluxul definit în Etapa 4:

* **ACQUIRE_DATA**: Încarcă fișierul de test în interfața Streamlit.
* **PREPROCESS**: Aplică aceiași parametri de scalare și vectorizare.
* **RN_INFERENCE**: Utilizează modelul antrenat din `models/trained_model.pt`.
* **THRESHOLD_CHECK**: Clasifică logul ca anomalie dacă probabilitatea este peste 0.4.
* **ALERT**: Declanșează notificarea vizuală și sonoră (Beep) în dashboard.

---

## 7. Structura Repository-ului la Finalul Etapei 5

* **data/**: Conține subfolderele `train/`, `validation/` și `test/` populate cu datele finale.
* **models/trained_model.pt**: Fișierul modelului antrenat (rezultatul principal).
* **results/training_history.csv**: Istoricul antrenării pe toate cele 20 de epoci.
* **results/test_metrics.json**: Fișier cu metrica finală (Accuracy: 1.0, F1: 1.0).
* **docs/loss_curve.png**: Graficul ce demonstrează scăderea erorii în timpul antrenării.
* **docs/screenshots/inference_real.png**: Imagine cu interfața realizând o detecție reală.

---

## 8. Checklist Final – Verificare înainte de predare

* [x] Model antrenat minim 10 epoci (rulate 20).
* [x] Performanță atinsă: **Acuratețe ≥ 65%** (realizat 100%) și **F1-score ≥ 0.60** (realizat 1.0).
* [x] Modelul antrenat este salvat și încărcat corect în UI.
* [x] Analiza erorilor industriale este completată în acest document.
* [x] Screenshot-ul cu inferența reală este prezent în folderul `docs/`.

---

**Tag Git**: `git tag -a v0.5-model-trained -m "Etapa 5 - Model antrenat"`

**Mesaj Commit**: `"Etapa 5 completă – Accuracy=1.0, F1=1.0"`
