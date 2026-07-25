# Fertilizer Logistics & Conversion v2.0
# Advanced Nutrient-to-Weight Engine & Organic Logistics

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Konversi & Logistik Pupuk", page_icon="🔄", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATA & CONFIGURATION ==========
DEFAULT_DATABASE = {
    "Urea": {"N": 46.0, "P": 0.0, "K": 0.0, "price": 2500, "type": "anorganik", "color": "#3b82f6"},
    "SP-36": {"N": 0.0, "P": 36.0, "K": 0.0, "price": 3000, "type": "anorganik", "color": "#10b981"},
    "KCl / MOP": {"N": 0.0, "P": 0.0, "K": 60.0, "price": 3500, "type": "anorganik", "color": "#f59e0b"},
    "ZA": {"N": 21.0, "P": 0.0, "K": 0.0, "price": 2200, "type": "anorganik", "color": "#06b6d4"},
    "NPK 15-15-15": {"N": 15.0, "P": 15.0, "K": 15.0, "price": 4000, "type": "anorganik", "color": "#8b5cf6"},
    "NPK 16-16-16": {"N": 16.0, "P": 16.0, "K": 16.0, "price": 4200, "type": "anorganik", "color": "#ec4899"},
    "TSP 46": {"N": 0.0, "P": 46.0, "K": 0.0, "price": 3800, "type": "anorganik", "color": "#14b8a6"},
    "Pupuk Kandang (Sapi)": {"N": 0.5, "P": 0.2, "K": 0.5, "price": 800, "type": "organik", "density": 0.5, "color": "#84cc16"},
    "Pupuk Kandang (Ayam)": {"N": 1.5, "P": 1.0, "K": 0.8, "price": 1200, "type": "organik", "density": 0.6, "color": "#65a30d"},
    "Kompos Matang": {"N": 1.2, "P": 0.8, "K": 1.2, "price": 1500, "type": "organik", "density": 0.55, "color": "#4d7c0f"},
    "Guano": {"N": 10.0, "P": 12.0, "K": 2.0, "price": 5000, "type": "organik", "density": 0.8, "color": "#166534"}
}

TRANSPORT_PROFILES = {
    "Motor / Pick-up Kecil": {"vol": 1.0, "weight": 800, "icon": "🛵"},
    "L300 / Carry": {"vol": 2.5, "weight": 1500, "icon": "🚐"},
    "Colt Diesel (Engkel)": {"vol": 6.0, "weight": 4000, "icon": "🚚"},
    "Truk Double (6 Ban)": {"vol": 9.0, "weight": 8000, "icon": "🚛"},
    "Fuso / Tronton": {"vol": 20.0, "weight": 15000, "icon": "🚢"}
}

# ========== DESIGN SYSTEM ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem 2rem; border-radius: 0 0 30px 30px;
        color: white; margin-bottom: 2rem; text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .kpi-card { background: white; border-radius: 18px; padding: 20px; border: 1px solid #e2e8f0; text-align: center; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #0f172a; }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.5rem;">🔄 Logistik & Konversi v2.1</h1>
        <p style="margin:5px 0 0 0; opacity:0.9;">Fertilizer Command Center: Precise Nutrient Math & Logistics ROI</p>
    </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR: EDITABLE DATABASE ---
    st.sidebar.header("⚙️ Kustomisasi Pupuk")
    st.sidebar.info("Modifikasi kadar hara dan harga pupuk untuk menyesuaikan dengan kondisi lokal.")
    
    custom_db = {}
    for name, info in DEFAULT_DATABASE.items():
        with st.sidebar.expander(f"📝 {name}", expanded=False):
            c_price = st.number_input(f"Harga (Rp/kg)", value=int(info['price']), key=f"p_{name}")
            c_n = st.number_input(f"N (%)", value=float(info['N']), key=f"n_{name}")
            c_p = st.number_input(f"P (%)", value=float(info['P']), key=f"p_n_{name}")
            c_k = st.number_input(f"K (%)", value=float(info['K']), key=f"k_{name}")
            custom_db[name] = {**info, "price": c_price, "N": c_n, "P": c_p, "K": c_k}

    menu = st.sidebar.selectbox("Navigasi Modul", ["🎯 Nutrient-to-Weight Engine", "🚚 Logistik & Armada", "💰 ROI Harga Satuan"])
    st.sidebar.divider()
    global_buffer = st.sidebar.slider("Buffer Cadangan (%)", 0, 20, 5)

    if menu == "🎯 Nutrient-to-Weight Engine":
        st.subheader("🎯 Konversi Kebutuhan Hara")
        st.info("💡 Masukkan target Nitrogen, Fosfor, atau Kalium untuk melihat kebutuhan berbagai jenis pupuk.")
        
        col_n, col_p, col_k = st.columns(3)
        with col_n: req_n = st.number_input("Target Nitrogen (kg N)", min_value=0.0, value=100.0)
        with col_p: req_p = st.number_input("Target Fosfor (kg P)", min_value=0.0, value=50.0)
        with col_k: req_k = st.number_input("Target Kalium (kg K)", min_value=0.0, value=50.0)
        
        comparison_data = []
        for name, info in custom_db.items():
            w_n = (req_n / (info['N'] / 100)) if info['N'] > 0 else float('inf')
            w_p = (req_p / (info['P'] / 100)) if info['P'] > 0 else float('inf')
            w_k = (req_k / (info['K'] / 100)) if info['K'] > 0 else float('inf')
            
            # Select relevant weight
            if req_n > 0 and info['N'] > 0: target_weight = w_n
            elif req_p > 0 and info['P'] > 0: target_weight = w_p
            elif req_k > 0 and info['K'] > 0: target_weight = w_k
            elif 'NPK' in name: target_weight = max(w_n if req_n > 0 else 0, w_p if req_p > 0 else 0, w_k if req_k > 0 else 0)
            else: target_weight = 0
            
            if 0 < target_weight < float('inf'):
                final_weight = target_weight * (1 + global_buffer/100)
                comparison_data.append({
                    "Pupuk": name,
                    "Kadar Terpakai": f"N:{info['N']}% P:{info['P']}% K:{info['K']}%",
                    "Berat (kg)": round(final_weight, 1),
                    "Karung (50kg)": round(final_weight / 50, 1),
                    "Biaya (Rp)": f"Rp {final_weight * info['price']:,.0f}"
                })
        
        if comparison_data:
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
            fig = go.Figure(go.Bar(x=[d['Pupuk'] for d in comparison_data], y=[d['Berat (kg)'] for d in comparison_data], marker_color='#3b82f6'))
            fig.update_layout(title="Perbandingan Berat Pupuk ke Target Hara", height=400)
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "🚚 Logistik & Armada":
        st.subheader("🚚 Perencanaan Logistik")
        col_l, col_r = st.columns(2)
        with col_l:
            fert_choice = st.selectbox("Pilih Pupuk", options=list(custom_db.keys()))
            total_mass = st.number_input("Total Berat (kg)", min_value=0, value=5000)
            density = custom_db[fert_choice].get('density', 0.8)
            total_vol = (total_mass / 1000) / density
        with col_r:
            transport_choice = st.selectbox("Pilih Armada", options=list(TRANSPORT_PROFILES.keys()))
            profile = TRANSPORT_PROFILES[transport_choice]
            num_trips = int(max(total_vol / profile['vol'], total_mass / profile['weight'])) + (1 if max(total_vol / profile['vol'], total_mass / profile['weight']) % 1 > 0 else 0)
            
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Volume (m³)", f"{total_vol:.1f}")
        with c2: st.metric("Jumlah Armada", f"{num_trips} {profile['icon']}")
        with c3: st.metric("Biaya Pupuk", f"Rp {total_mass * custom_db[fert_choice]['price']:,.0f}")

    elif menu == "💰 ROI Harga Satuan":
        st.subheader("💰 Efisiensi Biaya per Satuan Hara")
        st.markdown("Menghitung harga riil yang Anda bayar untuk setiap **1% nutrisi dalam 1 kg pupuk**.")
        roi_data = []
        for name, info in custom_db.items():
            total_nutrients = info['N'] + info['P'] + info['K']
            if total_nutrients > 0:
                roi_data.append({"Pupuk": name, "Nutrisi (%)": total_nutrients, "Harga/kg": info['price'], "Biaya per Unit Hara": round((info['price'] / total_nutrients), 2)})
        st.table(pd.DataFrame(roi_data).sort_values("Biaya per Unit Hara"))

if __name__ == "__main__":
    main()
