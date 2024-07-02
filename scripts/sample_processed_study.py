import json

from litreview.studies import Studies

studies = Studies(1)
# for study in studies.get_studies():
#     with open("./files/sample.json", "w") as f:
#         json.dump(study, f)

with open("files/sample_study.json") as f:
    study = json.load(f)

with open("files/study.json", "w") as f:
    json.dump(studies._process_study(study), f)
