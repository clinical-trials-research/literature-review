from litreview.clinical_trials_api import get_num_studies, studies_generator


def test_studies_generator():
    """
    Test ability to retrieve clinical trial studies.
    """
    studies = studies_generator()
    next(studies)


def test_get_num_studies():
    """
    Test ability to call /stats/size and retrieve number of studies.
    """
    assert get_num_studies() == 497445
