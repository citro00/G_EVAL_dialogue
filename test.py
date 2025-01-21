import requests

url = "http://localhost:4891/v1/chat/completions"

obj = '{"model": "Llama 3 8B Instruct",\
        "messages": [{"role":"user","content":"Who is Lionel Messi?"}],\
        "temperature": 0.28\
        }'

_return = requests.post(url,obj)
print(_return.text)