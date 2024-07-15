from litreview import ClinicalTrials

trials = ClinicalTrials(10)
studies = trials.get_studies()
for study in studies:
    trials._update_database(study)

# schema = {}
# for study in studies:
#     schema = trials.update_schema(study, schema)

# with open("schema.json", "w") as f:
#     json.dump(schema, f)

# with open("schema.json") as f:
#     schema = json.load()

# trials.create_database(schema)
