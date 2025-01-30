from prettytable import PrettyTable
from scipy.stats import spearmanr, pearsonr, kendalltau
import json
import re
import argparse
    
def calculate_correlation(pred_score, human_score, result):
    assert len(pred_score) == len(human_score)

    if (len(result) == 0):
        result = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}
    result['pearson'] += pearsonr(pred_score, human_score)[0]
    result['spearman'] += spearmanr(pred_score, human_score)[0]
    result['kendalltau'] += kendalltau(pred_score, human_score)[0]

    return result


def print_correlations(result, n):
    table = PrettyTable(['Pearson', 'Spearman', 'Kendall'])
    if(n==0):
        n=1
    table.add_row(
        [round(result['pearson']/n, 4), round(result['spearman']/n, 4), round(result['kendalltau']/n, 4)])
    print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp', type=str, default='results/overall_mean.json')
    args = parser.parse_args()

    jobj = json.load(open(args.input_fp))
    pred_scores, human_scores = {}, {}

    print("Calculating correlation for G-Eval")
    for item in jobj:
        dialog_id = item["dialog_id"]
        
        if (dialog_id not in pred_scores):
            pred_scores[dialog_id] = []
            human_scores[dialog_id] = []

        predicted_score = item["predicted_score"]
        
        pred_scores[dialog_id].append(predicted_score)
        human_scores[dialog_id].append(item['score'])

    print('len(pred_scores): {}'.format(len(pred_scores)))
    print('len(human_scores): {}'.format(len(human_scores)))

    results = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}
    d_counter = 0
    print(f"Predicted_scores: {pred_scores}\n")
    print(f"\nHuman_scores: {human_scores}")
    for dial_id in pred_scores:
        pred_scores_dial = pred_scores[dial_id]
        human_scores_dial = human_scores[dial_id]
        
        if (len(pred_scores_dial) > 1) or (len(human_scores_dial) > 1):
            results = calculate_correlation(pred_scores_dial, human_scores_dial, results)
            d_counter += 1
        else:
            print("Impossibile calcolare le metriche (dati mancanti)")

    print_correlations(results, d_counter)
