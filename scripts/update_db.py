from litreview import ClinicalTrials

trials = ClinicalTrials(schema_directory="files/schema.json")
trials.update_database()
