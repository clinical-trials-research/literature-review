import os

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

API_BASE = "https://clinicaltrials.gov/api/v2"
API_STUDIES = API_BASE + "/studies"
API_STUDY_SIZES = API_BASE + "/stats/size"
API_FIELD_VALUES = API_BASE + "/stats/field/values"
CONNECTION_STRING = os.getenv("CONNECTION_STRING")


def studies_generator(num_studies=1000):
    """
    Creates a generator to retrieve studies with every call.

    Args:
        num_studies (int, optional): The number of studies to retrieve with
                                     each call. Defaults to 1000.

    Yields:
        list[dict]: A list of studies, where each study is represented by a
                    dictionary mapping the study's field to its value.
    """
    params = {"pageSize": str(num_studies)}

    with httpx.Client() as client:
        response = client.get(API_STUDIES, params=params)
        response.raise_for_status()
        data = response.json()
        next_page_token = data.get("nextPageToken")

        while next_page_token:
            yield data.get("studies", [])
            params["pageToken"] = next_page_token
            response = client.get(API_STUDIES, params=params)
            response.raise_for_status()
            data = response.json()
            next_page_token = data.get("nextPageToken")


def process_study(data, field_to_piece, _parent_key=""):
    """
    Process each clinical trial study by flattening its structure and making it
    such that each field is represented by its more concise piece name.

    Args:
        data (dict): Dictionary to flatten.
        field_to_piece (dict): Dictionary that maps a field's name to its
                               shortened piece name.
        _parent_key (str): Used internally to keep track of the current key name.

    Returns:
        dict: Newly processed study.
    """
    flattened = {}
    for key, value in data.items():
        new_key = f"{_parent_key}.{key}" if _parent_key else key
        if new_key in field_to_piece:
            piece_name = field_to_piece[new_key]
            flattened[piece_name] = value
        elif isinstance(value, dict):
            flattened |= process_study(value, field_to_piece, new_key)
        elif isinstance(value, list) and all(isinstance(i, dict) for i in value):
            flattened[new_key] = [
                process_study(i, field_to_piece, new_key) for i in value
            ]
    return flattened


field_to_piece = {}
response = httpx.get(API_FIELD_VALUES)
response.raise_for_status()
for field in response.json():
    field_to_piece[field["field"]] = field["piece"]

mongo_client = MongoClient(CONNECTION_STRING)
database = mongo_client["clinical_trials"]
database_collection = database["trials"]

studies = studies_generator(1)
for study in next(studies):
    processed_study = process_study(study, field_to_piece)
    database_collection.insert_one(processed_study)

mongo_client.close()
