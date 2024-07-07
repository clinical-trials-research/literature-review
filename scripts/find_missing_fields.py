import json

with open("./files/sample_processed.json") as f:
    structure = json.load(f)

study = {key: value for key, value in structure.items() if not isinstance(value, list)}

with open("./files/test.json", "w") as f:
    json.dump(study, f)
