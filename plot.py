import argparse
import json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp', type=str, default='results/overall_mean.json')
    args = parser.parse_args()

    data = json.load(open(args.input_fp, encoding='utf-8'))

    human_scores = [obj['score'] for obj in data]
    predicted_scores = [obj['predicted_score'] for obj in data]
    dialogue_ids = [obj['dialog_id'] for obj in data]

    fig, ax = plt.subplots()
    
    ax.plot([0,1], [0,1], transform=ax.transAxes, color='red')
    ax.scatter(human_scores, predicted_scores, s=20) 
    ax.set_xlabel('Human Scores')
    ax.set_ylabel('Predicted Scores')
    ax.set_title('Human vs Predicted Scores')

    for i, txt in enumerate(dialogue_ids):
        ax.annotate(txt, (human_scores[i], predicted_scores[i]), fontsize=5)

    plt.show(block=True)