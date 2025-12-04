Disciplina: Rețele Neuronale
Instituție: POLITEHNICA București – FIIR
Student: Popa Alexia
Data: 04.12.2025

Scopul Etapei 4

Am construit un schelet complet funcțional al aplicației pentru detecția anomaliilor în loguri, unde modelul RN (în cazul nostru Isolation Forest) este definit, compilat, dar se afla intr-o faza incipita.

1. Tabelul Nevoie Reală → Soluție SIA → Modul Software
|   Nevoie reală concretă                                                   |   Cum o rezolvă SIA-ul vostru                                                              |   Modul software responsabil   |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------ |
| Detectarea logurilor anormale în timp real pentru dispozitive industriale | Model Isolation Forest → clasifică logurile ca normale/anormale și calculează scor anomali | Data Logging + RN Module + UI  |
| Alertare rapidă operator la apariția logurilor critice                    | Generare alertă pop-up și sunet beep când se detectează anomalii                           | RN Module + UI                 |
| Monitorizare evoluție anomalii în timp                                    | Grafic timeline cu numărul de anomalii pe oră                                              | UI + RN Module                 |

2. Contribuția Originală la Setul de Date
   
Total observații finale: 5000 (după Etapa 3 + Etapa 4)

**Tipul contribuției:**
[X] Date generate prin simulare fizică  
[ ] Date achiziționate cu senzori proprii  
[ ] Etichetare/adnotare manuală  
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:**
Am generat loguri simulate pentru diverse dispozitive, cu severitate variabilă și mesaje tipice.  
Fiecare log are timestamp, device, severity, message și label (0-normal / 1-anomalie).  
Aceste date originale au fost adăugate în setul final pentru a acoperi cel puțin 40% din total, asigurând relevanță pentru problema detectării anomaliilor.

**Locația codului:** `src/data_acquisition/generate_logs.py`  
**Locația datelor:** `data/generated/`  

**Dovezi:**
- Grafic comparativ: `docs/generated_vs_real.png`
- Tabel statistici: `docs/data_statistics.csv`

3. Diagrama State Machine a Întregului Sistem
   IDLE → LOAD_LOGS → PREPROCESS_LOGS → RN_INFERENCE → THRESHOLD_CHECK → 
  ├─ [Normal] → LOG_RESULT → UPDATE_UI → LOAD_LOGS (loop)
  └─ [Anomalie] → TRIGGER_ALERT → LOG_INCIDENT → UPDATE_UI → LOAD_LOGS (loop)
       ↓ [Stop/Exit]
     STOP
Am ales arhitectura monitorizare continuă loguri pentru că proiectul nostru detectează anomalii în logurile industriale și notifică operatorul.
Stările principale:

IDLE: Sistemul așteaptă date noi
LOAD_LOGS: Încarcă batch-uri de loguri din CSV
PREPROCESS_LOGS: Curăță textul, scalează severitatea, vectorizează mesajul
RN_INFERENCE: Modelul Isolation Forest rulează pe batch și calculează scorurile de anomalie
THRESHOLD_CHECK: Compară scorurile cu pragul implicit pentru decizie
UPDATE_UI / LOG_RESULT / TRIGGER_ALERT: Afișează rezultate în UI și generează notificări

Tranziții critice:

LOAD_LOGS → PREPROCESS_LOGS: când un batch este disponibil
RN_INFERENCE → THRESHOLD_CHECK: după ce modelul returnează scoruri
THRESHOLD_CHECK → ERROR: dacă există date lipsă sau corupte

Bucla de feedback funcționează astfel: rezultatele inferenței actualizează UI-ul și notificările operatorului în timp real.

4. Scheletul Complet al celor 3 Module
|   Modul                           |   Python (exemple tehnologii)   |   Cerință minimă funcțională                                                                                                         |
| --------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Data Logging / Acquisition** | `src/data_acquisition/`         | Generează CSV cu date originale și simulate, minimum 100 samples, cod fără erori                                                     |
| **2. Neural Network Module**      | `src/neural_network/model.py`   | Model Isolation Forest definit, compilat, poate fi salvat/încărcat, weights random                                                   |
| **3. Web Service / UI**           | `src/app/` (Streamlit)          | Primește input (batch CSV) și afișează output (normal/anomalie), alertă pop-up și beep, screenshot în `docs/screenshots/ui_demo.png` |

