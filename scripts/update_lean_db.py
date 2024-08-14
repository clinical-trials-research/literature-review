import sqlite3

from litreview import ClinicalTrials

connection = sqlite3.connect("./clinical_trials_lean.db")
schema_directory = "./files/schema_lean.json"

trials = ClinicalTrials(connection=connection, schema_directory=schema_directory)
trials.update_database()
