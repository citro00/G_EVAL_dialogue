# Implementazione della Metrica G-EVAL per la Valutazione di Sistemi NLG

## Obiettivi del Progetto
Questo progetto si propone di implementare il framework **G-EVAL** per valutare la qualità degli output generati dai sistemi di **Natural Language Generation (NLG)**, con particolare riferimento al task di generazione di dialoghi. G-EVAL combina tecniche innovative basate su **Chain-of-Thoughts (CoT)** e valutazione probabilistica, proponendo un approccio migliorato rispetto alle metriche tradizionali.

Gli obiettivi principali sono:

1. Comprendere e replicare le componenti chiave di G-EVAL descritte nell'articolo scientifico "G-EVAL: NLG Evaluation using GPT-4 with Better Human Alignment".
2. Progettare e implementare un sistema che:
   - Generi automaticamente i passaggi intermedi di valutazione (CoT).
   - Calcoli punteggi continui normalizzati tramite probabilità dei token.
   - Personalizzi i criteri di valutazione in base al task.
3. Valutare la correlazione tra i punteggi calcolati da G-EVAL e i giudizi umani, confrontandola con metriche di benchmark.

---

## Struttura del Progetto

### Classi e Moduli Principali

#### 1. **Generazione del Chain-of-Thoughts (CoT)**
- **Classe:** `generate_cot.py`
- **Descrizione:** Fornisce una funzione per generare automaticamente i passaggi intermedi necessari alla valutazione degli output NLG.
- **Funzione principale:** `generate_cot(model, cot_prompt)`
  - Input: modello (es. GPT-4), prompt CoT.
  - Output: stringa contenente i passaggi di valutazione generati.

#### 2. Calcolo della Media Pesata e Probabilità

Il calcolo delle probabilità è una componente chiave di questo progetto ed è utilizzato per determinare un punteggio medio ponderato basato sulle risposte generate dai modelli. Questo approccio permette di tenere conto della frequenza relativa di ogni punteggio assegnato, normalizzando i risultati in modo statistico.

- **Classe:** `weight_mean_score.py`
- **Descrizione:** Implementa il calcolo della media pesata dei punteggi generati dai modelli.
- **Funzione principale:** `weight_mean_score(ds)`
  - Input: dataset con punteggi multipli per ogni istanza.
  - Output: dataset arricchito con punteggi medi ponderati.

#### Formula per il Calcolo della Media Pesata

La formula utilizzata per calcolare il punteggio medio ponderato è la seguente:

$$ \text{Punteggio Predetto} = \sum_{i=1}^{n} p(s_i) \cdot s_i $$

Dove:
-  $ s_i $ rappresenta un punteggio specifico assegnato al dialogo.
-  $ ps_i $ rappresenta la probabilità associata al punteggio $ s_i $ , calcolata come:

$$ p(s_i) = \frac{\text{conteggio di } s_i}{\text{numero totale di risposte}} $$

#### 3. **Analisi Statistica delle Correlazioni**
- **Classe:** `calculate_correlation.py`
- **Descrizione:** Confronta i punteggi di G-EVAL con quelli umani utilizzando metriche statistiche.
- **Funzioni principali:**
  - `calculate_correlation(pred_score, human_score, result)`
    - Calcola le correlazioni di Pearson, Spearman e Kendall-Tau.
  - `print_correlations(result)`
    - Stampa i risultati in formato tabellare.

  Formule utilizzate:
  - **Pearson:**

    $$r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}}$$
    
  - **Spearman:**

    $$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
 
    Dove $d_i$ è la differenza tra i ranghi di ogni coppia.

  - **Kendall-Tau:**
    
    $$\tau = \frac{C - D}{\sqrt{(C + D + T_x)(C + D + T_y)}}$$
    
    Dove $C$ è il numero di coppie concordanti, $D$ è il numero di coppie discordanti, e $T_x$, $T_y$ sono i legami.

---

### Dataset Utilizzati

#### 1. **Input Dati Originali**
- `dstc9_data.json`: Contiene conversazioni grezze con campi _context_, _response_, _models_, e _scores_.

#### 2. **Dati Trasformati**
- `transformed_data_dial.json`: Dialoghi strutturati per analisi, arricchiti con identificatori di dialogo (_dialog_id_) e turni.
- `transformed_data_response.json`: Dataset di risposte elaborate dai modelli.

---

### Esempio di `transformed_data_response.json`

Ecco un esempio della struttura dei dati trasformati per l'analisi dei dialoghi:

```json
[
  {
    "dialog_id": "ID univoco del dialogo",
    "turns": [
      {
        "speaker": "user",
        "utterance": "Messaggio inviato dall'utente"
      },
      {
        "speaker": "system",
        "utterance": "Messaggio inviato dal sistema"
      }
    ],
    "score": "Valore numerico (float) che rappresenta lo score o la qualità del dialogo",
    "system_id": "Identificativo del sistema (ad es. chatbot1.json)",
    "system_output": "Output finale fornito dal sistema"
  }
]

```

## Componenti del Framework G-EVAL

### 1. Prompt Design
- Ogni prompt è progettato per includere:
  1. Introduzione al task (es. valutazione di coerenza o fluidità).
  2. Criteri dettagliati, come:
     - **Coerenza (1-5):** Struttura e organizzazione logica del testo.
     - **Coinvolgimento (1-3):** Interesse e rilevanza della risposta.

Esempio di prompt:
```plaintext
Valuta la coerenza del seguente dialogo su una scala da 1 a 5.
1: Non coerente | 5: Molto coerente
Input:
{{Dialog}}
```

### 2. Chain-of-Thoughts (CoT)
- Il CoT fornisce passaggi intermedi per rendere il processo di valutazione trasparente e ripetibile.
- Esempio di CoT generato:
  1. Leggi attentamente il contesto del dialogo.
  2. Valuta la coerenza tra le risposte del sistema e il contesto.
  3. Assegna un punteggio seguendo i criteri definiti.

### 3. Funzione di Scoring
- Integra una normalizzazione basata sulle probabilità dei token generati dal modello.
- Questo approccio migliora la precisione della valutazione, riducendo il bias verso risposte estreme.

---

## Benchmark e Valutazione

### Benchmark Utilizzati
1. **SummEval:** Valutazione di riassunti basata su coerenza, fluency e rilevanza.
2. **Topical-Chat:** Analisi di dialoghi focalizzata su naturalezza, coerenza e coinvolgimento.
3. **QAGS:** Misurazione della consistenza nei riassunti per evitare allucinazioni.

### Metriche Statistiche
- **Spearman** ($\rho$): Analizza la correlazione tra ranking di punteggi.
- **Kendall-Tau** ($\tau$): Misura la concordanza tra coppie.
- **Pearson** ($r$): Valuta la linearità tra punteggi.

Esempio di output:
| Pearson | Spearman | Kendall |
|---------|----------|---------|
| 0.85    | 0.82     | 0.78    |

---

## Esecuzione del Progetto

### Setup Ambiente
Per iniziare, assicurarsi di avere Python 3.7+ e installare le dipendenze:
```bash
pip install openai tqdm prettytable scipy
```

### Esempi di Esecuzione

1. **Generazione del Chain-of-Thoughts:**
   ```bash
   python3 generate_cot.py --model "GPT-4" --prompt-fp "prompts/coh_cot.txt"
   ```

2. **Calcolo della Media Pesata:**
   ```bash
   python3 weight_mean_score.py --result "results/llama_overall_detailed_dial.json"
   ```

3. **Analisi delle Correlazioni:**
   ```bash
   python3 calculate_correlation.py --input_fp "results/overall_mean.json"
   ```

4. **Trasformazione Dataset:**
   ```bash
   python3 transform_dataset.py --input_fp "data/dstc9_data.json"
   ```

---

## Risorse
- **Articolo di riferimento:** [G-EVAL: NLG Evaluation using GPT-4](https://arxiv.org/abs/2301.13848)
- **Repository GitHub di supporto:** [geval](https://github.com/nlpyang/geval)

