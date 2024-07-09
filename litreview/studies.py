import json

import httpx

API_BASE = "https://clinicaltrials.gov/api/v2"
API_STUDIES = API_BASE + "/studies"
API_STUDY_SIZES = API_BASE + "/stats/size"
API_FIELD_VALUES = API_BASE + "/stats/field/values"
JSON_TO_TABLE = {
    "protocolSection.identificationModule.secondaryIdInfos": "SecondaryIdInfos",
    "protocolSection.sponsorCollaboratorsModule.collaborators": "Collaborators",
    "Condition": "Condition",
    "Keyword": "Keyword",
    "Phase": "Phase",
    "protocolSection.armsInterventionsModule.armGroups": "ArmGroups",
    "protocolSection.armsInterventionsModule.interventions": "Interventions",
    "protocolSection.outcomesModule.primaryOutcomes": "PrimaryOutcomes",
    "protocolSection.outcomesModule.secondaryOutcomes": "SecondaryOutcomes",
    "protocolSection.contactsLocationsModule.overallOfficials": "OverallOfficials",
    "protocolSection.contactsLocationsModule.locations": "Locations",
    "protocolSection.referencesModule.references": "StudyReferences",
    "derivedSection.conditionBrowseModule.meshes": "ConditionMeshes",
    "derivedSection.interventionBrowseModule.meshes": "InterventionMeshes",
    "derivedSection.conditionBrowseModule.ancestors": "ConditionAncestors",
    "derivedSection.interventionBrowseModule.ancestors": "InterventionAncestors",
    "derivedSection.conditionBrowseModule.browseLeaves": "ConditionBrowseLeaves",
    "derivedSection.interventionBrowseModule.browseLeaves": "InterventionBrowseLeaves",
    "derivedSection.conditionBrowseModule.browseBranches": "ConditionBrowseBranches",
    "derivedSection.interventionBrowseModule.browseBranches": "InterventionBrowseBranches",
    "protocolSection.outcomesModule.otherOutcomes": "OtherOutcomes",
    "resultsSection.participantFlowModule.groups": "FlowGroups",
    "resultsSection.baselineCharacteristicsModule.groups": "BaselineGroups",
    "protocolSection.referencesModule.seeAlsoLinks": "SeeAlsoLinks",
    "documentSection.largeDocumentModule.largeDocs": "LargeDocs",
    "annotationSection.annotationModule.unpostedAnnotation.unpostedEvents": "UnpostedEvents",
    "derivedSection.miscInfoModule.submissionTracking.submissionInfos": "SubmissionInfos",
    "protocolSection.referencesModule.availIpds": "AvailIPDs",
    "resultsSection.participantFlowModule.periods": "FlowPeriods",
    "resultsSection.participantFlowModule.periods.milestones": "FlowMilestones",
    "resultsSection.participantFlowModule.periods.milestones.achievements": "FlowAchievements",
}


class Studies:
    """
    Provides an interface to access the ClinicalTrials API.
    """

    def __init__(self, num_studies=1000):
        self.num_studies = num_studies
        self._field_to_piece = self._get_field_to_piece()
        self._studies = self._get_studies_generator()
        self._structure = {}

    def get_studies(self):
        """
        Retrieve a list of normalized studies.
        """
        res = []
        for study in next(self._studies, []):
            processed_study = self._process_study(study)
            self._structure |= processed_study
            res.append(processed_study)
        # res = [self._process_study(study) for study in next(self._studies, [])]
        with open("./files/structure.json", "w") as f:
            json.dump(self._structure, f)
        return res

    def get_total_studies(self):
        """
        Return the total number of studies at clinicaltrials.gov.
        """
        response = httpx.get(API_STUDY_SIZES)
        response.raise_for_status()
        data = response.json()
        return data.get("totalStudies")

    def _get_studies_generator(self):
        """
        Creates a generator to retrieve studies with every call.

        Args:
            num_studies (int, optional): The number of studies to retrieve with
                                        each call. Defaults to 1000.

        Yields:
            list[dict]: A list of studies, where each study is represented by a
                        dictionary mapping the study's field to its value.
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

    def _get_field_to_piece(self):
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

    def _process_study(self, data, _parent_key=""):
        """
        Process each clinical trial study by flattening its structure and making it
        such that each field is represented by its more concise piece name.

        Args:
            data (dict): Dictionary to flatten.
            _parent_key (str): Used internally to keep track of the current key name.

        Returns:
            dict: Newly processed study.
        """
        flattened = {}
        for key, value in data.items():
            new_key = f"{_parent_key}.{key}" if _parent_key else key
            if new_key in self._field_to_piece:
                piece_name = self._field_to_piece[new_key]
                if isinstance(value, list):
                    value = ", ".join(value)
                flattened[piece_name] = value
            elif isinstance(value, dict):
                flattened |= self._process_study(value, new_key)
            elif isinstance(value, list) and all(isinstance(i, dict) for i in value):
                table_key = JSON_TO_TABLE.get(new_key, new_key)
                flattened[table_key] = [self._process_study(i, new_key) for i in value]
        return flattened
