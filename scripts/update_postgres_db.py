import psycopg

from litreview import ClinicalTrials

with psycopg.connect("dbname=clinical_trials user=wuihee") as connection:
    trials = ClinicalTrials(
        connection=connection, schema_directory="./files/schema_lean.json"
    )
    trials.update_database()
