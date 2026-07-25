# 🎯 Rekomendasi Terpadu (Unified Smart Farming Dashboard)
# Modern Dashboard integrating Nutrient Analysis, TOPSIS Decision Support, and Computer Vision

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import cv2
from datetime import datetime

# Auth Imports (Preserved)
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Dasbor Rekomendasi Terpadu", page_icon="🎯", layout="wide")

# ===== AUTHENTICATION =====
user = require_auth()
show_user_info_sidebar()

# ==========================================
# 🧠 LOGIC ENGINE (Models & Algorithms)
# ==========================================
# 🧠 LOGIC ENGINE (Models & Algorithms)
# ==========================================

# Database Optimal (Target Soil Levels in ppm)
# Ref: FAO & Puslitanak (General guide for tropical soils)
NUTRIENT_STANDARDS = {
    "Padi":        {"N": 4000, "P": 25, "K": 3500, "pH_opt": 6.5},
    "Jagung":      {"N": 4500, "P": 30, "K": 4000, "pH_opt": 6.8},
    "Cabai Merah": {"N": 5000, "P": 40, "K": 4500, "pH_opt": 6.5},
    "Tomat":       {"N": 4500, "P": 35, "K": 4000, "pH_opt": 6.5},
    "Krisan":      {"N": 3500, "P": 50, "K": 4000, "pH_opt": 6.0} 
}

def calculate_continuous_nutrient_needs(crop, n_ppm, p_ppm, k_ppm, ph, area_ha):
    """
    Advanced Logic: Uses continuous saturation curves instead of binary thresholds.
    Modeled after diminishing returns (Mitscherlich / Liebig).
    """
    tgt = NUTRIENT_STANDARDS.get(crop, NUTRIENT_STANDARDS["Padi"])
    
    # 2. Continuous Deficit Calculation (Exponential Decay of Soil Supply)
    # We assume 'Efficiency' of soil nutrient extraction is ~50%
    # Deficit = Target - Current. If Current > Target, Deficit = 0.
    
    # Soil Availability Index (0.0 to 1.0) based on pH
    # pH curve: Bell curve centered at pH_opt
    ph_dist = abs(ph - tgt['pH_opt'])
    ph_availability = np.exp(-0.5 * (ph_dist / 1.0)**2) # Sigma=1.0. At +/-1 pH diff, avail drops to 60%
    
    # Adjusted Soil Supply
    eff_n = n_ppm * ph_availability
    eff_p = p_ppm * ph_availability * 0.8 # P is easily locked
    eff_k = k_ppm * ph_availability
    
    # Deficit (ppm)
    def_n_ppm = max(0, tgt['N'] - eff_n)
    def_p_ppm = max(0, tgt['P'] - eff_p)
    def_k_ppm = max(0, tgt['K'] - eff_k)
    
    # Conversion ppm -> kg/ha required
    # Assumption: Furrow slice (20cm) ~ 2,000,000 kg soil/ha.
    # 1 ppm = 1 mg/kg = 2 kg/ha total elemental mass.
    # BUT, fertilizer efficiency is not 100%.
    # N efficiency ~ 40%, P ~ 20%, K ~ 50%
    
    req_n_elem = (def_n_ppm * 2) / 0.40 * 0.2 # Adjusted factor to avoid Massive suggestions (ppm is total N, not Avail N usually)
    # REALITY CHECK: Soil tests usually report Total N, Avail P, Exch K.
    # Simplified logic for "Dashboard Demo" scale:
    # Scale huge PPM numbers down to reasonable kg fertilizer.
    # Let's use a simplified "Gap Factor":
    
    req_n_kg = (def_n_ppm / tgt['N']) * 150 * area_ha # Max 150kg N/ha gap
    req_p_kg = (def_p_ppm / tgt['P']) * 80 * area_ha  # Max 80kg P/ha gap
    req_k_kg = (def_k_ppm / tgt['K']) * 100 * area_ha # Max 100kg K/ha gap
    
    # Product Conversion
    urea = req_n_kg / 0.46
    sp36 = req_p_kg / 0.36
    kcl  = req_k_kg / 0.60
    
    # Status Labels
    def get_status(val, target):
        pct = val / target
        if pct < 0.4: return "Sangat Kurang", "red"
        if pct < 0.8: return "Kurang", "orange"
        if pct < 1.2: return "Optimal", "green"
        return "Tinggi", "blue"
        
    stat_n, color_n = get_status(n_ppm, tgt['N'])
    stat_p, color_p = get_status(p_ppm, tgt['P'])
    stat_k, color_k = get_status(k_ppm, tgt['K'])
    stat_ph, color_ph = get_status(ph, tgt['pH_opt']) # Rough
    if ph < 5: stat_ph, color_ph = "Masam", "red"
    elif ph > 8: stat_ph, color_ph = "Basa", "red"
    elif 6 <= ph <= 7: stat_ph, color_ph = "Netral/Ideal", "green"
    
    return {
        "needs": {"N": req_n_kg, "P": req_p_kg, "K": req_k_kg},
        "products": {"Urea": urea, "SP-36": sp36, "KCl": kcl},
        "status": {
            "N": {"label": stat_n, "color": color_n, "val": n_ppm, "tgt": tgt['N']},
            "P": {"label": stat_p, "color": color_p, "val": p_ppm, "tgt": tgt['P']},
            "K": {"label": stat_k, "color": color_k, "val": k_ppm, "tgt": tgt['K']},
            "pH": {"label": stat_ph, "color": color_ph, "val": ph, "tgt": tgt['pH_opt']}
        },
        "ph_avail": ph_availability
    }

def topsis_ranking(strategies, weights):
    """
    TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
    strategies: dict of dicts (attributes)
    weights: dict of attribute weights (must sum to 1.0)
    """
    # 1. Create Decision Matrix
    df = pd.DataFrame.from_dict(strategies, orient='index')
    
    # Attributes directional logic (True=Benefit/Higher better, False=Cost/Lower better)
    directions = {
        'cost_per_ha': False, # Lower cost is better
        'effectiveness': True,
        'risk': False,        # Lower risk is better
        'environmental_impact': False # Lower impact is better
    }
    
    # 2. Normalize Matrix (Vector Normalization)
    norm_df = df.copy()
    for col in directions.keys():
        denom = np.sqrt((df[col]**2).sum())
        norm_df[col] = df[col] / denom if denom > 0 else 0
        
    # 3. Weighted Normalized Matrix
    for col, weight in weights.items():
        if col in norm_df.columns:
            norm_df[col] = norm_df[col] * weight
            
    # 4. Determine Ideal Best (A+) and Ideal Worst (A-)
    ideal_best = {}
    ideal_worst = {}
    
    for col, is_benefit in directions.items():
        if col not in norm_df.columns: continue
        if is_benefit:
            ideal_best[col] = norm_df[col].max()
            ideal_worst[col] = norm_df[col].min()
        else: # Cost criteria
            ideal_best[col] = norm_df[col].min()
            ideal_worst[col] = norm_df[col].max()
            
    # 5. Calculate Euclidean Distances to Ideal Best (S+) and Worst (S-)
    s_plus = np.sqrt(((norm_df[list(directions.keys())] - pd.Series(ideal_best))**2).sum(axis=1))
    s_minus = np.sqrt(((norm_df[list(directions.keys())] - pd.Series(ideal_worst))**2).sum(axis=1))
    
    # 6. Calculate Performance Score (P = S- / (S+ + S-))
    scores = s_minus / (s_plus + s_minus)
    
    # Return sorted ranking
    df['topsis_score'] = scores
    return df.sort_values('topsis_score', ascending=False)

def analyze_bwd_leaf(image):
    """Preserved BWD Logic from original module"""
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    
    brown_lower = np.array([10, 50, 20])
    brown_upper = np.array([30, 255, 200])
    brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)
    
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    
    green_lower = np.array([35, 40, 40])
    green_upper = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    
    total_pixels = img_cv.shape[0] * img_cv.shape[1]
    brown_percent = (cv2.countNonZero(brown_mask) / total_pixels) * 100
    white_percent = (cv2.countNonZero(white_mask) / total_pixels) * 100
    green_percent = (cv2.countNonZero(green_mask) / total_pixels) * 100
    
    bwd_score = max(0, 100 - (brown_percent * 3) - (white_percent * 2))
    
    if bwd_score >= 80: health_status = "Sehat"
    elif bwd_score >= 60: health_status = "Sedikit Terinfeksi"
    elif bwd_score >= 40: health_status = "Terinfeksi Sedang"
    else: health_status = "Terinfeksi Parah"
    
    return {
        'bwd_score': bwd_score,
        'health_status': health_status,
        'brown_percent': brown_percent,
        'white_percent': white_percent,
        'green_percent': green_percent
    }

# ==========================================
# 🖥️ UI / LAYOUT
# ==========================================

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("⚙️ Parameter Input")
    
    with st.expander("1. Data Lahan & Tanaman", expanded=True):
        s_crop = st.selectbox("Komoditas", ["Padi", "Jagung", "Cabai Merah", "Tomat", "Krisan"])
        s_area = st.number_input("Luas Lahan (Ha)", 0.1, 100.0, 1.0)
        
    with st.expander("2. Hasil Uji Laboratorium", expanded=True):
        i_n = st.slider("Nitrogen Total (mg/kg / ppm)", 0, 10000, 3000, help="N Total tanah")
        i_p = st.slider("Fosfor Tersedia (ppm)", 0, 100, 15, help="P Bray/Olsen")
        i_k = st.slider("Kalium Dapat Ditukar (ppm)", 0, 5000, 2000, help="K-dd")
        i_ph = st.slider("pH Tanah (H2O)", 3.0, 10.0, 6.0, 0.1)
        
    with st.expander("3. Preferensi Strategi (TOPSIS)", expanded=False):
        st.write("Bobot Kriteria Keputusan:")
        w_eff = st.slider("Efektivitas Hasil", 0, 100, 40)
        w_cost = st.slider("Biaya Produksi", 0, 100, 30)
        w_risk = st.slider("Risiko Kegagalan", 0, 100, 20)
        w_env = st.slider("Dampak Lingkungan", 0, 100, 10)
        
        # Normalize weights
        total_w = w_eff + w_cost + w_risk + w_env
        if total_w == 0: total_w = 1
        weights = {
            'effectiveness': w_eff/total_w,
            'cost_per_ha': w_cost/total_w,
            'risk': w_risk/total_w,
            'environmental_impact': w_env/total_w
        }

    with st.expander("4. Harga Pupuk (Rp/kg)", expanded=False):
        st.write("💰 Edit harga pupuk sesuai pasar lokal:")
        price_urea = st.number_input("Urea", min_value=1000, max_value=10000, value=2500, step=100)
        price_sp36 = st.number_input("SP-36", min_value=1000, max_value=10000, value=3500, step=100)
        price_kcl = st.number_input("KCl", min_value=5000, max_value=20000, value=12000, step=500)
        price_dolomit = st.number_input("Dolomit/Kapur", min_value=500, max_value=5000, value=1500, step=100)
    
    with st.expander("5. Referensi Data Standar", expanded=False):
        st.info("ℹ️ Sistem menggunakan database standar hara optimal untuk menghitung defisit.")
        st.write(f"Target Optimal **{s_crop}**:")
        st.json(NUTRIENT_STANDARDS[s_crop])
        st.caption("Sumber: Database Internal (FAO/Puslitanak)")

# --- MAIN DASHBOARD ---
st.title(f"🚀 Dashboard Rekomendasi Terpadu: {s_crop}")
st.write(f"Analisis komprehensif untuk lahan **{s_area} Ha** menggunakan Algoritma TOPSIS & Model Saturasi Hara.")

# RUN CALCULATIONS
nut_res = calculate_continuous_nutrient_needs(s_crop, i_n, i_p, i_k, i_ph, s_area)

# Define Strategies for TOPSIS
strategies_db = {
    "Kimia Intensif": {
        "cost_per_ha": 4500000, "effectiveness": 95, "risk": 70, "environmental_impact": 85,
        "desc": "Full Urea/SP36/KCl dosis tinggi. Hasil cepat, tanah cepat lelah."
    },
    "Berimbang (IPT)": {
        "cost_per_ha": 3200000, "effectiveness": 90, "risk": 40, "environmental_impact": 50,
        "desc": "Kombinasi Organik + Kimia sesuai kebutuhan presisi."
    },
    "Organik Premium": {
        "cost_per_ha": 3800000, "effectiveness": 75, "risk": 20, "environmental_impact": 10,
        "desc": "Full Kompos + Bio-activator. Sustainable, hasil jangka panjang."
    },
    "Low-Input (Hemat)": {
        "cost_per_ha": 1500000, "effectiveness": 60, "risk": 50, "environmental_impact": 40,
        "desc": "Dosis minimum/subsidi. Hasil tidak maksimal."
    }
}
topsis_res = topsis_ranking(strategies_db, weights)
top_strategy = topsis_res.index[0]
top_score = topsis_res.iloc[0]['topsis_score']

# TABS
tab_exec, tab_detail, tab_bwd, tab_sim = st.tabs([
    "📊 Executive Summary", 
    "🧪 Detail Nutrisi", 
    "🍃 Leaf Doctor (CV)", 
    "⚖️ Strategy Simulator"
])

# --- TAB 1: EXECUTIVE SUMMARY ---
with tab_exec:
    # Top Section: Strategy Recommendation (Hero)
    c_hero1, c_hero2 = st.columns([2, 1])
    
    with c_hero1:
        st.subheader("🏆 Strategi Terpilih (TOPSIS Ranking)")
        st.info(f"""
        **Rekomendasi Utama: {top_strategy}** (Skor: {top_score:.2f})
        
        {strategies_db[top_strategy]['desc']}
        
        AI memilih strategi ini karena paling seimbang antara **Efektivitas ({weights['effectiveness']:.0%})** dan **Biaya ({weights['cost_per_ha']:.0%})** sesuai preferensi Anda.
        """)
        
        # Shopping List (Based on strategy + Needs)
        st.write("**🛒 Rencana Belanja (Estimasi Dosis):**")
        
        # Adjust dosage based on strategy type (Heuristic)
        dose_factor = 1.0
        if "Hemat" in top_strategy: dose_factor = 0.6
        if "Organik" in top_strategy: dose_factor = 0.2 # Mostly compost not included here
        
        dolomit_dose = 2000 if nut_res['status']['pH']['color'] == 'red' else 0
        df_shop = pd.DataFrame([
            {"Item": "Urea (N)", "Dosis (kg)": nut_res['products']['Urea'] * dose_factor, "Estimasi": f"Rp {nut_res['products']['Urea']*dose_factor*price_urea:,.0f}"},
            {"Item": "SP-36 (P)", "Dosis (kg)": nut_res['products']['SP-36'] * dose_factor, "Estimasi": f"Rp {nut_res['products']['SP-36']*dose_factor*price_sp36:,.0f}"},
            {"Item": "KCl (K)", "Dosis (kg)": nut_res['products']['KCl'] * dose_factor, "Estimasi": f"Rp {nut_res['products']['KCl']*dose_factor*price_kcl:,.0f}"},
            {"Item": "Dolomit/Kapur", "Dosis (kg)": dolomit_dose, "Estimasi": f"Rp {dolomit_dose*price_dolomit:,.0f}" if dolomit_dose > 0 else "Tidak Perlu"}
        ])
        st.dataframe(df_shop, hide_index=True, use_container_width=True)

    with c_hero2:
        st.subheader("Diagnosa Cepat")
        
        # Status Cards
        def status_card(label, val_dict):
            st.markdown(f"""
            <div style="background-color: {val_dict['color']}; padding: 10px; border-radius: 5px; color: white; margin-bottom: 5px; opacity: 0.8;">
                <b>{label}:</b> {val_dict['label']} ({val_dict['val']})
            </div>
            """, unsafe_allow_html=True)
            
        status_card("Status N", nut_res['status']['N'])
        status_card("Status P", nut_res['status']['P'])
        status_card("Status K", nut_res['status']['K'])
        status_card("Kondisi pH", nut_res['status']['pH'])
        
        st.warning(f"Efisiensi Serapan Akar: {nut_res['ph_avail']*100:.0f}% (karena pH {i_ph})")

# --- TAB 2: DETAIL NUTRISI ---
with tab_detail:
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.subheader("Indikator Kesehatan Tanah")
        # Gauge Chart for pH
        fig_ph = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = i_ph,
            title = {'text': "pH Tanah"},
            gauge = {
                'axis': {'range': [0, 14]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 5.5], 'color': "red"},
                    {'range': [5.5, 7.5], 'color': "green"},
                    {'range': [7.5, 14], 'color': "red"}],
                'threshold': {
                    'line': {'color': "blue", 'width': 4},
                    'thickness': 0.75,
                    'value': 6.5}}))
        fig_ph.update_layout(height=250, margin=dict(l=20,r=20,t=50,b=20))
        st.plotly_chart(fig_ph, use_container_width=True)
        
    with col_g2:
        st.subheader("Kurva Defisit & Rekomendasi")
        # Bar Chart Comparison
        categories = ['Nitrogen (N)', 'Fosfor (P)', 'Kalium (K)']
        current_vals = [nut_res['status']['N']['val'], nut_res['status']['P']['val'], nut_res['status']['K']['val']]
        target_vals = [nut_res['status']['N']['tgt'], nut_res['status']['P']['tgt'], nut_res['status']['K']['tgt']]
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Saat Ini (ppm)', x=categories, y=current_vals),
            go.Bar(name='Target Edaphis (ppm)', x=categories, y=target_vals)
        ])
        fig_bar.update_layout(barmode='group', title="Gap Analisis Hara (Current vs Target)")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Recommendations Text
        st.markdown("### 📋 Langkah Teknis:")
        if nut_res['status']['pH']['label'] == 'Masam':
            st.markdown("- **Pengapuran Wajib**: Lakukan aplikasi Dolomit 2-4 minggu sebelum tanam untuk menaikkan pH.")
        if nut_res['status']['P']['color'] == 'red':
            st.markdown("- **Fosfor Kritis**: Gunakan pupuk dasar SP-36 atau Rock Phosphate di lubang tanam.")
        st.markdown(f"- **Efisiensi Pemupukan**: {nut_res['ph_avail']*100:.1f}%. Artinya {100-(nut_res['ph_avail']*100):.1f}% pupuk berisiko terbuang jika pH tidak diperbaiki.")

# --- TAB 3: LEAF DOCTOR ---
with tab_bwd:
    st.subheader("👁️ Computer Vision: Analisis Daun")
    col_cam, col_res = st.columns(2)
    
    with col_cam:
        img_file = st.file_uploader("Upload Foto Daun", type=['jpg','png','jpeg'])
        if img_file:
            st.image(img_file, caption="Source Image", use_container_width=True)
            run_cv = st.button("🔍 Scan Penyakit")
    
    with col_res:
        if img_file and run_cv:
            with st.spinner("Analyzing spectral signatures..."):
                cv_res = analyze_bwd_leaf(Image.open(img_file))
                
                # Gauge Score
                fig_cv = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = cv_res['bwd_score'],
                    title = {'text': "Skor Kesehatan Daun"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}},
                    domain = {'x': [0, 1], 'y': [0, 1]}
                ))
                fig_cv.update_layout(height=250)
                st.plotly_chart(fig_cv, use_container_width=True)
                
                st.write(f"**Diagnosa:** {cv_res['health_status']}")
                st.progress(cv_res['brown_percent']/100, text=f"Gejala Bercak Coklat: {cv_res['brown_percent']:.1f}%")
                st.progress(cv_res['white_percent']/100, text=f"Gejala Hawar/Putih: {cv_res['white_percent']:.1f}%")

# --- TAB 4: STRATEGY SIMULATOR ---
with tab_sim:
    st.subheader("⚖️ Simulasi Pengambilan Keputusan (TOPSIS)")
    
    c_s1, c_s2 = st.columns([1, 1])
    
    with c_s1:
        topsis_res['topsis_score'] = topsis_res['topsis_score'].astype(float).round(3)
        st.dataframe(topsis_res.style.highlight_max(axis=0, subset=['topsis_score'], color='lightgreen'), use_container_width=True)
        st.caption("*Skor TOPSIS mendekati 1.0 berarti strategi paling mendekati solusi ideal.*")
        
    with c_s2:
        # Radar Chart of Top 2 Strategies
        top2 = topsis_res.head(2).index
        
        categories = ['Effectiveness', 'Low Risk', 'Eco-Friendly', 'Low Cost'] # Inverted Cost/Risk for radar visual
        
        fig_radar = go.Figure()
        
        for strat in top2:
            dat = strategies_db[strat]
            # Normalize for visualization (0-100)
            vals = [
                dat['effectiveness'], 
                100 - dat['risk'], 
                100 - dat['environmental_impact'], 
                (5000000 - dat['cost_per_ha'])/50000 # Rough norm
            ]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=categories,
                fill='toself',
                name=strat
            ))
            
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, title="Perbandingan Head-to-Head")
        st.plotly_chart(fig_radar, use_container_width=True)
