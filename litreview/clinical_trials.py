import re
import sqlite3
from typing import Generator

import httpx

API_BASE = "https://clinicaltrials.gov/api/v2"
API_STUDIES = API_BASE + "/studies"
API_STUDY_SIZES = API_BASE + "/stats/size"
API_FIELD_VALUES = API_BASE + "/stats/field/values"


class ClinicalTrials:
    """
    Provides an interface to populate a SQL database with clinical trial.
    """

    def __init__(self, num_studies=1000, connection=None) -> None:
        self.num_studies = num_studies
        if not connection:
            self.connection = sqlite3.connect("clinical_trials.db")
        self.cursor = self.connection.cursor()
        self._studies_generator = self._create_studies_generator()
        self._field_to_piece = self._get_piece_map()

    def update_database(self, _table="Study") -> None:
        """
        We probably need to use recursion to update the database.
        Should I combine this method with normalize method?

        Args:
            _table (str, optional): _description_. Defaults to "Study".

        Raises:
            Exception: _description_
        """
        for study in next(self._studies_generator):
            for key, value in study.items():
                if isinstance(value, str):
                    if re.match(r"\d{4}-\d{2}(-\d{2})?", value):
                        pass
                    else:
                        pass
                elif isinstance(value, bool):
                    pass
                elif isinstance(value, list):
                    pass
                else:
                    raise Exception(f"Woah, weird type: {value}")

    def get_studies(self) -> list[dict]:
        """
        Retrieve a list of normalized studies.

        Returns:
            list[dict]: List of studies as dictionaries.
        """
        return [
            self._normalize_study(study) for study in next(self._studies_generator, [])
        ]

    def _normalize_study(self, study: dict, _parent_key="") -> dict:
        """
        Normalize a clinical trial study so that fields are as un-nested as
        possible. Also, convert field names to piece names.

        Args:
            study (dict): Clinical trial study converted from JSON to dict.

        Returns:
            dict: The processed study.
        """
        flattened = {}
        for key, value in study.items():
            new_key = f"{_parent_key}.{key}" if _parent_key else key

            # If the current key is a valid field, add it with its piece name.
            if new_key in self._field_to_piece:
                piece_name = self._field_to_piece[new_key]
                # Converts list (e.g. of keywords) to a string.
                if isinstance(value, list):
                    value = ", ".join(value)
                flattened[piece_name] = value

            # Recursively flatten study if value is a dictionary.
            elif isinstance(value, dict):
                flattened |= self._normalize_study(value, new_key)

            # If value is a list of dictionaries, recursively flatten each one.
            elif isinstance(value, list) and all(isinstance(i, dict) for i in value):
                flattened[_parent_key] = [
                    self._normalize_study(i, new_key) for i in value
                ]

        return flattened

    def _create_studies_generator(self) -> Generator:
        """
        Create a generator that yields batches of clinical trials. The number
        of trials is specified in the constructor as num_studies.

        Yields:
            Generator: Yields a list of clinical trials.
        """

        params = {"pageSize": str(self.num_studies)}

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

    def _get_piece_map(self):
        """
        Retruns a dictionary which maps the field name to the more concise
        piece name of clinical trials.
        """
        field_to_piece = {}
        response = httpx.get(API_FIELD_VALUES)
        response.raise_for_status()
        for field in response.json():
            field_to_piece[field["field"]] = field["piece"]
        return field_to_piece
