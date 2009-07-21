
-- LSST Database Schema
-- $Author$
-- $Revision$
-- $Date$
--
-- See <http://lsstdev.ncsa.uiuc.edu:8100/trac/wiki/Copyrights>
-- for copyright information.


CREATE TABLE AAA_Version_3_0_31 (version CHAR);

CREATE TABLE mops_Event_OrbitIdentification
(
	eventId BIGINT NULL,
	childObjectId BIGINT NULL,
	PRIMARY KEY (eventId),
	INDEX idx_mopsEventOrbitIdentificationToMovingObject_childObjectId (childObjectId ASC),
	KEY (eventId)
) ;


CREATE TABLE _mops_MoidQueue
(
	movingObjectId BIGINT NULL,
	movingObjectVersion INT NULL,
	eventId BIGINT NULL,
	insertTime TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (movingObjectId, movingObjectVersion),
	KEY (movingObjectId),
	INDEX idx_mopsMoidQueue_eventId (eventId ASC)
) ;


CREATE TABLE _mops_EonQueue
(
	movingObjectId BIGINT NULL,
	eventId BIGINT NULL,
	insertTime TIMESTAMP NULL,
	status CHAR(1) NULL DEFAULT 'I',
	PRIMARY KEY (movingObjectId),
	KEY (movingObjectId),
	INDEX idx__mopsEonQueue_eventId (eventId ASC)
) ;


CREATE TABLE _DIASourceToAlert
(
	alertId INTEGER NULL,
	diaSourceId BIGINT NULL,
	KEY (diaSourceId),
	KEY (alertId)
) ;


CREATE TABLE DIASource
(
	diaSourceId BIGINT NULL,
	ampExposureId BIGINT NULL,
	diaSourceToId BIGINT NULL,
	filterId TINYINT NULL,
	objectId BIGINT NULL,
	movingObjectId BIGINT NULL,
	procHistoryId INTEGER NULL,
	scId INTEGER NULL,
	ssmId BIGINT NULL,
	ra DOUBLE NULL,
	raErrForDetection FLOAT(0) NULL,
	raErrForWcs FLOAT(0) NULL,
	decl DOUBLE NULL,
	declErrForDetection FLOAT(0) NULL,
	declErrForWcs FLOAT(0) NULL,
	xFlux DOUBLE NULL,
	xFluxErr FLOAT(0) NULL,
	yFlux DOUBLE NULL,
	yFluxErr FLOAT(0) NULL,
	raFlux DOUBLE NULL,
	raFluxErr FLOAT(0) NULL,
	declFlux DOUBLE NULL,
	declFluxErr FLOAT(0) NULL,
	xPeak DOUBLE NULL,
	yPeak DOUBLE NULL,
	raPeak DOUBLE NULL,
	declPeak DOUBLE NULL,
	xAstrom DOUBLE NULL,
	xAstromErr FLOAT(0) NULL,
	yAstrom DOUBLE NULL,
	yAstromErr FLOAT(0) NULL,
	raAstrom DOUBLE NULL,
	raAstromErr FLOAT(0) NULL,
	declAstrom DOUBLE NULL,
	declAstromErr FLOAT(0) NULL,
	taiMidPoint DOUBLE NULL,
	taiRange FLOAT(0) NULL,
	lengthDeg DOUBLE NULL,
	psfFlux DOUBLE NULL,
	psfFluxErr FLOAT(0) NULL,
	apFlux DOUBLE NULL,
	apFluxErr FLOAT(0) NULL,
	modelFlux DOUBLE NULL,
	modelFluxErr FLOAT(0) NULL,
	instFlux DOUBLE NULL,
	instFluxErr FLOAT(0) NULL,
	nonGrayCorrFlux DOUBLE NULL,
	nonGrayCorrFluxErr FLOAT(0) NULL,
	atmCorrFlux DOUBLE NULL,
	atmCorrFluxErr FLOAT(0) NULL,
	apDia FLOAT(0) NULL,
	refMag FLOAT(0) NULL,
	Ixx FLOAT(0) NULL,
	IxxErr FLOAT(0) NULL,
	Iyy FLOAT(0) NULL,
	IyyErr FLOAT(0) NULL,
	Ixy FLOAT(0) NULL,
	IxyErr FLOAT(0) NULL,
	snr FLOAT(0) NULL,
	chi2 FLOAT(0) NULL,
	valx1 DOUBLE NULL,
	valx2 DOUBLE NULL,
	valy1 DOUBLE NULL,
	valy2 DOUBLE NULL,
	valxy DOUBLE NULL,
	obsCode CHAR(3) NULL,
	isSynthetic CHAR(1) NULL,
	mopsStatus CHAR(1) NULL,
	flagForAssociation SMALLINT NULL,
	flagForDetection SMALLINT NULL,
	flagForWcs SMALLINT NULL,
	flagClassification BIGINT NULL,
	PRIMARY KEY (diaSourceId),
	UNIQUE UQ_DIASource_diaSourceToId(diaSourceToId),
	KEY (ampExposureId),
	KEY (ampExposureId),
	KEY (filterId),
	KEY (movingObjectId),
	KEY (objectId),
	KEY (procHistoryId),
	INDEX idx_DIASource_ssmId (ssmId ASC),
	KEY (scId),
	INDEX idx_DIASource_psfMag (psfFlux ASC),
	INDEX idx_DIASource_taiMidPoint (taiMidPoint ASC)
) TYPE=MyISAM;


CREATE TABLE Alert
(
	alertId INTEGER NULL DEFAULT 0,
	ampExposureId BIGINT NULL,
	objectId BIGINT NULL,
	timeGenerated DATETIME NULL,
	imagePStampURL VARCHAR(255) NULL,
	templatePStampURL VARCHAR(255) NULL,
	alertURL VARCHAR(255) NULL,
	PRIMARY KEY (alertId),
	KEY (objectId),
	INDEX idx_Alert_timeGenerated (timeGenerated ASC),
	KEY (ampExposureId)
) TYPE=MyISAM;


CREATE TABLE Calibration_CCD_Exposure
(
	ccdExposureId BIGINT NULL,
	exposureId INTEGER NULL,
	calibTypeId TINYINT NULL,
	filterId TINYINT NULL,
	equinox FLOAT(0) NULL,
	ctype1 VARCHAR(20) NULL,
	ctype2 VARCHAR(20) NULL,
	crpix1 FLOAT(0) NULL,
	crpix2 FLOAT(0) NULL,
	crval1 DOUBLE NULL,
	crval2 DOUBLE NULL,
	cd1_1 DOUBLE NULL,
	cd2_1 DOUBLE NULL,
	cd1_2 DOUBLE NULL,
	cd2_2 DOUBLE NULL,
	dateObs DATETIME NULL,
	expTime FLOAT(0) NULL,
	nCombine INTEGER NULL DEFAULT 1,
	PRIMARY KEY (ccdExposureId),
	KEY (exposureId),
	KEY (ccdExposureId)
) ;


CREATE TABLE Calibration_Amp_Exposure
(
	ccdExposureId BIGINT NULL,
	ampExposureId BIGINT NULL,
	PRIMARY KEY (ampExposureId),
	KEY (ccdExposureId),
	KEY (ampExposureId)
) ;


CREATE TABLE mops_Event
(
	eventId BIGINT NULL AUTO_INCREMENT,
	procHistoryId INT NULL,
	eventType CHAR(1) NULL,
	eventTime TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	movingObjectId BIGINT NULL,
	movingObjectVersion INT NULL,
	orbitCode CHAR(1) NULL,
	d3 FLOAT(0) NULL,
	d4 FLOAT(0) NULL,
	ccdExposureId BIGINT NULL,
	classification CHAR(1) NULL,
	ssmId BIGINT NULL,
	PRIMARY KEY (eventId),
	KEY (movingObjectId),
	INDEX idx_mopsEvent_ccdExposureId (ccdExposureId ASC),
	INDEX idx_mopsEvent_movingObjectId (movingObjectId ASC, movingObjectVersion ASC),
	INDEX idx_mopsEvent_procHistoryId (procHistoryId ASC),
	INDEX idx_mopsEvent_ssmId (ssmId ASC)
) ;


CREATE TABLE _SourceToAmp_Exposure
(
	sourceId BIGINT NULL,
	ampExposureId BIGINT NULL,
	KEY (sourceId),
	KEY (ampExposureId)
) ;


CREATE TABLE placeholder_VarObject
(
	objectId BIGINT NULL,
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	raErr FLOAT(0) NULL,
	declErr FLOAT(0) NULL,
	flagForStage1 INTEGER NULL,
	flagForStage2 INTEGER NULL,
	flagForStage3 INTEGER NULL,
	uAmplitude FLOAT(0) NULL,
	uPeriod FLOAT(0) NULL,
	uTimescale FLOAT(0) NULL,
	gAmplitude FLOAT(0) NULL,
	gPeriod FLOAT(0) NULL,
	gTimescale FLOAT(0) NULL,
	rAmplitude FLOAT(0) NULL,
	rPeriod FLOAT(0) NULL,
	rTimescale FLOAT(0) NULL,
	iAmplitude FLOAT(0) NULL,
	iPeriod FLOAT(0) NULL,
	iTimescale FLOAT(0) NULL,
	zAmplitude FLOAT(0) NULL,
	zPeriod FLOAT(0) NULL,
	zTimescale FLOAT(0) NULL,
	yAmplitude FLOAT(0) NULL,
	yPeriod FLOAT(0) NULL,
	yTimescale FLOAT(0) NULL,
	uScalegram01 FLOAT(0) NULL,
	uScalegram02 FLOAT(0) NULL,
	uScalegram03 FLOAT(0) NULL,
	uScalegram04 FLOAT(0) NULL,
	uScalegram05 FLOAT(0) NULL,
	uScalegram06 FLOAT(0) NULL,
	uScalegram07 FLOAT(0) NULL,
	uScalegram08 FLOAT(0) NULL,
	uScalegram09 FLOAT(0) NULL,
	uScalegram10 FLOAT(0) NULL,
	uScalegram11 FLOAT(0) NULL,
	uScalegram12 FLOAT(0) NULL,
	uScalegram13 FLOAT(0) NULL,
	uScalegram14 FLOAT(0) NULL,
	uScalegram15 FLOAT(0) NULL,
	uScalegram16 FLOAT(0) NULL,
	uScalegram17 FLOAT(0) NULL,
	uScalegram18 FLOAT(0) NULL,
	uScalegram19 FLOAT(0) NULL,
	uScalegram20 FLOAT(0) NULL,
	uScalegram21 FLOAT(0) NULL,
	uScalegram22 FLOAT(0) NULL,
	uScalegram23 FLOAT(0) NULL,
	uScalegram24 FLOAT(0) NULL,
	uScalegram25 FLOAT(0) NULL,
	gScalegram01 FLOAT(0) NULL,
	gScalegram02 FLOAT(0) NULL,
	gScalegram03 FLOAT(0) NULL,
	gScalegram04 FLOAT(0) NULL,
	gScalegram05 FLOAT(0) NULL,
	gScalegram06 FLOAT(0) NULL,
	gScalegram07 FLOAT(0) NULL,
	gScalegram08 FLOAT(0) NULL,
	gScalegram09 FLOAT(0) NULL,
	gScalegram10 FLOAT(0) NULL,
	gScalegram11 FLOAT(0) NULL,
	gScalegram12 FLOAT(0) NULL,
	gScalegram13 FLOAT(0) NULL,
	gScalegram14 FLOAT(0) NULL,
	gScalegram15 FLOAT(0) NULL,
	gScalegram16 FLOAT(0) NULL,
	gScalegram17 FLOAT(0) NULL,
	gScalegram18 FLOAT(0) NULL,
	gScalegram19 FLOAT(0) NULL,
	gScalegram20 FLOAT(0) NULL,
	gScalegram21 FLOAT(0) NULL,
	gScalegram22 FLOAT(0) NULL,
	gScalegram23 FLOAT(0) NULL,
	gScalegram24 FLOAT(0) NULL,
	gScalegram25 FLOAT(0) NULL,
	rScalegram01 FLOAT(0) NULL,
	rScalegram02 FLOAT(0) NULL,
	rScalegram03 FLOAT(0) NULL,
	rScalegram04 FLOAT(0) NULL,
	rScalegram05 FLOAT(0) NULL,
	rScalegram06 FLOAT(0) NULL,
	rScalegram07 FLOAT(0) NULL,
	rScalegram08 FLOAT(0) NULL,
	rScalegram09 FLOAT(0) NULL,
	rScalegram10 FLOAT(0) NULL,
	rScalegram11 FLOAT(0) NULL,
	rScalegram12 FLOAT(0) NULL,
	rScalegram13 FLOAT(0) NULL,
	rScalegram14 FLOAT(0) NULL,
	rScalegram15 FLOAT(0) NULL,
	rScalegram16 FLOAT(0) NULL,
	rScalegram17 FLOAT(0) NULL,
	rScalegram18 FLOAT(0) NULL,
	rScalegram19 FLOAT(0) NULL,
	rScalegram20 FLOAT(0) NULL,
	rScalegram21 FLOAT(0) NULL,
	rScalegram22 FLOAT(0) NULL,
	rScalegram23 FLOAT(0) NULL,
	rScalegram24 FLOAT(0) NULL,
	rScalegram25 FLOAT(0) NULL,
	iScalegram01 FLOAT(0) NULL,
	iScalegram02 FLOAT(0) NULL,
	iScalegram03 FLOAT(0) NULL,
	iScalegram04 FLOAT(0) NULL,
	iScalegram05 FLOAT(0) NULL,
	iScalegram06 FLOAT(0) NULL,
	iScalegram07 FLOAT(0) NULL,
	iScalegram08 FLOAT(0) NULL,
	iScalegram09 FLOAT(0) NULL,
	iScalegram10 FLOAT(0) NULL,
	iScalegram11 FLOAT(0) NULL,
	iScalegram12 FLOAT(0) NULL,
	iScalegram13 FLOAT(0) NULL,
	iScalegram14 FLOAT(0) NULL,
	iScalegram15 FLOAT(0) NULL,
	iScalegram16 FLOAT(0) NULL,
	iScalegram17 FLOAT(0) NULL,
	iScalegram18 FLOAT(0) NULL,
	iScalegram19 FLOAT(0) NULL,
	iScalegram20 FLOAT(0) NULL,
	iScalegram21 FLOAT(0) NULL,
	iScalegram22 FLOAT(0) NULL,
	iScalegram23 FLOAT(0) NULL,
	iScalegram24 FLOAT(0) NULL,
	iScalegram25 FLOAT(0) NULL,
	zScalegram01 FLOAT(0) NULL,
	zScalegram02 FLOAT(0) NULL,
	zScalegram03 FLOAT(0) NULL,
	zScalegram04 FLOAT(0) NULL,
	zScalegram05 FLOAT(0) NULL,
	zScalegram06 FLOAT(0) NULL,
	zScalegram07 FLOAT(0) NULL,
	zScalegram08 FLOAT(0) NULL,
	zScalegram09 FLOAT(0) NULL,
	zScalegram10 FLOAT(0) NULL,
	zScalegram11 FLOAT(0) NULL,
	zScalegram12 FLOAT(0) NULL,
	zScalegram13 FLOAT(0) NULL,
	zScalegram14 FLOAT(0) NULL,
	zScalegram15 FLOAT(0) NULL,
	zScalegram16 FLOAT(0) NULL,
	zScalegram17 FLOAT(0) NULL,
	zScalegram18 FLOAT(0) NULL,
	zScalegram19 FLOAT(0) NULL,
	zScalegram20 FLOAT(0) NULL,
	zScalegram21 FLOAT(0) NULL,
	zScalegram22 FLOAT(0) NULL,
	zScalegram23 FLOAT(0) NULL,
	zScalegram24 FLOAT(0) NULL,
	zScalegram25 FLOAT(0) NULL,
	yScalegram01 FLOAT(0) NULL,
	yScalegram02 FLOAT(0) NULL,
	yScalegram03 FLOAT(0) NULL,
	yScalegram04 FLOAT(0) NULL,
	yScalegram05 FLOAT(0) NULL,
	yScalegram06 FLOAT(0) NULL,
	yScalegram07 FLOAT(0) NULL,
	yScalegram08 FLOAT(0) NULL,
	yScalegram09 FLOAT(0) NULL,
	yScalegram10 FLOAT(0) NULL,
	yScalegram11 FLOAT(0) NULL,
	yScalegram12 FLOAT(0) NULL,
	yScalegram13 FLOAT(0) NULL,
	yScalegram14 FLOAT(0) NULL,
	yScalegram15 FLOAT(0) NULL,
	yScalegram16 FLOAT(0) NULL,
	yScalegram17 FLOAT(0) NULL,
	yScalegram18 FLOAT(0) NULL,
	yScalegram19 FLOAT(0) NULL,
	yScalegram20 FLOAT(0) NULL,
	yScalegram21 FLOAT(0) NULL,
	yScalegram22 FLOAT(0) NULL,
	yScalegram23 FLOAT(0) NULL,
	yScalegram24 FLOAT(0) NULL,
	yScalegram25 FLOAT(0) NULL,
	primaryPeriod FLOAT(0) NULL,
	primaryPeriodErr FLOAT(0) NULL,
	uPeriodErr FLOAT(0) NULL,
	gPeriodErr FLOAT(0) NULL,
	rPeriodErr FLOAT(0) NULL,
	iPeriodErr FLOAT(0) NULL,
	zPeriodErr FLOAT(0) NULL,
	yPeriodErr FLOAT(0) NULL,
	PRIMARY KEY (objectId),
	KEY (objectId)
) ;


CREATE TABLE placeholder_ObjectPhotoZ
(
	objectId BIGINT NULL,
	redshift FLOAT(0) NULL,
	redshiftErr FLOAT(0) NULL,
	probability TINYINT NULL DEFAULT 100,
	photoZ1 FLOAT(0) NULL,
	photoZ1Err FLOAT(0) NULL,
	photoZ2 FLOAT(0) NULL,
	photoZ2Err FLOAT(0) NULL,
	photoZ1Outlier FLOAT(0) NULL,
	photoZ2Outlier FLOAT(0) NULL,
	KEY (objectId)
) ;


CREATE TABLE aux_Science_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE Object
(
	objectId BIGINT NULL,
	procHistoryId INTEGER NULL,
	ra DOUBLE NULL,
	raErr FLOAT(0) NULL,
	decl DOUBLE NULL,
	declErr FLOAT(0) NULL,
	muRa DOUBLE NULL,
	muRaErr FLOAT(0) NULL,
	muDecl DOUBLE NULL,
	muDeclErr FLOAT(0) NULL,
	xFlux DOUBLE NULL,
	xFluxErr FLOAT(0) NULL,
	yFlux DOUBLE NULL,
	yFluxErr FLOAT(0) NULL,
	raFlux DOUBLE NULL,
	raFluxErr FLOAT(0) NULL,
	declFlux DOUBLE NULL,
	declFluxErr FLOAT(0) NULL,
	xPeak DOUBLE NULL,
	yPeak DOUBLE NULL,
	raPeak DOUBLE NULL,
	declPeak DOUBLE NULL,
	xAstrom DOUBLE NULL,
	xAstromErr FLOAT(0) NULL,
	yAstrom DOUBLE NULL,
	yAstromErr FLOAT(0) NULL,
	raAstrom DOUBLE NULL,
	raAstromErr FLOAT(0) NULL,
	declAstrom DOUBLE NULL,
	declAstromErr FLOAT(0) NULL,
	refrRaAstrom FLOAT(0) NULL,
	refrRaAstromErr FLOAT(0) NULL,
	refrDeclAstrom FLOAT(0) NULL,
	refrDeclAstromErr FLOAT(0) NULL,
	parallax FLOAT(0) NULL,
	parallaxErr FLOAT(0) NULL,
	earliestObsTime DATETIME NULL,
	latestObsTime DATETIME NULL,
	primaryPeriod FLOAT(0) NULL,
	primaryPeriodErr FLOAT(0) NULL,
	ugColor DOUBLE NULL,
	grColor DOUBLE NULL,
	riColor DOUBLE NULL,
	izColor DOUBLE NULL,
	zyColor DOUBLE NULL,
	cx DOUBLE NULL,
	cxErr FLOAT(0) NULL,
	cy DOUBLE NULL,
	cyErr FLOAT(0) NULL,
	cz DOUBLE NULL,
	czErr FLOAT(0) NULL,
	flagForStage1 INTEGER NULL,
	flagForStage2 INTEGER NULL,
	flagForStage3 INTEGER NULL,
	isProvisional BOOL NULL DEFAULT FALSE,
	zone INTEGER NULL,
	uMag DOUBLE NULL,
	uMagErr FLOAT(0) NULL,
	uPetroMag DOUBLE NULL,
	uPetroMagErr FLOAT(0) NULL,
	uApMag DOUBLE NULL,
	uApMagErr FLOAT(0) NULL,
	uPosErrA FLOAT(0) NULL,
	uPosErrB FLOAT(0) NULL,
	uPosErrTheta FLOAT(0) NULL,
	uNumObs INTEGER NULL,
	uVarProb TINYINT NULL,
	uAmplitude FLOAT(0) NULL,
	uPeriod FLOAT(0) NULL,
	uPeriodErr FLOAT(0) NULL,
	uIx FLOAT(0) NULL,
	uIxErr FLOAT(0) NULL,
	uIy FLOAT(0) NULL,
	uIyErr FLOAT(0) NULL,
	uIxx FLOAT(0) NULL,
	uIxxErr FLOAT(0) NULL,
	uIyy FLOAT(0) NULL,
	uIyyErr FLOAT(0) NULL,
	uIxy FLOAT(0) NULL,
	uIxyErr FLOAT(0) NULL,
	uTimescale FLOAT(0) NULL,
	gMag DOUBLE NULL,
	gMagErr FLOAT(0) NULL,
	gPetroMag DOUBLE NULL,
	gPetroMagErr FLOAT(0) NULL,
	gApMag DOUBLE NULL,
	gApMagErr FLOAT(0) NULL,
	gPosErrA FLOAT(0) NULL,
	gPosErrB FLOAT(0) NULL,
	gPosErrTheta FLOAT(0) NULL,
	gNumObs INTEGER NULL,
	gVarProb TINYINT NULL,
	gAmplitude FLOAT(0) NULL,
	gPeriod FLOAT(0) NULL,
	gPeriodErr FLOAT(0) NULL,
	gIx FLOAT(0) NULL,
	gIxErr FLOAT(0) NULL,
	gIy FLOAT(0) NULL,
	gIyErr FLOAT(0) NULL,
	gIxx FLOAT(0) NULL,
	gIxxErr FLOAT(0) NULL,
	gIyy FLOAT(0) NULL,
	gIyyErr FLOAT(0) NULL,
	gIxy FLOAT(0) NULL,
	gIxyErr FLOAT(0) NULL,
	gTimescale FLOAT(0) NULL,
	rMag DOUBLE NULL,
	rMagErr FLOAT(0) NULL,
	rPetroMag DOUBLE NULL,
	rPetroMagErr FLOAT(0) NULL,
	rApMag DOUBLE NULL,
	rApMagErr FLOAT(0) NULL,
	rPosErrA FLOAT(0) NULL,
	rPosErrB FLOAT(0) NULL,
	rPosErrTheta FLOAT(0) NULL,
	rNumObs INTEGER NULL,
	rVarProb TINYINT NULL,
	rAmplitude FLOAT(0) NULL,
	rPeriod FLOAT(0) NULL,
	rPeriodErr FLOAT(0) NULL,
	rIx FLOAT(0) NULL,
	rIxErr FLOAT(0) NULL,
	rIy FLOAT(0) NULL,
	rIyErr FLOAT(0) NULL,
	rIxx FLOAT(0) NULL,
	rIxxErr FLOAT(0) NULL,
	rIyy FLOAT(0) NULL,
	rIyyErr FLOAT(0) NULL,
	rIxy FLOAT(0) NULL,
	rIxyErr FLOAT(0) NULL,
	rTimescale FLOAT(0) NULL,
	iMag DOUBLE NULL,
	iMagErr FLOAT(0) NULL,
	iPetroMag DOUBLE NULL,
	iPetroMagErr FLOAT(0) NULL,
	iApMag DOUBLE NULL,
	iApMagErr FLOAT(0) NULL,
	iPosErrA FLOAT(0) NULL,
	iPosErrB FLOAT(0) NULL,
	iPosErrTheta FLOAT(0) NULL,
	iNumObs INTEGER NULL,
	iVarProb TINYINT NULL,
	iAmplitude FLOAT(0) NULL,
	iPeriod FLOAT(0) NULL,
	iPeriodErr FLOAT(0) NULL,
	iIx FLOAT(0) NULL,
	iIxErr FLOAT(0) NULL,
	iIy FLOAT(0) NULL,
	iIyErr FLOAT(0) NULL,
	iIxx FLOAT(0) NULL,
	iIxxErr FLOAT(0) NULL,
	iIyy FLOAT(0) NULL,
	iIyyErr FLOAT(0) NULL,
	iIxy FLOAT(0) NULL,
	iIxyErr FLOAT(0) NULL,
	iTimescale FLOAT(0) NULL,
	zMag DOUBLE NULL,
	zMagErr FLOAT(0) NULL,
	zPetroMag DOUBLE NULL,
	zPetroMagErr FLOAT(0) NULL,
	zApMag DOUBLE NULL,
	zApMagErr FLOAT(0) NULL,
	zPosErrA FLOAT(0) NULL,
	zPosErrB FLOAT(0) NULL,
	zPosErrTheta FLOAT(0) NULL,
	zNumObs INTEGER NULL,
	zVarProb TINYINT NULL,
	zAmplitude FLOAT(0) NULL,
	zPeriod FLOAT(0) NULL,
	zPeriodErr FLOAT(0) NULL,
	zIx FLOAT(0) NULL,
	zIxErr FLOAT(0) NULL,
	zIy FLOAT(0) NULL,
	zIyErr FLOAT(0) NULL,
	zIxx FLOAT(0) NULL,
	zIxxErr FLOAT(0) NULL,
	zIyy FLOAT(0) NULL,
	zIyyErr FLOAT(0) NULL,
	zIxy FLOAT(0) NULL,
	zIxyErr FLOAT(0) NULL,
	zTimescale FLOAT(0) NULL,
	yMag DOUBLE NULL,
	yMagErr FLOAT(0) NULL,
	yPetroMag DOUBLE NULL,
	yPetroMagErr FLOAT(0) NULL,
	yApMag DOUBLE NULL,
	yApMagErr FLOAT(0) NULL,
	yPosErrA FLOAT(0) NULL,
	yPosErrB FLOAT(0) NULL,
	yPosErrTheta FLOAT(0) NULL,
	yNumObs INTEGER NULL,
	yVarProb TINYINT NULL,
	yAmplitude FLOAT(0) NULL,
	yPeriod FLOAT(0) NULL,
	yPeriodErr FLOAT(0) NULL,
	yIx FLOAT(0) NULL,
	yIxErr FLOAT(0) NULL,
	yIy FLOAT(0) NULL,
	yIyErr FLOAT(0) NULL,
	yIxx FLOAT(0) NULL,
	yIxxErr FLOAT(0) NULL,
	yIyy FLOAT(0) NULL,
	yIyyErr FLOAT(0) NULL,
	yIxy FLOAT(0) NULL,
	yIxyErr FLOAT(0) NULL,
	yTimescale FLOAT(0) NULL,
	PRIMARY KEY (objectId),
	INDEX idx_Object_ugColor (ugColor ASC),
	INDEX idx_Object_grColor (grColor ASC),
	INDEX idx_Object_riColor (riColor ASC),
	INDEX idx_Object_izColor (izColor ASC),
	INDEX idx_Object_zyColor (zyColor ASC),
	INDEX idx_Object_latestObsTime (latestObsTime ASC),
	KEY (procHistoryId)
) TYPE=MyISAM;


CREATE TABLE MovingObject
(
	movingObjectId BIGINT NULL,
	movingObjectVersion INT NULL DEFAULT '1',
	procHistoryId INTEGER NULL,
	taxonomicTypeId SMALLINT NULL,
	ssmObjectName VARCHAR(32) NULL,
	q DOUBLE NULL,
	e DOUBLE NULL,
	i DOUBLE NULL,
	node DOUBLE NULL,
	meanAnom DOUBLE NULL,
	argPeri DOUBLE NULL,
	distPeri DOUBLE NULL,
	timePeri DOUBLE NULL,
	epoch DOUBLE NULL,
	h_v DOUBLE NULL,
	g DOUBLE NULL DEFAULT 0.15,
	rotationPeriod DOUBLE NULL,
	rotationEpoch DOUBLE NULL,
	albedo DOUBLE NULL,
	poleLat DOUBLE NULL,
	poleLon DOUBLE NULL,
	d3 DOUBLE NULL,
	d4 DOUBLE NULL,
	orbFitResidual DOUBLE NULL,
	orbFitChi2 DOUBLE NULL,
	classification CHAR(1) NULL,
	ssmId BIGINT NULL,
	mopsStatus CHAR(1) NULL,
	stablePass CHAR(1) NULL,
	timeCreated TIMESTAMP NULL,
	uMag DOUBLE NULL,
	uMagErr FLOAT(0) NULL,
	uAmplitude FLOAT(0) NULL,
	uPeriod FLOAT(0) NULL,
	gMag DOUBLE NULL,
	gMagErr FLOAT(0) NULL,
	gAmplitude FLOAT(0) NULL,
	gPeriod FLOAT(0) NULL,
	rMag DOUBLE NULL,
	rMagErr FLOAT(0) NULL,
	rAmplitude FLOAT(0) NULL,
	rPeriod FLOAT(0) NULL,
	iMag DOUBLE NULL,
	iMagErr FLOAT(0) NULL,
	iAmplitude FLOAT(0) NULL,
	iPeriod FLOAT(0) NULL,
	zMag DOUBLE NULL,
	zMagErr FLOAT(0) NULL,
	zAmplitude FLOAT(0) NULL,
	zPeriod FLOAT(0) NULL,
	yMag DOUBLE NULL,
	yMagErr FLOAT(0) NULL,
	yAmplitude FLOAT(0) NULL,
	yPeriod FLOAT(0) NULL,
	flag INTEGER NULL,
	src01 DOUBLE NULL,
	src02 DOUBLE NULL,
	src03 DOUBLE NULL,
	src04 DOUBLE NULL,
	src05 DOUBLE NULL,
	src06 DOUBLE NULL,
	src07 DOUBLE NULL,
	src08 DOUBLE NULL,
	src09 DOUBLE NULL,
	src10 DOUBLE NULL,
	src11 DOUBLE NULL,
	src12 DOUBLE NULL,
	src13 DOUBLE NULL,
	src14 DOUBLE NULL,
	src15 DOUBLE NULL,
	src16 DOUBLE NULL,
	src17 DOUBLE NULL,
	src18 DOUBLE NULL,
	src19 DOUBLE NULL,
	src20 DOUBLE NULL,
	src21 DOUBLE NULL,
	convCode VARCHAR(8) NULL,
	o_minus_c DOUBLE NULL,
	moid1 DOUBLE NULL,
	moidLong1 DOUBLE NULL,
	moid2 DOUBLE NULL,
	moidLong2 DOUBLE NULL,
	arcLengthDays DOUBLE NULL,
	PRIMARY KEY (movingObjectId, movingObjectVersion),
	KEY (procHistoryId),
	INDEX idx_MovingObject_taxonomicTypeId (taxonomicTypeId ASC),
	INDEX idx_MovingObject_ssmId (ssmId ASC),
	INDEX idx_MovingObject_ssmObjectName (ssmObjectName ASC),
	INDEX idx_MovingObject_status (mopsStatus ASC)
) ;


CREATE TABLE Science_CCD_Exposure
(
	scienceCCDExposureId BIGINT NULL,
	scienceFPAExposureId INTEGER NULL,
	filterId TINYINT NULL,
	equinox FLOAT(0) NULL,
	url VARCHAR(255) NULL,
	ctype1 VARCHAR(20) NULL,
	ctype2 VARCHAR(20) NULL,
	crpix1 FLOAT(0) NULL,
	crpix2 FLOAT(0) NULL,
	crval1 DOUBLE NULL,
	crval2 DOUBLE NULL,
	cd1_1 DOUBLE NULL,
	cd2_1 DOUBLE NULL,
	cd1_2 DOUBLE NULL,
	cd2_2 DOUBLE NULL,
	dateObs DATETIME NULL,
	expTime FLOAT(0) NULL,
	photoFlam FLOAT(0) NULL,
	photoZP FLOAT(0) NULL,
	nCombine INTEGER NULL DEFAULT 1,
	taiMjd DOUBLE NULL,
	bixX INTEGER NULL,
	binY INTEGER NULL,
	saturationLimit BIGINT NULL,
	dataSection VARCHAR(24) NULL,
	ccdSize VARCHAR(50) NULL,
	gain DOUBLE NULL,
	readNoise DOUBLE NULL,
	PRIMARY KEY (scienceCCDExposureId),
	KEY (scienceCCDExposureId),
	KEY (scienceFPAExposureId)
) ;


CREATE TABLE Raw_CCD_Exposure
(
	rawCCDExposureId BIGINT NULL,
	rawFPAExposureId INTEGER NULL,
	procHistoryId INTEGER NULL,
	referenceRawFPAExposureId BIGINT NULL,
	filterId TINYINT NULL,
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	equinox FLOAT(0) NULL,
	url VARCHAR(255) NULL,
	ctype1 VARCHAR(20) NULL,
	ctype2 VARCHAR(20) NULL,
	crpix1 FLOAT(0) NULL,
	crpix2 FLOAT(0) NULL,
	crval1 DOUBLE NULL,
	crval2 DOUBLE NULL,
	cd11 DOUBLE NULL,
	cd21 DOUBLE NULL,
	cd12 DOUBLE NULL,
	cd22 DOUBLE NULL,
	dateObs DATETIME NULL,
	taiObs DATETIME NULL,
	mjdObs DOUBLE NULL,
	expTime FLOAT(0) NULL,
	darkTime FLOAT(0) NULL,
	zd FLOAT(0) NULL,
	airmass FLOAT(0) NULL,
	kNonGray DOUBLE NULL,
	c0 DOUBLE NULL,
	c0Err FLOAT(0) NULL,
	cx1 DOUBLE NULL,
	cx1Err FLOAT(0) NULL,
	cx2 DOUBLE NULL,
	cx2Err FLOAT(0) NULL,
	cy1 DOUBLE NULL,
	cy1Err FLOAT(0) NULL,
	cy2 DOUBLE NULL,
	cy2Err FLOAT(0) NULL,
	cxy DOUBLE NULL,
	cxyErr FLOAT(0) NULL,
	PRIMARY KEY (rawCCDExposureId),
	KEY (rawFPAExposureId),
	KEY (procHistoryId)
) ;


CREATE TABLE Raw_Amp_Exposure
(
	rawAmpExposureId BIGINT NULL,
	amplifierId SMALLINT NULL,
	rawCCDExposureId BIGINT NULL,
	procHistoryId INTEGER NULL,
	binX SMALLINT NULL,
	binY SMALLINT NULL,
	sizeX SMALLINT NULL,
	sizeY SMALLINT NULL,
	taiObs DATETIME NULL,
	expTime FLOAT(0) NULL,
	bias FLOAT(0) NULL,
	gain FLOAT(0) NULL,
	rdNoise FLOAT(0) NULL,
	telAngle FLOAT(0) NULL,
	az FLOAT(0) NULL,
	altitude FLOAT(0) NULL,
	flag SMALLINT NULL,
	zpt DOUBLE NULL,
	zptErr FLOAT(0) NULL,
	sky FLOAT(0) NULL,
	skySig FLOAT(0) NULL,
	skyErr FLOAT(0) NULL,
	psf_nstar INTEGER NULL,
	psf_apcorr FLOAT(0) NULL,
	psf_sigma1 FLOAT(0) NULL,
	psf_sigma2 FLOAT(0) NULL,
	psf_b FLOAT(0) NULL,
	psf_b_2G FLOAT(0) NULL,
	psf_p0 FLOAT(0) NULL,
	psf_beta FLOAT(0) NULL,
	psf_sigmap FLOAT(0) NULL,
	psf_nprof INTEGER NULL,
	psf_fwhm FLOAT(0) NULL,
	psf_sigma_x FLOAT(0) NULL,
	psf_sigma_y FLOAT(0) NULL,
	psf_posAngle FLOAT(0) NULL,
	psf_peak FLOAT(0) NULL,
	psf_x0 FLOAT(0) NULL,
	psf_x1 FLOAT(0) NULL,
	radesys VARCHAR(5) NULL,
	equinox FLOAT(0) NULL,
	ctype1 VARCHAR(20) NULL,
	ctype2 VARCHAR(20) NULL,
	cunit1 VARCHAR(10) NULL,
	cunit2 VARCHAR(10) NULL,
	crpix1 FLOAT(0) NULL,
	crpix2 FLOAT(0) NULL,
	crval1 FLOAT(0) NULL,
	crval2 FLOAT(0) NULL,
	cd11 FLOAT(0) NULL,
	cd12 FLOAT(0) NULL,
	cd21 FLOAT(0) NULL,
	cd22 FLOAT(0) NULL,
	cdelt1 FLOAT(0) NULL,
	cdelt2 FLOAT(0) NULL,
	PRIMARY KEY (rawAmpExposureId),
	KEY (amplifierId),
	KEY (rawCCDExposureId),
	KEY (procHistoryId)
) ;


CREATE TABLE _Science_FPA_ExposureToTemplateImage
(
	scienceFPAExposureId BIGINT NULL,
	templateImageId INTEGER NULL,
	KEY (templateImageId),
	KEY (scienceFPAExposureId)
) ;


CREATE TABLE _FPA_FringeToCMExposure
(
	biasExposureId INTEGER NULL,
	darkExposureId INTEGER NULL,
	flatExposureId INTEGER NULL,
	cmFringeExposureId INTEGER NULL,
	KEY (cmFringeExposureId),
	KEY (darkExposureId),
	KEY (flatExposureId),
	KEY (biasExposureId)
) ;


CREATE TABLE _FPA_FlatToCMExposure
(
	flatExposureId INTEGER NULL,
	biasExposureId INTEGER NULL,
	darkExposureId INTEGER NULL,
	cmFlatExposureId INTEGER NULL,
	KEY (biasExposureId),
	KEY (cmFlatExposureId),
	KEY (darkExposureId),
	KEY (flatExposureId)
) ;


CREATE TABLE _FPA_DarkToCMExposure
(
	darkExposureId INTEGER NULL,
	biasExposureId INTEGER NULL,
	cmDarkExposureId INTEGER NULL,
	KEY (cmDarkExposureId),
	KEY (darkExposureId),
	KEY (biasExposureId)
) ;


CREATE TABLE _FPA_BiasToCMExposure
(
	biasExposureId INTEGER NULL,
	cmBiasExposureId INTEGER NULL,
	KEY (cmBiasExposureId),
	KEY (biasExposureId)
) ;


CREATE TABLE prv_Snapshot
(
	snapshotId MEDIUMINT NULL,
	procHistoryId INTEGER NULL,
	snapshotDescr VARCHAR(255) NULL,
	PRIMARY KEY (snapshotId),
	KEY (procHistoryId)
) ;


CREATE TABLE prv_cnf_MaskAmpImage
(
	cMaskAmpImageId BIGINT NULL,
	amplifierId SMALLINT NULL,
	url VARCHAR(255) NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cMaskAmpImageId),
	KEY (amplifierId)
) ;


CREATE TABLE prv_cnf_Amplifier
(
	cAmplifierId SMALLINT NULL,
	amplifierId SMALLINT NULL,
	serialNumber VARCHAR(40) NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cAmplifierId),
	KEY (amplifierId)
) TYPE=MyISAM;


CREATE TABLE _aux_Science_FPA_Exposure_Group
(
	dummy INTEGER NULL
) ;


CREATE TABLE Visit
(
	visitId INTEGER NULL,
	rawFPAExposureId INTEGER NULL,
	PRIMARY KEY (visitId),
	KEY (rawFPAExposureId)
) ;


CREATE TABLE Science_FPA_Exposure
(
	scienceFPAExposureId INTEGER NULL,
	rawFPAExposureId INTEGER NULL,
	subtractedRawFPAExposureId INTEGER NULL,
	varianceRawFPAExposureId INTEGER NULL,
	cseGroupId MEDIUMINT NULL,
	PRIMARY KEY (scienceFPAExposureId),
	UNIQUE UQ_Science_FPA_Exposure_rawFPAExposureId(rawFPAExposureId),
	KEY (rawFPAExposureId),
	KEY (subtractedRawFPAExposureId),
	KEY (varianceRawFPAExposureId),
	KEY (cseGroupId)
) ;


CREATE TABLE Calibration_FPA_Exposure
(
	calibrationFPAExposureId INTEGER NULL,
	PRIMARY KEY (calibrationFPAExposureId),
	KEY (calibrationFPAExposureId)
) ;


CREATE TABLE Flat_FPA_Exposure
(
	flatExposureId INTEGER NULL,
	filterId TINYINT NULL,
	averPixelValue FLOAT(0) NULL,
	stdevPixelValue FLOAT(0) NULL,
	wavelength FLOAT(0) NULL,
	type TINYINT NULL,
	PRIMARY KEY (flatExposureId),
	KEY (flatExposureId)
) ;


CREATE TABLE Dark_FPA_Exposure
(
	darkExposureId INTEGER NULL,
	averPixelValue FLOAT(0) NULL,
	stdevPixelValue FLOAT(0) NULL,
	PRIMARY KEY (darkExposureId),
	KEY (darkExposureId)
) ;


CREATE TABLE Bias_FPA_Exposure
(
	biasExposureId INTEGER NULL,
	averPixelValue FLOAT(0) NULL,
	stdevPixelValue FLOAT(0) NULL,
	PRIMARY KEY (biasExposureId),
	KEY (biasExposureId)
) ;


CREATE TABLE mops_TrackletsToDIASource
(
	trackletId BIGINT NULL,
	diaSourceId BIGINT NULL,
	PRIMARY KEY (trackletId, diaSourceId),
	INDEX idx_mopsTrackletsToDIASource_diaSourceId (diaSourceId ASC),
	KEY (trackletId)
) ;


CREATE TABLE mops_TracksToTracklet
(
	trackId BIGINT NULL,
	trackletId BIGINT NULL,
	PRIMARY KEY (trackId, trackletId),
	INDEX idx_mopsTracksToTracklet_trackletId (trackletId ASC),
	KEY (trackId)
) ;


CREATE TABLE mops_MovingObjectToTracklet
(
	movingObjectId BIGINT NULL,
	trackletId BIGINT NULL,
	INDEX idx_mopsMovingObjectToTracklets_movingObjectId (movingObjectId ASC),
	INDEX idx_mopsMovingObjectToTracklets_trackletId (trackletId ASC)
) ;


CREATE TABLE mops_Event_TrackletRemoval
(
	eventId BIGINT NULL,
	trackletId BIGINT NULL,
	PRIMARY KEY (eventId),
	INDEX idx_mopsEventTrackletRemoval_trackletId (trackletId ASC),
	KEY (eventId)
) ;


CREATE TABLE mops_Event_TrackletPrecovery
(
	eventId BIGINT NULL,
	trackletId BIGINT NULL,
	ephemerisDistance FLOAT(0) NULL,
	ephemerisUncertainty FLOAT(0) NULL,
	PRIMARY KEY (eventId),
	INDEX idx_mopsEventTrackletPrecovery_trackletId (trackletId ASC),
	KEY (eventId)
) ;


CREATE TABLE mops_Event_TrackletAttribution
(
	eventId BIGINT NULL,
	trackletId BIGINT NULL,
	ephemerisDistance FLOAT(0) NULL,
	ephemerisUncertainty FLOAT(0) NULL,
	PRIMARY KEY (eventId),
	INDEX idx_mopsEventTrackletAttribution_trackletId (trackletId ASC),
	KEY (eventId)
) ;


CREATE TABLE mops_Event_OrbitDerivation
(
	eventId BIGINT NULL,
	trackletId BIGINT NULL,
	PRIMARY KEY (eventId, trackletId),
	INDEX idx_mopsEventDerivation_trackletId (trackletId ASC),
	KEY (eventId)
) ;


CREATE TABLE _SourceToObject
(
	objectId BIGINT NULL,
	sourceId BIGINT NULL,
	splitPercentage TINYINT NULL,
	INDEX idx_SourceToObject_objectId (objectId ASC),
	INDEX idx_SourceToObject_sourceId (sourceId ASC)
) ;


CREATE TABLE prv_ProcHistory
(
	procHistoryId INTEGER NULL,
	PRIMARY KEY (procHistoryId)
) ;


CREATE TABLE prv_cnf_CCD
(
	cCCDId SMALLINT NULL,
	ccdId SMALLINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cCCDId),
	KEY (ccdId)
) ;


CREATE TABLE prv_Amplifier
(
	amplifierId SMALLINT NULL,
	ccdId SMALLINT NULL,
	amplifierDescr VARCHAR(80) NULL,
	PRIMARY KEY (amplifierId),
	KEY (ccdId)
) ;


CREATE TABLE prv_cnf_StageToPipeline
(
	cStageToPipelineId MEDIUMINT NULL,
	stageToPipelineId MEDIUMINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cStageToPipelineId),
	KEY (stageToPipelineId)
) ;


CREATE TABLE prv_cnf_PipelineToRun
(
	cPipelineToRunId MEDIUMINT NULL,
	pipelineToRunId MEDIUMINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cPipelineToRunId),
	KEY (pipelineToRunId)
) ;


CREATE TABLE aux_Fringe_FPA_CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Flat_FPA_CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Dark_FPA_CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Bias_FPA_CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE Source
(
	sourceId BIGINT NULL,
	ampExposureId BIGINT NULL,
	filterId TINYINT NULL,
	objectId BIGINT NULL,
	movingObjectId BIGINT NULL,
	procHistoryId INTEGER NULL,
	ra DOUBLE NULL,
	raErrForDetection FLOAT(0) NULL,
	raErrForWcs FLOAT(0) NULL,
	decl DOUBLE NULL,
	declErrForDetection FLOAT(0) NULL,
	declErrForWcs FLOAT(0) NULL,
	xFlux DOUBLE NULL,
	xFluxErr FLOAT(0) NULL,
	yFlux DOUBLE NULL,
	yFluxErr FLOAT(0) NULL,
	raFlux DOUBLE NULL,
	raFluxErr FLOAT(0) NULL,
	declFlux DOUBLE NULL,
	declFluxErr FLOAT(0) NULL,
	xPeak DOUBLE NULL,
	yPeak DOUBLE NULL,
	raPeak DOUBLE NULL,
	declPeak DOUBLE NULL,
	xAstrom DOUBLE NULL,
	xAstromErr FLOAT(0) NULL,
	yAstrom DOUBLE NULL,
	yAstromErr FLOAT(0) NULL,
	raAstrom DOUBLE NULL,
	raAstromErr FLOAT(0) NULL,
	declAstrom DOUBLE NULL,
	declAstromErr FLOAT(0) NULL,
	taiMidPoint DOUBLE NULL,
	taiRange FLOAT(0) NULL,
	psfFlux DOUBLE NULL,
	psfFluxErr FLOAT(0) NULL,
	apFlux DOUBLE NULL,
	apFluxErr FLOAT(0) NULL,
	modelFlux DOUBLE NULL,
	modelFluxErr FLOAT(0) NULL,
	petroFlux DOUBLE NULL,
	petroFluxErr FLOAT(0) NULL,
	instFlux DOUBLE NULL,
	instFluxErr FLOAT(0) NULL,
	nonGrayCorrFlux DOUBLE NULL,
	nonGrayCorrFluxErr FLOAT(0) NULL,
	atmCorrFlux DOUBLE NULL,
	atmCorrFluxErr FLOAT(0) NULL,
	apDia FLOAT(0) NULL,
	Ixx FLOAT(0) NULL,
	IxxErr FLOAT(0) NULL,
	Iyy FLOAT(0) NULL,
	IyyErr FLOAT(0) NULL,
	Ixy FLOAT(0) NULL,
	IxyErr FLOAT(0) NULL,
	snr FLOAT(0) NULL,
	chi2 FLOAT(0) NULL,
	sky FLOAT(0) NULL,
	skyErr FLOAT(0) NULL,
	flagForAssociation SMALLINT NULL,
	flagForDetection SMALLINT NULL,
	flagForWcs SMALLINT NULL,
	PRIMARY KEY (sourceId),
	KEY (ampExposureId),
	KEY (filterId),
	KEY (movingObjectId),
	KEY (objectId),
	KEY (procHistoryId)
) TYPE=MyISAM;


CREATE TABLE Raw_FPA_Exposure
(
	rawFPAExposureId INTEGER NULL,
	filterId TINYINT NULL,
	procHistoryId INTEGER NULL,
	visitId INTEGER NULL,
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	obsDate DATETIME NULL,
	tai DOUBLE NULL,
	taiDark DOUBLE NULL,
	azimuth FLOAT(0) NULL,
	altitude FLOAT(0) NULL,
	temperature FLOAT(0) NULL,
	texp FLOAT(0) NULL,
	flag SMALLINT NULL,
	ra_ll DOUBLE NULL,
	dec_ll DOUBLE NULL,
	ra_lr DOUBLE NULL,
	dec_lr DOUBLE NULL,
	ra_ul DOUBLE NULL,
	dec_ul DOUBLE NULL,
	ra_ur DOUBLE NULL,
	dec_ur DOUBLE NULL,
	PRIMARY KEY (rawFPAExposureId),
	UNIQUE UQ_Raw_FPA_Exposure_visitId(visitId),
	KEY (filterId),
	KEY (procHistoryId)
) TYPE=MyISAM;


CREATE TABLE mops_Tracklet
(
	trackletId BIGINT NULL AUTO_INCREMENT,
	-- Do we need ccdExposureId?
	ccdExposureId BIGINT NULL,
	procHistoryId INT NULL,
	ssmId BIGINT NULL,
	velRa DOUBLE NULL,
	velRaErr FLOAT(0) NULL,
	velDecl DOUBLE NULL,
	velDeclErr FLOAT(0) NULL,
	velTot DOUBLE NULL,
	accRa DOUBLE NULL,
	accRaErr FLOAT(0) NULL,
	accDecl DOUBLE NULL,
	accDeclErr FLOAT(0) NULL,
	extEpoch DOUBLE NULL,
	extRa DOUBLE NULL,
	extRaErr FLOAT(0) NULL,
	extDecl DOUBLE NULL,
	extDeclErr FLOAT(0) NULL,
	extMag DOUBLE NULL,
	extMagErr FLOAT(0) NULL,
	probability DOUBLE NULL,
	status CHAR(1) NULL,
	classification CHAR(1) NULL,
	PRIMARY KEY (trackletId),
	INDEX idx_mopsTracklets_ccdExposureId (ccdExposureId ASC),
	INDEX idx_mopsTracklets_ssmId (ssmId ASC),
	INDEX idx_mopsTracklets_classification (classification ASC),
	INDEX idx_mopsTracklets_extEpoch (extEpoch ASC)
) ;


CREATE TABLE sdqa_Rating_ForScienceCCDExposure
(
	sdqa_ratingId BIGINT NULL AUTO_INCREMENT,
	sdqa_metricId SMALLINT NULL,
	sdqa_thresholdId SMALLINT NULL,
	ccdExposureId BIGINT NULL,
	metricValue DOUBLE NULL,
	metricErr FLOAT(0) NULL,
	PRIMARY KEY (sdqa_ratingId),
	UNIQUE UQ_sdqa_Rating_ForScienceCCDExposure_metricId_ccdExposureId(sdqa_metricId, ccdExposureId),
	KEY (sdqa_metricId),
	KEY (sdqa_thresholdId),
	KEY (ccdExposureId)
) ;


CREATE TABLE prv_StageToProcHistory
(
	stageId SMALLINT NULL,
	procHistoryId INTEGER NULL,
	stageStart DATETIME NULL,
	stageEnd DATETIME NULL,
	KEY (stageId),
	KEY (procHistoryId)
) ;


CREATE TABLE prv_cnf_Telescope
(
	cTelescopeId SMALLINT NULL,
	telescopeId TINYINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cTelescopeId),
	KEY (telescopeId)
) ;


CREATE TABLE prv_cnf_Raft
(
	cRaftId TINYINT NULL,
	raftId SMALLINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cRaftId),
	KEY (raftId)
) ;


CREATE TABLE prv_cnf_Filter
(
	cFilterId TINYINT NULL,
	filterId TINYINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cFilterId),
	KEY (filterId)
) ;


CREATE TABLE prv_CCD
(
	ccdId SMALLINT NULL,
	raftId SMALLINT NULL,
	amp01 SMALLINT NULL,
	amp02 SMALLINT NULL,
	amp03 SMALLINT NULL,
	amp04 SMALLINT NULL,
	amp05 SMALLINT NULL,
	amp06 SMALLINT NULL,
	amp07 SMALLINT NULL,
	amp08 SMALLINT NULL,
	amp09 SMALLINT NULL,
	amp10 SMALLINT NULL,
	PRIMARY KEY (ccdId),
	KEY (raftId)
) ;


CREATE TABLE prv_StageToUpdatableColumn
(
	stageId SMALLINT NULL,
	columnId SMALLINT NULL,
	cStageToUpdateColumnId SMALLINT NULL,
	KEY (stageId),
	KEY (columnId),
	KEY (cStageToUpdateColumnId)
) ;


CREATE TABLE prv_StageToPipeline
(
	stageToPipelineId MEDIUMINT NULL,
	pipelineId TINYINT NULL,
	stageId SMALLINT NULL,
	PRIMARY KEY (stageToPipelineId),
	KEY (pipelineId),
	KEY (stageId)
) ;


CREATE TABLE prv_PipelineToRun
(
	pipelineToRunId MEDIUMINT NULL,
	runId MEDIUMINT NULL,
	pipelineId TINYINT NULL,
	PRIMARY KEY (pipelineToRunId),
	KEY (runId),
	KEY (pipelineId)
) ;


CREATE TABLE prv_cnf_StageToSlice
(
	cStageToSliceId MEDIUMINT NULL,
	stageToSliceId MEDIUMINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cStageToSliceId),
	KEY (stageToSliceId)
) ;


CREATE TABLE prv_cnf_Slice
(
	nodeId SMALLINT NULL,
	sliceId MEDIUMINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	KEY (nodeId),
	KEY (sliceId)
) ;


CREATE TABLE prv_cnf_PolicyKey
(
	policyKeyId INTEGER NULL,
	value TEXT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (policyKeyId),
	KEY (policyKeyId)
) ;


CREATE TABLE prv_cnf_Node
(
	cNodeId INTEGER NULL,
	nodeId SMALLINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cNodeId),
	KEY (nodeId)
) ;


CREATE TABLE _aux_FPA_Fringe2CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE _aux_FPA_Flat2CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE _aux_FPA_Dark2CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE _aux_FPA_Bias2CMExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE Science_Amp_Exposure
(
	scienceAmpExposureId BIGINT NULL,
	scienceCCDExposureId BIGINT NULL,
	sdqa_imageStatusId SMALLINT NULL,
	PRIMARY KEY (scienceAmpExposureId),
	KEY (scienceAmpExposureId),
	KEY (scienceCCDExposureId),
	KEY (sdqa_imageStatusId)
) ;


CREATE TABLE _Science_FPA_Exposure_Group
(
	cseGroupId MEDIUMINT NULL,
	darkTime DATETIME NULL,
	biasTime DATETIME NULL,
	u_fringeTime DATETIME NULL,
	g_fringeTime DATETIME NULL,
	r_fringeTime DATETIME NULL,
	i_fringeTime DATETIME NULL,
	z_fringeTime DATETIME NULL,
	y_fringeTime DATETIME NULL,
	u_flatTime DATETIME NULL,
	g_flatTime DATETIME NULL,
	r_flatTime DATETIME NULL,
	i_flatTime DATETIME NULL,
	z_flatTime DATETIME NULL,
	y_flatTime DATETIME NULL,
	cmBiasExposureId INTEGER NULL,
	cmDarkExposureId INTEGER NULL,
	u_cmFlatExposureId INTEGER NULL,
	g_cmFlatExposureId INTEGER NULL,
	r_cmFlatExposureId INTEGER NULL,
	i_cmFlatExposureId INTEGER NULL,
	z_cmFlatExposureId INTEGER NULL,
	y_cmFlatExposureId INTEGER NULL,
	u_cmFringeExposureId INTEGER NULL,
	g_cmFringeExposureId INTEGER NULL,
	r_cmFringeExposureId INTEGER NULL,
	i_cmFringeExposureId INTEGER NULL,
	z_cmFringeExposureId INTEGER NULL,
	y_cmFringeExposureId INTEGER NULL,
	PRIMARY KEY (cseGroupId),
	KEY (cmBiasExposureId),
	KEY (cmDarkExposureId),
	KEY (u_cmFlatExposureId)
) ;


CREATE TABLE mops_SSM
(
	ssmId BIGINT NULL AUTO_INCREMENT,
	ssmDescId SMALLINT NULL,
	q DOUBLE NULL,
	e DOUBLE NULL,
	i DOUBLE NULL,
	node DOUBLE NULL,
	argPeri DOUBLE NULL,
	timePeri DOUBLE NULL,
	epoch DOUBLE NULL,
	h_v DOUBLE NULL,
	h_ss DOUBLE NULL,
	g DOUBLE NULL,
	albedo DOUBLE NULL,
	ssmObjectName VARBINARY(32) NULL,
	PRIMARY KEY (ssmId),
	UNIQUE UQ_mopsSSM_ssmObjectName(ssmObjectName),
	INDEX idx_mopsSSM_ssmDescId (ssmDescId ASC),
	INDEX idx_mopsSSM_epoch (epoch ASC)
) ;


CREATE TABLE sdqa_Threshold
(
	sdqa_thresholdId SMALLINT NULL AUTO_INCREMENT,
	sdqa_metricId SMALLINT NULL,
	upperThreshold DOUBLE NULL,
	lowerThreshold DOUBLE NULL,
	createdDate TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (sdqa_thresholdId),
	UNIQUE UQ_sdqa_Threshold_sdqa_metricId(sdqa_metricId),
	KEY (sdqa_metricId)
) ;


CREATE TABLE sdqa_Rating_ForScienceFPAExposure
(
	sdqa_ratingId BIGINT NULL AUTO_INCREMENT,
	sdqa_metricId SMALLINT NULL,
	sdqa_thresholdId SMALLINT NULL,
	exposureId INTEGER NULL,
	metricValue DOUBLE NULL,
	metricErr FLOAT(0) NULL,
	PRIMARY KEY (sdqa_ratingId),
	UNIQUE UQ_sdqa_Rating_ForScienceFPAExposure_metricId_exposureId(sdqa_metricId, exposureId),
	KEY (exposureId),
	KEY (sdqa_metricId),
	KEY (sdqa_thresholdId)
) ;


CREATE TABLE sdqa_Rating_ForScienceAmpExposure
(
	sdqa_ratingId BIGINT NULL AUTO_INCREMENT,
	sdqa_metricId SMALLINT NULL,
	sdqa_thresholdId SMALLINT NULL,
	ampExposureId BIGINT NULL,
	metricValue DOUBLE NULL,
	metricErr FLOAT(0) NULL,
	PRIMARY KEY (sdqa_ratingId),
	UNIQUE UQ_sdqa_Rating_ForScienceAmpExposure_metricId_ampExposureId(sdqa_metricId, ampExposureId),
	KEY (sdqa_metricId),
	KEY (sdqa_thresholdId),
	KEY (ampExposureId)
) ;


CREATE TABLE _SourceClassifToDescr
(
	scId INTEGER NULL,
	scAttrId SMALLINT NULL,
	scDescrId SMALLINT NULL,
	status BIT NULL DEFAULT 1,
	KEY (scId),
	KEY (scAttrId),
	KEY (scDescrId)
) ;


CREATE TABLE _ObjectToType
(
	objectId BIGINT NULL,
	typeId SMALLINT NULL,
	probability TINYINT NULL DEFAULT 100,
	KEY (typeId),
	KEY (objectId)
) ;


CREATE TABLE _MovingObjectToType
(
	movingObjectId BIGINT NULL,
	typeId SMALLINT NULL,
	probability TINYINT NULL DEFAULT 100,
	KEY (typeId),
	KEY (movingObjectId)
) ;


CREATE TABLE _AlertToType
(
	alertTypeId SMALLINT NULL,
	alertId INTEGER NULL,
	KEY (alertId),
	KEY (alertTypeId)
) ;


CREATE TABLE prv_UpdatableColumn
(
	columnId SMALLINT NULL,
	tableId SMALLINT NULL,
	columnName VARCHAR(64) NULL,
	PRIMARY KEY (columnId),
	KEY (tableId)
) ;


CREATE TABLE prv_Telescope
(
	telescopeId TINYINT NULL,
	focalPlaneId TINYINT NULL,
	PRIMARY KEY (telescopeId),
	KEY (focalPlaneId)
) ;


CREATE TABLE prv_Raft
(
	raftId SMALLINT NULL,
	focalPlaneId TINYINT NULL,
	ccd01 SMALLINT NULL,
	ccd02 SMALLINT NULL,
	ccd03 SMALLINT NULL,
	ccd04 SMALLINT NULL,
	ccd05 SMALLINT NULL,
	ccd06 SMALLINT NULL,
	ccd07 SMALLINT NULL,
	ccd08 SMALLINT NULL,
	ccd09 SMALLINT NULL,
	PRIMARY KEY (raftId),
	KEY (focalPlaneId)
) ;


CREATE TABLE prv_Filter
(
	filterId TINYINT NULL,
	focalPlaneId TINYINT NULL,
	name VARCHAR(80) NULL,
	url VARCHAR(255) NULL,
	clam FLOAT(0) NULL,
	bw FLOAT(0) NULL,
	PRIMARY KEY (filterId),
	UNIQUE name(name),
	INDEX focalPlaneId (focalPlaneId ASC)
) TYPE=MyISAM;


CREATE TABLE prv_cnf_FocalPlane
(
	cFocalPlaneId SMALLINT NULL,
	focalPlaneId TINYINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cFocalPlaneId),
	KEY (focalPlaneId)
) ;


CREATE TABLE prv_StageToSlice
(
	stageToSliceId MEDIUMINT NULL,
	stageId SMALLINT NULL,
	sliceId MEDIUMINT NULL,
	PRIMARY KEY (stageToSliceId),
	KEY (stageId),
	KEY (sliceId)
) ;


CREATE TABLE prv_Stage
(
	stageId SMALLINT NULL,
	policyId MEDIUMINT NULL,
	stageName VARCHAR(255) NULL,
	PRIMARY KEY (stageId),
	KEY (policyId)
) ;


CREATE TABLE prv_Run
(
	runId MEDIUMINT NULL,
	policyId MEDIUMINT NULL,
	PRIMARY KEY (runId),
	KEY (policyId)
) ;


CREATE TABLE prv_PolicyKey
(
	policyKeyId INTEGER NULL,
	policyFileId INTEGER NULL,
	keyName VARCHAR(255) NULL,
	keyType VARCHAR(16) NULL,
	PRIMARY KEY (policyKeyId),
	KEY (policyFileId)
) ;


CREATE TABLE prv_Pipeline
(
	pipelineId TINYINT NULL,
	policyId MEDIUMINT NULL,
	pipelineName VARCHAR(64) NULL,
	PRIMARY KEY (pipelineId),
	KEY (policyId)
) ;


CREATE TABLE prv_Node
(
	nodeId SMALLINT NULL,
	policyId MEDIUMINT NULL,
	PRIMARY KEY (nodeId),
	KEY (policyId)
) ;


CREATE TABLE prv_cnf_SoftwarePackage
(
	packageId INTEGER NULL,
	version VARCHAR(255) NULL,
	directory VARCHAR(255) NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (packageId),
	KEY (packageId)
) ;


CREATE TABLE prv_cnf_Policy
(
	cPolicyId MEDIUMINT NULL,
	policyId MEDIUMINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (cPolicyId),
	KEY (policyId)
) ;


CREATE TABLE aux_Source
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_IR_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Science_FPA_SpectraExposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Flat_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Dark_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Calibration_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Bias_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE TemplateImage
(
	templateImageId INTEGER NULL,
	PRIMARY KEY (templateImageId)
) ;


CREATE TABLE PostageStampJpegs
(
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	sizeRa FLOAT(0) NULL,
	sizeDecl FLOAT(0) NULL,
	url VARCHAR(255) NULL
) ;


CREATE TABLE Fringe_FPA_CMExposure
(
	cdFringeExposureId INTEGER NULL,
	PRIMARY KEY (cdFringeExposureId)
) ;


CREATE TABLE Flat_FPA_CMExposure
(
	cmFlatExposureId INTEGER NULL,
	PRIMARY KEY (cmFlatExposureId)
) ;


CREATE TABLE Dark_FPA_CMExposure
(
	cmDarkExposureId INTEGER NULL,
	PRIMARY KEY (cmDarkExposureId)
) ;


CREATE TABLE CalibType
(
	calibTypeId TINYINT NULL,
	descr VARCHAR(255) NULL,
	PRIMARY KEY (calibTypeId)
) ;


CREATE TABLE Bias_FPA_CMExposure
(
	cmBiasExposureId INTEGER NULL,
	PRIMARY KEY (cmBiasExposureId)
) ;


CREATE TABLE mops_SSMDesc
(
	ssmDescId SMALLINT NULL AUTO_INCREMENT,
	prefix CHAR(4) NULL,
	description VARCHAR(100) NULL,
	PRIMARY KEY (ssmDescId)
) ;


CREATE TABLE _tmpl_mops_Prediction
(
	movingObjectId BIGINT NULL,
	movingObjectVersion INTEGER NULL,
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	mjd DOUBLE NULL,
	smia DOUBLE NULL,
	smaa DOUBLE NULL,
	pa DOUBLE NULL,
	mag DOUBLE NULL,
	magErr FLOAT(0) NULL
) TYPE=MyISAM;


CREATE TABLE _tmpl_mops_Ephemeris
(
	movingObjectId BIGINT NULL,
	movingObjectVersion INTEGER NULL,
	ra DOUBLE NULL,
	decl DOUBLE NULL,
	mjd DOUBLE NULL,
	smia DOUBLE NULL,
	smaa DOUBLE NULL,
	pa DOUBLE NULL,
	mag DOUBLE NULL,
	INDEX idx_mopsEphemeris_movingObjectId (movingObjectId ASC)
) TYPE=MyISAM;


CREATE TABLE _mops_Config
(
	configId BIGINT NULL AUTO_INCREMENT,
	configText TEXT NULL,
	PRIMARY KEY (configId)
) ;


CREATE TABLE sdqa_Metric
(
	sdqa_metricId SMALLINT NULL AUTO_INCREMENT,
	metricName VARCHAR(30) NULL,
	physicalUnits VARCHAR(30) NULL,
	dataType CHAR(1) NULL,
	definition VARCHAR(255) NULL,
	PRIMARY KEY (sdqa_metricId),
	UNIQUE UQ_sdqa_Metric_metricName(metricName)
) ;


CREATE TABLE sdqa_ImageStatus
(
	sdqa_imageStatusId SMALLINT NULL AUTO_INCREMENT,
	statusName VARCHAR(30) NULL,
	definition VARCHAR(255) NULL,
	PRIMARY KEY (sdqa_imageStatusId)
) ;


CREATE TABLE SourceClassifDescr
(
	scDescrId SMALLINT NULL,
	scDescr VARCHAR(255) NULL,
	PRIMARY KEY (scDescrId)
) ;


CREATE TABLE SourceClassifAttr
(
	scAttrId SMALLINT NULL,
	scAttrDescr VARCHAR(255) NULL,
	PRIMARY KEY (scAttrId)
) ;


CREATE TABLE SourceClassif
(
	scId INTEGER NULL,
	PRIMARY KEY (scId)
) ;


CREATE TABLE ObjectType
(
	typeId SMALLINT NULL,
	description VARCHAR(255) NULL,
	PRIMARY KEY (typeId)
) ;


CREATE TABLE DIASourceIDTonight
(
	DIASourceId BIGINT NULL
) ;


CREATE TABLE AlertType
(
	alertTypeId SMALLINT NULL,
	alertTypeDescr VARCHAR(50) NULL,
	PRIMARY KEY (alertTypeId)
) TYPE=MyISAM;


CREATE TABLE _tmpl_MatchPair
(
	first BIGINT NULL,
	second BIGINT NULL,
	distance DOUBLE NULL
) ;


CREATE TABLE _tmpl_IdPair
(
	first BIGINT NULL,
	second BIGINT NULL
) ;


CREATE TABLE _tmpl_Id
(
	id BIGINT NULL
) ;


CREATE TABLE prv_UpdatableTable
(
	tableId SMALLINT NULL,
	tableName VARCHAR(64) NULL,
	PRIMARY KEY (tableId)
) ;


CREATE TABLE prv_FocalPlane
(
	focalPlaneId TINYINT NULL,
	PRIMARY KEY (focalPlaneId)
) ;


CREATE TABLE prv_SoftwarePackage
(
	packageId INTEGER NULL,
	packageName VARCHAR(64) NULL,
	PRIMARY KEY (packageId)
) ;


CREATE TABLE prv_Slice
(
	sliceId MEDIUMINT NULL,
	PRIMARY KEY (sliceId)
) ;


CREATE TABLE prv_PolicyFile
(
	policyFileId INTEGER NULL,
	pathName VARCHAR(255) NULL,
	hashValue CHAR(32) NULL,
	modifiedDate BIGINT NULL,
	PRIMARY KEY (policyFileId)
) ;


CREATE TABLE prv_Policy
(
	policyId MEDIUMINT NULL,
	policyName VARCHAR(80) NULL,
	PRIMARY KEY (policyId)
) ;


CREATE TABLE prv_cnf_StageToUpdatableColumn
(
	c_stageToUpdatableColumn SMALLINT NULL,
	validityBegin DATETIME NULL,
	validityEnd DATETIME NULL,
	PRIMARY KEY (c_stageToUpdatableColumn)
) ;


CREATE TABLE placeholder_SQLLog
(
	sqlLogId BIGINT NULL,
	tstamp DATETIME NULL,
	elapsed FLOAT(0) NULL,
	userId INTEGER NULL,
	domain VARCHAR(80) NULL,
	ipaddr VARCHAR(80) NULL,
	query TEXT NULL,
	PRIMARY KEY (sqlLogId)
) TYPE=MyISAM;


CREATE TABLE placeholder_Source
(
	moment0 FLOAT(0) NULL,
	moment1_x FLOAT(0) NULL,
	moment1_y FLOAT(0) NULL,
	moment2_xx FLOAT(0) NULL,
	moment2_xy FLOAT(0) NULL,
	moment2_yy FLOAT(0) NULL,
	moment3_xxx FLOAT(0) NULL,
	moment3_xxy FLOAT(0) NULL,
	moment3_xyy FLOAT(0) NULL,
	moment3_yyy FLOAT(0) NULL,
	moment4_xxxx FLOAT(0) NULL,
	moment4_xxxy FLOAT(0) NULL,
	moment4_xxyy FLOAT(0) NULL,
	moment4_xyyy FLOAT(0) NULL,
	moment4_yyyy FLOAT(0) NULL
) ;


CREATE TABLE placeholder_Object
(
	uScalegram01 FLOAT(0) NULL,
	uScalegram02 FLOAT(0) NULL,
	uScalegram03 FLOAT(0) NULL,
	uScalegram04 FLOAT(0) NULL,
	uScalegram05 FLOAT(0) NULL,
	uScalegram06 FLOAT(0) NULL,
	uScalegram07 FLOAT(0) NULL,
	uScalegram08 FLOAT(0) NULL,
	uScalegram09 FLOAT(0) NULL,
	uScalegram10 FLOAT(0) NULL,
	uScalegram11 FLOAT(0) NULL,
	uScalegram12 FLOAT(0) NULL,
	uScalegram13 FLOAT(0) NULL,
	uScalegram14 FLOAT(0) NULL,
	uScalegram15 FLOAT(0) NULL,
	uScalegram16 FLOAT(0) NULL,
	uScalegram17 FLOAT(0) NULL,
	uScalegram18 FLOAT(0) NULL,
	uScalegram19 FLOAT(0) NULL,
	uScalegram20 FLOAT(0) NULL,
	uScalegram21 FLOAT(0) NULL,
	uScalegram22 FLOAT(0) NULL,
	uScalegram23 FLOAT(0) NULL,
	uScalegram24 FLOAT(0) NULL,
	uScalegram25 FLOAT(0) NULL,
	gScalegram01 FLOAT(0) NULL,
	gScalegram02 FLOAT(0) NULL,
	gScalegram03 FLOAT(0) NULL,
	gScalegram04 FLOAT(0) NULL,
	gScalegram05 FLOAT(0) NULL,
	gScalegram06 FLOAT(0) NULL,
	gScalegram07 FLOAT(0) NULL,
	gScalegram08 FLOAT(0) NULL,
	gScalegram09 FLOAT(0) NULL,
	gScalegram10 FLOAT(0) NULL,
	gScalegram11 FLOAT(0) NULL,
	gScalegram12 FLOAT(0) NULL,
	gScalegram13 FLOAT(0) NULL,
	gScalegram14 FLOAT(0) NULL,
	gScalegram15 FLOAT(0) NULL,
	gScalegram16 FLOAT(0) NULL,
	gScalegram17 FLOAT(0) NULL,
	gScalegram18 FLOAT(0) NULL,
	gScalegram19 FLOAT(0) NULL,
	gScalegram20 FLOAT(0) NULL,
	gScalegram21 FLOAT(0) NULL,
	gScalegram22 FLOAT(0) NULL,
	gScalegram23 FLOAT(0) NULL,
	gScalegram24 FLOAT(0) NULL,
	gScalegram25 FLOAT(0) NULL,
	rScalegram01 FLOAT(0) NULL,
	rScalegram02 FLOAT(0) NULL,
	rScalegram03 FLOAT(0) NULL,
	rScalegram04 FLOAT(0) NULL,
	rScalegram05 FLOAT(0) NULL,
	rScalegram06 FLOAT(0) NULL,
	rScalegram07 FLOAT(0) NULL,
	rScalegram08 FLOAT(0) NULL,
	rScalegram09 FLOAT(0) NULL,
	rScalegram10 FLOAT(0) NULL,
	rScalegram11 FLOAT(0) NULL,
	rScalegram12 FLOAT(0) NULL,
	rScalegram13 FLOAT(0) NULL,
	rScalegram14 FLOAT(0) NULL,
	rScalegram15 FLOAT(0) NULL,
	rScalegram16 FLOAT(0) NULL,
	rScalegram17 FLOAT(0) NULL,
	rScalegram18 FLOAT(0) NULL,
	rScalegram19 FLOAT(0) NULL,
	rScalegram20 FLOAT(0) NULL,
	rScalegram21 FLOAT(0) NULL,
	rScalegram22 FLOAT(0) NULL,
	rScalegram23 FLOAT(0) NULL,
	rScalegram24 FLOAT(0) NULL,
	rScalegram25 FLOAT(0) NULL,
	iScalegram01 FLOAT(0) NULL,
	iScalegram02 FLOAT(0) NULL,
	iScalegram03 FLOAT(0) NULL,
	iScalegram04 FLOAT(0) NULL,
	iScalegram05 FLOAT(0) NULL,
	iScalegram06 FLOAT(0) NULL,
	iScalegram07 FLOAT(0) NULL,
	iScalegram08 FLOAT(0) NULL,
	iScalegram09 FLOAT(0) NULL,
	iScalegram10 FLOAT(0) NULL,
	iScalegram11 FLOAT(0) NULL,
	iScalegram12 FLOAT(0) NULL,
	iScalegram13 FLOAT(0) NULL,
	iScalegram14 FLOAT(0) NULL,
	iScalegram15 FLOAT(0) NULL,
	iScalegram16 FLOAT(0) NULL,
	iScalegram17 FLOAT(0) NULL,
	iScalegram18 FLOAT(0) NULL,
	iScalegram19 FLOAT(0) NULL,
	iScalegram20 FLOAT(0) NULL,
	iScalegram21 FLOAT(0) NULL,
	iScalegram22 FLOAT(0) NULL,
	iScalegram23 FLOAT(0) NULL,
	iScalegram24 FLOAT(0) NULL,
	iScalegram25 FLOAT(0) NULL,
	zScalegram01 FLOAT(0) NULL,
	zScalegram02 FLOAT(0) NULL,
	zScalegram03 FLOAT(0) NULL,
	zScalegram04 FLOAT(0) NULL,
	zScalegram05 FLOAT(0) NULL,
	zScalegram06 FLOAT(0) NULL,
	zScalegram07 FLOAT(0) NULL,
	zScalegram08 FLOAT(0) NULL,
	zScalegram09 FLOAT(0) NULL,
	zScalegram10 FLOAT(0) NULL,
	zScalegram11 FLOAT(0) NULL,
	zScalegram12 FLOAT(0) NULL,
	zScalegram13 FLOAT(0) NULL,
	zScalegram14 FLOAT(0) NULL,
	zScalegram15 FLOAT(0) NULL,
	zScalegram16 FLOAT(0) NULL,
	zScalegram17 FLOAT(0) NULL,
	zScalegram18 FLOAT(0) NULL,
	zScalegram19 FLOAT(0) NULL,
	zScalegram20 FLOAT(0) NULL,
	zScalegram21 FLOAT(0) NULL,
	zScalegram22 FLOAT(0) NULL,
	zScalegram23 FLOAT(0) NULL,
	zScalegram24 FLOAT(0) NULL,
	zScalegram25 FLOAT(0) NULL,
	yScalegram01 FLOAT(0) NULL,
	yScalegram02 FLOAT(0) NULL,
	yScalegram03 FLOAT(0) NULL,
	yScalegram04 FLOAT(0) NULL,
	yScalegram05 FLOAT(0) NULL,
	yScalegram06 FLOAT(0) NULL,
	yScalegram07 FLOAT(0) NULL,
	yScalegram08 FLOAT(0) NULL,
	yScalegram09 FLOAT(0) NULL,
	yScalegram10 FLOAT(0) NULL,
	yScalegram11 FLOAT(0) NULL,
	yScalegram12 FLOAT(0) NULL,
	yScalegram13 FLOAT(0) NULL,
	yScalegram14 FLOAT(0) NULL,
	yScalegram15 FLOAT(0) NULL,
	yScalegram16 FLOAT(0) NULL,
	yScalegram17 FLOAT(0) NULL,
	yScalegram18 FLOAT(0) NULL,
	yScalegram19 FLOAT(0) NULL,
	yScalegram20 FLOAT(0) NULL,
	yScalegram21 FLOAT(0) NULL,
	yScalegram22 FLOAT(0) NULL,
	yScalegram23 FLOAT(0) NULL,
	yScalegram24 FLOAT(0) NULL,
	yScalegram25 FLOAT(0) NULL
) ;


CREATE TABLE placeholder_Alert
(
	__voEventId BIGINT NULL
) ;


CREATE TABLE aux_Object
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_SED
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_LIDARshot
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_FPA_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_CloudMap
(
	dummy INTEGER NULL
) ;


CREATE TABLE aux_Amp_Exposure
(
	dummy INTEGER NULL
) ;


CREATE TABLE _aux_Science_FPA_SpectraExposure_Group
(
	dummy INTEGER NULL
) ;


