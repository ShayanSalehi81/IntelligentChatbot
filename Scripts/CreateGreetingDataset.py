import os
import json


folder_path = 'Datasets/GreetingResponseDataset'
data = []

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        intent_name = filename.replace('.txt', '')

        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            sentences = file.read().splitlines()

        data.append({
            'intent': intent_name,
            'answers': sentences
        })

with open('Datasets/greeting_response.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)