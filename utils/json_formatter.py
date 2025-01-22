import json 
import time

ds = json.load(open("data/dstc9_data.json"))
_id = 0
items = []
for i in range(0, len(ds['contexts'])):
        dialogue = ds["contexts"][i]
        score = ds["scores"][i]
        response = ds["responses"][i]
        system_id = ds["models"][i]
        turns = []
        id = _id
        for i in range(0, len(dialogue)):
                if i % 2 == 1:
                        turn = "system"
                else:
                        turn = "user"

                dialogue_line = {"speaker":turn, "utterage":dialogue[i]}
                turns.append(dialogue_line)
        item = {
                "dialogue_id": id,
                "turns": turns,
                "score": score,
                "system_id": system_id
        }
        _id += 1
        items.append(item)         
        
with open("data/formatted_data.json", 'w') as f:
        json.dump(items, f)
