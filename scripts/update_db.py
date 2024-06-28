import sqlite3

from litreview.studies import Studies

database_schema = {
    "Study": [
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
    ],
    "SecondaryIdInfos": [
        "SecondaryId",
        "NCTId",
        "SecondaryIdType",
        "SecondaryIdDomain",
    ],
    "Collaborators": ["NCTId", "CollaboratorName", "CollaboratorClass"],
    "Condition": ["NCTId", "Condition"],
    "Keyword": ["NCTId", "Keyword"],
    "Phase": ["NCTId", "Phase"],
    "Interventions": ["NCTId", "InterventionType", "InterventionName"],
    "PrimaryOutcomes": [
        "NCTId",
        "PrimaryOutcomeMeasure",
        "PrimaryOutcomeDescription",
        "PrimaryOutcomeTimeFrame",
    ],
    "SecondaryOutcomes": [
        "NCTId",
        "SecondaryOutcomeMeasure",
        "SecondaryOutcomeDescription",
        "SecondaryOutcomeTimeFrame",
    ],
    "OverallOfficials": [
        "NCTId",
        "OverallOfficialName",
        "OverallOfficialAffiliation",
        "OverallOfficialRole",
    ],
    "Locations": [
        "NCTId",
        "LocationFacility",
        "LocationCity",
        "LocationState",
        "LocationZip",
        "LocationCountry",
    ],
    "ConditionMeshes": ["NCTId", "ConditionMeshId", "ConditionMeshTerm"],
    "InterventionMeshes": ["NCTId", "InterventionMeshId", "InterventionMeshTerm"],
    "ConditionAncestors": [
        "NCTId",
        "ConditionAncestorId",
        "ConditionAncestorTerm",
    ],
    "InterventionAncestors": [
        "NCTId",
        "InterventionAncestorId",
        "InterventionAncestorTerm",
    ],
    "ConditionBrowseLeaves": [
        "NCTId",
        "ConditionBrowseLeafId",
        "ConditionBrowseLeafName",
        "ConditionBrowseLeafAsFound",
        "ConditionBrowseLeafRelevance",
    ],
    "InterventionBrowseLeaves": [
        "NCTId",
        "InterventionBrowseLeafId",
        "InterventionBrowseLeafName",
        "InterventionBrowseLeafAsFound",
        "InterventionBrowseLeafRelevance",
    ],
    "ConditionBrowseBranches": [
        "NCTId",
        "ConditionBrowseBranchAbbrev",
        "ConditionBrowseBranchName",
    ],
    "InterventionBrowseBranches": [
        "NCTId",
        "InterventionBrowseBranchAbbrev",
        "InterventionBrowseBranchName",
    ],
}


def insert_study(cursor, study):
    pass
    # nctid = study.get("NCTId")
    # study_table = [study.get(i) for i in study_fields]
    # query = f'INSERT INTO Study ({", ".join(study_fields)}) VALUES ({("?, " * len(study_fields)).rstrip(", ")})'
    # cursor.execute(query, study_table)

    # def insert_field(data, table_name, fields):
    #     for entry in data:
    #         values = [nctid] + [entry.get(i) for i in fields]
    #         cursor.execute(
    #             f'INSERT INTO {table_name} ({"NCTId, " + ", ".join(fields)}) VALUES ({("?, " * (len(fields) + 1)).rstrip(", ")})',
    #             values,
    #         )

    # insert_field(
    #     study.get("protocolSection.identificationModule.secondaryIdInfos"),
    #     "SecondaryIdInfos",
    #     secondary_id_infos_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.sponsorCollaboratorsModule.collaborators"),
    #     "Collaborators",
    #     collaborators_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.armsInterventionsModule.interventions"),
    #     "Interventions",
    #     interventions_fields,
    # )
    # insert_field(
    #     study.get("Condition"),
    #     "Condition",
    #     condition_fields,
    # )
    # insert_field(
    #     study.get("Keyword"),
    #     "Keyword",
    #     keyword_fields,
    # )
    # insert_field(
    #     study.get("Phase"),
    #     "Phase",
    #     phase_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.outcomesModule.primaryOutcomes"),
    #     "PrimaryOutcomes",
    #     primary_outcomes_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.outcomesModule.secondaryOutcomes"),
    #     "SecondaryOutcomes",
    #     secondary_outcomes_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.contactsLocationsModule.overallOfficials"),
    #     "OverallOfficials",
    #     overall_officials_fields,
    # )
    # insert_field(
    #     study.get("protocolSection.contactsLocationsModule.locations"),
    #     "Locations",
    #     locations_fields,
    # )


studies = Studies(1)
connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()

for study in studies.get_studies():
    insert_study(cursor, study)

connection.commit()
connection.close()
