import openai
import json
import argparse
import tqdm
import time
from utils.automatic_cot import *
from utils.handler_outlier import *

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--prompt-fp', type=str, default='prompts/dialogue/overall_prompt_dialogue.txt')
    argparser.add_argument('--save-fp', type=str, default='results/llama_overall_detailed_dial.json')
    argparser.add_argument('--dataset-fp', type=str, default='data/transformed_data_dial.json')
    argparser.add_argument('--model', type=str, default='Llama 3 8B Instruct')
    argparser.add_argument('--cot-prompt', type=str, default='prompts/dialogue/overall_cot_dialogue.txt')
    argparser.add_argument('--instances', type=int, default=None)

    args = argparser.parse_args()
    
    openai.api_key = "not needed for a local LLM"
    openai.base_url = "http://localhost:4891/v1/"

    topical_chat = list(json.load(open(args.dataset_fp)))
    if args.instances:
        topical_chat = topical_chat[:args.instances]

    topical_chat[0:]
    prompt = open(args.prompt_fp).read()
    model = args.model
    ct, ignore = 0, 0

    new_json = []
    
    eval_steps = generate_cot(model, args.cot_prompt)
        
    prompt = prompt.replace('{{Steps}}', eval_steps)
    ct_tmp = 0
    for instance in tqdm.tqdm(topical_chat):
        ct_tmp += 1
        turns = instance['turns']
        
        # Commentare la lina seguente se l'esecuzione è sull'intero dialogo. Nel caso della valutazione di risposta lasciare attiva
        #system_output = instance['system_output']
        
        dialogue = [f"{item['speaker']}: {item['utterance']}  \n" for item in turns]
        dialogue = "".join(dialogue)
        cur_prompt = prompt.replace('{{Dialogue}}', dialogue)
        
        # Commentare la lina seguente se l'esecuzione è sull'intero dialogo. Nel caso della valutazione di risposta lasciare attiva
        #cur_prompt = cur_prompt.replace('{{System output}}', system_output)
        
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
                    stream=False,
                    #logprobs=True,
                    n=20,
                )

                #time.sleep(0.5)

                all_responses = [_response.choices[i].message.content for i in
                                 range( len(_response.choices))]
                
                all_responses = handler_outlier(all_responses)
                tqdm.tqdm.write(f"Response: {all_responses}")
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
    with open(args.save_fp, 'w') as f:
        json.dump(new_json, f, indent=4)
