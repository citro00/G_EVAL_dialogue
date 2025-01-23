import json
import argparse
import os

def weight_mean_score(ds):
    new_ds = []

    for item in ds:
        # Per ogni dialogo nel ds
        # Crea una copia dell'oggetto dialogo
        new_item = {**item}
    
        # Prende tutte le n valutazioni del modello per il dialogo corrente
        all_responses = item['all_responses']

        # Crea l'insieme algebrico degli scores
        scores = set(all_responses)
        score_probablities = []
        
        #Forse da cancellare
        for score in scores:
            # Calcola la probabilità di ogni score di essere predetto e inserisci in un array
            probability = all_responses.count(score) / len(all_responses)
            score_probablities.append((score, probability))

        weight_mean = 0
        for score, probability in score_probablities:
            # Calcolo della media pesata degli n score generati
            weight_mean += score*probability


        new_item['predicted_score'] = weight_mean
        new_item.pop('all_responses', None)
        new_ds.append(new_item)
    return new_ds

if __name__=='__main__':
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--result', type=str)
    argparser.add_argument('--output-fp', type=str)
    args = argparser.parse_args()
    
    ds = json.load(open(args.result))
    new_ds = weight_mean_score(ds)
    
    with open(args.output_fp, 'w') as fp:
        json.dump(new_ds, fp)
