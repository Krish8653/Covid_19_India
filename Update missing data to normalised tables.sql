USE [COVID_19]
GO

--UPDATING MISSING DATA FROM MOHFW TO NORMALISED TABLES

INSERT INTO STATE(STATE)
SELECT State FROM MOHFW WHERE State NOT IN (SELECT DISTINCT State FROM STATE);

INSERT INTO DATE(DATE)
SELECT DISTINCT DATE FROM MOHFW WHERE DATE NOT IN (SELECT DISTINCT (DATE) FROM DATE);

INSERT INTO CONFIRMED_CASES
(CON_DATE_ID
,CON_STATE_ID
,CONFIRMED_CASES)
SELECT
D.DATE_ID
,S.STATE_ID
,CONFIRMED_CASES_ON_THIS_DAY
FROM MOHFW M
JOIN STATE S ON M.STATE = S.STATE
JOIN DATE D ON M.DATE = D.DATE
WHERE D.DATE_ID NOT IN (SELECT DISTINCT (CON_DATE_ID) FROM CONFIRMED_CASES);

INSERT INTO CURED_CASES
(CUR_DATE_ID
,CUR_STATE_ID
,CURED_CASES)
SELECT
D.DATE_ID
,S.STATE_ID
,Recovered_cases_on_this_day
FROM MOHFW M
JOIN STATE S ON M.STATE = S.STATE
JOIN DATE D ON M.DATE = D.DATE
WHERE D.DATE_ID NOT IN (SELECT DISTINCT (CUR_DATE_ID) FROM CURED_CASES);

INSERT INTO DEATH_CASES
(DEATH_DATE_ID
,DEATH_STATE_ID
,DEATH_CASES)
SELECT
D.DATE_ID
,S.STATE_ID
,Death_cases_on_this_day
FROM MOHFW M
JOIN STATE S ON M.STATE = S.STATE
JOIN DATE D ON M.DATE = D.DATE
WHERE D.DATE_ID NOT IN (SELECT DISTINCT (DEATH_DATE_ID) FROM DEATH_CASES);


INSERT INTO ACTIVE_CASES
(ACT_DATE_ID
,ACT_STATE_ID
,ACTIVE_CASES)
SELECT
D.DATE_ID
,S.STATE_ID
,(C.CONFIRMED_CASES - (CU.CURED_CASES + DE.DEATH_CASES))
FROM MOHFW M
JOIN STATE S ON M.STATE = S.STATE
JOIN DATE D ON M.DATE = D.DATE
JOIN CONFIRMED_CASES C ON CON_DATE_ID = D.DATE_ID AND CON_STATE_ID = S.STATE_ID
JOIN CURED_CASES CU ON CUR_DATE_ID = D.DATE_ID AND CUR_STATE_ID = S.STATE_ID
JOIN DEATH_CASES DE ON DEATH_DATE_ID = D.DATE_ID AND DEATH_STATE_ID = S.STATE_ID
WHERE D.DATE_ID NOT IN (SELECT DISTINCT (ACT_DATE_ID) FROM ACTIVE_CASES);
GO


--UPDATE MOHFW
--SET  Confirmed_cases_on_this_day = Total_Confirmed
--	,Recovered_cases_on_this_day = Total_Cured
--	,Death_cases_on_this_day = Total_Death
--WHERE Confirmed_cases_on_this_day IS NULL
