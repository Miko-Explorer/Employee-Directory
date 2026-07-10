import streamlit as st
import pandas as pd

from database import run_query
from users import (
    get_all_users, get_user_by_id, create_user, update_user,
    soft_delete_user, restore_user, search_users, filter_by_status,
    count_users, count_by_status,
)
from roles import get_all_roles, create_role, update_role, delete_role, count_roles
from permissions import get_all_permissions, create_permission, update_permission, delete_permission, count_permissions
from user_roles import get_all_assignments, assign_role, remove_role, get_available_roles_for_user, get_user_roles, count_assignments
from role_permissions import get_all_mappings, assign_permission, remove_permission, get_available_permissions_for_role, get_role_permissions, count_mappings
from sessions import get_all_sessions, get_active_sessions, expire_session, count_sessions, count_active_sessions
from password_resets import get_all_resets, create_reset_token, count_resets, count_pending_resets
from email_verifications import get_all_verifications, create_verification, verify_email, count_verifications, count_verified
from audit_logs import get_all_logs, get_logs_by_action, get_logs_by_table, count_logs, count_logs_today
from system_settings import get_all_settings, get_settings_by_category, get_categories, create_setting, update_setting, delete_setting, count_settings

st.set_page_config(page_title="Employee Directory", page_icon=None, layout="wide")

CSS = """
<style>
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #1d243c, #252d4a, #2a314e, #1f2742);
        background-size: 400% 400%;
        animation: gradientShift 18s ease infinite;
    }
    body, p, span, div, li, .stMarkdown, .stMarkdown p {
        color: #e7e9fb;
    }
    .glass-card {
        background: rgba(42, 49, 78, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(90, 95, 122, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .glass-card h3, .glass-card h4 {
        color: #e7e9fb;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    .glass-header {
        background: rgba(42, 49, 78, 0.5);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-bottom: 1px solid rgba(90, 95, 122, 0.3);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .main-title {
        color: #e7e9fb;
        font-size: 1.5rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin: 0;
        padding: 0;
    }
    .sub-title {
        color: #898da5;
        font-size: 0.8rem;
        letter-spacing: 0.03em;
    }
    .section-label {
        color: #898da5;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }
    div[data-testid="stMetric"] {
        background: #2a314e;
        border: 1px solid #5a5f7a;
        border-radius: 12px;
        padding: 0.75rem 1rem;
    }
    div[data-testid="stMetric"] label {
        color: #898da5;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetric"] div {
        color: #e7e9fb;
        font-weight: 700;
    }
    .stButton button {
        background: #5a5f7a;
        border: none;
        color: #e7e9fb;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: #6a6f8a;
        color: #ffffff;
    }
    .stButton button[kind="secondary"] {
        background: transparent;
        border: 1px solid #5a5f7a;
        color: #898da5;
    }
    .stButton button[kind="secondary"]:hover {
        background: rgba(90, 95, 122, 0.15);
        border-color: #898da5;
        color: #e7e9fb;
    }
    div.stDataFrame {
        background: #2a314e;
        border: 1px solid #5a5f7a;
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stDataFrame"] {
        background: transparent;
    }
    div[data-testid="stDataFrame"] table {
        color: #e7e9fb;
        border-collapse: collapse;
        width: 100%;
    }
    div[data-testid="stDataFrame"] th {
        background: #1d243c !important;
        color: #e7e9fb !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        padding: 0.55rem 0.7rem !important;
        border: none !important;
    }
    div[data-testid="stDataFrame"] td {
        color: #e7e9fb;
        padding: 0.45rem 0.7rem !important;
        border-bottom: 1px solid #5a5f7a;
    }
    div[data-testid="stDataFrame"] tr:nth-child(even) td {
        background: #252d4a;
    }
    div[data-testid="stDataFrame"] tr:nth-child(odd) td {
        background: #2a314e;
    }
    div[data-testid="stDataFrame"] tr:hover td {
        background: #323a5a !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: #2a314e !important;
        border: 1px solid #5a5f7a !important;
        border-radius: 8px !important;
        color: #e7e9fb !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #898da5 !important;
        box-shadow: 0 0 0 2px rgba(137, 141, 165, 0.15) !important;
    }
    div[data-baseweb="select"] > div {
        background: #2a314e !important;
        border: 1px solid #5a5f7a !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span {
        color: #e7e9fb !important;
    }
    div[data-baseweb="popover"] li {
        color: #e7e9fb !important;
        background: #2a314e !important;
    }
    div[data-baseweb="popover"] li:hover {
        background: #5a5f7a !important;
    }
    div[data-testid="stTab"] {
        background: transparent;
        border-bottom: 1px solid #5a5f7a;
    }
    div[data-testid="stTab"] button {
        color: #898da5;
        background: transparent;
        border: none;
        font-weight: 500;
    }
    div[data-testid="stTab"] button[aria-selected="true"] {
        color: #e7e9fb;
        border-bottom: 2px solid #898da5;
    }
    div[data-testid="stSidebarNav"] { display: none; }
    section[data-testid="stSidebar"] {
        background: #1d243c;
        border-right: 1px solid #5a5f7a;
    }
    .stSidebar .stRadio div {
        gap: 0.25rem;
    }
    .stSidebar .stRadio label {
        color: #898da5;
        font-weight: 500;
        padding: 0.4rem 0.75rem;
        border-radius: 6px;
        transition: all 0.15s;
    }
    .stSidebar .stRadio label:hover {
        background: #2a314e;
        color: #e7e9fb;
    }
    .stSidebar .stRadio div[data-testid="stWidgetLabel"] {
        color: #5a5f7a;
        text-transform: uppercase;
        font-size: 0.65rem;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }
    .stSuccess {
        background: #1e2e2a;
        border: 1px solid #3a6a60;
        color: #88ccbb;
        border-radius: 8px;
    }
    .stError {
        background: #2e1e22;
        border: 1px solid #6a3a44;
        color: #cc8890;
        border-radius: 8px;
    }
    .stInfo {
        background: #1e2440;
        border: 1px solid #3a4a7a;
        color: #889acc;
        border-radius: 8px;
    }
    .stWarning {
        background: #2e2a1e;
        border: 1px solid #6a5a3a;
        color: #ccb888;
        border-radius: 8px;
    }
    hr {
        border-color: #5a5f7a;
        margin: 1.25rem 0;
    }
    .solid-metric {
        background: #2a314e;
        border: 1px solid #5a5f7a;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        text-align: center;
        min-height: 4.8rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .solid-metric label {
        color: #898da5;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: block;
        line-height: 1.3;
    }
    .solid-metric span {
        color: #e7e9fb;
        font-size: 1.5rem;
        font-weight: 700;
        display: block;
        margin-top: 0.2rem;
        line-height: 1.2;
    }
    div[data-testid="caption"] {
        color: #898da5;
        font-size: 0.72rem;
    }
    .st-emotion-cache-1wbqy5l, .st-emotion-cache-1wmy9hl {
        color: #e7e9fb !important;
    }
    .streamlit-expanderHeader {
        color: #e7e9fb !important;
    }
    .sidebar-brand {
        padding: 1.25rem 0.75rem 0.75rem 0.75rem;
        text-align: center;
        border-bottom: 1px solid #5a5f7a;
        margin-bottom: 0.75rem;
    }
    .sidebar-brand svg {
        margin-bottom: 0.35rem;
    }
    .sidebar-brand div:first-of-type {
        color: #e7e9fb;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .sidebar-brand div:nth-of-type(2) {
        color: #898da5;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    a[data-testid="stPageLink"] { display: none; }
    .download-button a {
        color: #898da5 !important;
        text-decoration: none !important;
    }
</style>
"""

LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="44" height="44" rx="10" fill="url(#grad)"/>
    <path d="M14 18h16M14 22h12M14 26h14M22 14v16" stroke="#e7e9fb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>
    <circle cx="30" cy="14" r="4" fill="#e7e9fb" opacity="0.9"/>
    <defs>
        <linearGradient id="grad" x1="0" y1="0" x2="44" y2="44">
            <stop stop-color="#5a5f7a"/>
            <stop offset="1" stop-color="#1d243c"/>
        </linearGradient>
    </defs>
</svg>
"""

st.markdown(CSS, unsafe_allow_html=True)

PAGES = [
    "Dashboard",
    "Users",
    "Roles",
    "Permissions",
    "User Roles",
    "Role Permissions",
    "Sessions",
    "Password Resets",
    "Email Verifications",
    "Audit Logs",
    "System Settings",
    "Reports",
]

with st.sidebar:
    st.markdown(f'<div class="sidebar-brand">{LOGO_SVG}<div>Directory</div><div>Employee Management System</div></div>', unsafe_allow_html=True)
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")

st.markdown(f'<div class="glass-header"><span class="main-title">{page}</span></div>', unsafe_allow_html=True)


def format_dt(val):
    if hasattr(val, "strftime") and not pd.isna(val):
        return val.strftime("%Y-%m-%d %H:%M")
    return val


def show_table(data, cols=None):
    if isinstance(data, pd.DataFrame):
        if data.empty:
            return
        df = data
    else:
        if not data:
            return
        df = pd.DataFrame(data)
    for c in df.select_dtypes(include=["datetime64", "datetime"]).columns:
        df[c] = df[c].apply(format_dt)
    display = df[cols] if cols else df
    st.dataframe(display, use_container_width=True, hide_index=True)


if page == "Dashboard":
    st.markdown('<div class="section-label">System Overview</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    kpis = [
        ("Total Users", count_users()),
        ("Active Roles", count_roles()),
        ("Permissions", count_permissions()),
        ("Active Sessions", count_active_sessions()),
        ("Events Today", count_logs_today()),
    ]
    for col, (label, val) in zip(cols, kpis):
        col.markdown(f'<div class="solid-metric"><label>{label}</label><span>{val}</span></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    status_data = count_by_status()
    if status_data:
        c1.markdown('<div class="section-label" style="margin-top:1.25rem;">User Status Distribution</div>', unsafe_allow_html=True)
        df = pd.DataFrame(status_data)
        c1.bar_chart(df.set_index("status"), color="#898da5")

    try:
        role_data = run_query("SELECT Roles, User_count FROM report_11")
        if role_data:
            c2.markdown('<div class="section-label" style="margin-top:1.25rem;">Users per Role</div>', unsafe_allow_html=True)
            df2 = pd.DataFrame(role_data)
            c2.bar_chart(df2.set_index("Roles"), color="#5a5f7a")
    except Exception:
        pass

    logs = get_all_logs(limit=8)
    if logs:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Recent Activity</div>', unsafe_allow_html=True)
        show_table(logs, ["created_at", "user_name", "action", "table_name"])

if page == "Users":
    tab1, tab2, tab3 = st.tabs(["All Users", "Create User", "Search & Filter"])
    with tab1:
        users = get_all_users()
        if users:
            show_table(users, ["user_id", "user_name", "email", "first_name", "last_name", "status", "created_at"])
            with st.expander("Update or Delete User"):
                opts = {f"{u['user_id']} | {u['user_name']}": u["user_id"] for u in users}
                sel = st.selectbox("Select user", list(opts.keys()), key="u_sel")
                uid = opts[sel]
                u = get_user_by_id(uid)[0]
                col1, col2 = st.columns(2)
                with col1:
                    fn = st.text_input("First Name", value=u["first_name"], key="u_fn")
                    ln = st.text_input("Last Name", value=u["last_name"], key="u_ln")
                    em = st.text_input("Email", value=u["email"], key="u_em")
                with col2:
                    ph = st.text_input("Phone", value=u["phone_number"], key="u_ph")
                    sts = st.selectbox("Status", ["active", "suspended", "locked", "inactive"], index=["active", "suspended", "locked", "inactive"].index(u["status"]) if u["status"] in ["active", "suspended", "locked", "inactive"] else 0, key="u_sts")
                    pic = st.text_input("Profile URL", value=u["profile_picture_url"], key="u_pic")
                c3, c4 = st.columns(2)
                with c3:
                    if st.button("Save Changes"):
                        update_user(uid, first_name=fn, last_name=ln, email=em, phone_number=ph, status=sts, profile_picture_url=pic)
                        st.success("User record has been updated.")
                        st.rerun()
                with c4:
                    if u["deleted_at"] is None:
                        if st.button("Deactivate User", type="secondary"):
                            soft_delete_user(uid)
                            st.success("User has been deactivated.")
                            st.rerun()
                    else:
                        if st.button("Restore User"):
                            restore_user(uid)
                            st.success("User has been restored.")
                            st.rerun()
        else:
            st.info("No user records found.")
    with tab2:
        with st.form("create_user"):
            c1, c2 = st.columns(2)
            with c1:
                un = st.text_input("Username")
                em = st.text_input("Email")
                pw = st.text_input("Password", type="password")
                fn = st.text_input("First Name")
            with c2:
                ln = st.text_input("Last Name")
                ph = st.text_input("Phone Number")
                pp = st.text_input("Profile URL", value="")
                sts = st.selectbox("Status", ["active", "suspended", "locked", "inactive"])
            if st.form_submit_button("Create User"):
                if not all([un, em, pw, fn, ln]):
                    st.error("Username, email, password, first name, and last name are required.")
                else:
                    try:
                        create_user(un, em, pw, fn, ln, ph, pp, sts)
                        st.success(f"User '{un}' has been created.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Could not create user: {ex}")
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            q = st.text_input("Search by name, username, or email")
            if q:
                r = search_users(q)
                if r:
                    show_table(r, ["user_id", "user_name", "first_name", "last_name", "email", "status"])
                else:
                    st.info("No matching users found.")
        with c2:
            fs = st.selectbox("Filter by status", ["", "active", "suspended", "locked", "inactive"])
            if fs:
                r = filter_by_status(fs)
                if r:
                    show_table(r, ["user_id", "user_name", "first_name", "last_name", "email"])
                else:
                    st.info(f"No users with status '{fs}'.")

if page == "Roles":
    tab1, tab2 = st.tabs(["All Roles", "Create Role"])
    with tab1:
        roles = get_all_roles()
        if roles:
            show_table(roles, ["role_id", "role_name", "description", "created_at"])
            with st.expander("Edit or Delete Role"):
                opts = {r["role_name"]: r["role_id"] for r in roles}
                sel = st.selectbox("Select role", list(opts.keys()))
                rid = opts[sel]
                r = [x for x in roles if x["role_id"] == rid][0]
                nm = st.text_input("Role Name", value=r["role_name"])
                desc = st.text_input("Description", value=r["description"] or "")
                if st.button("Save Changes"):
                    update_role(rid, role_name=nm, description=desc if desc else None)
                    st.success("Role has been updated.")
                    st.rerun()
                if st.button("Delete", type="secondary"):
                    try:
                        delete_role(rid)
                        st.success("Role has been deleted.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Cannot delete role: {ex}")
        else:
            st.info("No roles found.")
    with tab2:
        with st.form("create_role"):
            nm = st.text_input("Role Name")
            desc = st.text_area("Description")
            if st.form_submit_button("Create Role"):
                if nm:
                    try:
                        create_role(nm, desc if desc else None)
                        st.success(f"Role '{nm}' has been created.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")
                else:
                    st.error("Role name is required.")

if page == "Permissions":
    tab1, tab2 = st.tabs(["All Permissions", "Create Permission"])
    with tab1:
        perms = get_all_permissions()
        if perms:
            show_table(perms, ["permission_id", "permission_name", "resource", "action", "description"])
            with st.expander("Edit or Delete Permission"):
                opts = {f"{p['permission_name']} ({p['resource']}:{p['action']})": p["permission_id"] for p in perms}
                sel = st.selectbox("Select permission", list(opts.keys()))
                pid = opts[sel]
                p = [x for x in perms if x["permission_id"] == pid][0]
                nm = st.text_input("Name", value=p["permission_name"])
                rs = st.text_input("Resource", value=p["resource"])
                ac = st.text_input("Action", value=p["action"])
                desc = st.text_input("Description", value=p["description"] or "")
                if st.button("Save Changes"):
                    update_permission(pid, permission_name=nm, resource=rs, action=ac, description=desc if desc else None)
                    st.success("Permission has been updated.")
                    st.rerun()
                if st.button("Delete", type="secondary"):
                    try:
                        delete_permission(pid)
                        st.success("Permission has been deleted.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Cannot delete permission: {ex}")
        else:
            st.info("No permissions found.")
    with tab2:
        with st.form("create_permission"):
            nm = st.text_input("Permission Name")
            rs = st.text_input("Resource")
            ac = st.text_input("Action")
            desc = st.text_area("Description")
            if st.form_submit_button("Create Permission"):
                if nm and rs and ac:
                    try:
                        create_permission(nm, rs, ac, desc if desc else None)
                        st.success(f"Permission '{nm}' has been created.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")
                else:
                    st.error("Name, resource, and action are required.")

if page == "User Roles":
    tab1, tab2 = st.tabs(["View Assignments", "Manage"])
    with tab1:
        assignments = get_all_assignments()
        if assignments:
            show_table(assignments, ["user_name", "first_name", "last_name", "role_name", "assigned_at"])
            st.caption(f"Total: {len(assignments)} assignment(s)")
        else:
            st.info("No role assignments found.")
    with tab2:
        users = get_all_users()
        roles = get_all_roles()
        if users and roles:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Assign Role**")
                u_opts = {f"{u['user_name']} ({u['first_name']} {u['last_name']})": u["user_id"] for u in users}
                su = st.selectbox("User", list(u_opts.keys()), key="ur_a_user")
                uid = u_opts[su]
                avail = get_available_roles_for_user(uid)
                if avail:
                    r_opts = {r["role_name"]: r["role_id"] for r in avail}
                    sr = st.selectbox("Role", list(r_opts.keys()), key="ur_a_role")
                    rid = r_opts[sr]
                    ab = st.number_input("Assigned by (user ID)", min_value=1, value=1)
                    if st.button("Assign"):
                        try:
                            assign_role(uid, rid, ab)
                            st.success("Role has been assigned.")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"Error: {ex}")
                else:
                    st.info("User already has all roles.")
            with c2:
                st.markdown("**Remove Role**")
                u_opts2 = {f"{u['user_name']} ({u['first_name']} {u['last_name']})": u["user_id"] for u in users}
                su2 = st.selectbox("User", list(u_opts2.keys()), key="ur_r_user")
                uid2 = u_opts2[su2]
                cur = get_user_roles(uid2)
                if cur:
                    r_opts2 = {r["role_name"]: r["role_id"] for r in cur}
                    sr2 = st.selectbox("Role to remove", list(r_opts2.keys()))
                    rid2 = r_opts2[sr2]
                    if st.button("Remove", type="secondary"):
                        remove_role(uid2, rid2)
                        st.success("Role has been removed.")
                        st.rerun()
                else:
                    st.info("User has no roles to remove.")
        else:
            st.info("No users or roles available.")

if page == "Role Permissions":
    tab1, tab2 = st.tabs(["View Mappings", "Manage"])
    with tab1:
        mappings = get_all_mappings()
        if mappings:
            show_table(mappings, ["role_name", "permission_name", "resource", "action", "assigned_at"])
            st.caption(f"Total: {len(mappings)} mapping(s)")
        else:
            st.info("No permission mappings found.")
    with tab2:
        roles = get_all_roles()
        perms = get_all_permissions()
        if roles and perms:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Assign Permission**")
                r_opts = {r["role_name"]: r["role_id"] for r in roles}
                sr = st.selectbox("Role", list(r_opts.keys()), key="rp_a_role")
                rid = r_opts[sr]
                avail = get_available_permissions_for_role(rid)
                if avail:
                    p_opts = {f"{p['permission_name']} ({p['resource']}:{p['action']})": p["permission_id"] for p in avail}
                    sp = st.selectbox("Permission", list(p_opts.keys()))
                    pid = p_opts[sp]
                    if st.button("Assign"):
                        try:
                            assign_permission(rid, pid)
                            st.success("Permission has been assigned.")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"Error: {ex}")
                else:
                    st.info("Role already has all permissions.")
            with c2:
                st.markdown("**Remove Permission**")
                r_opts2 = {r["role_name"]: r["role_id"] for r in roles}
                sr2 = st.selectbox("Role", list(r_opts2.keys()), key="rp_r_role")
                rid2 = r_opts2[sr2]
                cur = get_role_permissions(rid2)
                if cur:
                    p_opts2 = {f"{p['permission_name']} ({p['resource']}:{p['action']})": p["permission_id"] for p in cur}
                    sp2 = st.selectbox("Permission to remove", list(p_opts2.keys()))
                    pid2 = p_opts2[sp2]
                    if st.button("Remove", type="secondary"):
                        remove_permission(rid2, pid2)
                        st.success("Permission has been removed.")
                        st.rerun()
                else:
                    st.info("Role has no permissions to remove.")
        else:
            st.info("No roles or permissions available.")

if page == "Sessions":
    view = st.radio("View", ["All Sessions", "Active Only"], horizontal=True)
    sessions = get_active_sessions() if view == "Active Only" else get_all_sessions()
    if sessions:
        show_table(sessions)
        with st.expander("Expire a Session"):
            opts = {f"#{s['session_id']} | {s.get('user_name','?')}": s["session_id"] for s in sessions}
            sel = st.selectbox("Session", list(opts.keys()))
            if st.button("Expire", type="secondary"):
                expire_session(opts[sel])
                st.success("Session has been expired.")
                st.rerun()
    else:
        st.info("No sessions recorded.")

if page == "Password Resets":
    tab1, tab2 = st.tabs(["View Resets", "Create Token"])
    with tab1:
        resets = get_all_resets()
        if resets:
            df = pd.DataFrame(resets)
            for c in df.select_dtypes(include=["datetime64", "datetime"]).columns:
                df[c] = df[c].apply(format_dt)
            df["used"] = df["used_at"].apply(lambda x: "Yes" if x else "No")
            show_table(df, ["user_name", "token", "expires_at", "used", "created_at"])
            st.caption(f"Pending: {count_pending_resets()}  |  Total: {count_resets()}")
        else:
            st.info("No password reset records found.")
    with tab2:
        users = get_all_users()
        if users:
            opts = {f"{u['user_name']}": u["user_id"] for u in users}
            sel = st.selectbox("Select user", list(opts.keys()))
            if st.button("Generate Token"):
                try:
                    create_reset_token(opts[sel])
                    st.success("Reset token has been generated.")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error: {ex}")
        else:
            st.info("No users available.")

if page == "Email Verifications":
    tab1, tab2 = st.tabs(["View Verifications", "Create Token"])
    with tab1:
        verifications = get_all_verifications()
        if verifications:
            df = pd.DataFrame(verifications)
            for c in df.select_dtypes(include=["datetime64", "datetime"]).columns:
                df[c] = df[c].apply(format_dt)
            df["verified"] = df["verified_at"].apply(lambda x: "Yes" if x else "No")
            show_table(df, ["user_name", "token", "expires_at", "verified", "created_at"])
            st.caption(f"Verified: {count_verified()}  |  Total: {count_verifications()}")
            unverified = [v for v in verifications if v["verified_at"] is None]
            if unverified:
                with st.expander("Mark Token as Verified"):
                    opts = {f"{v['user_name']} ({v['token'][:20]}...)": v["verification_id"] for v in unverified}
                    sel = st.selectbox("Select token", list(opts.keys()))
                    if st.button("Mark Verified"):
                        verify_email(opts[sel])
                        st.success("Token has been marked as verified.")
                        st.rerun()
        else:
            st.info("No email verification records found.")
    with tab2:
        users = get_all_users()
        if users:
            opts = {f"{u['user_name']}": u["user_id"] for u in users}
            sel = st.selectbox("Select user", list(opts.keys()))
            if st.button("Generate Token"):
                try:
                    create_verification(opts[sel])
                    st.success("Verification token has been generated.")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error: {ex}")
        else:
            st.info("No users available.")

if page == "Audit Logs":
    filt = st.radio("Filter", ["All Events", "By Action", "By Table"], horizontal=True)
    if filt == "By Action":
        actions = run_query("SELECT DISTINCT action FROM audit_logs ORDER BY action")
        if actions:
            al = [a["action"] for a in actions]
            sel = st.selectbox("Select action", al)
            logs = get_logs_by_action(sel)
        else:
            logs = []
    elif filt == "By Table":
        tables = run_query("SELECT DISTINCT table_name FROM audit_logs WHERE table_name IS NOT NULL ORDER BY table_name")
        if tables:
            tl = [t["table_name"] for t in tables]
            sel = st.selectbox("Select table", tl)
            logs = get_logs_by_table(sel)
        else:
            logs = []
    else:
        logs = get_all_logs()
    if logs:
        show_table(logs, [c for c in ["created_at", "user_name", "action", "table_name", "record_id", "ip_address"] if c in logs[0]])
        st.caption(f"Showing {len(logs)} event(s)")
    else:
        st.info("No audit events found.")

if page == "System Settings":
    tab1, tab2, tab3 = st.tabs(["All Settings", "Create Setting", "By Category"])
    with tab1:
        settings = get_all_settings()
        if settings:
            show_table(settings, ["setting_id", "setting_key", "setting_value", "category", "description", "updated_at"])
            with st.expander("Edit or Delete Setting"):
                opts = {s["setting_key"]: s["setting_id"] for s in settings}
                sel = st.selectbox("Select setting", list(opts.keys()))
                sid = opts[sel]
                s = [x for x in settings if x["setting_id"] == sid][0]
                val = st.text_input("Value", value=s["setting_value"])
                desc = st.text_input("Description", value=s["description"] or "")
                if st.button("Save Changes"):
                    update_setting(sid, setting_value=val, description=desc if desc else None)
                    st.success("Setting has been updated.")
                    st.rerun()
                if st.button("Delete", type="secondary"):
                    delete_setting(sid)
                    st.success("Setting has been deleted.")
                    st.rerun()
        else:
            st.info("No settings found.")
    with tab2:
        with st.form("create_setting"):
            k = st.text_input("Key")
            v = st.text_input("Value")
            cat = st.text_input("Category")
            desc = st.text_area("Description")
            if st.form_submit_button("Create Setting"):
                if k and v and cat:
                    try:
                        create_setting(k, v, cat, desc if desc else None)
                        st.success(f"Setting '{k}' has been created.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")
                else:
                    st.error("Key, value, and category are required.")
    with tab3:
        cats = get_categories()
        if cats:
            cl = [c["category"] for c in cats]
            sel = st.selectbox("Select category", cl)
            data = get_settings_by_category(sel)
            if data:
                show_table(data, ["setting_key", "setting_value", "description"])
        else:
            st.info("No categories found.")

if page == "Reports":
    REPORTS = {
        "User Demographics": {
            "report_1": "Count users by account status",
            "report_2": "Count users by registration month",
            "report_3": "Count users by registration year",
            "report_4": "Count users with vs. without soft-delete",
        },
        "Session & Activity": {
            "report_5": "Sessions per day",
            "report_6": "Sessions per month",
            "report_7": "Sessions per user per day",
            "report_8": "Average sessions per user",
            "report_9": "Active vs expired sessions",
            "report_10": "Most common IPs",
        },
        "Role & Permission Distribution": {
            "report_11": "Users per role",
            "report_12": "Permissions per role",
            "report_13": "Roles with no users",
        },
        "Audit Log Analytics": {
            "report_14": "Actions by operation type",
            "report_15": "Actions per user",
            "report_16": "Actions per affected table",
            "report_17": "Daily volume per table",
            "report_18": "Total daily volume",
        },
        "User Filters": {
            "report_19": "User filter by status",
            "report_20": "User filter by soft-delete status",
            "report_21": "Users registered in last 30 days",
        },
        "Combined Analysis": {
            "report_22": "Logins per user per day",
            "report_23": "Users per role with recent login",
            "report_24": "Admin action breakdown",
            "report_25": "Suspicious IPs (>50 sessions)",
            "report_26": "Soft-deleted users per role",
        },
    }
    cat = st.selectbox("Report Category", list(REPORTS.keys()))
    reports = REPORTS[cat]
    rpt = st.selectbox("Select Report", list(reports.keys()), format_func=lambda x: f"{x}  -  {reports[x]}")
    if st.button("Run Report"):
        try:
            result = run_query(f"SELECT * FROM {rpt}")
            if result:
                show_table(result)
                st.caption(f"Returned {len(result)} row(s)")
                csv = pd.DataFrame(result).to_csv(index=False)
                st.download_button("Download CSV", csv, f"{rpt}.csv", "text/csv")
            else:
                st.info("Report returned no data.")
        except Exception as ex:
            st.error(f"Could not run report: {ex}")