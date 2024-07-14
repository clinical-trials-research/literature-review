import json

from litreview import ClinicalTrials

trials = ClinicalTrials(10)

# studies = trials.get_studies()
# schema = {}
# for study in studies:
#     schema = trials.update_schema(study, schema)

# with open("schema.json", "w") as f:
#     json.dump(schema, f)

with open("schema.json") as f:
    schema = json.load(f)

trials.create_database(schema)
