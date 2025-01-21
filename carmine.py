import json
import openai
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr

# Configura l'API OpenAI
openai.api_key = "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"  
# Carica il dataset
with open("dstc9_data.json", "r") as file:
    data = json.load(file)

# Estrarre i contesti e le risposte dal dataset
contexts = []
responses = []

for item in data['contexts']:
    # Consideriamo solo i contesti completi
    if len(item) > 0:
        contexts.append(" ".join(item))  # Uniamo i messaggi del contesto in una stringa
for item in data['responses']:
    if len(item) > 0:
        responses.append(item[0])  # Prendiamo la prima risposta generata per ogni contesto

# Funzione per valutare un dialogo con GPT-4
def evaluate_with_g_eval(context, response):
    prompt = f"""
    Task: Valutazione della qualità di un dialogo.
    Criteri:
    1. Coerenza (1-5): La risposta è coerente con il contesto.
    2. Rilevanza (1-5): La risposta è pertinente al tema.
    3. Fluenza (1-5): La risposta è ben scritta e grammaticalmente corretta.

    Context: {context}
    Generated Response: {response}

    Fornisci una spiegazione dettagliata per ciascun punteggio.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Valuta i dialoghi in base ai criteri forniti."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response['choices'][0]['message']['content']
        return parse_scores(content)  # Estrai i punteggi
    except Exception as e:
        print(f"Errore durante la valutazione: {e}")
        return None

# Funzione per estrarre i punteggi dalla risposta di GPT-4
def parse_scores(content):
    try:
        lines = content.split("\n")
        scores = []
        for line in lines:
            if ":" in line:
                scores.append(float(line.split(":")[1].strip()))
        return scores
    except Exception as e:
        print(f"Errore durante l'estrazione dei punteggi: {e}")
        return None

# Valutazione dei dialoghi
results = []
for context, response in zip(contexts, responses):
    print(f"Valutazione in corso per il contesto: {context[:50]}...")
    scores = evaluate_with_g_eval(context, response)
    if scores and len(scores) == 3:  # Controlla che ci siano 3 punteggi
        results.append({
            "context": context,
            "response": response,
            "coherence": scores[0],
            "relevance": scores[1],
            "fluency": scores[2]
        })

# Salva i risultati in un DataFrame e in un file CSV
if results:
    df = pd.DataFrame(results)
    df.to_csv("g_eval_results.csv", index=False)
    print("Risultati salvati in g_eval_results.csv")
    # Mostra statistiche sui punteggi
    print("Statistiche sui punteggi:")
    print(df.describe())
else:
    print("Nessuna valutazione completata. Controlla i log per errori.")

# Calcola correlazioni (se disponibili punteggi umani)
# Se hai valutazioni umane, sostituisci human_scores con la lista di punteggi
# human_scores = [...]  # Aggiungi qui i punteggi umani per il confronto
# spearman_corr = spearmanr(df["coherence"], human_scores)
# pearson_corr = pearsonr(df["coherence"], human_scores)
# print(f"Spearman: {spearman_corr}, Pearson: {pearson_corr}")

