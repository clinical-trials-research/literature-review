import sqlite3
import pyodbc

import sqlite3

from tqdm import tqdm

from litreview.studies import Studies

UPDATE_DB_QUERY = """
CREATE TABLE
    IF NOT EXISTS Study (
        NCTId TEXT,
        OrgStudyId TEXT,
        OrgFullName TEXT,
        OrgClass TEXT,
        BriefTitle TEXT,
        OfficialTitle TEXT,
        Acronym TEXT,
        StatusVerifiedDate DATE,
        OverallStatus TEXT,
        HasExpandedAccess INTEGER,
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
        OversightHasDMC INTEGER,
        BriefSummary TEXT,
        DetailedDescription TEXT,
        Condition TEXT,
        Keyword TEXT,
        StudyType TEXT,
        PatientRegistry INTEGER,
        DesignObservationalModel TEXT,
        DesignTimePerspective TEXT,
        EnrollmentCount INTEGER,
        EnrollmentType TEXT,
        EligibilityCriteria TEXT,
        HealthyVolunteers INTEGER,
        Sex TEXT,
        MinimumAge TEXT,
        MaximumAge TEXT,
        StdAge TEXT,
        StudyPopulation TEXT,
        SamplingMethod TEXT,
        VersionHolder DATE,
        HasResults INTEGER,
        StartDateType TEXT,
        IsFDARegulatedDrug INTEGER,
        IsFDARegulatedDevice INTEGER,
        Phase TEXT,
        DesignAllocation TEXT,
        DesignInterventionModel TEXT,
        DesignPrimaryPurpose TEXT,
        DesignMasking TEXT,
        DesignWhoMasked TEXT,
        IPDSharing TEXT,
        ResultsFirstSubmitDate DATE,
        ResultsFirstSubmitQCDate DATE,
        ResultsFirstPostDate DATE,
        ResultsFirstPostDateType TEXT,
        EventsFrequencyThreshold TEXT,
        AgreementPISponsorEmployee INTEGER,
        AgreementRestrictiveAgreement INTEGER,
        PointOfContactTitle TEXT,
        PointOfContactOrganization TEXT,
        PointOfContactEMail TEXT,
        PointOfContactPhone TEXT,
        ResponsiblePartyInvestigatorFullName TEXT,
        ResponsiblePartyInvestigatorTitle TEXT,
        ResponsiblePartyInvestigatorAffiliation TEXT,
        ResponsiblePartyOldNameTitle TEXT,
        ResponsiblePartyOldOrganization TEXT,
        FlowPreAssignmentDetails TEXT,
        EventsTimeFrame TEXT,
        EventsDescription TEXT,
        LimitationsAndCaveatsDescription TEXT,
        AgreementRestrictionType TEXT,
        AgreementOtherDetails TEXT,
        LastKnownStatus TEXT,
        BioSpecRetention TEXT,
        BioSpecDescription TEXT,
        GenderBased INTEGER,
        NCTIdAlias TEXT,
        FlowRecruitmentDetails TEXT,
        BaselinePopulationDescription TEXT,
        IsUSExport INTEGER,
        WhyStopped TEXT,
        DesignInterventionModelDescription TEXT,
        IPDSharingDescription TEXT,
        IsUnapprovedDevice INTEGER,
        PointOfContactPhoneExt TEXT,
        DesignMaskingDescription TEXT,
        GenderDescription TEXT,
        TargetDuration TEXT,
        OrgStudyIdType TEXT,
        OrgStudyIdLink TEXT,
        IPDSharingInfoType TEXT,
        IPDSharingTimeFrame TEXT,
        IPDSharingAccessCriteria TEXT,
        DispFirstSubmitDate DATE,
        DispFirstSubmitQCDate DATE,
        DispFirstPostDate DATE,
        DispFirstPostDateType TEXT,
        RemovedCountry TEXT,
        UnpostedResponsibleParty TEXT,
        EstimatedResultsFirstSubmitDate DATE,
        FirstMCPPostDate DATE,
        FirstMCPPostDateType TEXT,
        IPDSharingURL TEXT,
        DelayedPosting INTEGER,
        ExpandedAccessNCTId TEXT,
        ExpandedAccessStatusForNCTId TEXT,
        FlowTypeUnitsAnalyzed TEXT,
        LargeDocNoSAP INTEGER
    );

CREATE TABLE
    IF NOT EXISTS SecondaryIdInfos (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SecondaryId TEXT,
        SecondaryIdType TEXT,
        SecondaryIdDomain TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS ArmGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ArmGroupLabel TEXT,
        ArmGroupType TEXT,
        ArmGroupDescription TEXT,
        ArmGroupInterventionName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS Collaborators (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        CollaboratorName TEXT,
        CollaboratorClass TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS Interventions (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionType TEXT,
        InterventionName TEXT,
        InterventionDescription TEXT,
        InterventionArmGroupLabel TEXT,
        InterventionOtherName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS PrimaryOutcomes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        PrimaryOutcomeMeasure TEXT,
        PrimaryOutcomeDescription TEXT,
        PrimaryOutcomeTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS SecondaryOutcomes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SecondaryOutcomeMeasure TEXT,
        SecondaryOutcomeDescription TEXT,
        SecondaryOutcomeTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS OverallOfficials (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        OverallOfficialName TEXT,
        OverallOfficialAffiliation TEXT,
        OverallOfficialRole TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS Locations (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        LocationFacility TEXT,
        LocationCity TEXT,
        LocationState TEXT,
        LocationZip TEXT,
        LocationCountry TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS StudyReferences (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ReferencePMID TEXT,
        ReferenceType TEXT,
        ReferenceCitation TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS ConditionMeshes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionMeshId TEXT,
        ConditionMeshTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS InterventionMeshes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionMeshId TEXT,
        InterventionMeshTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS ConditionAncestors (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionAncestorId TEXT,
        ConditionAncestorTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS InterventionAncestors (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionAncestorId TEXT,
        InterventionAncestorTerm TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS ConditionBrowseLeaves (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionBrowseLeafId TEXT,
        ConditionBrowseLeafName TEXT,
        ConditionBrowseLeafAsFound TEXT,
        ConditionBrowseLeafRelevance TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS InterventionBrowseLeaves (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionBrowseLeafId TEXT,
        InterventionBrowseLeafName TEXT,
        InterventionBrowseLeafAsFound TEXT,
        InterventionBrowseLeafRelevance TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS ConditionBrowseBranches (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        ConditionBrowseBranchAbbrev TEXT,
        ConditionBrowseBranchName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS InterventionBrowseBranches (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        InterventionBrowseBranchAbbrev TEXT,
        InterventionBrowseBranchName TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS OtherOutcomes (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        OtherOutcomeMeasure TEXT,
        OtherOutcomeDescription TEXT,
        OtherOutcomeTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS CentralContacts (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        CentralContactName TEXT,
        CentralContactRole TEXT,
        CentralContactPhone TEXT,
        CentralContactEMail TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS FlowGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        FlowGroupId TEXT,
        FlowGroupTitle TEXT,
        FlowGroupDescription TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS BaselineGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        BaselineGroupId TEXT,
        BaselineGroupTitle TEXT,
        BaselineGroupDescription TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS EventGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        EventGroupId TEXT,
        EventGroupTitle TEXT,
        EventGroupDescription TEXT,
        EventGroupDeathsNumAffected INTEGER,
        EventGroupDeathsNumAtRisk INTEGER,
        EventGroupSeriousNumAffected INTEGER,
        EventGroupSeriousNumAtRisk INTEGER,
        EventGroupOtherNumAffected INTEGER,
        EventGroupOtherNumAtRisk INTEGER,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS SeeAlsoLinks (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SeeAlsoLinkLabel TEXT,
        SeeAlsoLinkURL TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS LargeDocs (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        LargeDocTypeAbbrev TEXT,
        LargeDocHasProtocol BOOLEAN,
        LargeDocHasSAP BOOLEAN,
        LargeDocHasICF BOOLEAN,
        LargeDocLabel TEXT,
        LargeDocDate DATE,
        LargeDocUploadDate DATE,
        LargeDocFilename TEXT,
        LargeDocSize INTEGER,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS UnpostedEvents (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        UnpostedEventType TEXT,
        UnpostedEventDate DATE,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS SubmissionInfos (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SubmissionReleaseDate DATE,
        SubmissionResetDate DATE,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS AvailIPDs (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        AvailIPDId TEXT,
        AvailIPDType TEXT,
        AvailIPDURL TEXT,
        AvailIPDComment TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS FlowPeriods (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        FlowPeriodTitle TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS FlowMilestones (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        FlowPeriodsId INT,
        FlowMilestoneType TEXT,
        FOREIGN KEY (FlowPeriodsId) REFERENCES FlowPeriods (ID)
    );

CREATE TABLE
    IF NOT EXISTS FlowAchievements (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        FlowMilestonesId INT,
        FlowAchievementGroupId TEXT,
        FlowAchievementNumSubjects TEXT,
        FOREIGN KEY (FlowMilestonesId) REFERENCES FlowMilestones (ID)
    );

CREATE TABLE
    IF NOT EXISTS BaselineDenoms (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        BaselineDenomUnits TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS BaselineDenomCounts (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        BaselineDenomsId INT,
        BaselineDenomCountGroupId TEXT,
        BaselineDenomCountValue TEXT,
        FOREIGN KEY (BaselineDenomsId) REFERENCES BaselineDenoms (ID)
    );

CREATE TABLE
    IF NOT EXISTS BaselineMeasures (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        BaselineMeasureTitle TEXT,
        BaselineMeasureParamType TEXT,
        BaselineMeasureUnitOfMeasure TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS BaselineClasses (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        BaselineMeasureId INT,
        FOREIGN KEY (BaselineMeasureId) REFERENCES BaselineMeasures (ID)
    );

CREATE TABLE
    IF NOT EXISTS BaselineCategories (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        BaselineClassId INT,
        BaselineCategoryTitle TEXT,
        FOREIGN KEY (BaselineClassId) REFERENCES BaselineClasses (ID)
    );

CREATE TABLE
    IF NOT EXISTS BaselineMeasurements (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        BaselineCategoryId INT,
        FOREIGN KEY (BaselineCategoryId) REFERENCES BaselineCategories (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeMeasures (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        OutcomeMeasureType TEXT,
        OutcomeMeasureTitle TEXT,
        OutcomeMeasureDescription TEXT,
        OutcomeMeasuresPopulationDescription TEXT,
        OutcomeMeasuresReportingStatus TEXT,
        OutcomeMeasuresParamType TEXT,
        OutcomeMeasuresDispersionType TEXT,
        OutcomeMeasuresUnitOfMeasure TEXT,
        OutcomeMeasuresTimeFrame TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeGroups (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeMeasureId INT,
        OutcomeGroupId TEXT,
        OutcomeGroupTitle TEXT,
        OutcomeGroupDescription TEXT,
        FOREIGN KEY (OutcomeMeasureId) REFERENCES OutcomeMeasures (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeDenoms (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeMeasureId INT,
        OutcomeDenomUnits TEXT,
        FOREIGN KEY (OutcomeMeasureId) REFERENCES OutcomeMeasures (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeDenomCounts (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeDenomId INT,
        OutcomeDenomUnits TEXT,
        FOREIGN KEY (OutcomeDenomId) REFERENCES OutcomeDenoms (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeClasses (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeMeasureId INT,
        FOREIGN KEY (OutcomeMeasureId) REFERENCES OutcomeMeasures (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeCategories (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeClassId INT,
        FOREIGN KEY (OutcomeClassId) REFERENCES OutcomeClasses (ID)
    );

CREATE TABLE
    IF NOT EXISTS OutcomeMeasurements (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OutcomeCategoryId INT,
        OutcomeMeasurementGroupId TEXT,
        OutcomeMeasurementValue TEXT,
        OutcomeMeasurementLowerLimit TEXT,
        OutcomeMeasurementUpperLimit TEXT,
        FOREIGN KEY (OutcomeCategoryId) REFERENCES OutcomeCategories (ID)
    );

CREATE TABLE
    IF NOT EXISTS OtherEvents (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        OtherEventTerm TEXT,
        OtherEventOrganSystem TEXT,
        OtherEventAssessmentType TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS OtherEventStats (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        OtherEventsId INT,
        OtherEventStatsGroupId TEXT,
        OtherEventStatsNumEvents INT,
        OtherEventStatsNumAffected INT,
        OtherEventStatsNumAtRisk INT
    );

CREATE TABLE
    IF NOT EXISTS SeriousEvents (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        NCTId TEXT,
        SeriousEventTerm TEXT,
        SeriousEventOrganSystem TEXT,
        SeriousEventSourceVocabulary TEXT,
        SeriousEventAssessmentType TEXT,
        FOREIGN KEY (NCTId) REFERENCES Study (NCTId)
    );

CREATE TABLE
    IF NOT EXISTS SeriousEventStats (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        SeriousEventsId INT,
        SeriousEventStatsGroupId TEXT,
        SeriousEventStatsNumAffected INT,
        SeriousEventStatsNumAtRisk INT,
        FOREIGN KEY (SeriousEventsId) REFERENCES SeriousEvents (ID)
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
        "NCTId",
        "SecondaryId",
        "SecondaryIdType",
        "SecondaryIdDomain",
    ],
    "ArmGroups": [
        "NCTId",
        "ArmGroupLabel",
        "ArmGroupType",
        "ArmGroupDescription",
        "ArmGroupInterventionName",
    ],
    "Collaborators": [
        "NCTId",
        "CollaboratorName",
        "CollaboratorClass",
    ],
    "Interventions": [
        "NCTId",
        "InterventionType",
        "InterventionName",
        "InterventionDescription",
        "InterventionArmGroupLabel",
        "InterventionOtherName",
    ],
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
    "StudyReferences": [
        "NCTId",
        "ReferencePMID",
        "ReferenceType",
        "ReferenceCitation",
    ],
    "ConditionMeshes": [
        "NCTId",
        "ConditionMeshId",
        "ConditionMeshTerm",
    ],
    "InterventionMeshes": [
        "NCTId",
        "InterventionMeshId",
        "InterventionMeshTerm",
    ],
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
    "OtherOutcomes": [
        "NCTId",
        "OtherOutcomeMeasure",
        "OtherOutcomeDescription",
        "OtherOutcomeTimeFrame",
    ],
    "CentralContacts": [
        "NCTId",
        "CentralContactName",
        "CentralContactRole",
        "CentralContactPhone",
        "CentralContactEMail",
    ],
    "FlowGroups": [
        "NCTId",
        "FlowGroupId",
        "FlowGroupTitle",
        "FlowGroupDescription",
    ],
    "BaselineGroups": [
        "NCTId",
        "BaselineGroupId",
        "BaselineGroupTitle",
        "BaselineGroupDescription",
    ],
    "EventGroups": [
        "NCTId",
        "EventGroupId",
        "EventGroupTitle",
        "EventGroupDescription",
        "EventGroupDeathsNumAffected",
        "EventGroupDeathsNumAtRisk",
        "EventGroupSeriousNumAffected",
        "EventGroupSeriousNumAtRisk",
        "EventGroupOtherNumAffected",
        "EventGroupOtherNumAtRisk",
    ],
    "SeeAlsoLinks": [
        "NCTId",
        "SeeAlsoLinkLabel",
        "SeeAlsoLinkURL",
    ],
    "LargeDocs": [
        "NCTId",
        "LargeDocTypeAbbrev",
        "LargeDocHasProtocol",
        "LargeDocHasSAP",
        "LargeDocHasICF",
        "LargeDocLabel",
        "LargeDocDate",
        "LargeDocUploadDate",
        "LargeDocFilename",
        "LargeDocSize",
    ],
    "UnpostedEvents": [
        "NCTId",
        "UnpostedEventType",
        "UnpostedEventDate",
    ],
    "SubmissionInfos": [
        "NCTId",
        "SubmissionReleaseDate",
        "SubmissionResetDate",
    ],
    "AvailIPDs": [
        "NCTId",
        "AvailIPDId",
        "AvailIPDType",
        "AvailIPDURL",
        "AvailIPDComment",
    ],
    "FlowPeriods": [
        "NCTId",
        "FlowPeriodTitle",
    ],
    "FlowMilestones": [
        "FlowPeriodsId",
        "FlowMilestoneType",
    ],
    "FlowAchievements": [
        "FlowMilestonesId",
        "FlowAchievementGroupId",
        "FlowAchievementNumSubjects",
    ],
    "BaselineDenoms": ["ID", "NCTId", "BaselineDenomUnits"],
    "BaselineDenomCounts": [
        "BaselineDenomsId",
        "BaselineDenomCountGroupId",
        "BaselineDenomCountValue",
    ],
    "BaselineMeasures": [
        "NCTId",
        "BaselineMeasureTitle",
        "BaselineMeasureParamType",
        "BaselineMeasureUnitOfMeasure",
    ],
    "BaselineClasses": [
        "BaselineMeasureId",
    ],
    "BaselineCategories": [
        "BaselineClassId",
        "BaselineCategoryTitle",
    ],
    "BaselineMeasurements": [
        "BaselineCategoryId",
    ],
    "OutcomeMeasures": [
        "NCTId",
        "OutcomeMeasureType",
        "OutcomeMeasureTitle",
        "OutcomeMeasureDescription",
        "OutcomeMeasuresPopulationDescription",
        "OutcomeMeasuresReportingStatus",
        "OutcomeMeasuresParamType",
        "OutcomeMeasuresDispersionType",
        "OutcomeMeasuresUnitOfMeasure",
        "OutcomeMeasuresTimeFrame",
    ],
    "OutcomeGroups": [
        "OutcomeMeasureId",
        "OutcomeGroupId",
        "OutcomeGroupTitle",
        "OutcomeGroupDescription",
    ],
    "OutcomeDenoms": [
        "OutcomeMeasureId",
        "OutcomeDenomUnits",
    ],
    "OutcomeDenomCounts": [
        "OutcomeDenomId",
        "OutcomeDenomUnits",
    ],
    "OutcomeClasses": [
        "OutcomeMeasureId",
    ],
    "OutcomeCategories": [
        "OutcomeClassId",
    ],
    "OutcomeMeasurements": [
        "OutcomeCategoryId",
        "OutcomeMeasurementGroupId",
        "OutcomeMeasurementValue",
        "OutcomeMeasurementLowerLimit",
        "OutcomeMeasurementUpperLimit",
    ],
    "OtherEvents": [
        "NCTId",
        "OtherEventTerm",
        "OtherEventOrganSystem",
        "OtherEventAssessmentType",
    ],
    "OtherEventStats": [
        "OtherEventsId",
        "OtherEventStatsGroupId",
        "OtherEventStatsNumEvents",
        "OtherEventStatsNumAffected",
        "OtherEventStatsNumAtRisk",
    ],
    "SeriousEvents": [
        "NCTId",
        "SeriousEventTerm",
        "SeriousEventOrganSystem",
        "SeriousEventSourceVocabulary",
        "SeriousEventAssessmentType",
    ],
    "SeriousEventStats": [
        "SeriousEventsId",
        "SeriousEventStatsGroupId",
        "SeriousEventStatsNumAffected",
        "SeriousEventStatsNumAtRisk",
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


server = 'clinicaltrials.database.windows.net'
database = 'Clinical Trials'
username = 'azureuser'
password = 'dazgig-gEdder-8cessa'
mssql_conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
mssql_cursor = mssql_conn.cursor()


mssql_cursor.execute(UPDATE_DB_QUERY)

studies = Studies(1000)
total_studies = studies.get_total_studies()

with tqdm(total=total_studies, unit="studies") as pbar:
    for _ in range((total_studies // 1000) + 1):
        for study in studies.get_studies():
            insert_study(mssql_cursor, study)
            pbar.update(1)
        mssql_conn.commit()

mssql_conn.close()


# Connect to SQLite
sqlite_conn = sqlite3.connect('clinical_trials.db')
cursor = sqlite_conn.cursor()


