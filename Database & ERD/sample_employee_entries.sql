-- ============================================================
-- SAMPLE DATA (10 ENTRIES PER TABLE)
-- Designed for testing Aggregations, Filters & Combined Analysis
-- All constraints (FKs, UNIQUE, CHECK) are respected.
-- Run this AFTER your schema creation script.
-- ============================================================

-- ============================================================
-- 1. ROLES (10 entries)
-- ============================================================
INSERT INTO roles (role_id, role_name, description, created_at, updated_at) VALUES
(1, 'Admin', 'Full system access with all permissions', '2025-01-15 09:00:00', '2026-06-28 10:00:00'),
(2, 'Manager', 'Can approve requests and manage team members', '2025-02-20 10:00:00', '2026-06-28 10:00:00'),
(3, 'Employee', 'Standard user access', '2025-03-10 11:30:00', '2026-06-28 10:00:00'),
(4, 'HR Specialist', 'Manages employee records and onboarding', '2025-04-05 08:15:00', '2026-06-28 10:00:00'),
(5, 'Payroll Officer', 'Handles salary and compensation data', '2025-05-12 13:45:00', '2026-06-28 10:00:00'),
(6, 'IT Support', 'Manages system access and technical issues', '2025-06-18 09:30:00', '2026-06-28 10:00:00'),
(7, 'Department Head', 'Oversees departmental operations', '2025-07-22 14:00:00', '2026-06-28 10:00:00'),
(8, 'Recruiter', 'Manages hiring and candidate pipelines', '2025-08-14 10:30:00', '2026-06-28 10:00:00'),
(9, 'Compliance Officer', 'Ensures policy adherence and audits', '2025-09-05 08:00:00', '2026-06-28 10:00:00'),
(10, 'Intern', 'Limited access for training purposes', '2025-10-10 11:00:00', '2026-06-28 10:00:00');

-- ============================================================
-- 2. PERMISSIONS (10 entries)
-- ============================================================
INSERT INTO permissions (permission_id, permission_name, resource, action, description, created_at) VALUES
(1, 'view_users', 'users', 'view', 'Can view user profiles', '2026-01-15 09:00:00'),
(2, 'create_users', 'users', 'create', 'Can create new user accounts', '2026-01-15 09:00:00'),
(3, 'edit_users', 'users', 'edit', 'Can edit user details', '2026-01-15 09:00:00'),
(4, 'delete_users', 'users', 'delete', 'Can delete user accounts', '2026-01-15 09:00:00'),
(5, 'view_roles', 'roles', 'view', 'Can view role definitions', '2026-01-15 09:00:00'),
(6, 'edit_roles', 'roles', 'edit', 'Can modify role definitions', '2026-01-15 09:00:00'),
(7, 'view_reports', 'reports', 'view', 'Can view system reports', '2026-01-15 09:00:00'),
(8, 'export_reports', 'reports', 'export', 'Can export reports', '2026-01-15 09:00:00'),
(9, 'view_settings', 'settings', 'view', 'Can view system settings', '2026-01-15 09:00:00'),
(10, 'edit_settings', 'settings', 'edit', 'Can modify system settings', '2026-01-15 09:00:00');

-- ============================================================
-- 3. USERS (10 entries) – Includes Active, Suspended, Locked, Soft-Deleted
-- ============================================================
INSERT INTO users (
    user_id, user_name, email, password_hash, salt, first_name, last_name, 
    phone_number, profile_picture_url, status, last_login_ip, last_login_at, 
    created_at, updated_at, deleted_at
) VALUES
(1, 'jdoe', 'john.doe@company.com', 'hash_12345', 'salt_abc123', 'John', 'Doe', 
 '09171234567', 'https://cdn.company.com/avatars/jdoe.jpg', 'active', '192.168.1.100', '2026-06-25 08:30:00', 
 '2025-01-15 09:00:00', '2026-06-28 10:00:00', NULL),

(2, 'jsmith', 'jane.smith@company.com', 'hash_67890', 'salt_def456', 'Jane', 'Smith', 
 '09171234568', 'https://cdn.company.com/avatars/jsmith.jpg', 'active', '192.168.1.101', '2026-06-25 09:15:00', 
 '2025-02-20 10:00:00', '2026-06-28 10:00:00', NULL),

(3, 'mjohnson', 'mike.johnson@company.com', 'hash_11111', 'salt_ghi789', 'Mike', 'Johnson', 
 '09171234569', 'https://cdn.company.com/avatars/mjohnson.jpg', 'active', '192.168.1.102', '2026-06-24 16:45:00', 
 '2025-03-10 11:30:00', '2026-06-28 10:00:00', NULL),

(4, 'swilliams', 'sarah.williams@company.com', 'hash_22222', 'salt_jkl012', 'Sarah', 'Williams', 
 '09171234570', 'https://cdn.company.com/avatars/swilliams.jpg', 'active', '192.168.1.103', '2026-06-24 14:20:00', 
 '2025-04-05 08:15:00', '2026-06-28 10:00:00', NULL),

(5, 'rbrown', 'robert.brown@company.com', 'hash_33333', 'salt_mno345', 'Robert', 'Brown', 
 '09171234571', 'https://cdn.company.com/avatars/rbrown.jpg', 'suspended', '192.168.1.104', '2026-06-23 11:30:00', 
 '2025-05-12 13:45:00', '2026-06-28 10:00:00', NULL),

(6, 'ldavis', 'linda.davis@company.com', 'hash_44444', 'salt_pqr678', 'Linda', 'Davis', 
 '09171234572', 'https://cdn.company.com/avatars/ldavis.jpg', 'active', '192.168.1.105', '2026-06-25 10:00:00', 
 '2025-06-18 09:30:00', '2026-06-28 10:00:00', NULL),

(7, 'pwilson', 'paul.wilson@company.com', 'hash_55555', 'salt_stu901', 'Paul', 'Wilson', 
 '09171234573', 'https://cdn.company.com/avatars/pwilson.jpg', 'active', '192.168.1.106', '2026-06-22 08:45:00', 
 '2025-07-22 14:00:00', '2026-06-28 10:00:00', NULL),

(8, 'mmartinez', 'maria.martinez@company.com', 'hash_66666', 'salt_vwx234', 'Maria', 'Martinez', 
 '09171234574', 'https://cdn.company.com/avatars/mmartinez.jpg', 'active', '192.168.1.107', '2026-06-25 11:20:00', 
 '2025-08-14 10:30:00', '2026-06-28 10:00:00', NULL),

(9, 'jtaylor', 'james.taylor@company.com', 'hash_77777', 'salt_yza567', 'James', 'Taylor', 
 '09171234575', 'https://cdn.company.com/avatars/jtaylor.jpg', 'suspended', '192.168.1.108', '2026-06-21 09:00:00', 
 '2025-09-05 08:00:00', '2026-06-28 10:00:00', '2026-06-28 10:00:00'),

(10, 'awilson', 'amy.wilson@company.com', 'hash_88888', 'salt_bcd890', 'Amy', 'Wilson', 
 '09171234576', 'https://cdn.company.com/avatars/awilson.jpg', 'locked', '192.168.1.109', '2026-06-24 15:30:00', 
 '2025-10-10 11:00:00', '2026-06-28 10:00:00', '2026-06-28 10:00:00');

-- ============================================================
-- 4. USER_ROLES (10 entries) – Repeating roles (multiple Employees)
-- ============================================================
INSERT INTO user_roles (user_id, role_id, assigned_at, assigned_by) VALUES
(1, 1, '2026-01-15 09:00:00', 1),   -- John Doe → Admin
(2, 3, '2026-01-15 09:00:00', 1),   -- Jane Smith → Employee (Repeating)
(3, 2, '2026-01-15 09:00:00', 1),   -- Mike Johnson → Manager
(4, 3, '2026-01-15 09:00:00', 2),   -- Sarah Williams → Employee (Repeating)
(5, 3, '2026-01-15 09:00:00', 2),   -- Robert Brown → Employee (Repeating)
(6, 4, '2026-01-15 09:00:00', 3),   -- Linda Davis → HR Specialist
(7, 5, '2026-01-15 09:00:00', 3),   -- Paul Wilson → Payroll Officer
(8, 6, '2026-01-15 09:00:00', 1),   -- Maria Martinez → IT Support
(9, 3, '2026-01-15 09:00:00', 1),   -- James Taylor → Employee (Soft-deleted)
(10, 10, '2026-01-15 09:00:00', 6); -- Amy Wilson → Intern (Locked)

-- ============================================================
-- 5. ROLE_PERMISSIONS (10 entries) – Admin gets all 10 permissions
-- ============================================================
INSERT INTO role_permissions (role_id, permission_id, assigned_at) VALUES
(1, 1, '2026-01-15 09:00:00'),
(1, 2, '2026-01-15 09:00:00'),
(1, 3, '2026-01-15 09:00:00'),
(1, 4, '2026-01-15 09:00:00'),
(1, 5, '2026-01-15 09:00:00'),
(1, 6, '2026-01-15 09:00:00'),
(1, 7, '2026-01-15 09:00:00'),
(1, 8, '2026-01-15 09:00:00'),
(1, 9, '2026-01-15 09:00:00'),
(1, 10, '2026-01-15 09:00:00');

-- ============================================================
-- 6. SESSIONS (10 entries) – Multiple sessions per user (Repeating)
--    User 1: 4 sessions, User 2: 3, User 3: 2, User 4: 1
-- ============================================================
INSERT INTO sessions (user_id, session_token, ip_address, user_agent, expires_at, created_at) VALUES
-- User 1 (jdoe) – 4 sessions
(1, 'sess_a1b2c3d4e5f6g7h8i9j0', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-21 09:30:00', '2026-06-20 09:30:00'),
(1, 'sess_k1l2m3n4o5p6q7r8s9t0', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-23 14:15:00', '2026-06-22 14:15:00'),
(1, 'sess_u1v2w3x4y5z6a7b8c9d0', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-25 08:00:00', '2026-06-24 08:00:00'),
(1, 'sess_e1f2g3h4i5j6k7l8m9n0', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-26 17:30:00', '2026-06-25 17:30:00'),

-- User 2 (jsmith) – 3 sessions
(2, 'sess_o1p2q3r4s5t6u7v8w9x0', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-06-22 11:20:00', '2026-06-21 11:20:00'),
(2, 'sess_y1z2a3b4c5d6e7f8g9h0', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-06-24 09:45:00', '2026-06-23 09:45:00'),
(2, 'sess_i1j2k3l4m5n6o7p8q9r0', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-06-26 13:10:00', '2026-06-25 13:10:00'),

-- User 3 (mjohnson) – 2 sessions
(3, 'sess_s1t2u3v4w5x6y7z8a9b0', '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', '2026-06-25 09:00:00', '2026-06-24 09:00:00'),
(3, 'sess_c1d2e3f4g5h6i7j8k9l0', '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', '2026-06-25 18:30:00', '2026-06-24 18:30:00'),

-- User 4 (swilliams) – 1 session
(4, 'sess_m1n2o3p4q5r6s7t8u9v0', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', '2026-06-24 10:30:00', '2026-06-23 10:30:00');

-- ============================================================
-- 7. PASSWORD_RESETS (10 entries) – Repeating users (User 1 & 3 have 2 each)
-- ============================================================
INSERT INTO password_resets (user_id, token, expires_at, used_at, created_at) VALUES
-- User 1 (jdoe) – 2 resets
(1, 'reset_a1b2c3d4e5f6g7h8i9', '2026-06-20 10:00:00', '2026-06-20 09:30:00', '2026-06-20 09:00:00'),
(1, 'reset_x1y2z3a4b5c6d7e8f9g0', '2026-06-22 10:00:00', NULL, '2026-06-22 09:00:00'),

-- User 2 (jsmith) – 1 reset
(2, 'reset_j0k1l2m3n4o5p6q7r8', '2026-06-21 15:00:00', NULL, '2026-06-21 14:00:00'),

-- User 3 (mjohnson) – 2 resets
(3, 'reset_s9t0u1v2w3x4y5z6a7', '2026-06-22 09:00:00', '2026-06-22 08:15:00', '2026-06-22 08:00:00'),
(3, 'reset_h1i2j3k4l5m6n7o8p9q0', '2026-06-24 09:00:00', '2026-06-24 08:45:00', '2026-06-24 08:00:00'),

-- User 4 (swilliams) – 1 reset
(4, 'reset_b8c9d0e1f2g3h4i5j6', '2026-06-23 12:00:00', NULL, '2026-06-23 11:00:00'),

-- User 5 (rbrown) – 1 reset
(5, 'reset_k7l8m9n0o1p2q3r4s5', '2026-06-24 17:00:00', NULL, '2026-06-24 16:00:00'),

-- User 6 (ldavis) – 1 reset
(6, 'reset_t6u5v4w3x2y1z0a9b8', '2026-06-25 11:00:00', '2026-06-25 10:20:00', '2026-06-25 10:00:00'),

-- User 7 (pwilson) – 1 reset
(7, 'reset_c7d8e9f0g1h2i3j4k5', '2026-06-26 10:00:00', NULL, '2026-06-26 09:00:00'),

-- User 8 (mmartinez) – 1 reset
(8, 'reset_l6m7n8o9p0q1r2s3t4', '2026-06-27 15:00:00', '2026-06-27 14:30:00', '2026-06-27 14:00:00');

-- ============================================================
-- 8. EMAIL_VERIFICATIONS (10 entries) – Repeating users (User 2 & 5 have 2 each)
-- ============================================================
INSERT INTO email_verifications (user_id, token, verified_at, expires_at, created_at) VALUES
-- User 1 (jdoe) – 1 verification
(1, 'verif_a1b2c3d4e5f6g7h8i9', '2026-06-20 09:30:00', '2026-06-21 09:00:00', '2026-06-20 09:00:00'),

-- User 2 (jsmith) – 2 verifications
(2, 'verif_j0k1l2m3n4o5p6q7r8', NULL, '2026-06-22 14:00:00', '2026-06-21 14:00:00'),
(2, 'verif_r1s2t3u4v5w6x7y8z9a0', NULL, '2026-06-25 14:00:00', '2026-06-24 14:00:00'),

-- User 3 (mjohnson) – 1 verification
(3, 'verif_s9t0u1v2w3x4y5z6a7', '2026-06-22 08:15:00', '2026-06-23 08:00:00', '2026-06-22 08:00:00'),

-- User 4 (swilliams) – 1 verification
(4, 'verif_b8c9d0e1f2g3h4i5j6', NULL, '2026-06-24 11:00:00', '2026-06-23 11:00:00'),

-- User 5 (rbrown) – 2 verifications
(5, 'verif_k7l8m9n0o1p2q3r4s5', NULL, '2026-06-25 16:00:00', '2026-06-24 16:00:00'),
(5, 'verif_v1w2x3y4z5a6b7c8d9e0', '2026-06-26 16:00:00', '2026-06-27 16:00:00', '2026-06-26 16:00:00'),

-- User 6 (ldavis) – 1 verification
(6, 'verif_t6u5v4w3x2y1z0a9b8', '2026-06-25 10:20:00', '2026-06-26 10:00:00', '2026-06-25 10:00:00'),

-- User 7 (pwilson) – 1 verification
(7, 'verif_c7d8e9f0g1h2i3j4k5', NULL, '2026-06-27 09:00:00', '2026-06-26 09:00:00'),

-- User 8 (mmartinez) – 1 verification
(8, 'verif_l6m7n8o9p0q1r2s3t4', '2026-06-27 14:30:00', '2026-06-28 14:00:00', '2026-06-27 14:00:00');

-- ============================================================
-- 9. AUDIT_LOGS (10 entries) – Repeating LOGINs (User 1, 2, 3)
-- ============================================================
INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent, created_at) VALUES
-- LOGIN actions (6 entries – repeating)
(1, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-20 09:30:00'),
(1, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-22 08:00:00'),

(2, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-06-21 11:20:00'),
(2, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-06-24 13:10:00'),

(3, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', '2026-06-24 09:00:00'),
(3, 'LOGIN', NULL, NULL, NULL, NULL, '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', '2026-06-24 18:30:00'),

-- UPDATE actions (2 entries)
(4, 'UPDATE', 'users', 2, '{"phone_number": "09171234568"}', '{"phone_number": "09171234599"}', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', '2026-06-23 10:30:00'),
(6, 'UPDATE', 'users', 3, '{"status": "active"}', '{"status": "suspended"}', '192.168.1.105', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-24 16:00:00'),

-- CREATE action (1 entry)
(1, 'CREATE', 'users', 11, NULL, '{"first_name": "Chris", "last_name": "Anderson"}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2026-06-22 08:00:00'),

-- DELETE action (1 entry)
(3, 'DELETE', 'sessions', 5, '{"session_id": 5, "user_id": 5}', NULL, '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', '2026-06-23 11:20:00');

-- ============================================================
-- 10. SYSTEM_SETTINGS (10 entries) – Diverse Categories
-- ============================================================
INSERT INTO system_settings (setting_key, setting_value, category, description, updated_at) VALUES
('site_name', 'Acme Employee Directory', 'general', 'The name of the application', '2026-06-20 09:00:00'),
('maintenance_mode', 'false', 'general', 'Enable/disable maintenance mode (true/false)', '2026-06-20 09:00:00'),
('max_login_attempts', '5', 'security', 'Maximum number of failed login attempts before lockout', '2026-06-21 09:00:00'),
('session_timeout_minutes', '60', 'security', 'Session expiry time in minutes', '2026-06-21 09:00:00'),
('password_min_length', '8', 'security', 'Minimum required password length', '2026-06-22 09:00:00'),
('require_special_chars', 'true', 'security', 'Require special characters in passwords', '2026-06-22 09:00:00'),
('smtp_host', 'smtp.gmail.com', 'email', 'SMTP server hostname for outgoing emails', '2026-06-23 09:00:00'),
('smtp_port', '587', 'email', 'SMTP server port number', '2026-06-23 09:00:00'),
('sender_email', 'noreply@company.com', 'email', 'Default sender email address', '2026-06-24 09:00:00'),
('max_upload_size_mb', '10', 'storage', 'Maximum file upload size in megabytes', '2026-06-24 09:00:00');