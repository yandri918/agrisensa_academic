
# Cuaca Pertanian - Weather for Agriculture (Open-Meteo Version)
# Module 27 - Comprehensive Weather Information & Agricultural Recommendations
# Version: 2.1.0 (Integrated Service)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import sys
import os
import requests 

# Add updated path logic
from utils.auth import require_auth, show_user_info_sidebar

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.weather_service import WeatherService

st.set_page_config(page_title="Cuaca Pertanian", page_icon="🌤️", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

weather_service = WeatherService()

# ========== HELPER FUNCTIONS (Preserved for UI Logic) ==========

def get_elevation(lat, lon):
    """Get elevation data from Open-Meteo Elevation API"""
    try:
        url = "https://api.open-meteo.com/v1/elevation"
        params = {"latitude": lat, "longitude": lon}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('elevation', [0])[0]
    except:
        pass
    return 0

def get_weather_icon(code):
    """Get weather icon based on WMO code"""
    # Simply using the existing robust mapping logic
    # 0: Clear sky
    if code == 0: return "☀️", "Cerah"
    if code == 1: return "🌤️", "Cerah Berawan"
    if code == 2: return "⛅", "Berawan"
    if code == 3: return "☁️", "Mendung"
    if code in [45, 48]: return "🌫️", "Kabut"
    if code in [51, 53, 55]: return "🌦️", "Gerimis"
    if code in [56, 57]: return "❄️", "Gerimis Beku"
    if code == 61: return "🌧️", "Hujan Ringan"
    if code == 63: return "🌧️", "Hujan Sedang"
    if code == 65: return "🌧️", "Hujan Lebat"
    if code in [66, 67]: return "❄️", "Hujan Beku"
    if code in [71, 73, 75]: return "☃️", "Salju"
    if code == 77: return "❄️", "Butiran Salju"
    if code == 80: return "🌦️", "Hujan Lokal Ringan"
    if code == 81: return "🌧️", "Hujan Lokal Sedang"
    if code == 82: return "⛈️", "Hujan Lokal Lebat"
    if code in [85, 86]: return "❄️", "Badai Salju"
    if code == 95: return "⛈️", "Badai Petir"
    if code in [96, 99]: return "⛈️", "Badai Petir & Hujan Es"
    return "❓", f"Unknown ({code})"

def get_climate_season(lat):
    month = datetime.now().month
    if abs(lat) <= 23.5:
        zone = "Tropis"
        season = "Musim Kemarau" if 4 <= month <= 9 else "Musim Hujan"
        icon = "☀️" if "Kemarau" in season else "🌧️"
    else:
        zone = "Non-Tropis" # Simplified for brevity in refactor
        season = "Musim (Global)"
        icon = "🌍"
    return zone, season, icon

def get_agricultural_recommendations(insight_data, lat):
    """Generate agricultural recommendations based on Insight Object"""
    recommendations = []
    
    rain_risk = insight_data.get('rain_risk_3d')
    rain_est = insight_data.get('seasonal_rain_est')
    
    # 1. Seasonal Insights
    _, season, _ = get_climate_season(lat)
    recommendations.append(f"🌍 **Musim (Deteksi):** {season}")

    # 2. Rain & Irrigation
    if rain_risk == "Tinggi":
        recommendations.append("🌧️ **Risiko Hujan Tinggi:** Tunda penyemprotan & pemupukan cair.")
    else:
        recommendations.append("✅ **Cuaca Stabil:** Aman untuk aktivitas pemupukan.")
        
    return recommendations

def get_farming_suitability(insight_data):
    """Determine suitability"""
    rain = insight_data.get('current_rain', 0)
    wind = insight_data.get('wind_speed', 0)
    
    return {
        "Penyemprotan": "🟢 Cocok" if rain == 0 and wind < 10 else "🔴 Tidak Cocok",
        "Pemupukan": "🟢 Cocok" if rain < 5 else "🟡 Hati-hati",
        "Panen": "🟢 Cocok" if rain == 0 else "🔴 Berisiko"
    }

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #0284c7; text-align: center; margin-bottom: 1rem; }
    .weather-card { background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); padding: 2rem; border-radius: 16px; border: 2px solid #0284c7; margin: 1rem 0; text-align: center; }
    .metric-card { background: white; padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .rec-box { background: #f0fdf4; border-left: 5px solid #16a34a; padding: 1rem; margin-bottom: 0.5rem; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
st.markdown('<h1 class="main-header">🌤️ Cuaca Pertanian & Altimeter</h1>', unsafe_allow_html=True)
st.markdown("**Data Cuaca Presisi (Powered by Open-Meteo)**")

# ========== LOCATION ==========
st.sidebar.header("📍 Lokasi Lahan")
tabs = st.tabs(["🗺️ Pilih di Peta", "📝 Input Manual"])

with tabs[0]:
    default_lat, default_lon = -7.150975, 110.140259 
    m = folium.Map(location=[default_lat, default_lon], zoom_start=8)
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, height=400, width=700)
    
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.success(f"📍 Terpilih: {lat:.5f}, {lon:.5f}")
    else:
        lat, lon = default_lat, default_lon

with tabs[1]:
    if 'manual_lat' not in st.session_state: st.session_state['manual_lat'] = lat
    if 'manual_lon' not in st.session_state: st.session_state['manual_lon'] = lon
    
    lat_input = st.number_input("Latitude", value=st.session_state['manual_lat'], format="%.5f")
    lon_input = st.number_input("Longitude", value=st.session_state['manual_lon'], format="%.5f")
    
    if st.button("Update Lokasi Manual"):
        lat, lon = lat_input, lon_input

# ========== GET DATA ==========
if st.button("🔍 Analisis Cuaca & Lahan", type="primary", use_container_width=True):
    with st.spinner("Mengambil data satelit & cuaca..."):
        # Use Service
        insight = weather_service.get_weather_forecast(lat, lon)
        
        if insight:
            st.session_state['weather_insight'] = insight
            st.session_state['data_lat'] = lat
            st.session_state['data_lon'] = lon
            st.success("✅ Data berhasil diambil!")

# ========== DISPLAY DASHBOARD ==========
if 'weather_insight' in st.session_state:
    data = st.session_state['weather_insight']
    
    # Processed Data from Service
    curr_temp = data['current_temp']
    curr_rain = data['current_rain']
    curr_hum = data['current_humidity']
    curr_wind = data['wind_speed']
    
    # 1. Main Weather Card
    col_main, col_info = st.columns([1, 2])
    
    with col_main:
        st.markdown(f"""
        <div class="weather-card">
            <h1 style="font-size: 4rem; margin:0;">🌤️</h1>
            <h2 style="margin:0;">{curr_temp}°C</h2>
            <p style="font-size: 1.2rem; font-weight:bold;">Real-time</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info:
        st.subheader("📊 Parameter Lahan")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class="metric-card">🌧️ <b>Hujan</b><br><h2>{curr_rain} mm</h2></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="metric-card">💧 <b>Kelembaban</b><br><h2>{curr_hum}%</h2></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="metric-card">💨 <b>Angin</b><br><h2>{curr_wind} km/h</h2></div>""", unsafe_allow_html=True)

    # 2. Recommendations & Suitability
    st.markdown("---")
    col_rec, col_suit = st.columns([3, 2])
    
    with col_rec:
        st.subheader("🌾 Rekomendasi Agronomi")
        recs = get_agricultural_recommendations(data, lat)
        for rec in recs:
            st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)
            
    with col_suit:
        st.subheader("📋 Kesesuaian Aktivitas")
        suits = get_farming_suitability(data)
        for act, status in suits.items():
            st.markdown(f"**{act}**: {status}")

    st.markdown("---")
    st.info("ℹ️ Modul ini menggunakan WeatherService v2.0 yang terintegrasi dengan Perencana Panen AI.")
else:
    st.info("👆 Silakan pilih lokasi di peta lalu klik tombol 'Analisis Cuaca & Lahan'")
