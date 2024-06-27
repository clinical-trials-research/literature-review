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


def insert_query(table_name, fields):
    return f'INSERT INTO {table_name} ({", ".join(fields)}) VALUES ({("?, " * len(fields)).rstrip(", ")})'


def insert_field(cursor, data, table_name, fields, nctid):
    for entry in data:
        values = [nctid] + [entry.get(i) for i in fields]
        cursor.execute(
            f'INSERT INTO {table_name} ({"NCTId, " + ", ".join(fields)}) VALUES ({("?, " * (len(fields) + 1)).rstrip(", ")})',
            values,
        )


def insert_study(cursor, study):
    nctid = study.get("NCTId")
    study_table = [study.get(i) for i in study_fields]
    cursor.execute(insert_query("Study", study_fields), study_table)

    insert_field(
        cursor,
        study.get("protocolSection.identificationModule.secondaryIdInfos"),
        "SecondaryIdInfos",
        secondary_id_infos_fields,
        nctid,
    )


studies = Studies(1)
connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()

for study in studies.get_studies():
    insert_study(cursor, study)

connection.commit()
connection.close()
