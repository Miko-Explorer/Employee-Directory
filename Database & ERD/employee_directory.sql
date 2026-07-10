#Create database for employee directory:
CREATE DATABASE employee_db; 

#Use database as a default schema:
USE employee_db; 

#User employee table management:
CREATE TABLE users(
	user_id INT AUTO_INCREMENT PRIMARY KEY, 
  user_name VARCHAR(100) NOT NULL UNIQUE, 
  email VARCHAR(100) NOT NULL UNIQUE, 
  password_hash VARCHAR(255) NOT NULL, 
  salt VARCHAR(64) NOT NULL, 
  first_name VARCHAR(100) NOT NULL, 
  last_name VARCHAR(100) NOT NULL, 
  phone_number VARCHAR(20) NOT NULL, 
  profile_picture_url VARCHAR(2048) NOT NULL, 
  status VARCHAR(20) NOT NULL, 
  last_login_ip VARCHAR(45) DEFAULT NULL, 
  last_login_at DATETIME DEFAULT NULL, 
		CONSTRAINT chk_last_login_users 
    CHECK(last_login_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
  created_at DATETIME NOT NULL, 
		CONSTRAINT chk_created_at_users 
    CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
  updated_at DATETIME NOT NULL, 
		CONSTRAINT chk_updated_at_users 
    CHECK(updated_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'),
  deleted_at DATETIME DEFAULT NULL, 
		CONSTRAINT chk_deleted_at_users 
		CHECK(deleted_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee roles table management:
CREATE TABLE roles(
	role_id INT AUTO_INCREMENT PRIMARY KEY, 
  role_name VARCHAR(50) NOT NULL, 
  description VARCHAR(200) DEFAULT NULL, 
  created_at DATETIME NOT NULL, 
		CONSTRAINT chk_created_at_roles 
    CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
  updated_at DATETIME NOT NULL, 
		CONSTRAINT chk_updated_at_roles 
    CHECK(updated_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee permissions table management:
CREATE TABLE permissions(
 permission_id INT AUTO_INCREMENT PRIMARY KEY, 
 permission_name VARCHAR(100) NOT NULL, 
 resource VARCHAR(100) NOT NULL, 
 action VARCHAR(50) NOT NULL, 
 description VARCHAR(200) DEFAULT NULL, 
 created_at DATETIME NOT NULL, 
	CONSTRAINT chk_created_at_permissions 
  CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee user-roles table management:
CREATE TABLE user_roles(
 user_id INT NOT NULL, 
 role_id INT NOT NULL, 
	PRIMARY KEY (user_id, role_id), 
	FOREIGN KEY(user_id) 
	REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
	FOREIGN KEY(role_id) 
	REFERENCES roles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
 assigned_at DATETIME NOT NULL, 
	CONSTRAINT chk_assigned_at_user_roles 
  CHECK(assigned_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
 assigned_by INT NOT NULL, 
	FOREIGN KEY(assigned_by) 
	REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
); 

#Employee permission roles table management:
CREATE TABLE role_permissions(
 role_id INT NOT NULL,
  PRIMARY KEY (role_id, permission_id), 
  FOREIGN KEY(role_id) 
	REFERENCES roles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
 permission_id INT NOT NULL, 
  FOREIGN KEY(permission_id) 
	REFERENCES permissions(permission_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
 assigned_at DATETIME NOT NULL, 
	CONSTRAINT chk_assigned_at_role_permissions 
	CHECK(assigned_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee sessions table management:
CREATE TABLE sessions(
	session_id INT AUTO_INCREMENT PRIMARY KEY, 
  user_id INT NOT NULL, 
		FOREIGN KEY(user_id) 
		REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  session_token VARCHAR(255) NOT NULL, 
  ip_address VARCHAR(45) NOT NULL, 
  user_agent VARCHAR(255) NOT NULL, 
  expires_at DATETIME NOT NULL,
		CONSTRAINT chk_expires_at_sessions 
    CHECK(expires_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
  created_at DATETIME NOT NULL,
		CONSTRAINT chk_created_at_sessions 
    CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee user password reset table management:
CREATE TABLE password_resets(
 reset_id INT AUTO_INCREMENT PRIMARY KEY, 
 user_id INT NOT NULL, 
	FOREIGN KEY(user_id) 
  REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
 token VARCHAR(255) NOT NULL UNIQUE,
 expires_at DATETIME NOT NULL, 
 used_at DATETIME DEFAULT NULL, 
 created_at DATETIME NOT NULL
); 

#Employee email verification table management:
CREATE TABLE email_verifications(
	verification_id INT AUTO_INCREMENT PRIMARY KEY, 
  user_id INT NOT NULL, 
		FOREIGN KEY(user_id) 
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  token VARCHAR(255) NOT NULL UNIQUE, 
  verified_at DATETIME DEFAULT NULL, 
		CONSTRAINT chk_verified_at_email_verif 
    CHECK(verified_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'), 
  expires_at DATETIME NOT NULL, 
		CONSTRAINT chk_expires_at_email_verif 
    CHECK(expires_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59'),
  created_at DATETIME NOT NULL, 
		CONSTRAINT chk_created_at_email_verif 
    CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee audit logs table management; 
CREATE TABLE audit_logs(
	log_id INT AUTO_INCREMENT PRIMARY KEY, 
  user_id INT DEFAULT NULL, 
		FOREIGN KEY(user_id) 
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  action VARCHAR(50) NOT NULL, 
  table_name VARCHAR(100) DEFAULT NULL, 
  record_id INT DEFAULT NULL, 
  old_values JSON DEFAULT NULL, 
  new_values JSON DEFAULT NULL, 
  ip_address VARCHAR(45) NOT NULL, 
  user_agent VARCHAR(255) NOT NULL, 
  created_at DATETIME NOT NULL, 
		CONSTRAINT chk_created_at_audit_logs 
    CHECK(created_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#Employee system settings table management:
CREATE TABLE system_settings(
	setting_id INT AUTO_INCREMENT PRIMARY KEY, 
  setting_key VARCHAR(100) NOT NULL UNIQUE, 
  setting_value TEXT NOT NULL, 
  category VARCHAR(50) NOT NULL, 
  description VARCHAR(200) DEFAULT NULL, 
  updated_at DATETIME NOT NULL, 
		CONSTRAINT chk_updated_at_sys_settings 
    CHECK(updated_at BETWEEN '1000-01-01 00:00:00' AND '9999-12-31 23:59:59')
); 

#==============================#

#Display all tables:
SELECT * FROM users; 
SELECT * FROM roles; 
SELECT * FROM permissions; 
SELECT * FROM user_roles; 
SELECT * FROM role_permissions; 
SELECT * FROM sessions; 
SELECT * FROM password_resets; 
SELECT * FROM email_verifications; 
SELECT * FROM audit_logs; 
SELECT * FROM system_settings;