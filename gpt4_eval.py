import openai
import json
import argparse
import tqdm
import time
import requests

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--prompt-fp', type=str, default='prompts/summeval/con_detailed.txt')
    argparser.add_argument('--save-fp', type=str, default='results/gpt4_con_detailed_openai.json')
    argparser.add_argument('--summeval-fp', type=str, default='data/summeval.json')
    argparser.add_argument('--model', type=str, default='Llama 3 8B Instruct')
    args = argparser.parse_args()

    summeval = json.load(open(args.summeval_fp))
    prompt = open(args.prompt_fp).read()
    ct, ignore = 0, 0

    new_json = []
    for instance in tqdm.tqdm(summeval):
        print(f"i'm entered the for loop")
        #time.sleep(5)
        source = instance['source']
        system_output = instance['system_output']
        #cur_prompt = prompt.replace('{{Document}}', source).replace('{{Summary}}', system_output)
        cur_prompt = prompt
        instance['prompt'] = cur_prompt
        while True:
            print(f"i'm entered the while loop")
            #time.sleep(2)
            try:
                print(f"i'm entered the try statement")
                #time.sleep(2)
                """_response = openai.ChatCompletion.create(
                    model=args.model,
                    messages=[{"role": "system", "content": cur_prompt}],
                    temperature=2,
                    max_tokens=5,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    # logprobs=40,
                    n=20
                )"""
                url = "http://localhost:4891/v1/chat/completions"
                body = f'{{"model": "{args.model}",\
                        "messages": [{{"role": "system", "content": "{cur_prompt}"}}],\
                        "temperature": 2,\
                        "stop":"None"\
                        }}'
                
                _response = requests.post(url, body.encode('utf-8'))
                time.sleep(0.5)
                print(f"Response: {_response.text}")
                _response = _response.json()
                all_responses = [_response['choices'][i]['message']['content'] for i in
                                 range(len(_response['choices']))]
                instance['all_responses'] = all_responses
                new_json.append(instance)
                ct += 1
                break
            except Exception as e:
                print(f"i'm entered the except statement")
                time.sleep(2)
                print(f"Exception:{e}")
                print("#####################################")
                if ("limit" in str(e)):
                    time.sleep(2)
                else:
                    ignore += 1
                    print('ignored', ignore)

                    break
            
        break

    print('ignored total', ignore)
    with open(args.save_fp, 'w') as f:
        json.dump(new_json, f, indent=4)
