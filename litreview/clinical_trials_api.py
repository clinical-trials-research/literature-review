import httpx

API_BASE = "https://clinicaltrials.gov/api/v2"
API_STUDIES = API_BASE + "/studies"
API_STUDY_SIZES = API_BASE + "/stats/size"
API_FIELD_VALUES = API_BASE + "/stats/field/values"


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
