import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Control Room & Jurnal Harian", page_icon="📓", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== CONFIG & PATHS ==========
DATA_DIR = "data"
JOURNAL_FILE = os.path.join(DATA_DIR, "activity_journal.csv")
GROWTH_FILE = os.path.join(DATA_DIR, "growth_journal.csv")
COST_FILE = os.path.join(DATA_DIR, "cost_journal.csv")

# ========== DESIGN SYSTEM (Premium Glassmorphism) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    * { font-family: 'Outfit', sans-serif; }

    .main { background-color: #f8fafc; }

    .header-container {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        padding: 3rem 2rem; border-radius: 0 0 40px 40px;
        color: white; margin-bottom: 2rem; text-align: center;
        box-shadow: 0 15px 30px -10px rgba(6, 78, 59, 0.3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px; padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover { transform: translateY(-5px); }

    .kpi-card {
        background: white; border-radius: 20px; padding: 22px;
        border: 1px solid #e2e8f0; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #064e3b; line-height: 1; }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 8px; }

    .module-card {
        background: white; border-radius: 20px; padding: 20px;
        border-left: 6px solid #10b981; margin-bottom: 15px;
        display: flex; align-items: center; gap: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .module-icon { font-size: 2rem; }
    .module-info h4 { margin: 0; color: #1e293b; }
    .module-info p { margin: 0; font-size: 0.85rem; color: #64748b; }

    .metric-pill {
        display: inline-block;
        background: #ecfdf5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA STRUCTURES ---
COMMODITY_PARAMS = {
    "Padi Inpari": {"basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"], "specific": ["jumlah_anakan", "panjang_malai_cm", "persen_pengisian"], "stages": ["Vegetatif", "Primordia", "Berbunga", "Pengisian Bulir", "Masak"], "Tb": 10, "target_gdd": 1200},
    "Jagung Hibrida": {"basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"], "specific": ["jumlah_tongkol", "baris_biji", "panjang_tongkol_cm"], "stages": ["Vegetatif", "Tasseling", "Silking", "Pengisian Biji", "Masak Fisiologis"], "Tb": 10, "target_gdd": 1400},
    "Cabai Rawit": {"basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"], "specific": ["jumlah_buah", "panjang_buah_cm", "diameter_buah_mm"], "stages": ["Vegetatif", "Berbunga", "Berbuah Muda", "Berbuah Matang", "Panen"], "Tb": 15, "target_gdd": 1800}
}
COST_CATEGORIES = {
    "🌱 Benih/Bibit": ["Benih Hibrida", "Benih Lokal", "Bibit", "Lainnya"],
    "💊 Pupuk": ["Urea", "NPK", "TSP/SP36", "KCl", "Organik", "Hayati", "Lainnya"],
    "🛡️ Pestisida": ["Insektisida", "Fungisida", "Herbisida", "Nabati", "Lainnya"],
    "👷 Tenaga Kerja": ["Keluarga", "Harian", "Borongan", "Lainnya"]
}

# --- DATA HELPERS ---
def init_all_data():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    for f in [JOURNAL_FILE, GROWTH_FILE, COST_FILE]:
        if not os.path.exists(f): pd.DataFrame().to_csv(f, index=False)

def load_journal():
    try:
        return pd.read_csv(JOURNAL_FILE) if os.path.exists(JOURNAL_FILE) else pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def load_growth():
    try:
        return pd.read_csv(GROWTH_FILE) if os.path.exists(GROWTH_FILE) else pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def load_costs():
    try:
        return pd.read_csv(COST_FILE) if os.path.exists(COST_FILE) else pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def save_activity(data):
    df = load_journal()
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pd.concat([df, pd.DataFrame([data])], ignore_index=True).to_csv(JOURNAL_FILE, index=False)

def save_growth(data):
    df = load_growth()
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pd.concat([df, pd.DataFrame([data])], ignore_index=True).to_csv(GROWTH_FILE, index=False)

def save_cost(data):
    df = load_costs()
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pd.concat([df, pd.DataFrame([data])], ignore_index=True).to_csv(COST_FILE, index=False)

# --- MAIN UI ---
def main():
    init_all_data()

    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:3rem;">🛸 AgriSensa Control Room</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:1.2rem; font-weight:300;">
            Central Monitoring, Activity Ledger & Strategic Analytics v2.0
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_dash, tab_activity, tab_growth, tab_timeline, tab_analytics = st.tabs([
        "🛸 Command Center", "📝 Input Aktivitas", "📏 Pantau Pertumbuhan", "📅 Timeline & Review", "📊 Laporan Strategis"
    ])

    # Load data for real-time stats
    df_activities = load_journal()
    df_growth = load_growth()
    df_costs = load_costs()

    with tab_dash:
        st.subheader("🛸 Dashboard Monitoring Terpusat")
        
        # Top KPI bar
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{len(df_activities)}</div><div class="kpi-label">Total Aktivitas</div></div>""", unsafe_allow_html=True)
        with col2:
            avg_height = df_growth['tinggi_cm'].mean() if not df_growth.empty and 'tinggi_cm' in df_growth else 0
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{avg_height:.1f} cm</div><div class="kpi-label">Rata-rata Tinggi</div></div>""", unsafe_allow_html=True)
        with col3:
            total_expense = df_costs['total'].sum() if not df_costs.empty and 'total' in df_costs else 0
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">Rp {total_expense/1e6:.1f}jt</div><div class="kpi-label">Total Pengeluaran</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">Normal</div><div class="kpi-label">Status Agroklimat</div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        c_left, c_right = st.columns([2, 1])
        
        with c_left:
            st.markdown("### 📅 Timeline Strategis (7 Hari Terakhir)")
            recent_acts = df_activities.sort_values('tanggal', ascending=False).head(5) if not df_activities.empty else pd.DataFrame()
            if not recent_acts.empty:
                for _, row in recent_acts.iterrows():
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; color:#64748b; font-size:0.8rem; font-weight:600;">
                            <span>{row['tanggal']}</span>
                            <span style="background:#10b981; color:white; padding:2px 8px; border-radius:10px;">{row['kategori']}</span>
                        </div>
                        <h4 style="margin:10px 0 5px 0; color:#0f172a;">{row['judul']}</h4>
                        <p style="margin:0; font-size:0.9rem; color:#475569;">{row['catatan']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada aktivitas tercatat. Mulai catat di tab 'Jurnal Aktivitas'.")

        with c_right:
            st.markdown("### ⚡ Pintasan Modul")
            shortcuts = [
                ("🌍 Soil Map v2.0", "Pantau nutrisi tanah & kelembaban real-time", "🗺️"),
                ("🔍 Diagnostik AI v2.0", "Analisis penyakit hara via Expert System", "🔍"),
                ("📦 Logistik v2.1", "Konversi pupuk & kalkulasi armada", "🛒"),
                ("💹 Analisis RAB", "Dashboard ROI & Kelayakan Usaha", "💰")
            ]
            for title, desc, icon in shortcuts:
                st.markdown(f"""
                <div class="module-card">
                    <div class="module-icon">{icon}</div>
                    <div class="module-info">
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 🔔 Alert & Notifikasi")
            st.warning("Diagnosa Terakhir: **Blas Padi (High Probability)**. Segera cek kondisi lahan Blok A.")
            st.info("Kebutuhan Pupuk: Stok Urea menipis untuk pemupukan susulan II.")

    with tab_activity:
        col_left, col_right = st.columns([1, 1])
        
        # --- ACTIVITY INPUT ---
        with col_left:
            st.subheader("📝 Catat Aktivitas Harian")
            
            with st.form("activity_form", clear_on_submit=True):
                act_date = st.date_input("📅 Tanggal", datetime.now())
                
                col_cat, col_loc = st.columns(2)
                with col_cat:
                    act_category = st.selectbox("Kategori", [
                        "✅ Umum", "💧 Penyiraman", "💊 Pemupukan", 
                        "🛡️ Pengendalian Hama", "🛠️ Perawatan", 
                        "🚜 Panen", "💰 Pembelian"
                    ])
                with col_loc:
                    act_location = st.text_input("Lokasi/Blok", placeholder="Blok A, Lahan 1")
                
                act_title = st.text_input("📌 Judul Aktivitas", placeholder="Contoh: Pemupukan NPK Fase Vegetatif")
                act_notes = st.text_area("📄 Catatan Detail", placeholder="Dosis, kondisi cuaca, kendala yang dihadapi...", height=100)
                
                col_pri, col_stat = st.columns(2)
                with col_pri:
                    act_priority = st.selectbox("Prioritas", ["Rendah", "Sedang", "Tinggi", "Kritis"])
                with col_stat:
                    act_status = st.selectbox("Status", ["Direncanakan", "Sedang Berjalan", "Selesai"])
                
                col_cost, col_cat_cost = st.columns(2)
                with col_cost:
                    act_cost = st.number_input("💰 Biaya (Rp)", min_value=0, step=1000, value=0)
                with col_cat_cost:
                    if act_cost > 0:
                        act_cost_cat = st.selectbox("Kategori Biaya", list(COST_CATEGORIES.keys()))
                    else:
                        act_cost_cat = ""
                
                submit_activity = st.form_submit_button("💾 Simpan Aktivitas", use_container_width=True, type="primary")
            
            if submit_activity:
                if act_title:
                    save_activity({
                        'tanggal': act_date.strftime("%Y-%m-%d"),
                        'kategori': act_category,
                        'judul': act_title,
                        'catatan': act_notes,
                        'biaya': act_cost,
                        'kategori_biaya': act_cost_cat,
                        'lokasi': act_location,
                        'prioritas': act_priority,
                        'status': act_status,
                        'foto_path': ""
                    })
                    st.success("✅ Aktivitas berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("❌ Judul aktivitas wajib diisi!")
    
    # --- GROWTH TRACKING INPUT ---
    with col_right:
        st.subheader("📏 Catat Pertumbuhan (Advanced)")
        
        with st.form("growth_form", clear_on_submit=True):
            growth_date = st.date_input("📅 Tanggal Pengukuran", datetime.now(), key="gdate")
            
            col_com, col_var = st.columns(2)
            with col_com:
                growth_commodity = st.selectbox("Komoditas", list(COMMODITY_PARAMS.keys()))
            with col_var:
                growth_variety = st.text_input("Varietas", placeholder="Contoh: Inpari 32")
            
            col_hst, col_loc = st.columns(2)
            with col_hst:
                growth_hst = st.number_input("Usia (HST)", min_value=1, value=1)
            with col_loc:
                growth_location = st.text_input("Lokasi", placeholder="Blok/Plot", key="gloc")
            
            st.markdown("**📊 Parameter Dasar**")
            col_p1, col_p2, col_p3 = st.columns(3)
            
            params = COMMODITY_PARAMS[growth_commodity]
            
            with col_p1:
                if "tinggi_cm" in params["basic"]:
                    growth_height = st.number_input("Tinggi (cm)", min_value=0.0, value=0.0, step=0.1)
                else:
                    growth_height = 0.0
            
            with col_p2:
                if "jumlah_daun" in params["basic"]:
                    growth_leaves = st.number_input("Jumlah Daun", min_value=0, value=0)
                else:
                    growth_leaves = 0
            
            with col_p3:
                if "diameter_batang_mm" in params["basic"]:
                    growth_diameter = st.number_input("Diameter Batang (mm)", min_value=0.0, value=0.0, step=0.1)
                elif "lebar_kanopi_cm" in params["basic"]:
                    growth_diameter = st.number_input("Lebar Kanopi (cm)", min_value=0.0, value=0.0, step=0.1)
                elif "lebar_daun_cm" in params["basic"]:
                    growth_diameter = st.number_input("Lebar Daun (cm)", min_value=0.0, value=0.0, step=0.1)
                else:
                    growth_diameter = 0.0
            
            st.markdown(f"**🎯 Parameter Spesifik {growth_commodity}**")
            specific_params = {}
            
            if len(params["specific"]) >= 3:
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    key1 = params["specific"][0]
                    specific_params[key1] = st.number_input(
                        key1.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
                with col_s2:
                    key2 = params["specific"][1]
                    specific_params[key2] = st.number_input(
                        key2.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
                with col_s3:
                    key3 = params["specific"][2]
                    specific_params[key3] = st.number_input(
                        key3.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
            
            st.markdown("**🔬 Parameter Lanjutan**")
            col_a1, col_a2, col_a3, col_a4 = st.columns(4)
            
            with col_a1:
                growth_spad = st.number_input("SPAD (0-99)", min_value=0.0, max_value=99.0, value=0.0, step=0.1)
            with col_a2:
                growth_disease = st.slider("Skor Penyakit", 0, 5, 0, help="0=Sehat, 5=Parah")
            with col_a3:
                growth_pest = st.slider("Skor Hama", 0, 5, 0, help="0=Tidak ada, 5=Parah")

            st.markdown("---")
            st.markdown("**🌡️ Hitung GDD (Thermal Time)**")
            col_t1, col_t2 = st.columns(2)
            with col_t1: t_max = st.number_input("Suhu Max (°C)", value=32.0, key="tmax")
            with col_t2: t_min = st.number_input("Suhu Min (°C)", value=24.0, key="tmin")
            gdd_today = max(0, (t_max + t_min)/2 - params.get('Tb', 10))
            st.caption(f"Estimasi GDD Hari Ini: **{gdd_today:.1f}**")

            submit_growth = st.form_submit_button("💾 Simpan Data Pertumbuhan", use_container_width=True, type="primary")
            
            if submit_growth:
                df_growth_all = load_growth()
                df_kom = df_growth_all[df_growth_all['komoditas'] == growth_commodity] if not df_growth_all.empty else pd.DataFrame()
                prev_gdd = df_kom['gdd_cumulative'].max() if not df_kom.empty and 'gdd_cumulative' in df_kom else 0.0
                
                param_str = json.dumps(specific_params)
                
                save_growth({
                    'tanggal': growth_date.strftime("%Y-%m-%d"),
                    'komoditas': growth_commodity,
                    'varietas': growth_variety,
                    'lokasi': growth_location,
                    'usia_hst': growth_hst,
                    'tinggi_cm': growth_height,
                    'jumlah_daun': growth_leaves,
                    'diameter_batang_mm': growth_diameter,
                    'lebar_kanopi_cm': 0.0,
                    'spad': growth_spad,
                    'stage': "Vegetatif",
                    'penyakit_score': growth_disease,
                    'hama_score': growth_pest,
                    'gdd_cumulative': prev_gdd + gdd_today,
                    'param_spesifik': param_str,
                    'catatan': "",
                    'foto_path': ""
                })
                st.success(f"✅ Data pertumbuhan {growth_commodity} berhasil disimpan!")
                st.rerun()
    
    # --- COST TRACKING INPUT ---
    st.divider()
    st.subheader("💰 Catat Pengeluaran Detail")
    
    with st.form("cost_form", clear_on_submit=True):
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1: cost_date = st.date_input("📅 Tanggal", datetime.now(), key="cdate")
        with col_c2: cost_category = st.selectbox("Kategori", list(COST_CATEGORIES.keys()), key="ccat")
        with col_c3: cost_subcategory = st.selectbox("Sub-Kategori", COST_CATEGORIES[cost_category])
        
        col_c4, col_c5, col_c6 = st.columns(3)
        with col_c4: cost_item = st.text_input("Nama Item", placeholder="Contoh: Urea 50kg")
        with col_c5: cost_qty = st.number_input("Jumlah", min_value=0.0, value=1.0, step=0.1)
        with col_c6: cost_unit = st.text_input("Satuan", placeholder="kg, liter, karung")
        
        col_c7, col_c8 = st.columns(2)
        with col_c7: cost_price = st.number_input("Harga Satuan (Rp)", min_value=0, step=100, value=0)
        with col_c8:
            cost_total = cost_qty * cost_price
            st.metric("Total Biaya", f"Rp {cost_total:,.0f}")
        
        col_c9, col_c10 = st.columns(2)
        with col_c9: cost_supplier = st.text_input("Supplier/Toko", placeholder="Nama toko/supplier")
        with col_c10: cost_location = st.text_input("Lokasi Penggunaan", placeholder="Blok/Lahan", key="cloc")
        
        cost_notes = st.text_area("Catatan", placeholder="Informasi tambahan...", height=60, key="cnotes")
        submit_cost = st.form_submit_button("💾 Simpan Pengeluaran", use_container_width=True, type="primary")
        
        if submit_cost:
            if cost_item and cost_total > 0:
                save_cost({
                    'tanggal': cost_date.strftime("%Y-%m-%d"),
                    'kategori_biaya': cost_category,
                    'sub_kategori': cost_subcategory,
                    'item': cost_item,
                    'jumlah': cost_qty,
                    'satuan': cost_unit,
                    'harga_satuan': cost_price,
                    'total': cost_total,
                    'supplier': cost_supplier,
                    'lokasi': cost_location,
                    'catatan': cost_notes
                })
                st.success(f"✅ Pengeluaran Rp {cost_total:,.0f} berhasil dicatat!")
                st.rerun()
            else:
                st.error("❌ Nama item dan total biaya harus diisi!")

# ========================================
# TAB 2: TIMELINE & REVIEW
# ========================================
    # ========================================
    # TAB 2: TIMELINE & REVIEW
    # ========================================
    with tab_timeline:
        st.subheader("📅 Timeline Aktivitas & Pertumbuhan")
        
        # Filters
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            filter_type = st.multiselect("Tipe Data", ["Aktivitas", "Pertumbuhan", "Pengeluaran"], default=["Aktivitas", "Pertumbuhan", "Pengeluaran"])
        
        with col_f2:
            if not df_activities.empty or not df_growth.empty:
                all_dates = []
                if not df_activities.empty: all_dates.extend(pd.to_datetime(df_activities['tanggal']).tolist())
                if not df_growth.empty: all_dates.extend(pd.to_datetime(df_growth['tanggal']).tolist())
                if all_dates:
                    min_d, max_d = min(all_dates).date(), max(all_dates).date()
                    date_range = st.date_input("Rentang Tanggal", value=(min_d, max_d), key="date_range")
                else: date_range = None
            else: date_range = None
        
        with col_f3: search_keyword = st.text_input("🔍 Cari Kata Kunci", placeholder="Cari judul, catatan...")
        with col_f4: sort_order = st.selectbox("Urutan", ["Terbaru", "Terlama"])
        
        st.divider()
        
        timeline = []
        if "Aktivitas" in filter_type and not df_activities.empty:
            for _, row in df_activities.iterrows():
                timeline.append({
                    'date': pd.to_datetime(row['tanggal']), 'raw_date': row['tanggal'],
                    'type': 'activity', 'title': row['judul'], 'desc': row['catatan'],
                    'meta': row['kategori'], 'cost': row['biaya'] if pd.notna(row['biaya']) else 0,
                    'location': row.get('lokasi', ''), 'priority': row.get('prioritas', ''),
                    'status': row.get('status', ''), 'style': 'expense' if row['biaya'] > 0 else 'journal-card'
                })
        
        if "Pertumbuhan" in filter_type and not df_growth.empty:
            for _, row in df_growth.iterrows():
                timeline.append({
                    'date': pd.to_datetime(row['tanggal']), 'raw_date': row['tanggal'],
                    'type': 'growth', 'title': f"Monitoring {row['komoditas']}",
                    'desc': row['tinggi_cm'], 'meta': f"HST {row['usia_hst']}", # Store value directly
                    'cost': 0, 'location': row.get('lokasi', ''), 'priority': '',
                    'status': '', 'style': 'growth'
                })

        if "Pengeluaran" in filter_type and not df_costs.empty:
            for _, row in df_costs.iterrows():
                timeline.append({
                    'date': pd.to_datetime(row['tanggal']), 'raw_date': row['tanggal'],
                    'type': 'cost', 'title': f"{row['item']}", 'desc': f"{row['kategori_biaya']}",
                    'meta': row.get('supplier', ''), 'cost': row['total'],
                    'location': row.get('lokasi', ''), 'priority': '', 'status': '', 'style': 'cost'
                })
        
        if date_range and len(date_range) == 2:
            timeline = [t for t in timeline if date_range[0] <= t['date'].date() <= date_range[1]]
        
        if search_keyword:
            timeline = [t for t in timeline if search_keyword.lower() in t['title'].lower() or search_keyword.lower() in str(t['desc']).lower()]
        
        timeline.sort(key=lambda x: x['date'], reverse=(sort_order == "Terbaru"))
        
        if timeline:
            import re
            def strip_html(text):
                if not isinstance(text, str): return text
                return re.sub('<[^<]+?>', '', text)

            for item in timeline:
                with st.container():
                    # Header Row: Date and Cost
                    c_h1, c_h2 = st.columns([3, 1])
                    with c_h1:
                        st.caption(f"📅 {item['raw_date']} | 🏷️ {strip_html(str(item['meta']))}")
                    with c_h2:
                        if item['cost'] > 0:
                            st.markdown(f"<p style='text-align:right; color:#ef4444; font-weight:bold; margin:0;'>Rp {item['cost']:,.0f}</p>", unsafe_allow_html=True)
                    
                    # Title and Main Content
                    icon = "📝" if item['type'] == 'activity' else "📈" if item['type'] == 'growth' else "💰"
                    st.markdown(f"#### {icon} {strip_html(str(item['title']))}")
                    
                    if item['type'] == 'growth':
                        val = strip_html(str(item['desc']))
                        st.success(f"📏 Tinggi Tanaman: {val} cm")
                    else:
                        st.write(strip_html(str(item['desc'])))
                    
                    if item.get('location'):
                        st.caption(f"📍 Lokasi: {strip_html(str(item['location']))}")
                    
                    st.divider()
        else:
            st.info("Belum ada data yang sesuai filter.")

    # ========================================
    # TAB 3: ANALYTICS & REPORTS
    # ========================================
    with tab_analytics:
        st.subheader("📊 Analytics Dashboard & Reports")
        
        # --- COST ANALYTICS ---
        st.markdown("### 💰 Analisis Biaya")
        if not df_costs.empty:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig_pie = px.pie(df_costs.groupby('kategori_biaya')['total'].sum().reset_index(), values='total', names='kategori_biaya', title='📊 Distribusi Kategori Biaya')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_chart2:
                df_temp = df_costs.copy()
                df_temp['tanggal'] = pd.to_datetime(df_temp['tanggal'])
                daily_costs = df_temp.groupby('tanggal')['total'].sum().reset_index()
                fig_time = px.line(daily_costs, x='tanggal', y='total', title='📈 Tren Pengeluaran', markers=True)
                st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("Belum ada data biaya untuk dianalisis.")
        
        st.divider()

        # --- GROWTH ANALYTICS ---
        st.markdown("### 📈 Analisis Pertumbuhan & Lingkungan (GDD)")
        if not df_growth.empty:
            commodities = df_growth['komoditas'].unique()
            sel_kom = st.selectbox("Pilih Komoditas", commodities)
            df_kom = df_growth[df_growth['komoditas'] == sel_kom].sort_values('usia_hst')
            
            # Correlation Chart: Height vs GDD
            from plotly.subplots import make_subplots
            fig_corr = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig_corr.add_trace(
                go.Scatter(x=df_kom['usia_hst'], y=df_kom['tinggi_cm'], name="Tinggi (cm)", line=dict(color='#10b981', width=4)),
                secondary_y=False,
            )
            
            if 'gdd_cumulative' in df_kom.columns:
                fig_corr.add_trace(
                    go.Scatter(x=df_kom['usia_hst'], y=df_kom['gdd_cumulative'], name="GDD Kumulatif", line=dict(color='#f59e0b', width=2, dash='dot')),
                    secondary_y=True,
                )
            
            fig_corr.update_layout(
                title=dict(text=f"Korelasi Pertumbuhan vs Thermal Time (GDD) - {sel_kom}"),
                xaxis=dict(title=dict(text="Usia (HST)")),
                yaxis=dict(title=dict(text="Tinggi Tanaman (cm)", font=dict(color="#10b981")), tickfont=dict(color="#10b981")),
                yaxis2=dict(title=dict(text="GDD Kumulatif", font=dict(color="#f59e0b")), tickfont=dict(color="#f59e0b")),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Growth Stage Visualization
            st.info(f"💡 **Insight**: Akumulasi GDD saat ini adalah **{df_kom['gdd_cumulative'].max() if 'gdd_cumulative' in df_kom else 0:.1f}**. Pantau apakah kecepatan pertumbuhan sesuai dengan target termal varietas.")
        else:
            st.info("Belum ada data pertumbuhan untuk dianalisis.")
        
        st.divider()
        
        # --- EXPORT SECTION ---
        st.markdown("### 📥 Export Data")
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            if not df_activities.empty: st.download_button("📄 Download Aktivitas (CSV)", df_activities.to_csv(index=False).encode('utf-8'), "aktivitas.csv", "text/csv")
        with col_e2:
            if not df_growth.empty: st.download_button("📊 Download Pertumbuhan (CSV)", df_growth.to_csv(index=False).encode('utf-8'), "pertumbuhan.csv", "text/csv")
        with col_e3:
            if not df_costs.empty: st.download_button("💰 Download Pengeluaran (CSV)", df_costs.to_csv(index=False).encode('utf-8'), "pengeluaran.csv", "text/csv")

if __name__ == "__main__":
    main()
