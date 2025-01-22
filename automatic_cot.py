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
            max_tokens=4,
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