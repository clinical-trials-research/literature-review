import sqlite3

COMMAND = """
CREATE TABLE Study (
    NCTId TEXT PRIMARY KEY,
    OrgStudyId TEXT,
    OrgFullName TEXT,
    OrgClass TEXT,
    BriefTitle TEXT,
    OfficialTitle TEXT,
    StatusVerifiedDate DATE,
    OverallStatus TEXT,
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
    DesignPrimaryPurpose TEXT,
    DesignMasking TEXT,
    EligibilityCriteria TEXT,
    HealthyVolunteers BOOLEAN,
    Sex TEXT,
    MinimumAge TEXT,
    MaximumAge TEXT,
    VersionHolder DATE,
    HasResults BOOLEAN
);

CREATE TABLE SecondaryIdInfos (
    SecondaryId TEXT PRIMARY KEY,
    NCTId TEXT,
    SecondaryIdType TEXT,
    SecondaryIdDomain TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Collaborators (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    CollaboratorName TEXT,
    CollaboratorClass TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Condition (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    Condition TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Keyword (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    Keyword TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Phase (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    Phase TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Interventions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    InterventionType TEXT,
    InterventionName TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE PrimaryOutcomes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    PrimaryOutcomeMeasure TEXT,
    PrimaryOutcomeDescription TEXT,
    PrimaryOutcomeTimeFrame TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE SecondaryOutcomes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    SecondaryOutcomeMeasure TEXT,
    SecondaryOutcomeDescription TEXT,
    SecondaryOutcomeTimeFrame TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE OverallOfficials (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    OverallOfficialName TEXT,
    OverallOfficialAffiliation TEXT,
    OverallOfficialRole TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE Locations (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    LocationFacility TEXT,
    LocationCity TEXT,
    LocationState TEXT,
    LocationZip TEXT,
    LocationCountry TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE ConditionMeshes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    ConditionMeshId TEXT,
    ConditionMeshTerm TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE InterventionMeshes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    InterventionMeshId TEXT,
    InterventionMeshTerm TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE ConditionAncestors (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    ConditionAncestorId TEXT,
    ConditionAncestorTerm TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE InterventionAncestors (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    InterventionAncestorId TEXT,
    InterventionAncestorTerm TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE ConditionBrowseLeaves (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    ConditionBrowseLeafId TEXT,
    ConditionBrowseLeafName TEXT,
    ConditionBrowseLeafAsFound TEXT,
    ConditionBrowseLeafRelevance TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE InterventionBrowseLeaves (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    InterventionBrowseLeafId TEXT,
    InterventionBrowseLeafName TEXT,
    InterventionBrowseLeafAsFound TEXT,
    InterventionBrowseLeafRelevance TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE ConditionBrowseBranches (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    ConditionBrowseBranchAbbrev TEXT,
    ConditionBrowseBranchName TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);

CREATE TABLE InterventionBrowseBranches (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NCTId TEXT,
    InterventionBrowseBranchAbbrev TEXT,
    InterventionBrowseBranchName TEXT,
    FOREIGN KEY (NCTId) REFERENCES Study(NCTId)
);
"""

connection = sqlite3.connect("./clinical_trials.db")
cursor = connection.cursor()
cursor.executescript(COMMAND)
connection.commit()
connection.close()
