import json

with open('raw.json', 'r', encoding='utf-8') as sour:
    a = sour.read()

js = json.loads(a)

with open('formatted_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(js, outfile, indent=4, ensure_ascii=False)
