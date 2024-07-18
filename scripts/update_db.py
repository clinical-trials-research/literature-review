from litreview import ClinicalTrials

trials = ClinicalTrials(num_studies=100, schema_directory="files/schema.json")
trials.update_database()
