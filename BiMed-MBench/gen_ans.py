import bimedix_inference
import sys
import os
import json
from tqdm import tqdm
from PIL import Image

model_path = sys.argv[1]
lang = sys.argv[2]
model_id = model_path.split('/')[-1]

print(f"Model: {model_path}")
print(f"Language: {lang}")
out = f"./data/eval_out_files/{model_id}/{lang}_ans.jsonl"
os.makedirs(os.path.dirname(f"./data/eval_out_files/{model_id}/"), exist_ok=True)
print(f"Out: {out}")

vlm = bimedix_inference.Inference(model_path)

metadata = {}
image_folder = "./data/test_sets/images/"

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

if lang == 'ara':
    question_file = "./data/test_sets/bimed-mbench_ara.jsonl"
if lang == 'eng':
    question_file = "./data/test_sets/bimed-mbench_eng.jsonl"

data = load_jsonl(question_file)
outfile = open(out,'w')

for ex in tqdm(data):
    # print(ex)
    question_id = ex['question_id']
    image = image_folder+ex['image']
    text = ex['text']
    prompt = text.replace('<image>','').strip()
    answer_id = f"{question_id}_ans"

    answer = vlm.gen_answer(text,image)
    
    line = {
        'question_id': question_id,
        'prompt': prompt,
        'text': answer,
        'answer_id': answer_id,
        'model_id': model_id,
        'metadata': metadata
    }
    outfile.write(json.dumps(line,ensure_ascii=False)+'\n')
    outfile.flush()

# image = "./data/test_sets/images/21139713_F0003.jpg"
# question = "Describe this?"
# print(vlm.gen_answer(question,image))