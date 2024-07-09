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
        LargeDocNoSAP INTEGER,
    )
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