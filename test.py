import json

ds = json.load(open("data/dstc9_data.json"))

num_context = len(set(ds['contexts']))
num_response = len(set(ds['responses']))
num_scores = len(set(ds['scores']))

print(f"Context: {num_context}; Respnses: {num_response}; Scores: {num_scores}")