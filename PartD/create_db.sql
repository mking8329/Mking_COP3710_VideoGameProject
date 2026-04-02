CREATE TABLE Franchise (
    FranchiseID    NUMBER NOT NULL,
    FranchiseName  VARCHAR2(150) NOT NULL,
    Publisher      VARCHAR2(150) NOT NULL,
    StartYear      NUMBER(4) NOT NULL,
    WebsiteURL     VARCHAR2(255),
    CONSTRAINT PK_Franchise PRIMARY KEY (FranchiseID),
    CONSTRAINT UQ_Franchise_Name UNIQUE (FranchiseName),
    CONSTRAINT CK_Franchise_StartYear CHECK (StartYear >= 1950)
);

CREATE TABLE Platform (
    PlatformID     NUMBER NOT NULL,
    PlatformName   VARCHAR2(100) NOT NULL,
    Manufacturer   VARCHAR2(100) NOT NULL,
    ReleaseYear    NUMBER(4) NOT NULL,
    CONSTRAINT PK_Platform PRIMARY KEY (PlatformID),
    CONSTRAINT UQ_Platform_Name UNIQUE (PlatformName),
    CONSTRAINT CK_Platform_ReleaseYear CHECK (ReleaseYear >= 1970)
);

CREATE TABLE Region (
    RegionID       NUMBER NOT NULL,
    RegionName     VARCHAR2(100) NOT NULL,
    Currency       VARCHAR2(50) NOT NULL,
    CONSTRAINT PK_Region PRIMARY KEY (RegionID),
    CONSTRAINT UQ_Region_Name UNIQUE (RegionName)
);

CREATE TABLE Game (
    GameID         NUMBER NOT NULL,
    Title          VARCHAR2(200) NOT NULL,
    ReleaseDate    DATE NOT NULL,
    Genre          VARCHAR2(100) NOT NULL,
    ESRBRating     VARCHAR2(10),
    FranchiseID    NUMBER NOT NULL,
    CONSTRAINT PK_Game PRIMARY KEY (GameID)
);

CREATE TABLE GamePlatform (
    GameID                 NUMBER NOT NULL,
    PlatformID             NUMBER NOT NULL,
    ReleaseDateOnPlatform  DATE NOT NULL,
    PlatformExclusive      NUMBER(1) DEFAULT 0 NOT NULL,
    CONSTRAINT PK_GamePlatform PRIMARY KEY (GameID, PlatformID),
    CONSTRAINT CK_GP_Exclusive CHECK (PlatformExclusive IN (0, 1))
);

CREATE TABLE QuarterlySales (
    GameID       NUMBER NOT NULL,
    RegionID     NUMBER NOT NULL,
    SalesYear    NUMBER(4) NOT NULL,
    QuarterNum   NUMBER(1) NOT NULL,
    UnitsSold    NUMBER NOT NULL,
    Revenue      NUMBER(15,2) NOT NULL,
    CONSTRAINT PK_QuarterlySales PRIMARY KEY (GameID, RegionID, SalesYear, QuarterNum),
    CONSTRAINT CK_QS_Quarter CHECK (QuarterNum BETWEEN 1 AND 4),
    CONSTRAINT CK_QS_Units CHECK (UnitsSold >= 0),
    CONSTRAINT CK_QS_Revenue CHECK (Revenue >= 0),
    CONSTRAINT CK_QS_Year CHECK (SalesYear >= 1950)
);

CREATE TABLE FranchisePerformanceRank (
    FranchiseID       NUMBER NOT NULL,
    GlobalRank        NUMBER NOT NULL,
    TotalRevenue      NUMBER(15,2) NOT NULL,
    LastUpdatedDate   DATE NOT NULL,
    CONSTRAINT PK_FranchisePerformanceRank PRIMARY KEY (FranchiseID),
    CONSTRAINT CK_FPR_Rank CHECK (GlobalRank > 0),
    CONSTRAINT CK_FPR_Revenue CHECK (TotalRevenue >= 0)
);

ALTER TABLE Game
ADD CONSTRAINT FK_Game_Franchise
FOREIGN KEY (FranchiseID)
REFERENCES Franchise(FranchiseID);

ALTER TABLE GamePlatform
ADD CONSTRAINT FK_GP_Game
FOREIGN KEY (GameID)
REFERENCES Game(GameID);

ALTER TABLE GamePlatform
ADD CONSTRAINT FK_GP_Platform
FOREIGN KEY (PlatformID)
REFERENCES Platform(PlatformID);

ALTER TABLE QuarterlySales
ADD CONSTRAINT FK_QS_Game
FOREIGN KEY (GameID)
REFERENCES Game(GameID);

ALTER TABLE QuarterlySales
ADD CONSTRAINT FK_QS_Region
FOREIGN KEY (RegionID)
REFERENCES Region(RegionID);

ALTER TABLE FranchisePerformanceRank
ADD CONSTRAINT FK_FPR_Franchise
FOREIGN KEY (FranchiseID)
REFERENCES Franchise(FranchiseID);

COMMIT;