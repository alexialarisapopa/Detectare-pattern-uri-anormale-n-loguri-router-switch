# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Popa Alexia  
**Link Repository GitHub:** https://github.com/alexialarisapopa/Detectare-pattern-uri-anormale-n-loguri-router-switch/blob/main/README_Etapa4_Arhitectura_SIA.md  
**Data:** 04.12.2025  

---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN**.  
Am construit un schelet complet funcțional al aplicației pentru detecția anomaliilor în loguri, unde modelul RN (Multi-Layer Perceptron / Autoencoder) este definit și compilat, aflându-se într-o fază incipientă. Toate modulele pornesc fără erori și pipeline-ul rulează end-to-end.

---

## 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Detectarea logurilor anormale în timp real pentru dispozitive industriale | Model RN (Clasificator) → clasifică logurile ca normale/anormale și calculează scor anomalie | Data Logging + RN Module + UI |
| Alertare rapidă operator la apariția logurilor critice | Generare alertă pop-up și sunet beep când se detectează anomalii | RN Module + UI |
| Monitorizare evoluție anomalii în timp | Grafic timeline cu numărul de anomalii pe oră | UI + RN Module |

---

## 2. Contribuția Voastră Originală la Setul de Date

**Total observații finale:** 5,000 (după Etapa 3 + Etapa 4)  
**Observații originale:** 2,000 (40%)  

**Tipul contribuției:** [X] Date generate prin simulare fizică  
[ ] Date achiziționate cu senzori proprii  
[ ] Etichetare/adnotare manuală  
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:** Am generat loguri simulate pentru diverse dispozitive, cu severitate variabilă și mesaje tipice. Fiecare log are timestamp, device, severity, message și label (0-normal / 1-anomalie). Aceste date originale au fost adăugate în setul final pentru a acoperi cel puțin 40% din total, asigurând relevanță pentru problema detectării anomaliilor.

**Locația codului:** `src/data_acquisition/generate_logs.py`  
**Locația datelor:** `data/generated/`  

**Dovezi:** - Grafic comparativ: `docs/generated_vs_real.png`  
- Tabel statistici: `docs/data_statistics.csv`  

---

## 3. Diagrama State Machine a Întregului Sistem

**Locație:** `docs/state_machine.png`  

**IDLE → LOAD_LOGS → PREPROCESS_LOGS → RN_INFERENCE → THRESHOLD_CHECK →** **├─ [Normal] → LOG_RESULT → UPDATE_UI → LOAD_LOGS (loop)** **└─ [Anomalie] → TRIGGER_ALERT → LOG_INCIDENT → UPDATE_UI → LOAD_LOGS (loop)** **↓ [Stop/Exit] STOP**

### Justificarea State Machine-ului ales:  
Am ales arhitectura de monitorizare continuă loguri deoarece proiectul nostru necesită procesarea secvențială a evenimentelor industriale pentru a notifica operatorul în timp real.

**Stările principale:**
1. **IDLE**: Sistemul așteaptă date noi.
2. **LOAD_LOGS**: Încarcă batch-uri de loguri din CSV.
3. **PREPROCESS_LOGS**: Curăță textul, scalează severitatea, vectorizează mesajul.
4. **RN_INFERENCE**: Rețeaua Neuronală rulează pe batch și calculează scorurile de anomalie.
5. **THRESHOLD_CHECK**: Compară scorurile cu pragul implicit pentru decizie.
6. **UPDATE_UI / TRIGGER_ALERT**: Afișează rezultate și generează notificări (vizuale și sonore).

---

## 4. Scheletul Complet al celor 3 Module Cerute

| **Modul** | **Tehnologii** | **Cerință minimă funcțională** |
|-----------|----------------|--------------------------------|
| **1. Data Logging** | `src/data_acquisition/` | Generează CSV cu date originale (min. 100 samples), cod fără erori |
| **2. Neural Network** | `src/neural_network/` | Model RN definit, compilat, poate fi salvat/încărcat |
| **3. Web Service / UI** | `src/app/` (Streamlit) | Primește batch CSV, afișează normal/anomalie, alertă pop-up și beep |

---

## Structura Repository-ului la Finalul Etapei 4

```text
proiect-rn-popa-alexia/
├── data/
│   ├── generated/      # Date originale (min 40%)
│   └── processed/      # Dataset final (5000 samples)
├── src/
│   ├── data_acquisition/  # MODUL 1
│   ├── neural_network/    # MODUL 2
│   └── app/               # MODUL 3
├── docs/
│   ├── state_machine.png
│   └── screenshots/
│       └── ui_demo.png
├── models/  # Untrained model
├── README_Etapa4_Arhitectura_SIA.md
└── requirements.txt
