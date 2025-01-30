from argparse import ArgumentParser
import json

def main():
    argparse = ArgumentParser()
    argparse.add_argument('--input_fp', type=str, default='data/topical_chat.json', required=True)
    argparse.add_argument('--output_fp', type=str, default='data/topical_chat_formatted.json', required=True)
    argparse.add_argument('--dimension', type=str, default='overall')
    args = argparse.parse_args()

    data = None
    with open(args.input_fp, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_obj = []
    for dialog in data:
        speakers = ["A", "B"]
        turns_scr= dialog['source']
        turns_list = turns_scr.split("\n")
        turns_obj = [{"speaker": speakers[i % 2], "utterance": turns_list[i].strip()} for i in range(len(turns_list)) if turns_list[i].strip() != ""]
        dialog_id = "dm-test-" + str(abs(hash(turns_scr)))
        score = dialog['scores'][args.dimension]
        system_id = dialog['system_id']
        system_output = dialog['system_output']

        output_obj.append({
            "dialog_id": dialog_id,
            "turns": turns_obj,
            "scores": score,
            "system_id": system_id,
            "system_output": system_output
        })

    print(f"Number of dialogs: {len(output_obj)}")
    with open(args.output_fp, 'w', encoding='utf-8') as file:
        json.dump(output_obj, file, indent=4)


if __name__ == "__main__":
    main()