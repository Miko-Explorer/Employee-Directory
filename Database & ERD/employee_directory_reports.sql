#USER DEMOGRAPHICS STATISICS
#Count users by account status: 
CREATE VIEW report_1 
AS SELECT 
	U.status AS Status, 
  COUNT(U.user_id) AS User_count
FROM users AS U
WHERE U.deleted_at IS NULL
GROUP BY Status
ORDER BY User_count DESC; 

#Count users by registration month:
CREATE VIEW report_2
AS SELECT
	DATE_FORMAT(U.created_at, '%M') AS Month, 
  COUNT(U.user_id) AS User_count
FROM users AS U
WHERE U.deleted_at IS NULL
GROUP BY Month
ORDER BY User_count DESC; 

#Count users by registration year:
CREATE VIEW report_3
AS SELECT
	DATE_FORMAT(U.created_at, '%Y') AS Year, 
  COUNT(U.user_id) AS User_count
FROM users AS U
WHERE U.deleted_at IS NULL
GROUP BY Year
ORDER BY User_count DESC; 

#Count users with VS. without soft-delete:
CREATE VIEW report_4
AS SELECT 
	SUM(CASE WHEN U.deleted_at IS NULL THEN 1 ELSE 0 END) AS Without_soft_delete, 
  SUM(CASE WHEN U.deleted_at IS NOT NULL THEN 1 ELSE 0 END) AS With_soft_delete
FROM users AS U;

#SESSION & ACTIVITY METRICS:
#Count total sessions created per day:
CREATE VIEW report_5
AS SELECT
	DATE_FORMAT(S.created_at, '%m/%d') AS Day, 
  COUNT(S.user_id) AS User_count
FROM sessions AS S
INNER JOIN
 users AS U ON S.user_id = U.user_id
WHERE U.deleted_at IS NULL
GROUP BY Day
ORDER BY User_count DESC; 

#Count total sessions created per month:
CREATE VIEW report_6
AS SELECT
	DATE_FORMAT(S.created_at, '%M') AS Month, 
  COUNT(S.user_id) AS User_count
FROM sessions AS S
INNER JOIN
 users AS U ON S.user_id = U.user_id
WHERE U.deleted_at IS NULL
GROUP BY Month
ORDER BY User_count DESC; 

#Count sessions per user:
CREATE VIEW report_7
AS SELECT
	S.user_id AS User_id, 
  U.user_name AS Username,
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname,
  DATE_FORMAT(S.created_at, '%m/%d') AS Date, 
  COUNT(S.session_id) AS Session_count
FROM sessions AS S
INNER JOIN
	users AS U ON S.user_id = U.user_id
WHERE U.deleted_at IS NULL
GROUP BY User_id, Username, Date
ORDER BY Session_count DESC; 

#Average sessions per user:
CREATE VIEW report_8
AS SELECT 
	r7.User_id, 
  r7.Username,
  r7.Fullname,
  AVG(r7.Session_count) AS Average_session_count
FROM report_7 AS r7
GROUP BY r7.User_id, r7.Username
ORDER BY Average_session_count DESC; 

#Count active and expired sessions:
CREATE VIEW report_9
AS SELECT 
	SUM(CASE WHEN S.expires_at >= NOW() THEN 1 ELSE 0 END) AS Active_sessions_count, 
  SUM(CASE WHEN S.expires_at < NOW() THEN 1 ELSE 0 END) AS Expired_sessions_count
FROM sessions as S; 

#Most common IP address:
CREATE VIEW report_10
AS SELECT
	S.ip_address As IP_address, 
  COUNT(S.user_id) AS User_count
FROM sessions AS S
INNER JOIN 
 users AS U ON S.user_id = U.user_id
WHERE U.deleted_at IS NULL
GROUP BY IP_address
ORDER BY User_count DESC; 

#==============================#

#ROLE & PERMISSION DISTRIBUTION:
#Count users per role:
CREATE VIEW report_11
AS SELECT
	R.role_name AS Roles, 
  COUNT(UR.user_id) AS User_count
FROM roles AS R
INNER JOIN
	user_roles AS UR ON R.role_id = UR.role_id
INNER JOIN
	users AS U ON U.user_id = UR.user_id
WHERE U.deleted_at IS NULL
GROUP BY Roles
ORDER BY User_count DESC; 

#Count permissions per role:
CREATE VIEW report_12
AS SELECT
	R.role_id AS Role_id,
	R.role_name AS Roles, 
  COUNT(RP.permission_id) AS Permission_count
FROM role_permissions AS RP
INNER JOIN
 roles AS R ON RP.role_id = R.role_id
GROUP BY Role_id, Roles
ORDER BY Permission_count DESC; 

#List of roles with no users:
CREATE VIEW report_13
AS SELECT
	R.role_name AS Roles, 
  COUNT(UR.user_id) AS User_count
FROM roles AS R
LEFT JOIN
	user_roles AS UR ON R.role_id = UR.role_id
GROUP BY Roles
HAVING User_count = 0;

#==============================#

#AUDIT LOG ANALYTICS:
#Count actions by operation type:
CREATE VIEW report_14
AS SELECT
	AL.action AS Operation_type, 
  COUNT(AL.log_id) AS Action_count
FROM audit_logs AS AL
GROUP BY Operation_type
ORDER BY Action_count DESC; 

#Count actions per user:
CREATE VIEW report_15
AS SELECT
	AL.user_id as User_id,
  U.user_name as Username,
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname,
  COUNT(AL.action) AS Action_count
FROM audit_logs AS AL
INNER JOIN
	users AS U ON AL.user_id = U.user_id
WHERE U.deleted_at IS NULL
GROUP BY User_id
ORDER BY Action_count DESC;  

#Count actions per affected table:
CREATE VIEW report_16
AS SELECT 
	AL.table_name AS Table_name, 
  COUNT(AL.action) AS Action_count
FROM audit_logs AS AL
GROUP BY Table_name
ORDER BY Action_count DESC; 

#Daily audit log volume per table:
CREATE VIEW report_17
AS SELECT
	DATE_FORMAT(AL.created_at, '%m/%d') AS Date, 
  AL.table_name AS Table_name,
  COUNT(AL.created_at) AS Audit_log_volume
FROM audit_logs AS AL
GROUP BY Date, Table_name
ORDER BY Audit_log_volume DESC; 

#Daily audit log volumne (total):
CREATE VIEW report_18
AS SELECT
	DATE_FORMAT(AL.created_at, '%m/%d') AS Date, 
  COUNT(AL.created_at) AS Audit_log_volume
FROM audit_logs AS AL
GROUP BY Date
ORDER BY Audit_log_volume DESC; 

#==============================#

#USER FILTERS:
#User filter by status:
CREATE VIEW report_19
AS SELECT
	U.user_id AS User_id, 
  U.user_name AS Username,
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname,
  CASE 
		WHEN U.status = 'active' THEN 'YES'
    WHEN U.status != 'active' THEN 'NO'
	END AS Is_user_active
FROM users AS U
WHERE U.deleted_at IS NULL; 

#User filter by soft-delete status:
CREATE VIEW report_20
AS SELECT
	U.user_id AS User_id, 
  U.user_name AS Username, 
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname, 
  CASE
		WHEN U.deleted_at IS NOT NULL THEN 'User account deleted'
    WHEN U.deleted_at IS NULL THEN 'User account still active or existing'
	END AS Soft_delete_status
FROM users as U;

#User filter by date range (users registered in the last 30 days):
CREATE VIEW report_21
AS SELECT 
	U.user_id AS User_id, 
  U.user_name AS Username, 
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname, 
  CASE 
		WHEN DATEDIFF(NOW(), U.created_at) >= 30 THEN 'YES'
    WHEN DATEDIFF(NOW(), U.created_at) < 30 THEN 'NO'
	END AS Registered_last_30_days
FROM users AS U
WHERE U.deleted_at IS NULL; 

#==============================#

#COMBINED ANALYSIS:
#Count logins per user per day:
CREATE VIEW report_22
AS SELECT
	AL.user_id AS User_id,
  U.user_name AS Username,
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname,
  DATE_FORMAT(AL.created_at, '%m/%d/%y') AS Date, 
  AL.action AS Action, 
  COUNT(AL.action) AS Total_logins_per_day_per_user
FROM audit_logs AS AL
INNER JOIN
	users AS U ON AL.user_id = U.user_id
WHERE AL.action = 'LOGIN'
	AND U.deleted_at IS NULL
GROUP BY User_id, Username, Fullname, Date, Action
ORDER BY Total_logins_per_day_per_user DESC; 
  
#Count users per role, but only users that have logged in for the last 30 days:
CREATE VIEW report_23
AS SELECT
	R.role_id AS Role_id,
  R.role_name AS Roles, 
  COUNT(AL.action) AS User_count_last_loggin_for_last_30days
FROM roles AS R
INNER JOIN 
	user_roles AS UR ON UR.role_id = R.role_id
INNER JOIN 
	audit_logs AS AL ON UR.user_id = AL.user_id
INNER JOIN
	users AS U ON AL.user_id = U.user_id
WHERE AL.created_at 
	BETWEEN DATE_SUB(AL.created_at, INTERVAL DAY(AL.created_at) - 1 DAY) 
	AND LAST_DAY(AL.created_at) 
  AND AL.action = 'LOGIN'
  AND U.deleted_at IS NULL
GROUP BY Role_id, Roles
ORDER BY User_count_last_loggin_for_last_30days DESC; 

#Count audit actions by type made by an Admin:
CREATE VIEW report_24
AS SELECT
	R.role_id AS Role_id,
  R.role_name AS Roles, 
  U.user_id AS User_id, 
  CONCAT(U.first_name, ' ', U.last_name) AS Fullname, 
  COUNT(AL.action) as Total_actions
FROM roles AS R
INNER JOIN
	user_roles AS UR ON UR.role_id = R.role_id
INNER JOIN
	users AS U ON UR.user_id = U.user_id
INNER JOIN
 audit_logs AS AL ON AL.user_id = U.user_id
WHERE UR.user_id = 1
GROUP BY Role_id, Roles, User_id, Fullname
ORDER BY Total_actions DESC; 

#Count sessions per IP address having more than 50 session (to detect possible bots):
CREATE VIEW report_25
AS SELECT
	S.ip_address AS IP_address, 
  COUNT(S.session_id) AS Suspicious_session_count
FROM sessions AS S
GROUP BY IP_address
HAVING COUNT(S.session_id) > 50
ORDER BY Suspicious_session_count DESC;  

#Count soft-deleted users per role:
CREATE VIEW report_26
AS SELECT 
	R.role_id AS Role_id, 
  R.role_name AS Roles, 
  COUNT(U.user_id) AS User_count_with_soft_delete_per_role
FROM roles AS R
INNER JOIN
	user_roles AS UR ON UR.role_id = R.role_id
INNER JOIN
	users AS U ON UR.user_id = U.user_id
WHERE U.deleted_at IS NOT NULL
GROUP BY Role_id, Roles
ORDER BY User_count_with_soft_delete_per_role DESC;  

#==============================#

#Display all reports:
SELECT * FROM report_1; 
SELECT * FROM report_2; 
SELECT * FROM report_3; 
SELECT * FROM report_4; 
SELECT * FROM report_5;
SELECT * FROM report_6; 
SELECT * FROM report_7; 
SELECT * FROM report_8;
SELECT * FROM report_9; 
SELECT * FROM report_10; 
SELECT * FROM report_11;
SELECT * FROM report_12; 
SELECT * FROM report_13; 
SELECT * FROM report_14;
SELECT * FROM report_15; 
SELECT * FROM report_16; 
SELECT * FROM report_17;
SELECT * FROM report_18;
SELECT * FROM report_19; 
SELECT * FROM report_20;
SELECT * FROM report_21; 
SELECT * FROM report_22; 
SELECT * FROM report_23; 
SELECT * FROM report_24; 
SELECT * FROM report_25; 
SELECT * FROM report_26;