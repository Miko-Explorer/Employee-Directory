# Employee Directory

- A Streamlit + MySQL app for managing employees, roles, permissions, sessions, and audit logs.
- Features a dark navy-themed UI with glassmorphism accents for enterprise directory management.

---

## Table of Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Quick start](#quick-start)
- [Database setup](#database-setup)
- [Database schema](#database-schema)
- [SQL views (reporting)](#sql-views-reporting)
- [Application modules](#application-modules)
- [UI / UX](#ui--ux)
- [Security](#security)
- [Development & testing](#development--testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User management** — create, edit, soft-delete, restore employees with salted password hashing
- **Role-based access control (RBAC)** — define roles and permissions, assign roles to users, map permissions to roles
- **Session tracking** — monitor active/expired sessions per user with IP and user agent details
- **Password reset & email verification** — generate and validate tokens with configurable expiry windows
- **Audit logging** — record every CREATE, UPDATE, DELETE, and LOGIN action with old/new JSON values
- **System settings** — key-value application settings grouped by category (general, security, email, storage)
- **26 pre-built SQL views** — user demographics, session metrics, role distribution, audit analytics, and combined analysis
- **Dashboard** — 5 essential KPIs (Total Users, Active Roles, Permissions, Active Sessions, Events Today) with two bar charts
- **Dark navy theme** — animated gradient background, frosted-glass headers, styled tables with alternating rows, custom SVG logo

---

## Tech stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Web framework | Streamlit 1.28+ |
| Data manipulation | pandas 1.5+ |
| DB connector | mysql-connector-python 8.0+ |
| Database server | MySQL 8.0+ |
| UI styling | Custom CSS (navy palette + glassmorphism) |

See `requirements.txt` for pinned versions.

---

## Project structure

```
Employee Directory/
├─ .gitignore                      # Ignores secrets, cache, venvs, IDE files
├─ .streamlit/
│  └─ secrets.toml                 # MySQL credentials (git-ignored)
├─ Data Dictionary/
│  ├─ Data Dictionary (PDF ver.).pdf   # Schema reference (PDF)
│  └─ Data Dictionary (Sheet ver.).xlsx # Schema reference (Excel)
├─ Database & ERD/
│  ├─ ERD_employee_db.mwb          # MySQL Workbench model
│  ├─ ERD_employee_db.pdf          # ERD diagram (PDF)
│  ├─ employee_directory.sql       # DB + 10 tables DDL
│  ├─ employee_directory_reports.sql # 26 reporting views
│  └─ sample_employee_entries.sql  # 50 sample rows per table
├─ audit_logs.py                   # Audit trail recording and retrieval
├─ database.py                     # DB connection + run_query() / run_many()
├─ email_verifications.py          # Email verification token workflow
├─ main.py                         # App entry, CSS theme, routing (12 pages)
├─ password_resets.py              # Password reset token workflow
├─ permissions.py                  # Permission CRUD
├─ README.md                       # This file
├─ requirements.txt                # Python dependencies
├─ role_permissions.py             # Role-permission mapping
├─ roles.py                        # Role CRUD
├─ sessions.py                     # Session management
├─ system_settings.py              # System settings CRUD
├─ user_roles.py                   # User-role assignment
└─ users.py                        # User CRUD with password hashing
```

---

## Quick start

- **Clone the repo:**
  ```bash
  git clone https://github.com/your-username/employee-directory.git
  cd employee-directory
  ```

- **Set up a virtual environment and install deps:**
  ```bash
  python -m venv .venv
  source .venv/bin/activate        # Linux/macOS
  .venv\Scripts\activate           # Windows
  pip install -r requirements.txt
  ```

- **Configure `.streamlit/secrets.toml`** with MySQL credentials:
  ```toml
  [mysql]
  host = "localhost"
  user = "your_user"
  password = "your_password"
  database = "employee_db"
  port = 3306
  ```
  > Never commit this file — it's in `.gitignore`.

- **Run database scripts** (see [Database setup](#database-setup)).

- **Launch the app:**
  ```bash
  streamlit run main.py
  ```
  Open `http://localhost:8501`.

---

## Database setup

- Scripts live in `Database & ERD/`.
- **Run in order:**

  1. **Create database and tables:**
     ```bash
     mysql -u your_user -p < "Database & ERD/employee_directory.sql"
     ```
     Creates `employee_db` and 10 tables (`users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `sessions`, `password_resets`, `email_verifications`, `audit_logs`, `system_settings`) with foreign keys and CHECK constraints.

  2. **Insert sample data (optional):**
     ```bash
     mysql -u your_user -p employee_db < "Database & ERD/sample_employee_entries.sql"
     ```
      Populates 50 sample rows per table for testing.

  3. **Create reporting views:**
     ```bash
     mysql -u your_user -p employee_db < "Database & ERD/employee_directory_reports.sql"
     ```
     Creates 26 views consumed by the Reports page.

- Alternatively, execute the SQL files in MySQL Workbench or any MySQL client.

---

## Database schema

### `users` table

| Column | Type | Constraints |
|---|---|---|
| `user_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `user_name` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `email` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` |
| `salt` | `VARCHAR(64)` | `NOT NULL` |
| `first_name` | `VARCHAR(100)` | `NOT NULL` |
| `last_name` | `VARCHAR(100)` | `NOT NULL` |
| `phone_number` | `VARCHAR(20)` | `NOT NULL` |
| `profile_picture_url` | `VARCHAR(2048)` | `NOT NULL` |
| `status` | `VARCHAR(20)` | `NOT NULL` |
| `last_login_ip` | `VARCHAR(45)` | `DEFAULT NULL` |
| `last_login_at` | `DATETIME` | `DEFAULT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |
| `updated_at` | `DATETIME` | `NOT NULL` |
| `deleted_at` | `DATETIME` | `DEFAULT NULL` (soft-delete) |

### `roles` table

| Column | Type | Constraints |
|---|---|---|
| `role_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `role_name` | `VARCHAR(50)` | `NOT NULL` |
| `description` | `VARCHAR(200)` | `DEFAULT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |
| `updated_at` | `DATETIME` | `NOT NULL` |

### `permissions` table

| Column | Type | Constraints |
|---|---|---|
| `permission_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `permission_name` | `VARCHAR(100)` | `NOT NULL` |
| `resource` | `VARCHAR(100)` | `NOT NULL` |
| `action` | `VARCHAR(50)` | `NOT NULL` |
| `description` | `VARCHAR(200)` | `DEFAULT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |

### `user_roles` table

| Column | Type | Constraints |
|---|---|---|
| `user_id` | `INT` | `PK`, `FK → users(user_id) ON DELETE RESTRICT` |
| `role_id` | `INT` | `PK`, `FK → roles(role_id) ON DELETE RESTRICT` |
| `assigned_at` | `DATETIME` | `NOT NULL` |
| `assigned_by` | `INT` | `NOT NULL`, `FK → users(user_id)` |

### `role_permissions` table

| Column | Type | Constraints |
|---|---|---|
| `role_id` | `INT` | `PK`, `FK → roles(role_id) ON DELETE RESTRICT` |
| `permission_id` | `INT` | `PK`, `FK → permissions(permission_id) ON DELETE RESTRICT` |
| `assigned_at` | `DATETIME` | `NOT NULL` |

### `sessions` table

| Column | Type | Constraints |
|---|---|---|
| `session_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `user_id` | `INT` | `FK → users(user_id) ON DELETE CASCADE` |
| `session_token` | `VARCHAR(255)` | `NOT NULL` |
| `ip_address` | `VARCHAR(45)` | `NOT NULL` |
| `user_agent` | `VARCHAR(255)` | `NOT NULL` |
| `expires_at` | `DATETIME` | `NOT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |

### `password_resets` table

| Column | Type | Constraints |
|---|---|---|
| `reset_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `user_id` | `INT` | `FK → users(user_id) ON DELETE CASCADE` |
| `token` | `VARCHAR(255)` | `NOT NULL`, `UNIQUE` |
| `expires_at` | `DATETIME` | `NOT NULL` |
| `used_at` | `DATETIME` | `DEFAULT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |

### `email_verifications` table

| Column | Type | Constraints |
|---|---|---|
| `verification_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `user_id` | `INT` | `FK → users(user_id) ON DELETE CASCADE` |
| `token` | `VARCHAR(255)` | `NOT NULL`, `UNIQUE` |
| `verified_at` | `DATETIME` | `DEFAULT NULL` |
| `expires_at` | `DATETIME` | `NOT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |

### `audit_logs` table

| Column | Type | Constraints |
|---|---|---|
| `log_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `user_id` | `INT` | `FK → users(user_id) ON DELETE CASCADE` |
| `action` | `VARCHAR(50)` | `NOT NULL` |
| `table_name` | `VARCHAR(100)` | `DEFAULT NULL` |
| `record_id` | `INT` | `DEFAULT NULL` |
| `old_values` | `JSON` | `DEFAULT NULL` |
| `new_values` | `JSON` | `DEFAULT NULL` |
| `ip_address` | `VARCHAR(45)` | `NOT NULL` |
| `user_agent` | `VARCHAR(255)` | `NOT NULL` |
| `created_at` | `DATETIME` | `NOT NULL` |

### `system_settings` table

| Column | Type | Constraints |
|---|---|---|
| `setting_id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` |
| `setting_key` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `setting_value` | `TEXT` | `NOT NULL` |
| `category` | `VARCHAR(50)` | `NOT NULL` |
| `description` | `VARCHAR(200)` | `DEFAULT NULL` |
| `updated_at` | `DATETIME` | `NOT NULL` |

---

## SQL views (reporting)

`employee_directory_reports.sql` creates 26 views across 6 categories:

### User Demographics

| View | Description |
|---|---|
| `report_1` | Count users by account status |
| `report_2` | Count users by registration month |
| `report_3` | Count users by registration year |
| `report_4` | Count users with vs. without soft-delete |

### Session & Activity Metrics

| View | Description |
|---|---|
| `report_5` | Total sessions created per day |
| `report_6` | Total sessions created per month |
| `report_7` | Sessions per user per day |
| `report_8` | Average sessions per user |
| `report_9` | Count active and expired sessions |
| `report_10` | Most common IP addresses |

### Role & Permission Distribution

| View | Description |
|---|---|
| `report_11` | Count users per role |
| `report_12` | Count permissions per role |
| `report_13` | List roles with no users |

### Audit Log Analytics

| View | Description |
|---|---|
| `report_14` | Count actions by operation type |
| `report_15` | Count actions per user |
| `report_16` | Count actions per affected table |
| `report_17` | Daily audit log volume per table |
| `report_18` | Daily audit log volume (total) |

### User Filters

| View | Description |
|---|---|
| `report_19` | Users filtered by account status |
| `report_20` | Users filtered by soft-delete status |
| `report_21` | Users registered in the last 30 days |

### Combined Analysis

| View | Description |
|---|---|
| `report_22` | Logins per user per day |
| `report_23` | Users per role with login in last 30 days |
| `report_24` | Audit actions by Admin (user_id = 1) |
| `report_25` | Suspicious IPs with more than 50 sessions |
| `report_26` | Soft-deleted users per role |

- All views can be run from the Reports page with CSV export.

---

## Application modules

| Module | File | Role |
|---|---|---|
| **Entry point** | `main.py` | Page config, dark navy CSS theme, SVG logo sidebar, radio navigation across 12 pages, Dashboard with 5 KPIs and two bar charts |
| **Database layer** | `database.py` | `get_connection()` + `run_query()` / `run_many()` — parameterized MySQL executor returning dicts or row count |
| **User management** | `users.py` | Full CRUD, search/filter, soft-delete/restore, password hashing with SHA-256 + salt |
| **Role management** | `roles.py` | Role CRUD |
| **Permission management** | `permissions.py` | Permission CRUD scoped by resource and action |
| **User-role assignment** | `user_roles.py` | Assign/remove roles, list available roles per user, unassigned users query |
| **Role-permission mapping** | `role_permissions.py` | Assign/remove permissions to roles, list available permissions per role |
| **Session management** | `sessions.py` | Create sessions with tokens, list active/all, expire manually, cleanup expired |
| **Password resets** | `password_resets.py` | Generate reset tokens, validate expiry/usage, mark as used |
| **Email verifications** | `email_verifications.py` | Generate verification tokens, mark as verified, validate expiry |
| **Audit logging** | `audit_logs.py` | Log actions with old/new JSON, retrieve by user/action/table/date range |
| **System settings** | `system_settings.py` | Key-value settings CRUD with category grouping |

---

## UI / UX

- **Dark navy theme** — animated gradient background (`#1d243c`, `#252d4a`, `#2a314e`), frosted-glass headers, solid metric cards with subtle shadows
- **Color palette** — `#1d243c` (background/sidebar), `#2a314e` (cards/inputs), `#5a5f7a` (borders/buttons), `#898da5` (muted text/charts), `#e7e9fb` (primary text)
- **Sidebar** — `#1d243c` backdrop, centered "Directory" SVG logo with gradient, hidden-label radio nav across 12 pages
- **Tables** — alternating row backgrounds (`#2a314e` / `#252d4a`), `#1d243c` header with uppercase white text, hover highlight
- **Interactions** — slate button hover glow, `st.rerun()` on CRUD mutations for instant refresh, toast messages for success/error/info
- **Dashboard** — 5 solid-metric KPIs in a single row, two side-by-side bar charts (user status distribution, users per role), recent audit log table

---

## Security

- **Password storage** — `password_hash` + `salt` columns use SHA-256 hashing. Upgrade to bcrypt/Argon2 before production deployment.
- **Secrets** — `.streamlit/secrets.toml` is git-ignored. Use environment variables or a secrets manager in production.
- **SQL injection** — prevented by parameterized queries in all modules (maintain this pattern).
- **Soft-delete** — user records are never permanently removed from the database; `deleted_at` preserves data integrity.
- **Recommended** — input validation, rate limiting on login/reset endpoints, TLS/SSL for database and deployment connections.

---

## Development & testing

- **Run locally:** ensure MySQL is running with `employee_db` created, then `streamlit run main.py`.
- **Schema changes:** update the corresponding Python module and the SQL script if altering tables or views.
- **Testing:** no test suite yet. Consider:
  - Unit tests for `run_query()` with a mock MySQL connection
  - Integration tests against a dedicated test database
  - `streamlit.testing` for UI component tests

---

## Contributing

- Fork the repo, create a feature branch (`feat/your-feature`), make changes, and open a PR.
- Avoid committing secrets, large binaries, or modifying the `Data Dictionary/` and `Database & ERD/` folders.

---

## Contact

Maintained by **Miko-Explorer** — open an issue on [GitHub](https://github.com/Miko-Explorer/Employee-Directory).
