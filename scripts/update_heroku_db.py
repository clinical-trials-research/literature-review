import os

import psycopg
from dotenv import load_dotenv

from litreview import ClinicalTrials

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

with psycopg.connect(DATABASE_URL) as connection:
    trials = ClinicalTrials(
        connection=connection,
        schema_directory="./files/schema_lean.json",
    )
    trials.update_database()
