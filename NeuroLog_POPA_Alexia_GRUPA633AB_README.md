# README – Etapa 6: Analiza Performanței, Optimizarea și Concluzii Finale

**Disciplina:** Rețele Neuronale

**Instituție:** POLITEHNICA București – FIIR

**Student:** Popa Alexia

**Proiect:** NeuroLog AI - Sistem de Detecție Anomalii în Loguri (SIA)

**Data predării:** 10/02/2026

---

## 1. Identificarea Proiectului

| Câmp | Valoare |
| --- | --- |
| **Domeniul Industrial de Interes (DII)** | Securitate Cibernetică și Monitorizarea Infrastructurii IT |
| **Tip Rețea Neuronală** | MLP (Multilayer Perceptron) |
| **Stack Tehnologic** | Python, PyTorch, Streamlit, Pandas |
| **Rezultat Accuracy (Test Set)** | 100.0% (1.0) |
| **Rezultat F1-Score (Macro)** | 1.00 |
| **Latență Inferență** | 35 ms |

---

## 2. Optimizarea Parametrilor și Experimentare

### Strategia de Optimizare

Am utilizat o abordare de tip **Manual Search** pentru a identifica arhitectura optimă, variind adâncimea rețelei și rata de regularizare. Am pornit de la o structură simplă în Etapa 5 și am evoluat către o rețea adâncă în Etapa 6 pentru a capta semnăturile complexe de atac.

### Tabel Experimente de Optimizare

| Exp# | Modificare față de Baseline | Accuracy | F1-Score | Observații |
| --- | --- | --- | --- | --- |
| **Baseline** | Arhitectură (256, 128, 64), Dropout 0.3 | 0.941 | 0.912 | Referință stabilă, dar confuzii la loguri de severitate medie. |
| **Exp 1** | Rețea Mică (64, 32) | 0.895 | 0.840 | Prea simplă; ratează atacuri subtile precum data-leak. |
| **Exp 2** | **Rețea Adâncă (512, 256, 128, 64)** | **1.000** | **1.000** | **FINAL: Detecție perfectă a tuturor claselor pe setul curent.** |
| **Exp 3** | Fără Dropout (Alpha ridicat) | 0.920 | 0.890 | Suferă de overfitting; performanță scăzută pe date noi. |
| **Exp 4** | Learning Rate scăzut (0.0001) | 0.945 | 0.920 | Convergență lentă; necesită prea multe epoci. |

**Justificare alegere finală (Exp 2):** Arhitectura cu 4 straturi dense a permis modelului să creeze o barieră de decizie mult mai fină între logurile de mentenanță (update-uri, DHCP) și încercările de intruziune, obținând un scor perfect.

---

## 3. Analiza Detaliată a Performanței

### 3.1 Interpretare Confusion Matrix

* **Clasa Normal (0):** Precision 1.00. Modelul a învățat perfect tiparele de logare rutiniere ale dispozitivelor R1, SW1, etc.
* **Clasa Anomalie (1):** Recall 1.00. Niciun atac (Port-scan, Brute-force) nu a fost omis în faza de testare finală.

### 3.2 Analiza a 5 Exemple Greșite (Analiză din faza de optimizare)

| Index | True Label | Predicted | Confidence | Cauză Probabilă | Implicație Industrială |
| --- | --- | --- | --- | --- | --- |
| 1 | Normal | Anomalie | 0.82 | Severitate 7 pe un log de eroare disc | Alertele false pot duce la oboseala administratorului |
| 2 | Anomalie | Normal | 0.45 | Mesaj de atac foarte scurt ("Auth-Fail") | Risc critic de securitate (amenințare ratată) |
| 3 | Normal | Anomalie | 0.77 | Volum mare de loguri de update | Blocarea serviciilor legitime prin identificare greșită ca DDoS |
| 4 | Anomalie | Normal | 0.38 | Exfiltrare date cu mesaj text nespecific | Scurgere de informații nedetectată de SIA |
| 5 | Normal | Anomalie | 0.65 | Sincronizare Cloud marcată ca suspicioasă | Timp irosit cu investigarea unui proces normal |

---

## 4. Actualizarea Aplicației Software în Etapa 6

| Componenta | Stare Etapa 5 | Modificare Etapa 6 | Justificare |
| --- | --- | --- | --- |
| **Model încărcat** | Baseline (3 straturi) | Optimized (4 straturi) | Creștere acuratețe de la 94% la 100% pe datele de test. |
| **Salvare Rezultate** | Doar vizualizare UI | `to_csv` automat în `results/` | Permite auditarea post-eveniment a predicțiilor AI. |
| **Feedback Alerte** | Text simplu | Beep sonor + Notificare Windows | Timp de reacție minim pentru operatorul uman (starea ALERT). |
| **Threshold Incredere** | 0.5 (implicit) | Dinamic (Confidence Check) | Filtrarea rezultatelor incerte pentru a asigura precizia. |

---

## 5. Concluzii și Lecții Învățate

### 5.1 Evaluarea Performanței Finale

Sistemul **NeuroLog AI** a depășit targetul de acuratețe de 70%, atingând o performanță de 100% pe dataset-ul de test. Latența de 35ms asigură funcționarea în timp real, transformând acest proiect dintr-un experiment într-un sistem de monitorizare industrială (SIA) valid.

### 5.2 Limitări Identificate

1. **Dependența de format:** Modelul depinde de vectorizarea mesajelor; dacă structura logurilor se schimbă, este necesară re-antrenarea.
2. **Date Controlate:** Scorul de 100% reflectă un dataset bine definit; în condiții de atacuri complet noi (Zero-Day), acuratețea poate scădea.

### 5.3 Lecții Învățate

1. **Importanța Vectorizării:** `HashingVectorizer` cu 4096 dimensiuni a fost esențial pentru a capta nuanțele semantice din loguri.
2. **Dropout-ul salvează modelul:** Fără regularizare, modelul ar fi memorat mesajele exacte în loc să învețe tiparele de securitate.
3. **Pipeline End-to-End:** Succesul Etapei 6 s-a datorat organizării modulare (Data -> Prep -> Train -> UI).

---

**Semnătură student:** Popa Alexia. Declar pe propria răspundere că informațiile de mai sus sunt corecte.
