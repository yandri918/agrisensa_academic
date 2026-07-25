# Analisis NPK Advanced - Scientific Approach
# Input dan analisis data NPK tanah dengan rekomendasi pupuk berbasis ilmiah

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime
import uuid

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Analisis NPK Advanced", page_icon="📊", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATA STORAGE ==========
NPK_ANALYSIS_FILE = "data/npk_analysis_records.json"

def load_records():
    if os.path.exists(NPK_ANALYSIS_FILE):
        with open(NPK_ANALYSIS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_records(records):
    os.makedirs(os.path.dirname(NPK_ANALYSIS_FILE), exist_ok=True)
    with open(NPK_ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# ========== SCIENTIFIC THRESHOLDS (Balitbang Indonesia) ==========
BALITBANG_THRESHOLDS = {
    'n_total': {  # % (persen)
        'unit': '%',
        'thresholds': [0.1, 0.2, 0.5, 0.75],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 0.3
    },
    'p_bray': {  # ppm (Bray-1 method)
        'unit': 'ppm',
        'thresholds': [4, 7, 10, 15],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 12
    },
    'p_olsen': {  # ppm (Olsen method - for alkaline soils)
        'unit': 'ppm',
        'thresholds': [5, 10, 15, 20],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 15
    },
    'k_dd': {  # cmol(+)/kg (dapat ditukar)
        'unit': 'cmol(+)/kg',
        'thresholds': [0.1, 0.2, 0.5, 1.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 0.4
    },
    'ca_dd': {  # cmol(+)/kg
        'unit': 'cmol(+)/kg',
        'thresholds': [2, 5, 10, 20],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 8
    },
    'mg_dd': {  # cmol(+)/kg
        'unit': 'cmol(+)/kg',
        'thresholds': [0.3, 1.0, 2.0, 8.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 1.5
    },
    'cec': {  # cmol(+)/kg (Cation Exchange Capacity)
        'unit': 'cmol(+)/kg',
        'thresholds': [5, 16, 24, 40],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 20
    },
    'c_organic': {  # %
        'unit': '%',
        'thresholds': [1.0, 2.0, 4.2, 6.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 3.0
    },
    # ========== MICRONUTRIENTS ==========
    'fe': {  # ppm (DTPA extractable)
        'unit': 'ppm',
        'thresholds': [2.5, 4.5, 10.0, 20.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 6.0
    },
    'mn': {  # ppm (DTPA extractable)
        'unit': 'ppm',
        'thresholds': [1.0, 2.0, 5.0, 15.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 5.0
    },
    'cu': {  # ppm (DTPA extractable)
        'unit': 'ppm',
        'thresholds': [0.1, 0.2, 0.5, 1.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 0.3
    },
    'zn': {  # ppm (DTPA extractable)
        'unit': 'ppm',
        'thresholds': [0.5, 1.0, 2.0, 5.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 1.5
    },
    'b': {  # ppm (Hot water extractable)
        'unit': 'ppm',
        'thresholds': [0.2, 0.5, 1.0, 2.0],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 0.8
    },
    'mo': {  # ppm
        'unit': 'ppm',
        'thresholds': [0.05, 0.1, 0.2, 0.5],
        'labels': ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'],
        'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#14b8a6'],
        'optimal': 0.15
    }
}

# pH Availability data (relative availability %)
PH_AVAILABILITY = {
    'pH': [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
    'N': [20, 40, 60, 80, 95, 100, 100, 95, 85, 70, 50],
    'P': [30, 35, 45, 70, 95, 100, 95, 80, 60, 40, 25],
    'K': [60, 70, 85, 95, 100, 100, 100, 95, 90, 80, 70],
    'Ca': [30, 45, 65, 85, 95, 100, 100, 100, 100, 95, 90],
    'Mg': [30, 45, 65, 85, 95, 100, 100, 100, 100, 95, 90],
    'S': [70, 75, 85, 95, 100, 100, 100, 95, 85, 75, 60],
    'Fe': [100, 100, 95, 85, 70, 50, 30, 15, 5, 2, 1],
    'Mn': [100, 100, 90, 75, 55, 35, 20, 10, 5, 2, 1],
    'B': [60, 65, 75, 85, 95, 100, 100, 95, 85, 70, 55],
    'Cu': [85, 85, 80, 75, 70, 60, 50, 40, 30, 25, 20],
    'Zn': [90, 85, 75, 60, 45, 35, 25, 15, 10, 5, 3],
    'Mo': [10, 15, 25, 40, 60, 80, 95, 100, 100, 95, 90]
}

def classify_nutrient(value, nutrient_key):
    """Classify nutrient value based on Balitbang thresholds"""
    if nutrient_key not in BALITBANG_THRESHOLDS:
        return 'N/A', '#6b7280', 2
    
    thresholds = BALITBANG_THRESHOLDS[nutrient_key]['thresholds']
    labels = BALITBANG_THRESHOLDS[nutrient_key]['labels']
    colors = BALITBANG_THRESHOLDS[nutrient_key]['colors']
    
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            return labels[i], colors[i], i
    return labels[-1], colors[-1], len(thresholds)

def get_ph_availability(ph_value, nutrient):
    """Get nutrient availability at given pH"""
    ph_data = PH_AVAILABILITY['pH']
    nutrient_data = PH_AVAILABILITY.get(nutrient, [50]*len(ph_data))
    
    # Linear interpolation
    if ph_value <= ph_data[0]:
        return nutrient_data[0]
    if ph_value >= ph_data[-1]:
        return nutrient_data[-1]
    
    for i in range(len(ph_data) - 1):
        if ph_data[i] <= ph_value <= ph_data[i+1]:
            slope = (nutrient_data[i+1] - nutrient_data[i]) / (ph_data[i+1] - ph_data[i])
            return nutrient_data[i] + slope * (ph_value - ph_data[i])
    
    return 50


# ========== MAIN APP ==========
st.title("📊 Analisis NPK Advanced")
st.markdown("**Analisis Kesuburan Tanah Berbasis Standar Balitbang Indonesia**")

# Main Tabs
tab_input, tab_hasil, tab_ph, tab_sekunder, tab_mikro, tab_texture, tab_ai = st.tabs([
    "📝 Input Data Lab",
    "📊 Hasil Analisis",
    "🔬 pH & Ketersediaan",
    "🌿 Unsur Sekunder",
    "🔬 Mikronutrien",
    "🌍 Tekstur Tanah",
    "🤖 AI Rekomendasi"
])

# Initialize session state for NPK data
if 'npk_data' not in st.session_state:
    st.session_state.npk_data = {
        'analyzed': False,
        'n_total': 0.25,
        'p_bray': 10.0,
        'k_dd': 0.35,
        'ph': 6.5,
        'ca_dd': 6.0,
        'mg_dd': 1.2,
        'cec': 18.0,
        'c_organic': 2.5,
        'soil_type': 'Lempung',
        'area_ha': 1.0,
        'location': '',
        # Micronutrients
        'fe': 5.0,
        'mn': 3.0,
        'cu': 0.3,
        'zn': 1.0,
        'b': 0.5,
        'mo': 0.1,
        # Soil texture
        'sand': 40.0,
        'silt': 40.0,
        'clay': 20.0
    }

# ========== TAB 1: INPUT DATA ==========
with tab_input:
    st.subheader("📝 Input Hasil Uji Laboratorium")
    st.info("💡 Masukkan hasil uji lab tanah sesuai standar Balitbang. Semua analisis menggunakan metodologi standar nasional.")
    
    # Method selection
    method_col1, method_col2 = st.columns(2)
    with method_col1:
        p_method = st.radio("Metode Analisis P:", ["Bray-1 (pH < 7)", "Olsen (pH ≥ 7)"], horizontal=True)
    with method_col2:
        st.markdown("**Referensi:** Petunjuk Teknis Analisis Kimia Tanah (Balitbang, 2009)")
    
    st.divider()
    
    # Main inputs - 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧪 Unsur Makro Primer")
        
        n_total = st.number_input(
            "N-Total (%)",
            min_value=0.0, max_value=2.0, value=0.25, step=0.01,
            help="Range: 0-2%. Standar: 0.21-0.50 = Sedang"
        )
        
        if p_method == "Bray-1 (pH < 7)":
            p_value = st.number_input(
                "P-Tersedia (Bray-1) ppm",
                min_value=0.0, max_value=100.0, value=10.0, step=0.5,
                help="Range: 0-100 ppm. Standar: 8-10 = Sedang"
            )
            p_key = 'p_bray'
        else:
            p_value = st.number_input(
                "P-Tersedia (Olsen) ppm",
                min_value=0.0, max_value=100.0, value=12.0, step=0.5,
                help="Range: 0-100 ppm. Standar: 11-15 = Sedang"
            )
            p_key = 'p_olsen'
        
        k_dd = st.number_input(
            "K-dd (cmol(+)/kg)",
            min_value=0.0, max_value=5.0, value=0.35, step=0.05,
            help="Range: 0-5. Standar: 0.21-0.50 = Sedang"
        )
    
    with col2:
        st.markdown("### 🌱 Parameter Pendukung")
        
        ph_value = st.number_input(
            "pH Tanah (H₂O)",
            min_value=3.0, max_value=10.0, value=6.5, step=0.1,
            help="Optimal: 6.0-7.0 untuk sebagian besar tanaman"
        )
        
        c_organic = st.number_input(
            "C-Organik (%)",
            min_value=0.0, max_value=15.0, value=2.5, step=0.1,
            help="Range: 0-15%. Standar: 2.1-4.2 = Sedang"
        )
        
        cec = st.number_input(
            "KTK/CEC (cmol(+)/kg)",
            min_value=0.0, max_value=100.0, value=18.0, step=1.0,
            help="Kapasitas Tukar Kation. Standar: 17-24 = Sedang"
        )
    
    with col3:
        st.markdown("### 🌿 Unsur Sekunder")
        
        ca_dd = st.number_input(
            "Ca-dd (cmol(+)/kg)",
            min_value=0.0, max_value=50.0, value=6.0, step=0.5,
            help="Range: 0-50. Standar: 6-10 = Sedang"
        )
        
        mg_dd = st.number_input(
            "Mg-dd (cmol(+)/kg)",
            min_value=0.0, max_value=20.0, value=1.2, step=0.1,
            help="Range: 0-20. Standar: 1.1-2.0 = Sedang"
        )
        
        s_value = st.number_input(
            "S-Tersedia (ppm)",
            min_value=0.0, max_value=100.0, value=15.0, step=1.0,
            help="Range: 0-100 ppm. Kritis: <10 ppm"
        )
    
    st.divider()
    
    # Additional info
    add_col1, add_col2, add_col3 = st.columns(3)
    
    with add_col1:
        soil_type = st.selectbox(
            "Jenis Tanah",
            ["Lempung", "Lempung Berpasir", "Lempung Berliat", "Pasir", "Liat", "Gambut"]
        )
    
    with add_col2:
        location = st.text_input("Lokasi Sampel", placeholder="Desa, Kecamatan, Kabupaten")
    
    with add_col3:
        area_ha = st.number_input("Luas Lahan (ha)", min_value=0.01, value=1.0, step=0.1)
    
    # Analyze Button
    st.divider()
    if st.button("🔬 Analisis Lengkap", type="primary", use_container_width=True):
        # Save to session state
        st.session_state.npk_data = {
            'analyzed': True,
            'n_total': n_total,
            'p_value': p_value,
            'p_key': p_key,
            'k_dd': k_dd,
            'ph': ph_value,
            'ca_dd': ca_dd,
            'mg_dd': mg_dd,
            's_value': s_value,
            'cec': cec,
            'c_organic': c_organic,
            'soil_type': soil_type,
            'area_ha': area_ha,
            'location': location
        }
        st.success("✅ Data tersimpan! Lihat hasil di tab **📊 Hasil Analisis**")
        st.balloons()

# ========== TAB 2: HASIL ANALISIS ==========
with tab_hasil:
    st.subheader("📊 Hasil Analisis Kesuburan Tanah")
    
    if not st.session_state.npk_data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Silakan input data di tab **📝 Input Data Lab** terlebih dahulu.")
    else:
        data = st.session_state.npk_data
        
        st.info(f"📍 Lokasi: **{data.get('location', 'Tidak diketahui')}** | 📐 Luas: **{data.get('area_ha', 1)} ha** | 🏔️ Jenis Tanah: **{data.get('soil_type', 'Unknown')}**")
        
        # Classification results
        st.markdown("### 🎯 Klasifikasi Unsur Hara (Standar Balitbang)")
        
        # NPK Primary
        npk_col1, npk_col2, npk_col3 = st.columns(3)
        
        with npk_col1:
            n_label, n_color, n_idx = classify_nutrient(data['n_total'], 'n_total')
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid {n_color};">
                <h3 style="margin:0; color: #1e40af;">🔵 Nitrogen (N)</h3>
                <p style="font-size: 2rem; font-weight: 700; color: {n_color}; margin: 0.5rem 0;">
                    {data['n_total']:.2f}%
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong style="color: {n_color};">{n_label}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with npk_col2:
            p_key = data.get('p_key', 'p_bray')
            p_label, p_color, p_idx = classify_nutrient(data['p_value'], p_key)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid {p_color};">
                <h3 style="margin:0; color: #065f46;">🟢 Fosfor (P)</h3>
                <p style="font-size: 2rem; font-weight: 700; color: {p_color}; margin: 0.5rem 0;">
                    {data['p_value']:.1f} ppm
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong style="color: {p_color};">{p_label}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with npk_col3:
            k_label, k_color, k_idx = classify_nutrient(data['k_dd'], 'k_dd')
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        padding: 1.5rem; border-radius: 12px; border-left: 5px solid {k_color};">
                <h3 style="margin:0; color: #92400e;">🟡 Kalium (K)</h3>
                <p style="font-size: 2rem; font-weight: 700; color: {k_color}; margin: 0.5rem 0;">
                    {data['k_dd']:.2f} cmol/kg
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong style="color: {k_color};">{k_label}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Supporting Parameters
        st.markdown("### 📈 Parameter Pendukung")
        
        supp_col1, supp_col2, supp_col3, supp_col4 = st.columns(4)
        
        with supp_col1:
            # pH classification
            ph = data['ph']
            if ph < 4.5: ph_label = "Sangat Masam"
            elif ph < 5.5: ph_label = "Masam"
            elif ph < 6.5: ph_label = "Agak Masam"
            elif ph < 7.5: ph_label = "Netral"
            elif ph < 8.5: ph_label = "Agak Alkalis"
            else: ph_label = "Alkalis"
            
            st.metric("pH Tanah", f"{ph:.1f}", ph_label)
        
        with supp_col2:
            c_label, c_color, _ = classify_nutrient(data['c_organic'], 'c_organic')
            st.metric("C-Organik", f"{data['c_organic']:.1f}%", c_label)
        
        with supp_col3:
            cec_label, cec_color, _ = classify_nutrient(data['cec'], 'cec')
            st.metric("KTK/CEC", f"{data['cec']:.0f} cmol/kg", cec_label)
        
        with supp_col4:
            # Ca:Mg ratio
            ca_mg_ratio = data['ca_dd'] / data['mg_dd'] if data['mg_dd'] > 0 else 0
            ratio_status = "Ideal" if 3 <= ca_mg_ratio <= 5 else ("Rendah" if ca_mg_ratio < 3 else "Tinggi")
            st.metric("Rasio Ca:Mg", f"{ca_mg_ratio:.1f}:1", ratio_status)
        
        # Visualization
        st.divider()
        st.markdown("### 📊 Visualisasi Status Hara")
        
        # Radar chart
        categories = ['N-Total', 'P-Tersedia', 'K-dd', 'Ca-dd', 'Mg-dd', 'C-Organik']
        
        # Normalize to percentage of optimal
        n_pct = min(data['n_total'] / BALITBANG_THRESHOLDS['n_total']['optimal'] * 100, 150)
        p_pct = min(data['p_value'] / BALITBANG_THRESHOLDS['p_bray']['optimal'] * 100, 150)
        k_pct = min(data['k_dd'] / BALITBANG_THRESHOLDS['k_dd']['optimal'] * 100, 150)
        ca_pct = min(data['ca_dd'] / BALITBANG_THRESHOLDS['ca_dd']['optimal'] * 100, 150)
        mg_pct = min(data['mg_dd'] / BALITBANG_THRESHOLDS['mg_dd']['optimal'] * 100, 150)
        c_pct = min(data['c_organic'] / BALITBANG_THRESHOLDS['c_organic']['optimal'] * 100, 150)
        
        values = [n_pct, p_pct, k_pct, ca_pct, mg_pct, c_pct]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.3)',
            line=dict(color='#10b981', width=2),
            name='Status Hara'
        ))
        
        # Add optimal line (100%)
        fig_radar.add_trace(go.Scatterpolar(
            r=[100]*7,
            theta=categories + [categories[0]],
            line=dict(color='#f59e0b', width=2, dash='dash'),
            name='Optimal (100%)'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 150])),
            showlegend=True,
            title="Status Hara vs Optimal (%)",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# ========== TAB 3: pH & KETERSEDIAAN ==========
with tab_ph:
    st.subheader("🔬 pH & Ketersediaan Unsur Hara")
    st.info("💡 pH tanah sangat mempengaruhi ketersediaan unsur hara. Lihat dampak pH pada setiap unsur di bawah.")
    
    data = st.session_state.npk_data
    current_ph = data.get('ph', 6.5)
    
    # Current pH indicator
    st.markdown(f"### 📍 pH Tanah Anda: **{current_ph}**")
    
    # pH availability chart
    st.markdown("### 📈 Kurva Ketersediaan Hara Berdasarkan pH")
    
    df_ph = pd.DataFrame(PH_AVAILABILITY)
    
    # Melt for plotting
    nutrients_to_plot = ['N', 'P', 'K', 'Ca', 'Mg', 'Fe', 'Mn', 'Zn', 'B']
    
    fig_ph = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, nutrient in enumerate(nutrients_to_plot):
        fig_ph.add_trace(go.Scatter(
            x=df_ph['pH'],
            y=df_ph[nutrient],
            mode='lines+markers',
            name=nutrient,
            line=dict(width=2, color=colors[i % len(colors)]),
            marker=dict(size=6)
        ))
    
    # Add current pH line
    fig_ph.add_vline(x=current_ph, line_dash="dash", line_color="red",
                     annotation_text=f"pH Anda: {current_ph}")
    
    # Add optimal zone
    fig_ph.add_vrect(x0=6.0, x1=7.0, fillcolor="green", opacity=0.1,
                     annotation_text="Zona Optimal")
    
    fig_ph.update_layout(
        title="Ketersediaan Relatif Unsur Hara pada Berbagai pH (%)",
        xaxis_title="pH Tanah",
        yaxis_title="Ketersediaan Relatif (%)",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    st.plotly_chart(fig_ph, use_container_width=True)
    
    # Availability at current pH
    st.markdown(f"### 🎯 Ketersediaan Hara pada pH {current_ph}")
    
    avail_cols = st.columns(5)
    
    nutrients_display = ['N', 'P', 'K', 'Ca', 'Mg']
    
    for i, nut in enumerate(nutrients_display):
        avail = get_ph_availability(current_ph, nut)
        with avail_cols[i]:
            if avail >= 90:
                status_color = "#10b981"
                status = "Optimal"
            elif avail >= 70:
                status_color = "#f59e0b"
                status = "Cukup"
            else:
                status_color = "#ef4444"
                status = "Rendah"
            
            st.metric(nut, f"{avail:.0f}%", status)
    
    # Recommendations based on pH
    st.divider()
    st.markdown("### 💡 Rekomendasi pH")
    
    if current_ph < 5.5:
        st.warning("""
        **pH Terlalu Masam** - Rekomendasi:
        - Aplikasi kapur (CaCO₃) atau dolomit (CaMg(CO₃)₂)
        - Dosis estimasi: 2-4 ton/ha untuk menaikkan 1 unit pH
        - Perhatikan: Fe, Mn mungkin toksik di pH rendah
        """)
    elif current_ph > 7.5:
        st.warning("""
        **pH Terlalu Alkalis** - Rekomendasi:
        - Aplikasi belerang elemental (S) atau amonium sulfat
        - Tambahkan bahan organik kompos
        - Perhatikan: Fe, Mn, Zn kemungkinan defisien
        """)
    else:
        st.success("""
        **pH dalam Rentang Optimal!** ✅
        - Sebagian besar unsur hara tersedia dengan baik
        - Pertahankan dengan pemupukan berimbang dan bahan organik
        """)

# ========== TAB 4: UNSUR SEKUNDER ==========
with tab_sekunder:
    st.subheader("🌿 Analisis Unsur Sekunder & Mikro")
    
    data = st.session_state.npk_data
    
    if not data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input data terlebih dahulu.")
    else:
        # Secondary nutrients
        st.markdown("### 🔹 Unsur Sekunder (Ca, Mg, S)")
        
        sec_col1, sec_col2, sec_col3 = st.columns(3)
        
        with sec_col1:
            ca_label, ca_color, _ = classify_nutrient(data['ca_dd'], 'ca_dd')
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 12px; border-left: 5px solid {ca_color};">
                <h4 style="margin:0;">Kalsium (Ca)</h4>
                <p style="font-size: 1.5rem; font-weight: 700; color: {ca_color}; margin: 0.5rem 0;">
                    {data['ca_dd']:.1f} cmol/kg
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong>{ca_label}</strong></p>
                <p style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.5rem;">
                    Fungsi: Struktur dinding sel, pembelahan sel
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with sec_col2:
            mg_label, mg_color, _ = classify_nutrient(data['mg_dd'], 'mg_dd')
            st.markdown(f"""
            <div style="background: #ecfdf5; padding: 1.5rem; border-radius: 12px; border-left: 5px solid {mg_color};">
                <h4 style="margin:0;">Magnesium (Mg)</h4>
                <p style="font-size: 1.5rem; font-weight: 700; color: {mg_color}; margin: 0.5rem 0;">
                    {data['mg_dd']:.2f} cmol/kg
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong>{mg_label}</strong></p>
                <p style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.5rem;">
                    Fungsi: Inti klorofil, aktivasi enzim
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with sec_col3:
            s_val = data.get('s_value', 15)
            s_status = "Cukup" if s_val >= 10 else "Defisien"
            s_color = "#10b981" if s_val >= 10 else "#ef4444"
            st.markdown(f"""
            <div style="background: #fefce8; padding: 1.5rem; border-radius: 12px; border-left: 5px solid {s_color};">
                <h4 style="margin:0;">Sulfur (S)</h4>
                <p style="font-size: 1.5rem; font-weight: 700; color: {s_color}; margin: 0.5rem 0;">
                    {s_val:.0f} ppm
                </p>
                <p style="color: #6b7280; margin: 0;">Status: <strong>{s_status}</strong></p>
                <p style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.5rem;">
                    Fungsi: Sintesis protein, aroma
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Nutrient Ratios
        st.markdown("### ⚖️ Rasio Unsur Hara")
        
        ratio_col1, ratio_col2, ratio_col3 = st.columns(3)
        
        with ratio_col1:
            ca_mg = data['ca_dd'] / data['mg_dd'] if data['mg_dd'] > 0 else 0
            ca_mg_status = "Ideal (3-5)" if 3 <= ca_mg <= 5 else ("Rendah" if ca_mg < 3 else "Tinggi")
            st.metric("Ca : Mg", f"{ca_mg:.1f} : 1", ca_mg_status)
            st.caption("Ideal: 3-5 : 1")
        
        with ratio_col2:
            k_mg = data['k_dd'] / data['mg_dd'] if data['mg_dd'] > 0 else 0
            k_mg_status = "Ideal" if 0.2 <= k_mg <= 0.3 else ("Rendah" if k_mg < 0.2 else "Tinggi")
            st.metric("K : Mg", f"{k_mg:.2f} : 1", k_mg_status)
            st.caption("Ideal: 0.2-0.3 : 1")
        
        with ratio_col3:
            ca_k = data['ca_dd'] / data['k_dd'] if data['k_dd'] > 0 else 0
            st.metric("Ca : K", f"{ca_k:.1f} : 1")
            st.caption("Ideal: 10-20 : 1")

# ========== TAB 5: AI REKOMENDASI ==========
with tab_ai:
    st.subheader("🤖 Rekomendasi Pemupukan Berbasis AI")
    
    data = st.session_state.npk_data
    
    if not data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input data terlebih dahulu.")
    else:
        st.success("🧠 Analisis AI berdasarkan data lab, pH, tekstur tanah, dan standar Balitbang")
        
        # Calculate deficiencies
        n_def = max(0, BALITBANG_THRESHOLDS['n_total']['optimal'] - data['n_total'])
        p_def = max(0, BALITBANG_THRESHOLDS['p_bray']['optimal'] - data['p_value'])
        k_def = max(0, BALITBANG_THRESHOLDS['k_dd']['optimal'] - data['k_dd'])
        
        st.markdown("### 🎯 Prioritas Pemupukan")
        
        # Priority based on deficiency severity
        priorities = []
        if n_def > 0:
            n_sev = n_def / BALITBANG_THRESHOLDS['n_total']['optimal']
            priorities.append(('N', n_sev, n_def))
        if p_def > 0:
            p_sev = p_def / BALITBANG_THRESHOLDS['p_bray']['optimal']
            priorities.append(('P', p_sev, p_def))
        if k_def > 0:
            k_sev = k_def / BALITBANG_THRESHOLDS['k_dd']['optimal']
            priorities.append(('K', k_sev, k_def))
        
        priorities.sort(key=lambda x: x[1], reverse=True)
        
        if priorities:
            for i, (nutrient, severity, deficit) in enumerate(priorities, 1):
                sev_pct = severity * 100
                if sev_pct > 50:
                    urgency = "🔴 Kritis"
                elif sev_pct > 25:
                    urgency = "🟡 Perlu Perhatian"
                else:
                    urgency = "🟢 Maintenance"
                
                st.markdown(f"**{i}. {nutrient}** - {urgency} (Defisit: {sev_pct:.0f}%)")
        else:
            st.success("✅ Semua unsur makro dalam kondisi optimal!")
        
        st.divider()
        
        # Fertilizer recommendations
        st.markdown("### 📦 Rekomendasi Pupuk (per hektar)")
        
        area = data.get('area_ha', 1.0)
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("#### 💊 Pupuk Tunggal")
            
            # Urea for N
            if n_def > 0:
                # N deficit in % -> kg N needed
                # Assuming 2000 kg soil/m2 to depth 20cm = 2,000,000 kg/ha
                # 0.01% N = 200 kg N/ha
                n_kg_needed = n_def * 200 * area
                urea_kg = n_kg_needed / 0.46
                st.metric("Urea (46% N)", f"{urea_kg:.0f} kg", f"Rp {urea_kg * 2500:,.0f}")
            
            # SP-36 for P
            if p_def > 0:
                p_kg_needed = p_def * 2 * area  # rough conversion
                sp36_kg = p_kg_needed / 0.36
                st.metric("SP-36 (36% P₂O₅)", f"{sp36_kg:.0f} kg", f"Rp {sp36_kg * 3000:,.0f}")
            
            # KCl for K
            if k_def > 0:
                k_kg_needed = k_def * 100 * area
                kcl_kg = k_kg_needed / 0.60
                st.metric("KCl (60% K₂O)", f"{kcl_kg:.0f} kg", f"Rp {kcl_kg * 3500:,.0f}")
        
        with rec_col2:
            st.markdown("#### 🌿 Alternatif Pupuk Majemuk")
            
            # NPK compound alternatives
            st.markdown("""
            **Opsi 1: NPK 15-15-15**
            - Dosis: 300-400 kg/ha
            - Cocok untuk pemupukan dasar
            
            **Opsi 2: NPK 16-16-16**
            - Dosis: 250-350 kg/ha
            - Lebih ekonomis
            
            **Opsi 3: NPK 12-12-17**
            - Dosis: 300-400 kg/ha
            - Untuk tanaman berbuah (K tinggi)
            """)
        
        st.divider()
        
        # Application timing
        st.markdown("### ⏰ Waktu Aplikasi yang Disarankan")
        
        timing_data = {
            "Tahap": ["Tanam", "Vegetatif (21 HST)", "Generatif (45 HST)"],
            "Urea": ["1/3 dosis", "1/3 dosis", "1/3 dosis"],
            "SP-36": ["100%", "-", "-"],
            "KCl": ["1/2 dosis", "-", "1/2 dosis"]
        }
        
        st.table(pd.DataFrame(timing_data))
        
        # pH adjustment
        if data['ph'] < 5.5:
            st.warning(f"""
            ⚠️ **pH Tanah Rendah ({data['ph']})** - Tambahkan Kapur Pertanian!
            
            Rekomendasi: **Dolomit 2-3 ton/ha** untuk menaikkan pH ke 6.0-6.5
            """)

# ========== TAB 5: MIKRONUTRIEN ==========
with tab_mikro:
    st.subheader("🔬 Analisis Mikronutrien")
    st.info("💡 Mikronutrien dibutuhkan dalam jumlah kecil namun esensial untuk pertumbuhan tanaman")
    
    # Input mikronutrien
    st.markdown("### 📝 Input Data Mikronutrien")
    
    mikro_col1, mikro_col2, mikro_col3 = st.columns(3)
    
    with mikro_col1:
        fe_value = st.number_input("Fe/Besi (ppm)", 0.0, 100.0, 5.0, 0.5, help="DTPA Extractable. Kritis: <2.5 ppm")
        mn_value = st.number_input("Mn/Mangan (ppm)", 0.0, 50.0, 3.0, 0.5, help="DTPA Extractable. Kritis: <1.0 ppm")
    
    with mikro_col2:
        cu_value = st.number_input("Cu/Tembaga (ppm)", 0.0, 5.0, 0.3, 0.05, help="DTPA Extractable. Kritis: <0.2 ppm")
        zn_value = st.number_input("Zn/Seng (ppm)", 0.0, 20.0, 1.0, 0.1, help="DTPA Extractable. Kritis: <0.5 ppm")
    
    with mikro_col3:
        b_value = st.number_input("B/Boron (ppm)", 0.0, 5.0, 0.5, 0.1, help="Hot Water Extractable. Kritis: <0.2 ppm")
        mo_value = st.number_input("Mo/Molibdenum (ppm)", 0.0, 1.0, 0.1, 0.01, help="Kritis: <0.05 ppm")
    
    st.divider()
    
    # Classification results
    st.markdown("### 📊 Hasil Klasifikasi Mikronutrien")
    
    mikro_data = {
        'fe': fe_value, 'mn': mn_value, 'cu': cu_value,
        'zn': zn_value, 'b': b_value, 'mo': mo_value
    }
    mikro_names = {
        'fe': 'Besi (Fe)', 'mn': 'Mangan (Mn)', 'cu': 'Tembaga (Cu)',
        'zn': 'Seng (Zn)', 'b': 'Boron (B)', 'mo': 'Molibdenum (Mo)'
    }
    
    result_cols = st.columns(3)
    for i, (key, value) in enumerate(mikro_data.items()):
        with result_cols[i % 3]:
            status, color, score = classify_nutrient(value, key)
            optimal = BALITBANG_THRESHOLDS[key]['optimal']
            deficit = max(0, optimal - value)
            
            st.markdown(f"""
            <div style="background: {color}22; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid {color}; margin: 0.5rem 0;">
                <h4 style="margin: 0; color: {color};">{mikro_names[key]}</h4>
                <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{value} ppm</p>
                <p style="margin: 0;">Status: <strong>{status}</strong></p>
                <p style="margin: 0; font-size: 0.8rem;">Optimal: {optimal} ppm</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # pH Effect on Micronutrients
    st.markdown("### 📈 Pengaruh pH terhadap Ketersediaan Mikronutrien")
    
    ph_current = st.session_state.npk_data.get('ph', 6.5)
    
    # Create availability chart for micronutrients at current pH
    mikro_nutrients = ['Fe', 'Mn', 'Cu', 'Zn', 'B', 'Mo']
    availabilities = []
    for nutrient in mikro_nutrients:
        avail = get_ph_availability(ph_current, nutrient)
        availabilities.append(avail)
    
    fig_mikro = go.Figure()
    fig_mikro.add_trace(go.Bar(
        x=mikro_nutrients,
        y=availabilities,
        marker_color=['#ef4444' if a < 50 else '#eab308' if a < 80 else '#22c55e' for a in availabilities],
        text=[f"{a:.0f}%" for a in availabilities],
        textposition='outside'
    ))
    fig_mikro.update_layout(
        title=f"Ketersediaan Mikronutrien pada pH {ph_current:.1f}",
        xaxis_title="Mikronutrien",
        yaxis_title="Ketersediaan (%)",
        yaxis_range=[0, 110]
    )
    st.plotly_chart(fig_mikro, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Rekomendasi Pupuk Mikro")
    
    rec_mikro = []
    if fe_value < 2.5 or (ph_current > 7.0 and fe_value < 5.0):
        rec_mikro.append("🔴 **Fe (Besi)**: Aplikasikan Fe-EDTA 5-10 kg/ha atau FeSO4 10-25 kg/ha")
    if mn_value < 1.0 or (ph_current > 7.0 and mn_value < 3.0):
        rec_mikro.append("🔴 **Mn (Mangan)**: Aplikasikan MnSO4 5-15 kg/ha")
    if zn_value < 0.5:
        rec_mikro.append("🔴 **Zn (Seng)**: Aplikasikan ZnSO4 15-25 kg/ha")
    if cu_value < 0.1:
        rec_mikro.append("🔴 **Cu (Tembaga)**: Aplikasikan CuSO4 5-10 kg/ha")
    if b_value < 0.2:
        rec_mikro.append("🔴 **B (Boron)**: Aplikasikan Borax 5-10 kg/ha")
    if mo_value < 0.05:
        rec_mikro.append("🔴 **Mo (Molibdenum)**: Aplikasikan Na2MoO4 0.5-1 kg/ha")
    
    if rec_mikro:
        for r in rec_mikro:
            st.markdown(r)
    else:
        st.success("✅ Semua mikronutrien dalam kisaran cukup!")

# ========== TAB 6: TEKSTUR TANAH ==========
with tab_texture:
    st.subheader("🌍 Analisis Tekstur Tanah")
    st.info("💡 Tekstur tanah mempengaruhi retensi air, drainase, dan ketersediaan hara")
    
    # Input soil texture
    st.markdown("### 📝 Input Fraksi Tekstur")
    
    tex_col1, tex_col2 = st.columns(2)
    
    with tex_col1:
        sand = st.number_input("Pasir/Sand (%)", 0.0, 100.0, 40.0, 1.0)
        silt = st.number_input("Debu/Silt (%)", 0.0, 100.0, 40.0, 1.0)
        clay = st.number_input("Liat/Clay (%)", 0.0, 100.0, 20.0, 1.0)
        
        total = sand + silt + clay
        if abs(total - 100) > 0.1:
            st.error(f"⚠️ Total harus 100%. Saat ini: {total:.1f}%")
        else:
            st.success("✅ Total = 100%")
    
    # Soil texture classification (USDA)
    def get_soil_texture(sand, silt, clay):
        """USDA Soil Texture Classification"""
        if sand >= 85 and clay < 10:
            return "Pasir (Sand)", "#f4a460"
        elif sand >= 70 and clay < 15:
            return "Pasir Berlempung (Loamy Sand)", "#deb887"
        elif clay < 7 and silt < 50 and sand >= 43:
            return "Lempung Berpasir (Sandy Loam)", "#d2b48c"
        elif clay >= 40:
            return "Liat (Clay)", "#8b4513"
        elif clay >= 35 and sand >= 45:
            return "Liat Berpasir (Sandy Clay)", "#a0522d"
        elif clay >= 27 and sand < 20:
            return "Liat Berlempung (Silty Clay)", "#6b4423"
        elif silt >= 80:
            return "Debu (Silt)", "#c4aead"
        elif silt >= 50 and clay < 27:
            return "Lempung Berdebu (Silt Loam)", "#bdb76b"
        elif clay >= 27 and clay < 40 and sand >= 20 and sand < 45:
            return "Lempung Berliat (Clay Loam)", "#8b6914"
        else:
            return "Lempung (Loam)", "#32cd32"
    
    with tex_col2:
        if abs(total - 100) <= 0.1:
            texture_class, texture_color = get_soil_texture(sand, silt, clay)
            
            st.markdown(f"""
            <div style="background: {texture_color}33; padding: 1.5rem; border-radius: 12px; 
                        border: 3px solid {texture_color}; text-align: center;">
                <h2 style="color: {texture_color}; margin: 0;">🌍 {texture_class}</h2>
                <p style="margin-top: 0.5rem;">Pasir: {sand:.0f}% | Debu: {silt:.0f}% | Liat: {clay:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Properties
            st.markdown("### 📋 Karakteristik Tekstur")
            
            if "Pasir" in texture_class and "Lempung" not in texture_class:
                st.markdown("""
                - 💧 **Drainase**: Sangat cepat (risiko kekeringan)
                - 🌊 **Retensi Air**: Rendah
                - 🌱 **Retensi Hara**: Rendah (perlu pupuk lebih sering)
                - 🚜 **Pengolahan**: Mudah
                """)
            elif "Liat" in texture_class and "Lempung" not in texture_class:
                st.markdown("""
                - 💧 **Drainase**: Lambat (risiko genangan)
                - 🌊 **Retensi Air**: Tinggi
                - 🌱 **Retensi Hara**: Tinggi
                - 🚜 **Pengolahan**: Sulit (lengket saat basah)
                """)
            else:
                st.markdown("""
                - 💧 **Drainase**: Baik (seimbang)
                - 🌊 **Retensi Air**: Sedang (ideal)
                - 🌱 **Retensi Hara**: Baik
                - 🚜 **Pengolahan**: Mudah-Sedang
                """)
    
    st.divider()
    
    # Soil Texture Triangle Visualization
    st.markdown("### 📐 Segitiga Tekstur Tanah (USDA)")
    
    # Create ternary plot
    fig_texture = go.Figure(go.Scatterternary(
        a=[clay],  # Clay on top
        b=[silt],  # Silt on right
        c=[sand],  # Sand on left
        mode='markers',
        marker=dict(size=20, color='red', symbol='star'),
        name=f"Sampel: {texture_class}"
    ))
    
    fig_texture.update_layout(
        ternary=dict(
            sum=100,
            aaxis=dict(title='Liat (%)', min=0, linewidth=2, ticks='outside'),
            baxis=dict(title='Debu (%)', min=0, linewidth=2, ticks='outside'),
            caxis=dict(title='Pasir (%)', min=0, linewidth=2, ticks='outside'),
        ),
        title="Posisi Sampel pada Segitiga Tekstur",
        showlegend=True
    )
    
    st.plotly_chart(fig_texture, use_container_width=True)
    
    # Recommendations based on texture
    st.markdown("### 💡 Rekomendasi Berdasarkan Tekstur")
    
    if "Pasir" in texture_class and "Lempung" not in texture_class:
        st.warning("""
        ⚠️ **Tanah Berpasir** - Rekomendasi:
        - Tambahkan bahan organik 10-20 ton/ha untuk meningkatkan retensi air
        - Pemupukan lebih sering dengan dosis lebih kecil
        - Pertimbangkan irigasi tetes untuk efisiensi air
        """)
    elif "Liat" in texture_class and "Lempung" not in texture_class:
        st.warning("""
        ⚠️ **Tanah Berliat** - Rekomendasi:
        - Perbaiki drainase dengan saluran atau bedengan tinggi
        - Tambahkan bahan organik untuk memperbaiki struktur
        - Olah tanah saat kelembaban optimal
        """)
    else:
        st.success("""
        ✅ **Tekstur Ideal** - Lempung adalah tekstur terbaik untuk pertanian karena:
        - Keseimbangan drainase dan retensi air
        - Aerasi yang baik untuk akar
        - Retensi hara yang optimal
        """)

# Save message - hidden
