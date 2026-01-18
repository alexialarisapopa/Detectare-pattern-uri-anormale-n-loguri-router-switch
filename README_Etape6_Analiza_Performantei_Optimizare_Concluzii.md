# 📘 README – Etapa 6: Analiza Performanței, Optimizarea și Concluzii Finale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Popa Alexia  
**Link Repository GitHub:** https://github.com/alexialarisapopa/Detectare-pattern-uri-anormale-n-loguri-router-switch 
**Data predării:** 25.01.2026

---

## 1. Scopul Etapei 6

Această etapă corespunde punctelor 7, 8 și 9 din programa disciplinei. Obiectivul principal este maturizarea sistemului **NeuroLog AI** prin optimizarea hiperparametrilor, analiza erorilor în context industrial și formularea concluziilor finale înainte de examinare. Aceasta reprezintă versiunea finală a aplicației software, integrând feedback-ul iterativ din etapele anterioare.

---

## 2. MESAJ CHEIE – ÎNCHEIEREA CICLULUI DE DEZVOLTARE

Etapa 6 încheie ciclul formal de dezvoltare. Sistemul este acum complet și funcțional, trecând prin următoarele faze de maturizare:
- **Actualizarea State Machine:** Ajustarea pragurilor (thresholds) și adăugarea stărilor de eroare.
- **Sincronizarea Documentației:** Actualizarea README-urilor din etapele 3, 4 și 5 pentru a reflecta modelul final.
- **Re-testarea Pipeline-ului:** Verificarea fluxului complet de la achiziția datelor la alertarea în UI.

---

## 3. PREREQUISITE – Verificare Etapa 5 (OBLIGATORIU)

Înainte de a finaliza Etapa 6, am confirmat integritatea elementelor din Etapa 5:
- [x] Model antrenat baseline salvat în `models/trained_model.pt`
- [x] Metrici baseline raportate: Accuracy 0.94, F1-score 0.92
- [x] Istoricul antrenării salvat în `results/training_history.csv`
- [x] UI Streamlit funcțional cu inferență reală

---

## 4. Experimente de Optimizare și Tabel Comparativ

Am efectuat 4 experimente sistematice pentru a îmbunătăți performanța modelului:

| **Exp#** | **Modificare față de Baseline (Etapa 5)** | **Accuracy** | **F1-score** | **Latență** | **Observații** |
|----------|------------------------------------------|--------------|--------------|-------------|----------------|
| Baseline | Configurația inițială MLP | 0.94 | 0.92 | 45ms | Referință |
| Exp 1 | Learning rate 0.001 → 0.0005 | 0.95 | 0.93 | 45ms | Convergență mai lină |
| Exp 2 | Adăugare strat Dropout (0.5) | 0.96 | 0.94 | 46ms | Reduce semnificativ overfitting-ul |
| Exp 3 | Hashing features 4096 → 8192 | 0.98 | 0.97 | 52ms | Memorie mai mare, dar precizie sporită |
| Exp 4 | Batch Normalization + AdamW | 0.99 | 0.99 | 32ms | **BEST** - Optimizat cu ONNX export |

### Justificarea configurației finale:
Am ales **Exp 4** deoarece oferă cel mai bun echilibru între precizie (99%) și latență (32ms). Utilizarea AdamW și Batch Normalization a permis modelului să stabilizeze gradienții, obținând un F1-score aproape perfect, critic pentru detecția atacurilor cibernetice.

---

## 5. Actualizarea Aplicației Software în Etapa 6

### Tabel Modificări Aplicație Software

- **Model încărcat:** Înlocuirea `trained_model.pt` cu `optimized_model.pt` (+5% Accuracy).
- **Threshold alertă:** Modificat de la 0.5 la **0.35** pentru a minimiza riscul de False Negatives (atacuri ratate).
- **Stare nouă State Machine:** Adăugarea stării `AUDIT_LOGGING` pentru salvarea fiecărei predicții.
- **UI Improvements:** Adăugarea unui indicator vizual pentru Confidence Score și a unui buton de "Report False Positive".

### Diagrama State Machine Actualizată


---

## 6. Analiza Detaliată a Performanței

### 6.1 Interpretare Confusion Matrix
**Locație:** `docs/confusion_matrix_optimized.png`

- **Clasa Normal:** Performanță excelentă (99.8%). Mesajele standard de rețea sunt ușor de identificat.
- **Clasa Anomalie:** Performanță ridicată (96.5%). Confuziile apar rar, în general pe mesaje foarte scurte și ambigue.
- **Confuzii principale:** Clasa "Config_Error" este uneori confundată cu "Normal" când severitatea este mică.

### 6.2 Analiza a 5 Exemple Greșite
1. **ID #412:** Anomalie ratată. Mesaj: "User login". Cauză: Lipsă context IP.
2. **ID #1205:** Alarmă falsă. Mesaj hardware rar. Cauză: Date puține în training.
3. **ID #2890:** Anomalie ratată. Mesaj simulat complex. Cauză: Overlap semantic.
4. **ID #3501:** Anomalie ratată. Mesaj "Connection reset". Cauză: Ambiguitate naturală a logului.
5. **ID #4812:** Alarmă falsă. Eroare admin. Cauză: Severitate setată eronat la sursă.

---

## 7. Concluzii Finale și Lecții Învățate

### 7.1 Evaluarea Performanței Finale
Sistemul **NeuroLog AI** a atins obiectivele propuse:
- Model RN funcțional cu Accuracy 99%.
- Integrare completă în pipeline-ul industrial.
- Latență sub pragul de 50ms necesar pentru monitorizare real-time.

### 7.2 Limitări Identificate
- Modelul este dependent de calitatea etichetării inițiale.
- Latența poate crește la volume de date de peste 1 milion de loguri/secundă fără optimizare hardware (GPU).

### 7.3 Lecții Învățate
- **Tehnic:** Preprocesarea prin hashing este vitală pentru date textuale sparse.
- **Proces:** Testarea iterativă a salvat timp în faza de optimizare.
- **Industrial:** Un threshold scăzut este obligatoriu în securitate pentru a asigura siguranța datelor.

---

## 8. Structura Repository-ului la Final (OBLIGATORIE)

```text
proiect-rn-popa-alexia/
├── README.md (General)
├── etapa3_analiza_date.md
├── etapa4_arhitectura_sia.md
├── etapa5_antrenare_model.md
├── etapa6_optimizare_concluzii.md (Acest fișier)
├── docs/
│   ├── state_machine_v2.png
│   ├── confusion_matrix_optimized.png
│   └── screenshots/
│       └── inference_optimized.png
├── models/
│   └── optimized_model.pt
├── results/
│   ├── optimization_experiments.csv
│   └── final_metrics.json
└── src/
    └── app/
        └── gui.py (Versiunea finală)