import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Generator

import httpx
from tqdm import tqdm

API_BASE = "https://clinicaltrials.gov/api/v2"
API_STUDIES = API_BASE + "/studies"
API_STUDY_SIZES = API_BASE + "/stats/size"
API_FIELD_VALUES = API_BASE + "/stats/field/values"


class ClinicalTrials:
    """
    Provides an interface to manage a clinical trial database.
    """

    def __init__(
        self,
        *,
        num_studies=1000,
        connection=None,
        schema_directory="schema.json",
    ) -> None:
        """
        Initialize the ClinicalTrials interface.

        Args:
            num_studies (int, optional): The number of studies to generate
                                         with each call. Defaults to 1000.
            connection (_type_, optional): SQL database connection. Defaults
                                           to None.
            schema_directory (str, optional): Directory to load database schema
                                              from. Defaults to "./files/schema.json".
        """
        self.num_studies = num_studies
        self.schema_directory = schema_directory
        self.connection = (
            connection if connection else sqlite3.connect("clinical_trials.db")
        )
        self.cursor = self.connection.cursor()
        self._studies_generator = self._create_studies_generator()
        self._field_to_piece = self._get_piece_map()
        self._in_schema = {piece: False for piece in self._field_to_piece.values()}
        self._schema = self._load_schema()
        self._field_to_table = self._create_field_to_table()

    def query(self, *fields) -> list:
        """
        Query database for given fields.

        Returns:
            list: Returns list of results
        """
        tables = list(set(self._field_to_table[i] for i in fields))
        results = self.cursor.execute(
            f'SELECT {", ".join(fields)} FROM {", ".join(tables)}'
        ).fetchall()
        return results

    def get_studies(self) -> list[dict]:
        """
        Retrieve a list of normalized studies.

        Returns:
            list[dict]: List of studies as dictionaries.
        """
        return [
            self._normalize_study(study) for study in next(self._studies_generator, [])
        ]

    def update_database(self) -> None:
        """
        Creates and updates the database with num_studies for each call.
        """
        self._create_database(self._schema)

        # tqdm for progress bar!
        for study in tqdm(self.get_studies()):
            self._update_database(study, self._schema)

    def _update_database(
        self,
        study: dict,
        schema: dict,
        _table="Study",
        _prev_table=None,
        _prev_primary=None,
    ) -> None:
        """
        Recursively update a single study into the database.

        Args:
            study (dict): Single processed clinical trials study.
            schema (dict): Database schema.
            _table (str, optional): Table name. Defaults to "Study".
            _prev_table (str, optional): Previous table name. Defaults to None.
            _prev_primary (str, optional): Previous primary key. Defaults to None.
        """
        columns = []
        values = []

        if not _prev_table:
            primary = f'"{study["NCTId"]}"'
        else:
            # Fetch the last Id inserted.
            result = self.cursor.execute(
                f"SELECT Id FROM {_table} ORDER BY Id DESC LIMIT 1"
            ).fetchone()
            primary = 1 if not result else result[0] + 1

        for field, value in study.items():
            if field not in schema:
                logging.info(f"Skipping field: {field}")
                continue

            if isinstance(value, list):
                for entry in value:
                    self._update_database(
                        entry,
                        schema[field],
                        _table=field,
                        _prev_table=_table,
                        _prev_primary=primary,
                    )
            else:
                if schema[field] == "TEXT":
                    value = value.replace("'", "''")
                    value = f"'{value}'"
                columns.append(str(field))
                values.append(str(value))

        if _prev_table:
            columns.append(_prev_table + "Id")
            values.append(str(_prev_primary))

        query = (
            f"INSERT INTO {_table} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        )

        # Don't insert if columns / values are empty.
        if columns and values:
            self.cursor.execute(query)
            self.connection.commit()

    def _create_database(
        self,
        schema: dict,
        *,
        _table="Study",
        _prev_table=None,
        _primary="NCTId",
        _prev_primary=None,
        _primary_datatype="TEXT",
    ) -> None:
        """
        Recursively create database based on schema provided.

        Args:
            schema (dict): Database schema, where schema[field] = type.
            _table_name (str, optional): Table name to insert columns / values.
                                         Defaults to "Study".
            _prev_table (str, optional): Previous table name. Defaults to None.
            _primary (str, optional): Primary key. Defaults to "NCTId".
            _prev_primary (str, optional): Previous primary key. Defaults to None.
            _primary_datatype (str, optional): Primary key datatype. Defaults
                                               to "TEXT".
        """
        columns = []

        if not _primary:
            _primary = "Id"
            columns.append(f"{_primary} INTEGER PRIMARY KEY")

        for field, datatype in schema.items():
            if isinstance(datatype, dict):
                self._create_database(
                    datatype,
                    _table=field,
                    _prev_table=_table,
                    _primary=None,
                    _prev_primary=_primary,
                    _primary_datatype="INTEGER",
                )
            elif field == _primary:
                columns.append(f"{field} {datatype} PRIMARY KEY")
            else:
                columns.append(f"{field} {datatype}")

        if _prev_table and _prev_primary:
            foreign_key = f"{_prev_table}Id"
            columns.append(f"{foreign_key} {_primary_datatype}")
            columns.append(
                f"FOREIGN KEY ({foreign_key}) REFERENCES {_prev_table} ({_prev_primary})"
            )

        query = f"CREATE TABLE IF NOT EXISTS {_table} ({', '.join(columns)});"
        self.cursor.execute(query)
        self.connection.commit()

    def _create_field_to_table(self, _table="Study", _schema=None) -> dict:
        """
        Recursively create mapping of fields to their table names.

        Args:
            _table: Current table name.
            _schema: The current layer of schema.

        Returns:
            dict: Dictionary mapping fields to their table names.
        """
        field_to_table = {}
        if not _schema:
            _schema = self._schema
        for key, value in _schema.items():
            if isinstance(value, dict):
                field_to_table |= self._create_field_to_table(key, value)
            else:
                field_to_table[key] = _table
        return field_to_table

    def _load_schema(self, num_fields=81) -> dict:
        """
        Look for schema in given/default directory. If not found, generate and
        load it.

        Returns:
            dict: The loaded schema.
        """
        schema_path = Path(self.schema_directory)

        # If schema.json doesn't exist, create it.
        if not schema_path.is_file():
            # Keep updating until all the fields have been added to the schema.
            schema = {}
            fields_remaining = len(self._in_schema) - sum(self._in_schema.values())
            while fields_remaining > num_fields:
                fields_remaining = len(self._in_schema) - sum(self._in_schema.values())
                print(
                    f"Fields remaining to be updated to the schema: {fields_remaining}"
                )
                for study in self.get_studies():
                    schema = self._update_schema(study, schema)
                with open(self.schema_directory, "w") as f:
                    json.dump(schema, f)
        else:
            with open(self.schema_directory) as f:
                schema = json.load(f)
        return schema

    def _update_schema(self, study: dict, schema=None) -> dict:
        """
        Given a study, update the database schema.

        Args:
            study (dict): Clinical trials study.
        """
        if not schema:
            schema = {}

        for key, value in study.items():
            if key in schema and not isinstance(value, list):
                continue
            if isinstance(value, str):
                if re.match(r"^\d{4}-\d{2}(-\d{2})?$", value):
                    schema[key] = "DATE"
                else:
                    schema[key] = "TEXT"
            elif isinstance(value, bool):
                schema[key] = "BOOLEAN"
            elif isinstance(value, int):
                schema[key] = "INTEGER"
            elif isinstance(value, list):
                # Reduce list of dictionaries to 1 dictionary.
                for entry in value:
                    schema[key] = self._update_schema(entry, schema.get(key))
            else:
                raise Exception(f"Woah, weird type: {value}")
            self._in_schema[key] = True
        return schema

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
                flattened[new_key.replace(".", "")] = [
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

    def _get_piece_map(self) -> dict:
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
