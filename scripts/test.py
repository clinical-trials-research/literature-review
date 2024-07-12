import json

from litreview import ClinicalTrials

trials = ClinicalTrials(num_studies=1)
study = trials.get_studies()

# with open("sample.json", "w") as f:
#     json.dump(study[0], f)
