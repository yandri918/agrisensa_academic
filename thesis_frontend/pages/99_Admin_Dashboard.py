# AgriSensa Admin Dashboard
# Streamlit-only admin panel with session-based authentication

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Auth imports 
from utils.auth import require_auth, show_user_info_sidebar, get_current_user, is_authenticated, get_activity_log, get_users

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Admin Dashboard - AgriSensa",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== AUTH CHECK ==========
user = require_auth()

# Check if admin or superadmin
if user.get('role') not in ['admin', 'superadmin']:
    st.error("🚫 Akses ditolak! Halaman ini hanya untuk Admin.")
    st.info("Login dengan akun admin untuk mengakses dashboard ini.")
    st.stop()

show_user_info_sidebar()


# ========== STYLING ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .admin-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }
    .admin-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .admin-subtitle {
        opacity: 0.8;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE FOR DATA ==========
if 'commodities_db' not in st.session_state:
    st.session_state.commodities_db = [
        {'id': 1, 'name': 'Beras Premium', 'category': 'Pangan', 'unit': 'kg', 'price': 15000, 'active': True},
        {'id': 2, 'name': 'Cabai Rawit', 'category': 'Sayuran', 'unit': 'kg', 'price': 80000, 'active': True},
        {'id': 3, 'name': 'Bawang Merah', 'category': 'Sayuran', 'unit': 'kg', 'price': 45000, 'active': True},
        {'id': 4, 'name': 'Jagung Pipil', 'category': 'Pangan', 'unit': 'kg', 'price': 8000, 'active': True},
        {'id': 5, 'name': 'Kedelai', 'category': 'Pangan', 'unit': 'kg', 'price': 12000, 'active': True},
        {'id': 6, 'name': 'Gula Pasir', 'category': 'Pangan', 'unit': 'kg', 'price': 16000, 'active': True},
        {'id': 7, 'name': 'Bayam', 'category': 'Sayuran', 'unit': 'ikat', 'price': 5000, 'active': True},
        {'id': 8, 'name': 'Kangkung', 'category': 'Sayuran', 'unit': 'ikat', 'price': 4000, 'active': True},
        {'id': 9, 'name': 'Tomat', 'category': 'Sayuran', 'unit': 'kg', 'price': 15000, 'active': True},
        {'id': 10, 'name': 'Jeruk', 'category': 'Buah', 'unit': 'kg', 'price': 25000, 'active': True},
    ]

if 'manual_prices_db' not in st.session_state:
    st.session_state.manual_prices_db = []

if 'audit_log_db' not in st.session_state:
    st.session_state.audit_log_db = []


def log_action(action, table, record_id=None, details=""):
    """Log admin action."""
    st.session_state.audit_log_db.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user': user['username'],
        'action': action,
        'table': table,
        'record_id': record_id,
        'details': details
    })


def get_next_id(db_list):
    """Get next ID for a database."""
    if not db_list:
        return 1
    return max(item['id'] for item in db_list) + 1


# ========== HEADER ==========
role_badge = "👑 SUPER ADMIN" if user.get('role') == 'superadmin' else "🛡️ ADMIN"
st.markdown(f"""
<div class="admin-header">
    <h1 class="admin-title">🛡️ Admin Dashboard</h1>
    <p class="admin-subtitle">Enterprise Management Console - {role_badge}</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR NAVIGATION ==========
menu_items = ["📊 Dashboard", "🌾 Komoditas", "💰 Harga Manual", "📝 Audit Log"]

# Super Admin gets extra menus
if user.get('role') == 'superadmin':
    menu_items.extend(["👥 User Activity", "👤 Manage Users", "🗄️ Database Explorer", "📈 Analytics"])


menu = st.sidebar.radio(
    "📱 Menu Admin",
    menu_items,
    label_visibility="collapsed"
)



# ========== DASHBOARD ==========
if menu == "📊 Dashboard":
    st.subheader("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Komoditas", len(st.session_state.commodities_db))
    with col2:
        active = len([c for c in st.session_state.commodities_db if c['active']])
        st.metric("✅ Komoditas Aktif", active)
    with col3:
        st.metric("💰 Harga Manual", len(st.session_state.manual_prices_db))
    with col4:
        st.metric("📝 Total Log", len(st.session_state.audit_log_db))
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Aktivitas Terbaru")
    if st.session_state.audit_log_db:
        recent = st.session_state.audit_log_db[-10:][::-1]  # Last 10, reversed
        df = pd.DataFrame(recent)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas tercatat")

# ========== COMMODITIES ==========
elif menu == "🌾 Komoditas":
    st.subheader("🌾 Manajemen Komoditas")
    
    tab1, tab2, tab3 = st.tabs(["📋 Daftar", "➕ Tambah Baru", "📁 Import CSV"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Cari", placeholder="Nama komoditas...")
        with col2:
            category_filter = st.selectbox("Kategori", ["Semua", "Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"])
        
        # Filter data
        commodities = st.session_state.commodities_db
        if search:
            commodities = [c for c in commodities if search.lower() in c['name'].lower()]
        if category_filter != "Semua":
            commodities = [c for c in commodities if c['category'] == category_filter]
        
        if commodities:
            df = pd.DataFrame(commodities)
            df['active'] = df['active'].apply(lambda x: '✅' if x else '❌')
            df['price'] = df['price'].apply(lambda x: f"Rp {x:,}")
            df.columns = ['ID', 'Nama', 'Kategori', 'Unit', 'Harga', 'Aktif']
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Edit section
            st.markdown("---")
            st.subheader("✏️ Edit / Hapus Komoditas")
            
            commodity_options = {c['name']: c['id'] for c in commodities}
            if commodity_options:
                selected_name = st.selectbox("Pilih komoditas", list(commodity_options.keys()))
                selected_id = commodity_options[selected_name]
                selected = next(c for c in st.session_state.commodities_db if c['id'] == selected_id)
                
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Nama", value=selected['name'])
                        new_category = st.selectbox("Kategori", 
                            ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"],
                            index=["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"].index(selected['category']) if selected['category'] in ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"] else 0
                        )
                    with col2:
                        new_unit = st.text_input("Unit", value=selected['unit'])
                        new_price = st.number_input("Harga", value=selected['price'])
                    
                    new_active = st.checkbox("Aktif", value=selected['active'])
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                            for c in st.session_state.commodities_db:
                                if c['id'] == selected_id:
                                    c['name'] = new_name
                                    c['category'] = new_category
                                    c['unit'] = new_unit
                                    c['price'] = new_price
                                    c['active'] = new_active
                                    break
                            log_action('UPDATE', 'commodities', selected_id, f"Updated {new_name}")
                            st.success("✅ Berhasil diupdate!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.form_submit_button("🗑️ Hapus", use_container_width=True):
                            st.session_state.commodities_db = [c for c in st.session_state.commodities_db if c['id'] != selected_id]
                            log_action('DELETE', 'commodities', selected_id, f"Deleted {selected['name']}")
                            st.success("✅ Berhasil dihapus!")
                            st.rerun()
        else:
            st.info("Tidak ada komoditas ditemukan")
    
    with tab2:
        st.subheader("➕ Tambah Komoditas Baru")
        
        with st.form("add_commodity"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nama Komoditas *")
                category = st.selectbox("Kategori *", ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"])
            with col2:
                unit = st.selectbox("Unit", ["kg", "ikat", "butir", "ton"])
                price = st.number_input("Harga Referensi (Rp)", min_value=0)
            
            if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                if name:
                    new_id = get_next_id(st.session_state.commodities_db)
                    st.session_state.commodities_db.append({
                        'id': new_id,
                        'name': name,
                        'category': category,
                        'unit': unit,
                        'price': price,
                        'active': True
                    })
                    log_action('CREATE', 'commodities', new_id, f"Created {name}")
                    st.success(f"✅ Komoditas '{name}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Nama komoditas wajib diisi!")
    
    with tab3:
        st.subheader("📁 Import dari CSV")
        st.markdown("""
        **Format CSV:**
        ```
        name,category,unit,price
        Bayam Hijau,Sayuran,ikat,5000
        ```
        """)
        
        uploaded = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("📤 Import", type="primary"):
                count = 0
                for _, row in df.iterrows():
                    new_id = get_next_id(st.session_state.commodities_db)
                    st.session_state.commodities_db.append({
                        'id': new_id,
                        'name': row.get('name', ''),
                        'category': row.get('category', 'Lainnya'),
                        'unit': row.get('unit', 'kg'),
                        'price': row.get('price', 0),
                        'active': True
                    })
                    count += 1
                log_action('BULK_IMPORT', 'commodities', None, f"Imported {count} items")
                st.success(f"✅ {count} komoditas berhasil diimport!")
                st.rerun()

# ========== MANUAL PRICES ==========
elif menu == "💰 Harga Manual":
    st.subheader("💰 Harga Manual")
    
    tab1, tab2 = st.tabs(["📋 Daftar", "➕ Tambah Harga"])
    
    with tab1:
        if st.session_state.manual_prices_db:
            df = pd.DataFrame(st.session_state.manual_prices_db)
            df['price'] = df['price'].apply(lambda x: f"Rp {x:,}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada harga manual. Tambahkan di tab 'Tambah Harga'.")
    
    with tab2:
        st.subheader("➕ Tambah Harga Baru")
        
        commodity_options = {c['name']: c['id'] for c in st.session_state.commodities_db if c['active']}
        
        with st.form("add_price"):
            col1, col2 = st.columns(2)
            with col1:
                selected_commodity = st.selectbox("Komoditas", list(commodity_options.keys()) if commodity_options else ["Tidak ada"])
                price = st.number_input("Harga (Rp)", min_value=0)
                price_date = st.date_input("Tanggal", value=date.today())
            with col2:
                province = st.text_input("Provinsi", placeholder="Jawa Barat")
                city = st.text_input("Kota", placeholder="Bandung")
                price_type = st.selectbox("Tipe", ["retail", "wholesale", "farm_gate"])
            
            if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                if selected_commodity and price > 0:
                    new_id = get_next_id(st.session_state.manual_prices_db)
                    st.session_state.manual_prices_db.append({
                        'id': new_id,
                        'commodity': selected_commodity,
                        'price': price,
                        'date': price_date.isoformat(),
                        'province': province,
                        'city': city,
                        'type': price_type,
                        'reporter': user['username']
                    })
                    log_action('CREATE', 'manual_prices', new_id, f"Price for {selected_commodity}")
                    st.success("✅ Harga berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Pilih komoditas dan isi harga!")

# ========== AUDIT LOG ==========
elif menu == "📝 Audit Log":
    st.subheader("📝 Audit Log")
    
    if st.session_state.audit_log_db:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            action_filter = st.selectbox("Filter Aksi", ["Semua", "CREATE", "UPDATE", "DELETE", "BULK_IMPORT"])
        with col2:
            table_filter = st.selectbox("Filter Tabel", ["Semua", "commodities", "manual_prices"])
        
        logs = st.session_state.audit_log_db[::-1]  # Reverse to show newest first
        
        if action_filter != "Semua":
            logs = [l for l in logs if l['action'] == action_filter]
        if table_filter != "Semua":
            logs = [l for l in logs if l['table'] == table_filter]
        
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada log yang cocok dengan filter")
    else:
        st.info("Belum ada aktivitas tercatat")

# ========== USER ACTIVITY (SUPERADMIN ONLY) ==========
elif menu == "👥 User Activity":
    st.subheader("👥 User Activity Log")
    st.info("🔍 Monitor semua aktivitas login user di platform")
    
    activity_log = get_activity_log()
    
    if activity_log:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            action_filter = st.selectbox("Filter Aksi", ["Semua", "LOGIN", "LOGIN_FAILED", "REGISTER", "LOGOUT"])
        with col2:
            users_list = list(set([a['username'] for a in activity_log]))
            user_filter = st.selectbox("Filter User", ["Semua"] + users_list)
        
        logs = activity_log[::-1]  # Newest first
        
        if action_filter != "Semua":
            logs = [l for l in logs if l['action'] == action_filter]
        if user_filter != "Semua":
            logs = [l for l in logs if l['username'] == user_filter]
        
        if logs:
            df = pd.DataFrame(logs)
            
            # Select only needed columns (handle both API and local format)
            display_cols = []
            if 'timestamp' in df.columns:
                display_cols.append('timestamp')
            if 'username' in df.columns:
                display_cols.append('username')
            if 'action' in df.columns:
                display_cols.append('action')
            if 'details' in df.columns:
                display_cols.append('details')
            
            if display_cols:
                df = df[display_cols]
            
            # Add status icons
            def format_action(action):
                icons = {
                    'LOGIN': '✅',
                    'LOGIN_FAILED': '❌',
                    'REGISTER': '🆕',
                    'LOGOUT': '🚪'
                }
                return f"{icons.get(action, '📋')} {action}"
            
            if 'action' in df.columns:
                df['action'] = df['action'].apply(format_action)
            
            # Rename columns for display
            col_names = {'timestamp': 'Waktu', 'username': 'Username', 'action': 'Aksi', 'details': 'Detail'}
            df = df.rename(columns=col_names)
            
            st.dataframe(df, use_container_width=True, hide_index=True)

            
            # Stats
            st.markdown("---")
            st.subheader("📊 Statistik Login")
            col1, col2, col3 = st.columns(3)
            with col1:
                total_logins = len([l for l in activity_log if l['action'] == 'LOGIN'])
                st.metric("Total Login Sukses", total_logins)
            with col2:
                failed = len([l for l in activity_log if l['action'] == 'LOGIN_FAILED'])
                st.metric("Login Gagal", failed)
            with col3:
                unique_users = len(set([l['username'] for l in activity_log if l['action'] == 'LOGIN']))
                st.metric("User Unik", unique_users)
        else:
            st.info("Tidak ada log yang cocok dengan filter")
    else:
        st.info("Belum ada aktivitas user tercatat. User akan terlog saat login.")

# ========== MANAGE USERS (SUPERADMIN ONLY) ==========
elif menu == "👤 Manage Users":
    st.subheader("👤 Manage Users")
    st.info("👑 Kelola semua user yang terdaftar di platform")
    
    users = get_users()
    
    tab1, tab2 = st.tabs(["📋 Daftar User", "➕ Tambah User"])
    
    with tab1:
        if users:
            users_data = []
            for username, data in users.items():
                users_data.append({
                    'username': username,
                    'name': data['name'],
                    'email': data['email'],
                    'role': data['role']
                })
            
            df = pd.DataFrame(users_data)
            
            # Add role badges
            def format_role(role):
                badges = {
                    'superadmin': '👑 Super Admin',
                    'admin': '🛡️ Admin',
                    'user': '👤 User'
                }
                return badges.get(role, role)
            
            df['role'] = df['role'].apply(format_role)
            df.columns = ['Username', 'Nama', 'Email', 'Role']
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Role change
            st.markdown("---")
            st.subheader("🔄 Ubah Role User")
            
            non_super_users = [u for u in users.keys() if users[u]['role'] != 'superadmin']
            if non_super_users:
                selected_user = st.selectbox("Pilih User", non_super_users)
                new_role = st.selectbox("Role Baru", ["user", "admin"])
                
                if st.button("💾 Update Role", type="primary"):
                    users[selected_user]['role'] = new_role
                    log_action('UPDATE_ROLE', 'users', None, f"Changed {selected_user} to {new_role}")
                    st.success(f"✅ Role {selected_user} berhasil diubah menjadi {new_role}")
                    st.rerun()
            else:
                st.info("Tidak ada user yang bisa diubah rolenya")
        else:
            st.info("Belum ada user")
    
    with tab2:
        st.subheader("➕ Tambah User Baru")
        
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Nama *")
                new_username = st.text_input("Username *")
            with col2:
                new_email = st.text_input("Email")
                new_password = st.text_input("Password *", type="password")
            
            new_role = st.selectbox("Role", ["user", "admin"])
            
            if st.form_submit_button("💾 Tambah User", type="primary", use_container_width=True):
                if new_name and new_username and new_password:
                    if new_username.lower() in users:
                        st.error("❌ Username sudah digunakan!")
                    else:
                        users[new_username.lower()] = {
                            'password': new_password,
                            'role': new_role,
                            'name': new_name,
                            'email': new_email or f"{new_username}@agrisensa.com"
                        }
                        log_action('CREATE', 'users', None, f"Created user {new_username}")
                        st.success(f"✅ User {new_username} berhasil ditambahkan!")
                        st.rerun()
                else:
                    st.warning("⚠️ Lengkapi semua field wajib!")

# ========== DATABASE EXPLORER (SUPERADMIN ONLY) ==========
elif menu == "🗄️ Database Explorer":
    st.subheader("🗄️ Database Explorer")
    st.info("👑 Akses lengkap ke semua data yang tersimpan di platform")
    
    # Load NPK data from file
    import os
    NPK_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "soil_map_npk_data.json")
    npk_soil_data = []
    if os.path.exists(NPK_DATA_FILE):
        try:
            with open(NPK_DATA_FILE, 'r') as f:
                npk_soil_data = json.load(f)
        except:
            npk_soil_data = []
    
    # Load Journal data
    JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "..", "journal_data.json")
    journal_data = []
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, 'r') as f:
                journal_data = json.load(f)
        except:
            journal_data = []
    
    # Overview Stats
    st.markdown("### 📊 Database Overview")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("🌾 Komoditas", len(st.session_state.get('commodities_db', [])))
    with col2:
        st.metric("💰 Harga Manual", len(st.session_state.get('manual_prices_db', [])))
    with col3:
        st.metric("🗺️ NPK Tanah", len(npk_soil_data))
    with col4:
        st.metric("📓 Jurnal", len(journal_data))
    with col5:
        st.metric("👥 Activity", len(get_activity_log()))
    with col6:
        st.metric("👤 Users", len(get_users()))
    
    st.markdown("---")
    
    # Database Selector
    db_choice = st.selectbox(
        "🔍 Pilih Database untuk Dilihat",
        ["📋 Semua Database", "🌾 Commodities", "💰 Manual Prices", "🗺️ NPK Soil Map", "📓 Journal", "📝 Audit Log", "👥 User Activity", "👤 Users"]
    )

    
    if db_choice == "📋 Semua Database":
        # Show all databases
        st.markdown("### 🌾 Commodities Database")
        if st.session_state.get('commodities_db'):
            df = pd.DataFrame(st.session_state.commodities_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 💰 Manual Prices Database")
        if st.session_state.get('manual_prices_db'):
            df = pd.DataFrame(st.session_state.manual_prices_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 🗺️ NPK Soil Map Database")
        if npk_soil_data:
            df = pd.DataFrame(npk_soil_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 📓 Journal Database")
        if journal_data:
            df = pd.DataFrame(journal_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 📝 Audit Log Database")
        if st.session_state.get('audit_log_db'):
            df = pd.DataFrame(st.session_state.audit_log_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 👥 User Activity Log")
        activity = get_activity_log()
        if activity:
            df = pd.DataFrame(activity)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")
        
        st.markdown("### 👤 Users Database")
        users_db = get_users()
        if users_db:
            users_data = []
            for username, data in users_db.items():
                users_data.append({
                    'username': username,
                    'name': data['name'],
                    'email': data['email'],
                    'role': data['role'],
                    'password': '••••••••'  # Hide password
                })
            df = pd.DataFrame(users_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Kosong")

    
    elif db_choice == "🌾 Commodities":
        st.markdown("### 🌾 Commodities Database")
        if st.session_state.get('commodities_db'):
            df = pd.DataFrame(st.session_state.commodities_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                json_str = json.dumps(st.session_state.commodities_db, indent=2, default=str)
                st.download_button("📥 Download JSON", json_str, "commodities.json", "application/json")
            with col2:
                csv = df.to_csv(index=False)
                st.download_button("📥 Download CSV", csv, "commodities.csv", "text/csv")
        else:
            st.info("Database kosong")
    
    elif db_choice == "💰 Manual Prices":
        st.markdown("### 💰 Manual Prices Database")
        if st.session_state.get('manual_prices_db'):
            df = pd.DataFrame(st.session_state.manual_prices_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            json_str = json.dumps(st.session_state.manual_prices_db, indent=2, default=str)
            st.download_button("📥 Download JSON", json_str, "manual_prices.json", "application/json")
        else:
            st.info("Database kosong")
    
    elif db_choice == "🗺️ NPK Soil Map":
        st.markdown("### 🗺️ NPK Soil Map Database")
        st.info("📍 Data pengukuran NPK tanah dari peta interaktif")
        
        if npk_soil_data:
            df = pd.DataFrame(npk_soil_data)
            
            # Show columns
            display_cols = ['id', 'latitude', 'longitude', 'n_value', 'p_value', 'k_value', 'ph', 'soil_type', 'created_at']
            available_cols = [c for c in display_cols if c in df.columns]
            df_display = df[available_cols] if available_cols else df
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Stats
            st.markdown("---")
            st.subheader("📊 Statistik NPK")
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'n_value' in df.columns:
                    st.metric("🔵 Rata-rata N", f"{df['n_value'].mean():.1f} ppm")
            with col2:
                if 'p_value' in df.columns:
                    st.metric("🟢 Rata-rata P", f"{df['p_value'].mean():.1f} ppm")
            with col3:
                if 'k_value' in df.columns:
                    st.metric("🟠 Rata-rata K", f"{df['k_value'].mean():.1f} ppm")
            
            # Export
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                json_str = json.dumps(npk_soil_data, indent=2, default=str)
                st.download_button("📥 Download JSON", json_str, "npk_soil_data.json", "application/json")
            with col2:
                csv = df.to_csv(index=False)
                st.download_button("📥 Download CSV", csv, "npk_soil_data.csv", "text/csv")
        else:
            st.info("Belum ada data NPK. Tambahkan melalui halaman Peta Data Tanah.")
    
    elif db_choice == "📓 Journal":
        st.markdown("### 📓 Journal Database")
        st.info("📝 Data jurnal harian pertanian")
        
        if journal_data:
            df = pd.DataFrame(journal_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export
            st.markdown("---")
            json_str = json.dumps(journal_data, indent=2, default=str)
            st.download_button("📥 Download JSON", json_str, "journal_data.json", "application/json")
        else:
            st.info("Belum ada data jurnal. Tambahkan melalui halaman Jurnal Harian.")

    
    elif db_choice == "📝 Audit Log":
        st.markdown("### 📝 Audit Log Database")
        if st.session_state.get('audit_log_db'):
            df = pd.DataFrame(st.session_state.audit_log_db)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            json_str = json.dumps(st.session_state.audit_log_db, indent=2, default=str)
            st.download_button("📥 Download JSON", json_str, "audit_log.json", "application/json")
        else:
            st.info("Database kosong")
    
    elif db_choice == "👥 User Activity":
        st.markdown("### 👥 User Activity Log")
        activity = get_activity_log()
        if activity:
            df = pd.DataFrame(activity)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            json_str = json.dumps(activity, indent=2, default=str)
            st.download_button("📥 Download JSON", json_str, "user_activity.json", "application/json")
        else:
            st.info("Database kosong")
    
    elif db_choice == "👤 Users":
        st.markdown("### 👤 Users Database")
        users_db = get_users()
        if users_db:
            users_data = []
            for username, data in users_db.items():
                users_data.append({
                    'username': username,
                    'name': data['name'],
                    'email': data['email'],
                    'role': data['role']
                })
            df = pd.DataFrame(users_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Show password (superadmin only)
            st.markdown("---")
            st.warning("⚠️ Data sensitif - hanya untuk Super Admin")
            if st.checkbox("Tampilkan password"):
                for username, data in users_db.items():
                    st.text(f"{username}: {data['password']}")
        else:
            st.info("Database kosong")
    
    # System Info
    st.markdown("---")
    st.markdown("### ⚙️ System Info")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        - **Session State Keys:** {len(st.session_state)}
        - **Current User:** {user['username']}
        - **Role:** {user['role']}
        """)
    with col2:
        st.markdown(f"""
        - **Platform:** AgriSensa Streamlit
        - **Version:** 4.0.0
        - **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """)

# ========== ANALYTICS DASHBOARD (SUPERADMIN ONLY) ==========
elif menu == "📈 Analytics":
    st.subheader("📈 Analytics Dashboard")
    st.info("👑 Visualisasi dan analisis data platform secara keseluruhan")
    
    import plotly.express as px
    import plotly.graph_objects as go
    
    # Load all data sources
    import os
    NPK_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "soil_map_npk_data.json")
    npk_soil_data = []
    if os.path.exists(NPK_DATA_FILE):
        try:
            with open(NPK_DATA_FILE, 'r') as f:
                npk_soil_data = json.load(f)
        except:
            npk_soil_data = []
    
    JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "..", "journal_data.json")
    journal_data = []
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, 'r') as f:
                journal_data = json.load(f)
        except:
            journal_data = []
    
    # ========== OVERVIEW CARDS ==========
    st.markdown("### 📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        commodities_count = len(st.session_state.get('commodities_db', []))
        st.metric("🌾 Komoditas", commodities_count)
    with col2:
        npk_count = len(npk_soil_data)
        st.metric("🗺️ Data NPK", npk_count)
    with col3:
        users_count = len(get_users())
        st.metric("👤 Users", users_count)
    with col4:
        activity_count = len(get_activity_log())
        st.metric("📝 Activities", activity_count)
    
    st.markdown("---")
    
    # ========== PIE CHARTS ==========
    st.markdown("### 🥧 Komposisi Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Commodity Categories Pie
        commodities = st.session_state.get('commodities_db', [])
        if commodities:
            categories = {}
            for c in commodities:
                cat = c.get('category', 'Lainnya')
                categories[cat] = categories.get(cat, 0) + 1
            
            fig = px.pie(
                values=list(categories.values()),
                names=list(categories.keys()),
                title="📦 Distribusi Komoditas per Kategori",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data komoditas")
    
    with col2:
        # User Roles Pie
        users = get_users()
        if users:
            roles = {}
            for u, data in users.items():
                role = data.get('role', 'user')
                roles[role] = roles.get(role, 0) + 1
            
            fig = px.pie(
                values=list(roles.values()),
                names=list(roles.keys()),
                title="👥 Distribusi User per Role",
                color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data user")
    
    st.markdown("---")
    
    # ========== BAR CHARTS ==========
    st.markdown("### 📊 Perbandingan Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # NPK Values Bar Chart
        if npk_soil_data:
            n_values = [d.get('n_value', 0) for d in npk_soil_data]
            p_values = [d.get('p_value', 0) for d in npk_soil_data]
            k_values = [d.get('k_value', 0) for d in npk_soil_data]
            
            fig = go.Figure(data=[
                go.Bar(name='N (ppm)', x=['Rata-rata', 'Max', 'Min'], 
                       y=[sum(n_values)/len(n_values), max(n_values), min(n_values)],
                       marker_color='#3b82f6'),
                go.Bar(name='P (ppm)', x=['Rata-rata', 'Max', 'Min'], 
                       y=[sum(p_values)/len(p_values), max(p_values), min(p_values)],
                       marker_color='#10b981'),
                go.Bar(name='K (ppm)', x=['Rata-rata', 'Max', 'Min'], 
                       y=[sum(k_values)/len(k_values), max(k_values), min(k_values)],
                       marker_color='#f59e0b')
            ])
            fig.update_layout(
                title="🧪 Statistik Nilai NPK",
                barmode='group',
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data NPK")
    
    with col2:
        # Activity Types Bar Chart
        activity_log = get_activity_log()
        if activity_log:
            actions = {}
            for a in activity_log:
                action = a.get('action', 'OTHER')
                actions[action] = actions.get(action, 0) + 1
            
            fig = px.bar(
                x=list(actions.keys()),
                y=list(actions.values()),
                title="📝 Aktivitas per Tipe",
                labels={'x': 'Tipe Aksi', 'y': 'Jumlah'},
                color=list(actions.keys()),
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data aktivitas")
    
    st.markdown("---")
    
    # ========== TREND CHARTS ==========
    st.markdown("### 📈 Trend Over Time")
    
    # Activity Trend
    activity_log = get_activity_log()
    if activity_log:
        # Group by date
        from collections import defaultdict
        daily_counts = defaultdict(int)
        for a in activity_log:
            timestamp = a.get('timestamp', '')
            if timestamp:
                date_part = timestamp[:10]  # YYYY-MM-DD
                daily_counts[date_part] += 1
        
        if daily_counts:
            dates = sorted(daily_counts.keys())
            counts = [daily_counts[d] for d in dates]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, 
                y=counts,
                mode='lines+markers',
                name='Aktivitas',
                line=dict(color='#10b981', width=3),
                marker=dict(size=10)
            ))
            fig.update_layout(
                title="📊 Trend Aktivitas Harian",
                xaxis_title="Tanggal",
                yaxis_title="Jumlah Aktivitas",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data trend. Data akan muncul setelah ada aktivitas login/logout.")
    
    # NPK Trend (if data has dates)
    if npk_soil_data:
        # Check if data has created_at
        has_dates = any('created_at' in d for d in npk_soil_data)
        if has_dates:
            from collections import defaultdict
            npk_by_date = defaultdict(lambda: {'n': [], 'p': [], 'k': []})
            
            for d in npk_soil_data:
                created = d.get('created_at', '')
                if created:
                    date_part = created[:10]
                    npk_by_date[date_part]['n'].append(d.get('n_value', 0))
                    npk_by_date[date_part]['p'].append(d.get('p_value', 0))
                    npk_by_date[date_part]['k'].append(d.get('k_value', 0))
            
            if npk_by_date:
                dates = sorted(npk_by_date.keys())
                n_avg = [sum(npk_by_date[d]['n'])/len(npk_by_date[d]['n']) for d in dates]
                p_avg = [sum(npk_by_date[d]['p'])/len(npk_by_date[d]['p']) for d in dates]
                k_avg = [sum(npk_by_date[d]['k'])/len(npk_by_date[d]['k']) for d in dates]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=n_avg, mode='lines+markers', name='N (ppm)', line=dict(color='#3b82f6')))
                fig.add_trace(go.Scatter(x=dates, y=p_avg, mode='lines+markers', name='P (ppm)', line=dict(color='#10b981')))
                fig.add_trace(go.Scatter(x=dates, y=k_avg, mode='lines+markers', name='K (ppm)', line=dict(color='#f59e0b')))
                
                fig.update_layout(
                    title="🗺️ Trend Rata-rata NPK per Hari",
                    xaxis_title="Tanggal",
                    yaxis_title="Nilai (ppm)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========== DATA SUMMARY TABLE ==========
    st.markdown("### 📋 Ringkasan Data")
    
    summary_data = [
        {"Database": "🌾 Komoditas", "Total Records": len(st.session_state.get('commodities_db', [])), "Status": "✅ Active"},
        {"Database": "💰 Harga Manual", "Total Records": len(st.session_state.get('manual_prices_db', [])), "Status": "✅ Active"},
        {"Database": "🗺️ NPK Soil Map", "Total Records": len(npk_soil_data), "Status": "✅ Active"},
        {"Database": "📓 Journal", "Total Records": len(journal_data), "Status": "✅ Active"},
        {"Database": "📝 Audit Log", "Total Records": len(st.session_state.get('audit_log_db', [])), "Status": "✅ Active"},
        {"Database": "👥 User Activity", "Total Records": len(get_activity_log()), "Status": "✅ Active"},
        {"Database": "👤 Users", "Total Records": len(get_users()), "Status": "✅ Active"},
    ]
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
