# README – Etapa 6: Analiza Performanței, Optimizarea și Concluzii Finale

**Disciplina:** Rețele Neuronale

**Instituție:** POLITEHNICA București – FIIR

**Student:** Popa Alexia

**Link Repository GitHub:** https://github.com/alexialarisapopa/Detectare-pattern-uri-anormale-n-loguri-router-switch/edit/main/README_Etape6_Analiza_Performantei_Optimizare_Concluzii.md

**Data predării:** 10/02/2026

## 1. Identificare Proiect

| Câmp | Valoare |
| --- | --- |
| **Domeniul Industrial de Interes** | Securitate Cibernetică / Monitoring IT |
| **Tip Rețea Neuronală** | MLP (Multilayer Perceptron) |
| **Stack Tehnologic** | Python, PyTorch, Streamlit |
| **Acces Repository** | Public |

### Rezultate Cheie (Versiunea Finală vs Etapa 6)

| Metric | Țintă Minimă | Rezultat Etapa 6 | Status |
| --- | --- | --- | --- |
| Accuracy (Test Set) | ≥70% | **100.0%** | [✓] |
| F1-Score (Macro) | ≥0.65 | **1.00** | [✓] |
| Latență Inferență | ≤50 ms | **35 ms** | [✓] |
| Contribuție Date Originale | ≥40% | **40%** | [✓] |

---

## 2. Descrierea Nevoii și Soluția SIA

### 2.1 Nevoia Reală / Studiul de Caz

Problema concretă pe care o rezolvă proiectul este **detectarea proactivă a atacurilor cibernetice** mascate în jurnalele de sistem masive. Administratorii IT nu pot procesa manual mii de loguri pe secundă, riscând să rateze incidente critice precum exfiltrarea de date sau scanările de porturi.

**NeuroLog AI** înlocuiește analiza manuală cu automatizarea calculului de probabilitate a anomaliilor prin implementarea unei rețele neuronale MLP, eliminând eroarea umană. Am ales această soluție pentru a asigura o precizie imposibil de atins prin metode tradiționale, reușind să eliminăm complet alarmele false în setul de test. Sistemul garantează o monitorizare personalizată, fiind un instrument esențial pentru securitatea infrastructurilor critice.

### 2.2 Beneficii Măsurabile

1. **Reducerea timpului de detecție (MTTD):** Optimizarea sistemului pentru un răspuns de 35 ms.
2. **Precizie industrială:** Atingerea unei acuratețe de 100% pe scenariile de atac simulate.
3. **Eliminarea oboselii de alertare:** F1-score de 1.00 asigură faptul că fiecare alertă generată este reală.

---

## 3. Arhitectura SIA și State Machine

### 3.1 Cele 3 Module Software

| Modul | Tehnologie | Funcționalitate |
| --- | --- | --- |
| **Data Acquisition** | Python | Generare și echilibrare dataset (40% originale / 60% simulate). |
| **Neural Network** | PyTorch | Rețea MLP optimizată (512-256-128-64) pentru clasificare. |
| **UI / Web Service** | Streamlit | Interfață live pentru monitorizare și alerte vizuale. |

### 3.2 State Machine

| Stare | Descriere | Condiție Ieșire |
| --- | --- | --- |
| `IDLE` | Serverul pornit, așteaptă încărcarea fișierului de loguri. | Încărcare CSV în UI |
| `CONFIG_INIT` | Încărcarea automată a modelului `.pt` și a `scaler.pkl`. | Modele în memorie |
| `PREPROCESS` | Curățare Regex și vectorizare Hashing a mesajelor. | Tensors disponibili |
| `INFERENCE` | Rularea datelor prin MLP pentru generarea predicției. | Scor generat |
| `CONFIDENCE_CHECK` | Validarea rezultatului (threshold 0.5) și declanșarea alertei. | Afișare în UI |

---

## 4. Modelul RN – Antrenare și Optimizare

### 4.1 Arhitectura Rețelei

Am ales o arhitectură **MLP (Multilayer Perceptron)** adâncă pentru a capta corelațiile dintre textul logului și severitate:

* **Input:** 4097 neuroni (Hashing Vectorizer + Severity).
* **Hidden Layers:** 4 straturi (512, 256, 128, 64) cu activare **ReLU**.
* **Regularizare:** Dropout 0.3 pentru a preveni memorarea datelor simulate.
* **Output:** 1 neuron (Sigmoid) pentru probabilitatea de anomalie.

### 4.2 Tabel Experimente de Optimizare

| Exp# | Modificare față de Baseline | Accuracy | Timp antrenare | Observații |
| --- | --- | --- | --- | --- |
| **Baseline** | MLP (256, 128, 64) | 0.941 | ~10s | Referință stabilă. |
| **Exp 1** | Rețea Mică (64, 32) | 0.895 | ~5s | Ratează atacuri complexe. |
| **Exp 2** | **Adâncire (512, 256, 128, 64)** | **1.000** | **~15s** | **FINAL: Precizie perfectă.** |
| **Exp 3** | Dropout 0.3 -> 0.5 | 0.910 | ~15s | Regularizare prea agresivă. |

---

## 5. Analiza Performanței și Erori

### 5.1 Confusion Matrix

**Locație:** `docs/confusion_matrix_optimized.png`

**Interpretare:** Clasa **Anomalie (1)** are Recall 100%. Niciun atac cibernetic nu a fost omis de modelul optimizat.

### 5.2 Analiza Top 5 Erori (Faza de optimizare)

| # | Input | Predicție | Cauză Probabilă | Soluție Etapa 6 |
| --- | --- | --- | --- | --- |
| 1 | Eroare Disc (Sev 7) | Anomalie | Severitate mare interpretată ca atac. | Re-antrenare cu Exp 2. |
| 2 | Brute-force lent | Normal | Frecvență redusă a mesajelor. | Adâncire rețea (straturi). |
| 3 | Update Windows | Anomalie | Volum mare (fals DDoS). | Hashing vectorizer extins. |
| 4 | Data Leak scurt | Normal | Mesaj text nespecific. | Dropout ajustat. |
| 5 | Sync Cloud | Anomalie | Tipar atipic de upload. | Thresholding 0.5. |

---

## 6. Actualizări Aplicație Software

| Componentă | Stare Etapa 5 | Modificare Etapa 6 | Justificare |
| --- | --- | --- | --- |
| **Model** | `trained_model.h5` | `trained_model.pt` | Trecerea la PyTorch pentru optimizarea latenței. |
| **Configurare** | Hardcoded | `results/test_metrics.json` | Automatizarea citirii performanței. |
| **Threshold** | 0.5 | **0.5 (Conf. Check)** | Filtrarea predicțiilor nesigure. |
| **UI** | Tabel simplu | Dashboard cu Alerte | Reacție rapidă pentru operator. |

---

## 7. Concluzii și Lecții Învățate

1. **Scalarea datelor:** Fără `StandardScaler`, severitatea logului domina mesajul text.
2. **Arhitectura:** MLP-ul adânc este obligatoriu pentru prelucrarea textului hashed.
3. **Modularizare:** Separarea codului în module a facilitat atingerea latenței de **35ms**.
4. **Viitor:** Integrarea cu un sistem de blocare automată a IP-urilor suspecte (Sistem IoT).

---

**Semnătură student:** Popa Alexia

**Tag Git:** `v0.6-optimized-final`

---

### 📂 Structura Repository-ului Final

```text
Proiect_RN/
├──app/
|   ├── guy.py
|   ├── main.py
├── data/
│   ├── processed
│   ├── raw
│   ├── test
|   ├── train
│   ├── validation
├── docs/
│   ├── confusion_matrix_optimized.png
│   ├── learning_curves_final.png
│   ├── metrics_evolution.png
├── src/
│   ├── data_acquisition/ (generare_log.py)
│   ├── preprocessing/ (data_prep.py)
│   ├── neural_network/ (model.py, train.py, evaluare_finala.py)
├── models/
│   ├── trained_model.pt
│   └── scaler.pkl
├── results/
│   ├── test_metrics.json
│   └── predicted_logs_v2.csv
└── requirements.txt
```
