import json

from litreview.studies import Studies

studies = Studies(1)
for study in studies.get_studies():
    with open("./files/sample.json", "w") as f:
        json.dump(study, f)
