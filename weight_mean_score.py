import json
import argparse
import os

def weight_mean_score(ds):
    new_ds = []
    for item in ds:
        new_item = {**item}
    
        all_responses = item['all_responses']

        scores = set(all_responses)
        score_probablities = []
        for score in scores:
            probability = all_responses.count(score) / len(all_responses)
            score_probablities.append((score, probability))

        weight_mean = 0
        for score, probability in score_probablities:
            weight_mean += score*probability

        new_item['predicted_score'] = weight_mean
        new_item.pop('all_responses', None)
        new_ds.append(new_item)
    return new_ds
    
def calculate_overall(criteria_scores):
    pass

if __name__=='__main__':
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--result-dir', type=str, default='results/')
    argparser.add_argument('--output-dir', type=str, default='results/output/')
    argparser.add_argument('--overall-fp', type=str, default='results/overall/gpt4_overall_score.json')
    args = argparser.parse_args()

    files = os.listdir(args.result_dir)
    criteria = []
    for file in files:
        ds = json.load(open(args.result_dir+file))

        new_ds = weight_mean_score(ds)
        
        criteria_score = []
        for item in new_ds:
            criteria_score.append(item['predicted_score'])
        
        criteria.append(criteria_score)
                                
        new_file_name, file_extention = os.path.splitext(file)
        new_file_name = new_file_name+"_score"+file_extention
        with open(args.output_dir+new_file_name, 'w') as fp:
            json.dump(new_ds, fp)   
            
    overall = calculate_overall(criteria)
    
    ds = json.load(open(args.result_dir+files[0]))
    for i, item in enumerate(ds):
        item['predicted_score'] = overall[i]
    
    with open(args.overall_fp, 'w') as fp:
        json.dump(ds, fp)