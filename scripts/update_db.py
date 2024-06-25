import sqlite3

from litreview.studies import Studies

study_fields = [
    "NCTId",
    "OrgStudyId",
    "OrgFullName",
    "OrgClass",
    "BriefTitle",
    "OfficialTitle",
    "StatusVerifiedDate",
    "OverallStatus",
    "HasExpandedAccess",
    "StartDate",
    "PrimaryCompletionDate",
    "PrimaryCompletionDateType",
    "CompletionDate",
    "CompletionDateType",
    "StudyFirstSubmitDate",
    "StudyFirstSubmitQCDate",
    "StudyFirstPostDate",
    "StudyFirstPostDateType",
    "LastUpdateSubmitDate",
    "LastUpdatePostDate",
    "LastUpdatePostDateType",
    "ResponsiblePartyType",
    "LeadSponsorName",
    "LeadSponsorClass",
    "BriefSummary",
    "DetailedDescription",
    "StudyType",
    "DesignPrimaryPurpose",
    "DesignMasking",
    "EligibilityCriteria",
    "HealthyVolunteers",
    "Sex",
    "MinimumAge",
    "MaximumAge",
    "VersionHolder",
    "HasResults",
]


def insert_study(cursor, study):
    study_table = [study.get(i) for i in study_fields]

    cursor.execute(
        f'INSERT INTO Study ({", ".join(study_fields)}) VALUES ({("?, " * len(study_fields)).rstrip(", ")})',
        study_table,
    )


studies = Studies(1)
connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()


for study in studies.get_studies():
    insert_study(cursor, study)

connection.commit()
connection.close()
