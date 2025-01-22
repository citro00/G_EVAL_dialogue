import argparse
import openai

def generate_cot(model, cot_prompt):
    openai.api_key = "not needed for a local LLM"
    openai.base_url = "http://localhost:4891/v1/"
    
    prompt = open(cot_prompt).read()

    try:
        _response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            # logprobs=40,
            n=1
        )
        
        eval_steps = _response.choices[0].message.content
        return eval_steps
    except Exception as e:
        raise e
    
if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--prompt-fp', type=str, default='prompts/dialogue/cot/coh_cot.txt')
    argparser.add_argument('--save_fp', type=str, default='results/coh_cot_llama.json')
    argparser.add_argument('--model', type=str, default='Llama 3 8B Instruct')

    args = argparser.parse_args()

    eval_steps = generate_cot(args.model, args.prompt_fp)

    with open(args.save_fp, 'w') as f:
        f.write(eval_steps)