import os

from dotenv import load_dotenv
from pymongo import MongoClient

from litreview.clinical_trials_api import studies_generator

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
db = MongoClient(CONNECTION_STRING)

studies = studies_generator(5)
for study in next(studies):
    print(study)
