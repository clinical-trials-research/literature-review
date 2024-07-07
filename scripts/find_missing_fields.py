import json

with open("./files/test.json") as f:
    structure = json.load(f)

structure = {
    key: value for key, value in structure.items() if not isinstance(value, list)
}

with open("./files/test2.json", "w") as f:
    json.dump(structure, f)
