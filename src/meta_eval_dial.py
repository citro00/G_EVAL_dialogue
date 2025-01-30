from prettytable import PrettyTable
from scipy.stats import spearmanr, pearsonr, kendalltau
import json
import re
import argparse


def calculate_correlation(pred_score, human_score, result):
    assert len(pred_score) == len(human_score)
    
    only_pred_score = [val for val in pred_score.values()]
    only_human_score = [val for val in human_score.values()]

    result['pearson'] += pearsonr(only_pred_score, only_human_score)[0]
    result['spearman'] += spearmanr(only_pred_score, only_human_score)[0]
    result['kendalltau'] += kendalltau(only_pred_score, only_human_score)[0]

    return result


def print_correlations(result):
    table = PrettyTable(['Pearson', 'Spearman', 'Kendall'])

    table.add_row(
        [round(result['pearson'], 4), round(result['spearman'], 4), round(result['kendalltau'], 4)])
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
        
        pred_scores[dialog_id] = 0
        human_scores[dialog_id] = 0

        predicted_score = item["predicted_score"]

        pred_scores[dialog_id] = predicted_score
        human_scores[dialog_id] = item['score']

    print('len(pred_scores): {}'.format(len(pred_scores)))
    print('len(human_scores): {}'.format(len(human_scores)))

    results = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}

    if (len(pred_scores) > 1) or (len(human_scores) > 1):
        results = calculate_correlation(pred_scores, human_scores, results)
    else:
        print("Impossibile calcolare le metriche (dati mancanti)")

    print_correlations(results)
