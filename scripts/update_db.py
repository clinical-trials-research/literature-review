import sqlite3

from tqdm import tqdm

from litreview.studies import Studies

UPDATE_DB_QUERY = """
CREATE TABLE IF NOT EXISTS
    Study (
        NCTId TEXT PRIMARY KEY,
        OrgStudyId TEXT,
        OrgFullName TEXT,
        OrgClass TEXT,
        BriefTitle TEXT,
        OfficialTitle TEXT,
        Acronym TEXT,
        StatusVerifiedDate DATE,
        OverallStatus TEXT,
        LastKnownStatus TEXT,
        HasExpandedAccess BOOLEAN,
        StartDate DATE,
        PrimaryCompletionDate DATE,
        PrimaryCompletionDateType TEXT,
        CompletionDate DATE,
        CompletionDateType TEXT,
        StudyFirstSubmitDate DATE,
        StudyFirstSubmitQCDate DATE,
        StudyFirstPostDate DATE,
        StudyFirstPostDateType TEXT,
        LastUpdateSubmitDate DATE,
        LastUpdatePostDate DATE,
        LastUpdatePostDateType TEXT,
        ResponsiblePartyType TEXT,
        LeadSponsorName TEXT,
        LeadSponsorClass TEXT,
        BriefSummary TEXT,
        DetailedDescription TEXT,
        StudyType TEXT,
        DesignAllocation TEXT,
        DesignPrimaryPurpose TEXT,
        DesignMasking TEXT,
        EnrollmentCount INTEGER,
        EnrollmentType INTEGER,
        EligibilityCriteria TEXT,
        HealthyVolunteers BOOLEAN,
        Sex TEXT,
        MinimumAge TEXT,
        MaximumAge TEXT,
        VersionHolder DATE,
        HasResults BOOLEAN,
        OversightHasDMC BOOLEAN,
        IsFDARegulatedDrug BOOLEAN,
        IsFDARegulatedDevice BOOLEAN,
        IPDSharing TEXT,
        Condition TEXT,
        Keyword TEXT,
        Phase TEXT,
        StdAge TEXT,
        DatePulled DATETIME DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS
    SecondaryIdInfos (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SecondaryId TEXT,
        SecondaryIdType TEXT,
        SecondaryIdDomain TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    ArmGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ArmGroupLabel TEXT,
        ArmGroupType TEXT,
        ArmGroupDescription TEXT,
        ArmGroupInterventionName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    Collaborators (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        CollaboratorName TEXT,
        CollaboratorClass TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    Interventions (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionType TEXT,
        InterventionName TEXT,
        InterventionDescription TEXT,
        InterventionArmGroupLabel TEXT,
        InterventionOtherName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    PrimaryOutcomes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        PrimaryOutcomeMeasure TEXT,
        PrimaryOutcomeDescription TEXT,
        PrimaryOutcomeTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    SecondaryOutcomes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SecondaryOutcomeMeasure TEXT,
        SecondaryOutcomeDescription TEXT,
        SecondaryOutcomeTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    OverallOfficials (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        OverallOfficialName TEXT,
        OverallOfficialAffiliation TEXT,
        OverallOfficialRole TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    Locations (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        LocationFacility TEXT,
        LocationCity TEXT,
        LocationState TEXT,
        LocationZip TEXT,
        LocationCountry TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    StudyReferences (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ReferencePMID TEXT,
        ReferenceType TEXT,
        ReferenceCitation TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    ConditionMeshes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionMeshId TEXT,
        ConditionMeshTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    InterventionMeshes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionMeshId TEXT,
        InterventionMeshTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    ConditionAncestors (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionAncestorId TEXT,
        ConditionAncestorTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    InterventionAncestors (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionAncestorId TEXT,
        InterventionAncestorTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    ConditionBrowseLeaves (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionBrowseLeafId TEXT,
        ConditionBrowseLeafName TEXT,
        ConditionBrowseLeafAsFound TEXT,
        ConditionBrowseLeafRelevance TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    InterventionBrowseLeaves (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionBrowseLeafId TEXT,
        InterventionBrowseLeafName TEXT,
        InterventionBrowseLeafAsFound TEXT,
        InterventionBrowseLeafRelevance TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    ConditionBrowseBranches (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionBrowseBranchAbbrev TEXT,
        ConditionBrowseBranchName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE IF NOT EXISTS
    InterventionBrowseBranches (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionBrowseBranchAbbrev TEXT,
        InterventionBrowseBranchName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );
"""

STUDY_TABLE = [
    "NCTId",
    "OrgStudyId",
    "OrgFullName",
    "OrgClass",
    "BriefTitle",
    "OfficialTitle",
    "Acronym",
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
    "OversightHasDMC",
    "BriefSummary",
    "DetailedDescription",
    "Condition",
    "Keyword",
    "StudyType",
    "PatientRegistry",
    "DesignObservationalModel",
    "DesignTimePerspective",
    "EnrollmentCount",
    "EnrollmentType",
    "EligibilityCriteria",
    "HealthyVolunteers",
    "Sex",
    "MinimumAge",
    "MaximumAge",
    "StdAge",
    "StudyPopulation",
    "SamplingMethod",
    "VersionHolder",
    "HasResults",
    "StartDateType",
    "IsFDARegulatedDrug",
    "IsFDARegulatedDevice",
    "Phase",
    "DesignAllocation",
    "DesignInterventionModel",
    "DesignPrimaryPurpose",
    "DesignMasking",
    "DesignWhoMasked",
    "IPDSharing",
    "ResultsFirstSubmitDate",
    "ResultsFirstSubmitQCDate",
    "ResultsFirstPostDate",
    "ResultsFirstPostDateType",
    "EventsFrequencyThreshold",
    "AgreementPISponsorEmployee",
    "AgreementRestrictiveAgreement",
    "PointOfContactTitle",
    "PointOfContactOrganization",
    "PointOfContactEMail",
    "PointOfContactPhone",
    "ResponsiblePartyInvestigatorFullName",
    "ResponsiblePartyInvestigatorTitle",
    "ResponsiblePartyInvestigatorAffiliation",
    "ResponsiblePartyOldNameTitle",
    "ResponsiblePartyOldOrganization",
    "FlowPreAssignmentDetails",
    "EventsTimeFrame",
    "EventsDescription",
    "LimitationsAndCaveatsDescription",
    "AgreementRestrictionType",
    "AgreementOtherDetails",
    "LastKnownStatus",
    "BioSpecRetention",
    "BioSpecDescription",
    "GenderBased",
    "NCTIdAlias",
    "FlowRecruitmentDetails",
    "BaselinePopulationDescription",
    "IsUSExport",
    "WhyStopped",
    "DesignInterventionModelDescription",
    "IPDSharingDescription",
    "IsUnapprovedDevice",
    "PointOfContactPhoneExt",
    "DesignMaskingDescription",
    "GenderDescription",
    "TargetDuration",
    "OrgStudyIdType",
    "OrgStudyIdLink",
    "IPDSharingInfoType",
    "IPDSharingTimeFrame",
    "IPDSharingAccessCriteria",
    "DispFirstSubmitDate",
    "DispFirstSubmitQCDate",
    "DispFirstPostDate",
    "DispFirstPostDateType",
    "RemovedCountry",
    "UnpostedResponsibleParty",
    "EstimatedResultsFirstSubmitDate",
    "FirstMCPPostDate",
    "FirstMCPPostDateType",
    "IPDSharingURL",
    "DelayedPosting",
    "ExpandedAccessNCTId",
    "ExpandedAccessStatusForNCTId",
    "FlowTypeUnitsAnalyzed",
    "LargeDocNoSAP",
]
OTHER_TABLES = {
    "SecondaryIdInfos": [
        "ID",
        "NCTId",
        "SecondaryId",
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


connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()
cursor.executescript(UPDATE_DB_QUERY)

studies = Studies()
total_studies = studies.get_total_studies()

with tqdm(total=total_studies, unit="studies") as pbar:
    for _ in range((total_studies // 1000) + 1):
        for study in studies.get_studies():
            insert_study(cursor, study)
            pbar.update(1)
        connection.commit()

connection.close()
