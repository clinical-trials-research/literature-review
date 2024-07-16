from litreview import ClinicalTrials

trials = ClinicalTrials()
# studies = trials.get_studies()

# with open("schema.json", "w") as f:
#     json.dump(trials._schema, f)

# for study in studies:
#     trials._update_database(study, trials._schema)

# schema = {}
# for study in studies:
#     schema = trials.update_schema(study, schema)

# with open("schema.json", "w") as f:
#     json.dump(schema, f)

# with open("schema.json") as f:
#     schema = json.load()

# trials.create_database(schema)
