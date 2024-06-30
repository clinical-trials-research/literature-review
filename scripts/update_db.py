import sqlite3

from litreview.studies import Studies

STUDY_TABLE = [
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
    "DesignAllocation",
    "DesignPrimaryPurpose",
    "DesignMasking",
    "EnrollmentCount",
    "EnrollmentType",
    "EligibilityCriteria",
    "HealthyVolunteers",
    "Sex",
    "MinimumAge",
    "MaximumAge",
    "VersionHolder",
    "HasResults",
    "OversightHasDMC",
    "IsFDARegulatedDrug",
    "IsFDARegulatedDevice",
    "IPDSharing",
    "Condition",
    "Keyword",
    "Phase",
    "StdAge",
]
OTHER_TABLES = {
    "SecondaryIdInfos": [
        "SecondaryId",
        "NCTId",
        "SecondaryIdType",
        "SecondaryIdDomain",
    ],
    "ArmGroups": [
        "ID",
        "NCTId",
        "ArmGroupLabel",
        "ArmGroupType",
        "ArmGroupDescription",
        "ArmGroupInterventionName",
    ],
    "Collaborators": [
        "ID",
        "NCTId",
        "CollaboratorName",
        "CollaboratorClass",
    ],
    "Interventions": [
        "ID",
        "NCTId",
        "InterventionType",
        "InterventionName",
        "InterventionDescription",
        "InterventionArmGroupLabel",
        "InterventionOtherName",
    ],
    "PrimaryOutcomes": [
        "ID",
        "NCTId",
        "PrimaryOutcomeMeasure",
        "PrimaryOutcomeDescription",
        "PrimaryOutcomeTimeFrame",
    ],
    "SecondaryOutcomes": [
        "ID",
        "NCTId",
        "SecondaryOutcomeMeasure",
        "SecondaryOutcomeDescription",
        "SecondaryOutcomeTimeFrame",
    ],
    "OverallOfficials": [
        "ID",
        "NCTId",
        "OverallOfficialName",
        "OverallOfficialAffiliation",
        "OverallOfficialRole",
    ],
    "Locations": [
        "ID",
        "NCTId",
        "LocationFacility",
        "LocationCity",
        "LocationState",
        "LocationZip",
        "LocationCountry",
    ],
    "StudyReferences": [
        "ID",
        "NCTId",
        "ReferencePMID",
        "ReferenceType",
        "ReferenceCitation",
    ],
    "ConditionMeshes": [
        "ID",
        "NCTId",
        "ConditionMeshId",
        "ConditionMeshTerm",
    ],
    "InterventionMeshes": [
        "ID",
        "NCTId",
        "InterventionMeshId",
        "InterventionMeshTerm",
    ],
    "ConditionAncestors": [
        "ID",
        "NCTId",
        "ConditionAncestorId",
        "ConditionAncestorTerm",
    ],
    "InterventionAncestors": [
        "ID",
        "NCTId",
        "InterventionAncestorId",
        "InterventionAncestorTerm",
    ],
    "ConditionBrowseLeaves": [
        "ID",
        "NCTId",
        "ConditionBrowseLeafId",
        "ConditionBrowseLeafName",
        "ConditionBrowseLeafAsFound",
        "ConditionBrowseLeafRelevance",
    ],
    "InterventionBrowseLeaves": [
        "ID",
        "NCTId",
        "InterventionBrowseLeafId",
        "InterventionBrowseLeafName",
        "InterventionBrowseLeafAsFound",
        "InterventionBrowseLeafRelevance",
    ],
    "ConditionBrowseBranches": [
        "ID",
        "NCTId",
        "ConditionBrowseBranchAbbrev",
        "ConditionBrowseBranchName",
    ],
    "InterventionBrowseBranches": [
        "ID",
        "NCTId",
        "InterventionBrowseBranchAbbrev",
        "InterventionBrowseBranchName",
    ],
}


def insert_study(cursor, study):
    nctid = study.get("NCTId")
    values = [study.get(field) for field in STUDY_TABLE]
    query = f'INSERT INTO Study ({", ".join(STUDY_TABLE)}) VALUES ({("?, " * len(STUDY_TABLE)).rstrip(", ")})'
    cursor.execute(query, values)

    def insert_field(table_name, fields):
        table_values = study.get(table_name)
        if table_values:
            for entry in table_values:
                values = [nctid] + [entry.get(i) for i in fields]
                cursor.execute(
                    f'INSERT INTO {table_name} ({"NCTId, " + ", ".join(fields)}) VALUES ({("?, " * (len(fields) + 1)).rstrip(", ")})',
                    values,
                )

    for table_name, fields in OTHER_TABLES.items():
        insert_field(table_name, fields)


studies = Studies(5)
connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()

for study in studies.get_studies():
    insert_study(cursor, study)

connection.commit()
connection.close()
