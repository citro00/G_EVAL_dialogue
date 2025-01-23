import json
import os

# Percorsi per file sul Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
input_file = os.path.join(desktop_path, "dstc9_data.json")
output_file = os.path.join(desktop_path, "transformed_data.json")

# Carica i dati
with open(input_file, "r", encoding="utf-8") as file:
    original_data = json.load(file)

# Naviga nella struttura del dataset
try:
    contexts = original_data["contexts"]
    scores = original_data["scores"]
    models = original_data["models"]
    responses = original_data["responses"]
except KeyError as e:
    raise ValueError(f"Chiave mancante nel dataset JSON: {e}")

if not (len(contexts) and len(scores) and len(models) and len(responses)):
    raise ValueError("Una o più liste sono vuote nel dataset JSON.")

# Creazione del nuovo dataset
transformed_data = []
dialog_id = 1

for idx, context in enumerate(contexts):
    try:
        score = scores[idx]
        model = models[idx]
        response = responses[idx]
    except IndexError:
        raise ValueError(
            f"Non ci sono abbastanza valori di 'scores', 'models' o 'responses' per il dialogo {idx + 1}."
        )

    # Crea il dialogo
    dialog = {
        "dialog_id": str(dialog_id),
        "turns": [],
        "score": score,
        "system_id": model,
    }

    # Aggiungi contesto al dialogo
    for i, utterance in enumerate(context):
        speaker = "user" if i % 2 == 0 else "system"
        dialog["turns"].append({"speaker": speaker, "utterance": utterance})

    # Aggiungi la response come ultimo turno
    dialog["turns"].append({"speaker": "system", "utterance": response})

    transformed_data.append(dialog)
    dialog_id += 1

# Salva i nuovi dati in un file JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(transformed_data, file, indent=4, ensure_ascii=False)

print(f"Dataset trasformato salvato in {output_file}")
