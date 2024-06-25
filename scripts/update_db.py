import sqlite3

from litreview.studies import Studies

study_fields = (
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
)
secondary_id_infos_fields = (
    "SecondaryId",
    "SecondaryIdType",
    "SecondaryIdDomain",
)
collaborators_fields = (
    "CollaboratorName",
    "CollaboratorClass",
)
condition_fields = ("Condition",)
keyword_fields = ("Keyword",)
phase_fields = ("Phase",)
interventions_fields = (
    "InterventionType",
    "InterventionName",
)
primary_outcomes_fields = (
    "PrimaryOutcomeMeasure",
    "PrimaryOutcomeDescription",
    "PrimaryOutcomeTimeFrame",
)
secondary_outcomes_fields = (
    "SecondaryOutcomeMeasure",
    "SecondaryOutcomeDescription",
    "SecondaryOutcomeTimeFrame",
)
overall_officials_fields = (
    "OverallOfficialName",
    "OverallOfficialAffiliation",
    "OveralOfficialRole",
)
locations_fields = (
    "LocationFacility",
    "LocationCity",
    "LocationState",
    "LocationZip",
    "LocationCountry",
)
meshes_fields = (
    "ConditionMeshId",
    "ConditionMeshTerm",
    "InterventionMeshId",
    "InterventionMeshTerm",
)
ancestors_fields = (
    "ConditionAncestorId",
    "ConditionAncestorTerm",
    "InterventionAncestorId",
    "InterventionAncestorTerm",
)
browse_leaves_fields = (
    "ConditionBrowseLeafId",
    "ConditionBrowseLeafName",
    "ConditionBrowseLeafAsFound",
    "ConditionBrowseLeafRelevance",
    "ConditionBrowseleafId",
    "ConditionBrowseLeafName",
    "InterventionBrowseLeafRelevance",
)
browse_branches_fields = (
    "ConditionBrowseBranchAbbrev",
    "ConditionBrowseBranchName",
    "InterventionBrowseBranchAbbrev",
    "InterventionBrowseBranchName",
)


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
