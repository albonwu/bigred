import json


with open("dataset.jsonl", "r") as file:
    for line in file:
        data = json.loads(line)
        print("worked!")
