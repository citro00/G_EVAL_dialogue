import argparse
import json
import matplotlib.pyplot as plt


def add_identity(axes, *line_args, **line_kwargs):
    identity, = axes.plot([], [], *line_args, **line_kwargs)
    def callback(axes):
        low_x, high_x = axes.get_xlim()
        low_y, high_y = axes.get_ylim()
        low = max(low_x, low_y)
        high = min(high_x, high_y)
        identity.set_data([low, high], [low, high])
    callback(axes)
    axes.callbacks.connect('xlim_changed', callback)
    axes.callbacks.connect('ylim_changed', callback)
    return axes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp', type=str, default='results/overall_mean.json')
    args = parser.parse_args()

    data = json.load(open(args.input_fp, encoding='utf-8'))

    human_scores = [obj['score'] for obj in data]
    predicted_scores = [obj['predicted_score'] for obj in data]
    dialogue_ids = [obj['dialog_id'] for obj in data]

    fig, ax = plt.subplots()
    
    add_identity(ax, color='r', ls='--')
    ax.scatter(human_scores, predicted_scores, s=20) 
    ax.set_xlim([0, 6])
    ax.set_ylim([0, 6])

    ax.set_xlabel('Human Scores')
    ax.set_ylabel('Predicted Scores')
    ax.set_title('Human vs Predicted Scores')

    for i, txt in enumerate(dialogue_ids):
        ax.annotate(txt, (human_scores[i], predicted_scores[i]), fontsize=5)

    plt.show(block=True)