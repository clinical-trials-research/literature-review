import json
import re


def get_json():
    with open("./files/test.json") as f:
        structure = json.load(f)

    structure = {
        key: value for key, value in structure.items() if not isinstance(value, list)
    }

    with open("./files/flat_fields.json", "w") as f:
        json.dump(structure, f)


def create_query():
    with open("./files/flat_fields.json") as f:
        structure = json.load(f)

    for key, value in structure.items():
        if isinstance(value, int):
            data_type = "INTEGER"
        elif isinstance(value, bool):
            data_type = "BOOLEAN"
        elif isinstance(value, str):
            if re.match(r"\d{4}-\d{2}(-\d{2})?", value):
                data_type = "DATE"
            else:
                data_type = "TEXT"

        print(f"{key} {data_type},")


if __name__ == "__main__":
    create_query()
