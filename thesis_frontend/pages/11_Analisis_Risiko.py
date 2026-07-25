# Analisis Risiko Keberhasilan (AI) - Advanced Edition
# Multi-factor risk analysis with Monte Carlo simulation

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Analisis Risiko AI", page_icon="⚠️", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== CROP DATABASE ==========
CROP_DATABASE = {
    # Tanaman Padi-padian
    "🌾 Padi Sawah": {
        "category": "Serelia",
        "optimal_temp": (24, 30),
        "optimal_rainfall": (1500, 2500),
        "optimal_ph": (5.5, 7.0),
        "altitude": (0, 800),
        "growing_days": 120,
        "water_need": "Tinggi",
        "capital_per_ha": 15000000,
        "yield_potential": 6500,  # kg/ha
        "market_price": 5500  # Rp/kg
    },
    "🌽 Jagung": {
        "category": "Serelia",
        "optimal_temp": (21, 30),
        "optimal_rainfall": (1000, 1500),
        "optimal_ph": (5.8, 7.0),
        "altitude": (0, 1500),
        "growing_days": 100,
        "water_need": "Sedang",
        "capital_per_ha": 12000000,
        "yield_potential": 8000,
        "market_price": 4000
    },
    # Hortikultura - Sayuran
    "🌶️ Cabai Merah": {
        "category": "Hortikultura",
        "optimal_temp": (21, 27),
        "optimal_rainfall": (1500, 2500),
        "optimal_ph": (6.0, 6.8),
        "altitude": (300, 1200),
        "growing_days": 120,
        "water_need": "Tinggi",
        "capital_per_ha": 45000000,
        "yield_potential": 12000,
        "market_price": 35000
    },
    "🍅 Tomat": {
        "category": "Hortikultura",
        "optimal_temp": (18, 27),
        "optimal_rainfall": (1000, 1500),
        "optimal_ph": (6.0, 7.0),
        "altitude": (300, 1500),
        "growing_days": 90,
        "water_need": "Sedang",
        "capital_per_ha": 35000000,
        "yield_potential": 20000,
        "market_price": 8000
    },
    "🥬 Sawi/Pakcoy": {
        "category": "Hortikultura",
        "optimal_temp": (15, 25),
        "optimal_rainfall": (1000, 1500),
        "optimal_ph": (6.0, 7.0),
        "altitude": (500, 1500),
        "growing_days": 40,
        "water_need": "Tinggi",
        "capital_per_ha": 15000000,
        "yield_potential": 15000,
        "market_price": 6000
    },
    "🥕 Wortel": {
        "category": "Hortikultura",
        "optimal_temp": (16, 24),
        "optimal_rainfall": (1000, 1200),
        "optimal_ph": (6.0, 6.8),
        "altitude": (800, 1500),
        "growing_days": 100,
        "water_need": "Sedang",
        "capital_per_ha": 25000000,
        "yield_potential": 25000,
        "market_price": 7000
    },
    "🧅 Bawang Merah": {
        "category": "Hortikultura",
        "optimal_temp": (25, 32),
        "optimal_rainfall": (700, 1000),
        "optimal_ph": (5.6, 6.5),
        "altitude": (0, 800),
        "growing_days": 70,
        "water_need": "Sedang",
        "capital_per_ha": 75000000,
        "yield_potential": 12000,
        "market_price": 35000
    },
    "🧄 Bawang Putih": {
        "category": "Hortikultura",
        "optimal_temp": (15, 25),
        "optimal_rainfall": (800, 1200),
        "optimal_ph": (6.0, 7.0),
        "altitude": (800, 1500),
        "growing_days": 120,
        "water_need": "Sedang",
        "capital_per_ha": 65000000,
        "yield_potential": 8000,
        "market_price": 55000
    },
    "🥔 Kentang": {
        "category": "Hortikultura",
        "optimal_temp": (15, 21),
        "optimal_rainfall": (1000, 1500),
        "optimal_ph": (5.0, 6.0),
        "altitude": (1000, 2500),
        "growing_days": 100,
        "water_need": "Tinggi",
        "capital_per_ha": 55000000,
        "yield_potential": 20000,
        "market_price": 10000
    },
    # Buah-buahan
    "🍓 Stroberi": {
        "category": "Buah",
        "optimal_temp": (17, 22),
        "optimal_rainfall": (1200, 1800),
        "optimal_ph": (5.5, 6.5),
        "altitude": (1000, 1800),
        "growing_days": 120,
        "water_need": "Tinggi",
        "capital_per_ha": 150000000,
        "yield_potential": 15000,
        "market_price": 50000
    },
    "🍉 Semangka": {
        "category": "Buah",
        "optimal_temp": (25, 35),
        "optimal_rainfall": (400, 600),
        "optimal_ph": (6.0, 7.0),
        "altitude": (0, 600),
        "growing_days": 75,
        "water_need": "Tinggi",
        "capital_per_ha": 35000000,
        "yield_potential": 30000,
        "market_price": 4000
    },
    "🍈 Melon": {
        "category": "Buah",
        "optimal_temp": (25, 32),
        "optimal_rainfall": (500, 800),
        "optimal_ph": (6.0, 6.8),
        "altitude": (0, 800),
        "growing_days": 70,
        "water_need": "Tinggi",
        "capital_per_ha": 45000000,
        "yield_potential": 25000,
        "market_price": 10000
    },
    "🍇 Anggur": {
        "category": "Buah",
        "optimal_temp": (20, 30),
        "optimal_rainfall": (500, 700),
        "optimal_ph": (6.5, 7.5),
        "altitude": (0, 500),
        "growing_days": 365,
        "water_need": "Sedang",
        "capital_per_ha": 200000000,
        "yield_potential": 15000,
        "market_price": 60000
    },
    # Perkebunan
    "🌴 Kelapa Sawit": {
        "category": "Perkebunan",
        "optimal_temp": (24, 32),
        "optimal_rainfall": (2000, 3000),
        "optimal_ph": (4.5, 6.0),
        "altitude": (0, 500),
        "growing_days": 1460,  # 4 tahun
        "water_need": "Tinggi",
        "capital_per_ha": 60000000,
        "yield_potential": 22000,  # TBS/ha/tahun
        "market_price": 2400
    },
    "☕ Kopi Arabika": {
        "category": "Perkebunan",
        "optimal_temp": (15, 24),
        "optimal_rainfall": (1500, 2500),
        "optimal_ph": (5.5, 6.5),
        "altitude": (1000, 2000),
        "growing_days": 1095,  # 3 tahun
        "water_need": "Sedang",
        "capital_per_ha": 35000000,
        "yield_potential": 1500,
        "market_price": 80000
    }
}

# Risk factors weights
RISK_WEIGHTS = {
    "npk_adequacy": 0.15,
    "ph_suitability": 0.12,
    "temp_suitability": 0.12,
    "rainfall_suitability": 0.10,
    "altitude_suitability": 0.08,
    "water_availability": 0.12,
    "pest_control": 0.10,
    "experience": 0.08,
    "capital_adequacy": 0.08,
    "market_access": 0.05
}


def calculate_risk_score(crop_key, params):
    """Calculate comprehensive risk score"""
    crop = CROP_DATABASE[crop_key]
    scores = {}
    
    # 1. NPK Adequacy (0-1)
    n_adeq = min(params["n_total"] / 0.3, 1.0) if params["n_total"] < 0.3 else 1.0
    p_adeq = min(params["p_available"] / 15, 1.0) if params["p_available"] < 15 else 1.0
    k_adeq = min(params["k_dd"] / 0.4, 1.0) if params["k_dd"] < 0.4 else 1.0
    scores["npk_adequacy"] = (n_adeq + p_adeq + k_adeq) / 3
    
    # 2. pH Suitability
    ph = params["ph"]
    ph_min, ph_max = crop["optimal_ph"]
    if ph_min <= ph <= ph_max:
        scores["ph_suitability"] = 1.0
    elif ph < ph_min:
        scores["ph_suitability"] = max(0, 1 - (ph_min - ph) / 1.5)
    else:
        scores["ph_suitability"] = max(0, 1 - (ph - ph_max) / 1.5)
    
    # 3. Temperature Suitability
    temp = params["temp"]
    temp_min, temp_max = crop["optimal_temp"]
    if temp_min <= temp <= temp_max:
        scores["temp_suitability"] = 1.0
    elif temp < temp_min:
        scores["temp_suitability"] = max(0, 1 - (temp_min - temp) / 10)
    else:
        scores["temp_suitability"] = max(0, 1 - (temp - temp_max) / 10)
    
    # 4. Rainfall Suitability
    rain = params["rainfall"]
    rain_min, rain_max = crop["optimal_rainfall"]
    if rain_min <= rain <= rain_max:
        scores["rainfall_suitability"] = 1.0
    elif rain < rain_min:
        scores["rainfall_suitability"] = max(0, rain / rain_min)
    else:
        scores["rainfall_suitability"] = max(0.5, 1 - (rain - rain_max) / rain_max)
    
    # 5. Altitude Suitability
    alt = params["altitude"]
    alt_min, alt_max = crop["altitude"]
    if alt_min <= alt <= alt_max:
        scores["altitude_suitability"] = 1.0
    elif alt < alt_min:
        scores["altitude_suitability"] = max(0, 1 - (alt_min - alt) / 500)
    else:
        scores["altitude_suitability"] = max(0, 1 - (alt - alt_max) / 500)
    
    # 6. Water Availability
    water_map = {"Tadah Hujan": 0.4, "Semi-Irigasi": 0.7, "Irigasi Penuh": 1.0}
    base_water = water_map.get(params["irrigation"], 0.5)
    
    # Adjust based on crop need
    if crop["water_need"] == "Tinggi" and base_water < 0.7:
        scores["water_availability"] = base_water * 0.7
    else:
        scores["water_availability"] = base_water
    
    # 7. Pest Control
    pest_map = {"Tidak Ada": 0.2, "Minimal": 0.5, "IPM": 0.8, "Intensif": 1.0}
    scores["pest_control"] = pest_map.get(params["pest_control"], 0.5)
    
    # 8. Experience
    exp = params["experience"]
    scores["experience"] = min(exp / 10, 1.0)
    
    # 9. Capital Adequacy
    needed = crop["capital_per_ha"] * params["area_ha"]
    available = params["capital"]
    scores["capital_adequacy"] = min(available / needed, 1.0) if needed > 0 else 0.5
    
    # 10. Market Access
    market_map = {"Sulit": 0.3, "Sedang": 0.6, "Mudah": 0.9, "Kontrak": 1.0}
    scores["market_access"] = market_map.get(params["market_access"], 0.6)
    
    return scores


def monte_carlo_simulation(base_scores, n_simulations=1000):
    """Run Monte Carlo simulation for risk distribution"""
    np.random.seed(42)
    
    results = []
    
    for _ in range(n_simulations):
        # Add random variation to each factor
        sim_scores = {}
        for key, value in base_scores.items():
            # Random variation ±20%
            variation = np.random.normal(0, 0.1)
            sim_scores[key] = np.clip(value + variation, 0, 1)
        
        # Calculate weighted success probability
        success_prob = sum(
            sim_scores[k] * RISK_WEIGHTS[k] 
            for k in RISK_WEIGHTS.keys()
        )
        
        results.append(success_prob)
    
    return np.array(results)


def get_risk_level(probability):
    """Determine risk level"""
    if probability >= 0.8:
        return "Sangat Rendah", "🟢", "#10b981"
    elif probability >= 0.65:
        return "Rendah", "🟡", "#84cc16"
    elif probability >= 0.5:
        return "Sedang", "🟠", "#f59e0b"
    elif probability >= 0.35:
        return "Tinggi", "🔴", "#f97316"
    else:
        return "Sangat Tinggi", "⛔", "#ef4444"


# ========== MAIN APP ==========
st.title("⚠️ Analisis Risiko Keberhasilan (AI)")
st.markdown("**Multi-factor Risk Analysis dengan Monte Carlo Simulation**")

# Main tabs
tab_input, tab_hasil, tab_monte, tab_sensitivitas, tab_rekomendasi = st.tabs([
    "📝 Input Parameter",
    "📊 Hasil Analisis",
    "🎲 Monte Carlo",
    "📈 Sensitivitas",
    "💡 Rekomendasi"
])

# Initialize session state
if 'risk_data' not in st.session_state:
    st.session_state.risk_data = {
        'analyzed': False,
        'crop': None,
        'scores': {},
        'probability': 0,
        'monte_carlo': None
    }

# ========== TAB 1: INPUT ==========
with tab_input:
    st.subheader("📝 Input Parameter Rencana Tanam")
    st.info("💡 Pilih komoditas dan masukkan parameter untuk analisis risiko komprehensif")
    
    # Crop selection
    crop_options = list(CROP_DATABASE.keys())
    crop_categories = set(CROP_DATABASE[c]["category"] for c in crop_options)
    
    filter_cat = st.radio("Filter Kategori:", ["Semua"] + list(crop_categories), horizontal=True)
    
    if filter_cat != "Semua":
        filtered_crops = [c for c in crop_options if CROP_DATABASE[c]["category"] == filter_cat]
    else:
        filtered_crops = crop_options
    
    selected_crop = st.selectbox("🌱 Pilih Komoditas:", filtered_crops)
    
    # Show crop info
    crop_info = CROP_DATABASE[selected_crop]
    with st.expander(f"ℹ️ Informasi {selected_crop}", expanded=True):
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown(f"**Suhu Optimal:** {crop_info['optimal_temp'][0]}-{crop_info['optimal_temp'][1]}°C")
            st.markdown(f"**Curah Hujan:** {crop_info['optimal_rainfall'][0]}-{crop_info['optimal_rainfall'][1]} mm/th")
        with info_col2:
            st.markdown(f"**pH Ideal:** {crop_info['optimal_ph'][0]}-{crop_info['optimal_ph'][1]}")
            st.markdown(f"**Ketinggian:** {crop_info['altitude'][0]}-{crop_info['altitude'][1]} mdpl")
        with info_col3:
            st.markdown(f"**Masa Tanam:** {crop_info['growing_days']} hari")
            st.markdown(f"**Modal/ha:** Rp {crop_info['capital_per_ha']:,}")
    
    st.divider()
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧪 Kondisi Tanah")
        
        n_total = st.number_input("N-Total (%)", 0.0, 1.0, 0.25, 0.01,
                                  help="Nitrogen total tanah")
        p_available = st.number_input("P-Tersedia (ppm)", 0.0, 50.0, 12.0, 1.0,
                                      help="Fosfor tersedia")
        k_dd = st.number_input("K-dd (cmol/kg)", 0.0, 2.0, 0.35, 0.05,
                               help="Kalium dapat ditukar")
        ph = st.number_input("pH Tanah", 4.0, 9.0, 6.5, 0.1)
    
    with col2:
        st.markdown("### 🌦️ Kondisi Iklim & Lokasi")
        
        temp = st.number_input("Suhu Rata-rata (°C)", 10.0, 40.0, 27.0, 0.5)
        rainfall = st.number_input("Curah Hujan (mm/tahun)", 500.0, 4000.0, 1800.0, 100.0)
        altitude = st.number_input("Ketinggian (mdpl)", 0, 3000, 500, 50)
        irrigation = st.selectbox("Sistem Irigasi", 
                                  ["Tadah Hujan", "Semi-Irigasi", "Irigasi Penuh"])
    
    with col3:
        st.markdown("### 👨‍🌾 Manajemen & Ekonomi")
        
        experience = st.slider("Pengalaman (tahun)", 0, 30, 5)
        pest_control = st.selectbox("Pengendalian Hama", 
                                    ["Tidak Ada", "Minimal", "IPM", "Intensif"])
        area_ha = st.number_input("Luas Lahan (ha)", 0.1, 100.0, 1.0, 0.1)
        capital = st.number_input("Modal Tersedia (Rp)", 0, 500000000, 50000000, 5000000)
        market_access = st.selectbox("Akses Pasar", 
                                     ["Sulit", "Sedang", "Mudah", "Kontrak"])
    
    # Price section with default and manual input
    st.divider()
    st.markdown("### 💰 Asumsi Harga & Modal")
    
    # Row 1: Price
    price_col1, price_col2, price_col3 = st.columns(3)
    
    with price_col1:
        default_price = crop_info["market_price"]
        use_custom_price = st.checkbox("Harga kustom", value=False, key="price_check")
    
    with price_col2:
        if use_custom_price:
            selling_price = st.number_input(
                "Harga Jual (Rp/kg)", 
                min_value=100, 
                max_value=500000, 
                value=default_price,
                step=500,
                help="Masukkan estimasi harga jual Anda"
            )
        else:
            selling_price = default_price
            st.metric("Harga Default", f"Rp {default_price:,}/kg")
    
    with price_col3:
        # Price risk assessment
        if selling_price >= default_price * 1.2:
            price_risk = "⚠️ Optimistis"
            price_risk_score = 0.7
        elif selling_price >= default_price * 0.8:
            price_risk = "✅ Realistis"
            price_risk_score = 1.0
        else:
            price_risk = "⛔ Pesimistis"
            price_risk_score = 0.5
        
        st.metric("Asumsi Harga", price_risk)
        st.caption(f"Range: Rp {int(default_price*0.8):,} - {int(default_price*1.2):,}")
    
    # Row 2: Capital/Modal
    cap_col1, cap_col2, cap_col3 = st.columns(3)
    
    with cap_col1:
        default_capital = crop_info["capital_per_ha"]
        use_custom_capital = st.checkbox("Modal kustom", value=False, key="capital_check")
    
    with cap_col2:
        if use_custom_capital:
            capital_per_ha = st.number_input(
                "Modal/ha (Rp)", 
                min_value=1000000, 
                max_value=500000000, 
                value=default_capital,
                step=1000000,
                help="Masukkan estimasi modal per hektar"
            )
        else:
            capital_per_ha = default_capital
            st.metric("Modal Default/ha", f"Rp {default_capital:,.0f}")
    
    with cap_col3:
        # Capital risk assessment
        if capital_per_ha <= default_capital * 0.8:
            capital_risk = "⚠️ Efisien"
            capital_note = "Modal rendah, perlu keahlian"
        elif capital_per_ha <= default_capital * 1.2:
            capital_risk = "✅ Standar"
            capital_note = "Modal sesuai standar"
        else:
            capital_risk = "💸 Tinggi"
            capital_note = "Modal tinggi, pastikan kualitas"
        
        st.metric("Asumsi Modal", capital_risk)
        st.caption(capital_note)
    
    st.divider()
    
    if st.button("🔬 Analisis Risiko Komprehensif", type="primary", use_container_width=True):
        params = {
            "n_total": n_total,
            "p_available": p_available,
            "k_dd": k_dd,
            "ph": ph,
            "temp": temp,
            "rainfall": rainfall,
            "altitude": altitude,
            "irrigation": irrigation,
            "experience": experience,
            "pest_control": pest_control,
            "area_ha": area_ha,
            "capital": capital,
            "market_access": market_access,
            "selling_price": selling_price,
            "price_risk_score": price_risk_score,
            "capital_per_ha": capital_per_ha
        }
        
        # Calculate scores
        scores = calculate_risk_score(selected_crop, params)
        
        # Calculate weighted probability
        probability = sum(scores[k] * RISK_WEIGHTS[k] for k in RISK_WEIGHTS.keys())
        
        # Monte Carlo simulation
        monte_results = monte_carlo_simulation(scores)
        
        # Save to session state
        st.session_state.risk_data = {
            'analyzed': True,
            'crop': selected_crop,
            'params': params,
            'scores': scores,
            'probability': probability,
            'monte_carlo': monte_results
        }
        
        st.success("✅ Analisis selesai! Lihat hasil di tab **📊 Hasil Analisis**")
        st.balloons()

# ========== TAB 2: HASIL ==========
with tab_hasil:
    st.subheader("📊 Hasil Analisis Risiko")
    
    if not st.session_state.risk_data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input parameter terlebih dahulu.")
    else:
        data = st.session_state.risk_data
        crop = data['crop']
        scores = data['scores']
        probability = data['probability']
        
        risk_level, risk_icon, risk_color = get_risk_level(probability)
        
        # Main result
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {risk_color}20 0%, {risk_color}40 100%); 
                    padding: 2rem; border-radius: 16px; border: 3px solid {risk_color}; text-align: center;">
            <div style="font-size: 4rem;">{risk_icon}</div>
            <h2 style="color: {risk_color}; margin: 0.5rem 0;">Probabilitas Keberhasilan: {crop}</h2>
            <h1 style="font-size: 4rem; margin: 0.5rem 0; color: {risk_color};">{probability*100:.1f}%</h1>
            <p style="font-size: 1.5rem; color: #6b7280; margin: 0;">Level Risiko: <strong>{risk_level}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Factor breakdown
        st.markdown("### 📈 Breakdown 10 Faktor Risiko")
        
        factor_labels = {
            "npk_adequacy": "🧪 Kecukupan NPK",
            "ph_suitability": "⚗️ Kesesuaian pH",
            "temp_suitability": "🌡️ Kesesuaian Suhu",
            "rainfall_suitability": "🌧️ Kesesuaian CH",
            "altitude_suitability": "🏔️ Ketinggian",
            "water_availability": "💧 Ketersediaan Air",
            "pest_control": "🐛 Pengendalian OPT",
            "experience": "👨‍🌾 Pengalaman",
            "capital_adequacy": "💰 Kecukupan Modal",
            "market_access": "🏪 Akses Pasar"
        }
        
        # Create bar chart
        factor_data = pd.DataFrame([
            {"Factor": factor_labels[k], "Score": v * 100, "Weight": RISK_WEIGHTS[k] * 100}
            for k, v in scores.items()
        ])
        
        fig = go.Figure()
        
        colors = ['#ef4444' if s < 50 else '#f59e0b' if s < 70 else '#10b981' 
                  for s in factor_data['Score']]
        
        fig.add_trace(go.Bar(
            y=factor_data['Factor'],
            x=factor_data['Score'],
            orientation='h',
            marker_color=colors,
            text=[f"{s:.0f}%" for s in factor_data['Score']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Skor Tiap Faktor (%)",
            xaxis_title="Skor",
            xaxis_range=[0, 105],
            height=450,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        st.markdown("### 📊 Ringkasan")
        
        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        
        with sum_col1:
            strong = len([s for s in scores.values() if s >= 0.7])
            st.metric("Faktor Kuat (>70%)", f"{strong}/10")
        
        with sum_col2:
            weak = len([s for s in scores.values() if s < 0.5])
            st.metric("Faktor Lemah (<50%)", f"{weak}/10")
        
        with sum_col3:
            avg_score = np.mean(list(scores.values())) * 100
            st.metric("Rata-rata Skor", f"{avg_score:.1f}%")
        
        with sum_col4:
            crop_info = CROP_DATABASE[crop]
            potential_revenue = crop_info["yield_potential"] * crop_info["market_price"] * data['params']['area_ha']
            st.metric("Potensi Pendapatan", f"Rp {potential_revenue/1000000:.0f} Juta")

# ========== TAB 3: MONTE CARLO ==========
with tab_monte:
    st.subheader("🎲 Simulasi Monte Carlo")
    st.info("💡 Monte Carlo mensimulasikan 1000 skenario dengan variasi acak untuk melihat distribusi probabilitas keberhasilan.")
    
    if not st.session_state.risk_data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input parameter terlebih dahulu.")
    else:
        data = st.session_state.risk_data
        monte_results = data['monte_carlo'] * 100  # Convert to percentage
        
        # Distribution histogram
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Histogram(
            x=monte_results,
            nbinsx=30,
            marker_color='#10b981',
            opacity=0.7
        ))
        
        # Add mean line
        mean_val = np.mean(monte_results)
        fig_hist.add_vline(x=mean_val, line_dash="dash", line_color="red",
                          annotation_text=f"Mean: {mean_val:.1f}%")
        
        # Add percentile lines
        p5 = np.percentile(monte_results, 5)
        p95 = np.percentile(monte_results, 95)
        fig_hist.add_vline(x=p5, line_dash="dot", line_color="orange",
                          annotation_text=f"5%: {p5:.1f}%")
        fig_hist.add_vline(x=p95, line_dash="dot", line_color="blue",
                          annotation_text=f"95%: {p95:.1f}%")
        
        fig_hist.update_layout(
            title="Distribusi Probabilitas Keberhasilan (1000 Simulasi)",
            xaxis_title="Probabilitas Keberhasilan (%)",
            yaxis_title="Frekuensi",
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Statistics
        st.markdown("### 📊 Statistik Simulasi")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Mean", f"{np.mean(monte_results):.1f}%")
        with stat_col2:
            st.metric("Std Dev", f"{np.std(monte_results):.1f}%")
        with stat_col3:
            st.metric("Min-Max", f"{np.min(monte_results):.0f}-{np.max(monte_results):.0f}%")
        with stat_col4:
            st.metric("90% Confidence", f"{p5:.0f}-{p95:.0f}%")
        
        # Risk interpretation
        st.divider()
        st.markdown("### 🎯 Interpretasi Risiko")
        
        if p5 >= 60:
            st.success(f"""
            **Risiko Sangat Rendah** ✅
            - Bahkan dalam skenario pesimistis (5%), probabilitas keberhasilan masih **{p5:.0f}%**
            - Rencana tanam sangat layak dieksekusi
            """)
        elif p5 >= 40:
            st.warning(f"""
            **Risiko Moderat** ⚠️
            - Dalam skenario pesimistis, probabilitas turun ke **{p5:.0f}%**
            - Perlu mitigasi pada faktor-faktor lemah
            """)
        else:
            st.error(f"""
            **Risiko Tinggi** ⛔
            - Dalam skenario pesimistis, probabilitas hanya **{p5:.0f}%**
            - Sangat perlu perbaikan signifikan sebelum eksekusi
            """)

# ========== TAB 4: SENSITIVITAS ==========
with tab_sensitivitas:
    st.subheader("📈 Analisis Sensitivitas")
    st.info("💡 Lihat dampak perubahan setiap faktor terhadap probabilitas keberhasilan")
    
    if not st.session_state.risk_data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input parameter terlebih dahulu.")
    else:
        data = st.session_state.risk_data
        scores = data['scores']
        base_prob = data['probability']
        
        # Calculate sensitivity
        sensitivities = []
        
        for factor, weight in RISK_WEIGHTS.items():
            # Calculate impact if factor improves by 20%
            current = scores[factor]
            improved = min(current + 0.2, 1.0)
            impact = (improved - current) * weight * 100
            
            sensitivities.append({
                "Factor": factor,
                "Current": current * 100,
                "Weight": weight * 100,
                "Potential Impact": impact
            })
        
        sens_df = pd.DataFrame(sensitivities)
        sens_df = sens_df.sort_values("Potential Impact", ascending=False)
        
        # Tornado chart
        factor_labels = {
            "npk_adequacy": "🧪 Kecukupan NPK",
            "ph_suitability": "⚗️ Kesesuaian pH",
            "temp_suitability": "🌡️ Kesesuaian Suhu",
            "rainfall_suitability": "🌧️ Kesesuaian CH",
            "altitude_suitability": "🏔️ Ketinggian",
            "water_availability": "💧 Ketersediaan Air",
            "pest_control": "🐛 Pengendalian OPT",
            "experience": "👨‍🌾 Pengalaman",
            "capital_adequacy": "💰 Kecukupan Modal",
            "market_access": "🏪 Akses Pasar"
        }
        
        fig_sens = go.Figure()
        
        fig_sens.add_trace(go.Bar(
            y=[factor_labels[f] for f in sens_df['Factor']],
            x=sens_df['Potential Impact'],
            orientation='h',
            marker_color=['#10b981' if i > 1 else '#94a3b8' for i in sens_df['Potential Impact']],
            text=[f"+{i:.1f}%" for i in sens_df['Potential Impact']],
            textposition='auto'
        ))
        
        fig_sens.update_layout(
            title="Dampak Jika Faktor Ditingkatkan 20%",
            xaxis_title="Peningkatan Probabilitas (%)",
            height=450
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
        
        # Top priorities
        st.markdown("### 🎯 Prioritas Perbaikan")
        
        top_3 = sens_df.head(3)
        
        for i, row in top_3.iterrows():
            factor = factor_labels[row['Factor']]
            current = row['Current']
            impact = row['Potential Impact']
            
            st.markdown(f"""
            **{factor}**
            - Skor saat ini: **{current:.0f}%**
            - Potensi peningkatan: **+{impact:.1f}%** ke probabilitas total
            """)

# ========== TAB 5: REKOMENDASI ==========
with tab_rekomendasi:
    st.subheader("💡 Rekomendasi Mitigasi Risiko")
    
    if not st.session_state.risk_data.get('analyzed', False):
        st.warning("⚠️ Belum ada data. Input parameter terlebih dahulu.")
    else:
        data = st.session_state.risk_data
        scores = data['scores']
        crop = data['crop']
        crop_info = CROP_DATABASE[crop]
        
        # Generate recommendations based on weak factors
        st.markdown("### ⚠️ Faktor yang Perlu Diperbaiki")
        
        weak_factors = [(k, v) for k, v in scores.items() if v < 0.6]
        weak_factors.sort(key=lambda x: x[1])
        
        recommendations = {
            "npk_adequacy": {
                "issue": "Kesuburan tanah kurang",
                "actions": ["Aplikasi pupuk berimbang NPK", "Tambahkan bahan organik 10-20 ton/ha", "Uji lab tanah berkala"]
            },
            "ph_suitability": {
                "issue": "pH tidak optimal",
                "actions": ["Aplikasi kapur/dolomit untuk pH rendah", "Tambah sulfur/kompos untuk pH tinggi", "Konsultasi ahli tanah"]
            },
            "temp_suitability": {
                "issue": "Suhu kurang sesuai",
                "actions": ["Gunakan mulsa untuk moderasi suhu", "Pertimbangkan greenhouse/shade net", "Sesuaikan waktu tanam"]
            },
            "rainfall_suitability": {
                "issue": "Curah hujan tidak optimal",
                "actions": ["Tingkatkan drainase jika berlebih", "Siapkan irigasi cadangan", "Gunakan mulsa untuk retensi air"]
            },
            "altitude_suitability": {
                "issue": "Ketinggian kurang ideal",
                "actions": ["Pilih varietas adaptif", "Modifikasi mikroklimat", "Pertimbangkan komoditas lain"]
            },
            "water_availability": {
                "issue": "Ketersediaan air terbatas",
                "actions": ["Bangun embung/sumur bor", "Gunakan irigasi tetes", "Tanam varietas tahan kering"]
            },
            "pest_control": {
                "issue": "Pengendalian OPT lemah",
                "actions": ["Terapkan IPM terpadu", "Monitoring rutin mingguan", "Siapkan pestisida nabati/kimia"]
            },
            "experience": {
                "issue": "Pengalaman terbatas",
                "actions": ["Konsultasi penyuluh pertanian", "Ikuti pelatihan budidaya", "Bergabung kelompok tani"]
            },
            "capital_adequacy": {
                "issue": "Modal kurang memadai",
                "actions": ["Ajukan KUR pertanian", "Kurangi luas tanam", "Cari mitra/investor"]
            },
            "market_access": {
                "issue": "Akses pasar sulit",
                "actions": ["Jalin kontrak dengan pengepul", "Daftar ke koperasi", "Coba pemasaran online"]
            }
        }
        
        if weak_factors:
            for factor, score in weak_factors:
                rec = recommendations.get(factor, {"issue": "Perlu perbaikan", "actions": []})
                
                priority_color = "#ef4444" if score < 0.4 else "#f59e0b"
                
                st.markdown(f"""
                <div style="background: {priority_color}20; padding: 1rem; border-radius: 12px; 
                            border-left: 5px solid {priority_color}; margin: 1rem 0;">
                    <h4 style="margin: 0; color: #1f2937;">{factor.replace('_', ' ').title()} (Skor: {score*100:.0f}%)</h4>
                    <p style="margin: 0.5rem 0;"><strong>Masalah:</strong> {rec['issue']}</p>
                    <p style="margin: 0.5rem 0;"><strong>Aksi:</strong></p>
                    <ul style="margin: 0;">
                        {''.join(f'<li>{a}</li>' for a in rec['actions'])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Semua faktor dalam kondisi baik (>60%)! Lanjutkan dengan rencana tanam Anda.")
        
        # Economic projection
        st.divider()
        st.markdown("### 💰 Proyeksi Ekonomi")
        
        params = data['params']
        selling_price = params.get('selling_price', crop_info["market_price"])
        capital_per_ha = params.get('capital_per_ha', crop_info["capital_per_ha"])
        
        st.info(f"💵 **Harga Jual:** Rp {selling_price:,}/kg | **Modal/ha:** Rp {capital_per_ha:,}")
        
        potential_yield = crop_info["yield_potential"] * params["area_ha"] * data["probability"]
        gross_revenue = potential_yield * selling_price
        net_revenue = gross_revenue - capital_per_ha * params["area_ha"]
        roi = (net_revenue / (capital_per_ha * params["area_ha"])) * 100 if capital_per_ha > 0 else 0
        
        econ_col1, econ_col2, econ_col3, econ_col4 = st.columns(4)
        
        with econ_col1:
            st.metric("Expected Yield", f"{potential_yield:,.0f} kg")
        with econ_col2:
            st.metric("Gross Revenue", f"Rp {gross_revenue/1000000:.1f} Juta")
        with econ_col3:
            st.metric("Net Revenue", f"Rp {net_revenue/1000000:.1f} Juta", 
                     delta="Profit" if net_revenue > 0 else "Loss")
        with econ_col4:
            st.metric("Expected ROI", f"{roi:.0f}%")

# Footer
st.markdown("---")
st.caption("""
⚠️ **Disclaimer:** Model ini menggunakan perhitungan berbasis skenario dan simulasi Monte Carlo.
Hasil analisis bersifat estimatif dan perlu divalidasi dengan kondisi lapangan aktual.
""")
