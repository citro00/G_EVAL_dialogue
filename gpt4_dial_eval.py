import openai
import json
import argparse
import tqdm
import time
from automatic_cot import *

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--prompt-fp', type=str, default='prompts/dialogue/eval/coh_prompt.txt')
    argparser.add_argument('--save_fp', type=str, default='results/gpt4_con_detailed_openai.json')
    argparser.add_argument('--summeval-fp', type=str, default='data/transformed_data.json')
    argparser.add_argument('--model', type=str, default='Llama 3 8B Instruct')
    argparser.add_argument('--cot-prompt', type=str, default='prompts/dialogue/cot_prompt.txt')
    argparser.add_argument('--instances', type=int, default=None)

    args = argparser.parse_args()
    
    openai.api_key = "not needed for a local LLM"
    openai.base_url = "http://localhost:4891/v1/"

    topical_chat = list(json.load(open(args.summeval_fp)))
    if args.instances:
        topical_chat = topical_chat[:args.instances]

    topical_chat[0:]
    prompt = open(args.prompt_fp).read()
    model = args.model
    ct, ignore = 0, 0

    new_json = []
    
    eval_steps = generate_cot(model, args.cot_prompt)
    prompt = prompt.replace('{{Steps}}', eval_steps)
    
    for instance in tqdm.tqdm(topical_chat):
        turns = instance['turns']
        dialogue = [f"{item['speaker']}: {item['utterance']}" for item in turns]
        dialogue = "\n".join(dialogue)
        cur_prompt = prompt.replace('{{Dialogue}}', dialogue)
        instance['prompt'] = cur_prompt
        while True:
            try:
                _response = openai.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": cur_prompt}],
                    temperature=1,
                    max_tokens=4,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    # logprobs=40,
                    n=1,
                )

                time.sleep(0.5)

                all_responses = [_response.choices[i].message.content for i in
                                 range(len(_response.choices))]
                instance['all_responses'] = all_responses
                new_json.append(instance)
                ct += 1
                break
            except Exception as e:
                print(e)
                if ("limit" in str(e)):
                    time.sleep(2)
                else:
                    ignore += 1
                    print('ignored', ignore)

                    break

    print('ignored total', ignore)
    with open(args.save_fp, 'w') as f:
        json.dump(new_json, f, indent=4)
