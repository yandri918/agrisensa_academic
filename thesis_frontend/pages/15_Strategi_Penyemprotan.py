# Strategi Penyemprotan Cerdas
# Advanced smart spraying strategy with weather integration, cost optimization, and scheduling

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import folium
from streamlit_folium import st_folium

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Strategi Penyemprotan", page_icon="💧", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== PEST & DISEASE DATABASE ==========
PEST_DISEASE_DB = {
    # ===== PADI =====
    "Wereng Coklat": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Padi"],
        "active_ingredient": "Imidakloprid",
        "dosage_per_ha": "200-300 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00) atau Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 32,
            "min_humidity": 60,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Thiamethoxam",
        "safety_period": 14,
        "irac_group": "4A"  # Neonicotinoid
    },
    "Wereng Hijau": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Padi"],
        "active_ingredient": "Buprofezin",
        "dosage_per_ha": "500-750 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 10,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 32,
            "min_humidity": 60,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Piridaben",
        "safety_period": 14,
        "irac_group": "16"  # Inhibitor kitin
    },
    "Penggerek Batang Padi": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Padi"],
        "active_ingredient": "Karbofuran",
        "dosage_per_ha": "10-15 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 14,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 65,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Fipronil",
        "safety_period": 21,
        "irac_group": "1A"  # Karbamat
    },
    "Blas Padi": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Padi"],
        "active_ingredient": "Triklorfosmethyl", # Usually Isoprothiolane/Tricyclazole
        "dosage_per_ha": "500-750 g",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Azoxystrobin",
        "safety_period": 14,
        "irac_group": "F2"  # Dicarboximides/Phosphoro-thiolates
    },
    "Hawar Daun Bakteri": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Padi"],
        "active_ingredient": "Bakterisida Tembaga",
        "dosage_per_ha": "2-3 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 5,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 28,
            "min_humidity": 75,
            "no_rain_hours": 8
        },
        "resistance_management": "Rotasi dengan Streptomisin",
        "safety_period": 10,
        "irac_group": "M1"  # Tembaga
    },
    "Busuk Pelepah Daun": {
        "type": "Penyakit",
        "severity": "Medium",
        "target_crops": ["Padi"],
        "active_ingredient": "Validamycin",
        "dosage_per_ha": "500-750 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 10,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Hexaconazole",
        "safety_period": 14,
        "irac_group": "U"  # Unknown/Antibiotik
    },
    
    # ===== JAGUNG =====
    "Ulat Grayak": {
        "type": "Hama",
        "severity": "Medium",
        "target_crops": ["Jagung", "Padi", "Cabai"],
        "active_ingredient": "Klorpirifos",
        "dosage_per_ha": "1-2 L",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 65,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Emamektin Benzoat",
        "safety_period": 7,
        "irac_group": "1B"  # Organofosfat
    },
    "Penggerek Jagung": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Jagung"],
        "active_ingredient": "Deltamethrin",
        "dosage_per_ha": "250-500 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Spinosad",
        "safety_period": 7,
        "irac_group": "3A"  # Piretroid
    },
    "Bulai Jagung": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Jagung"],
        "active_ingredient": "Metalaxyl",
        "dosage_per_ha": "1-2 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 28,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Dimethomorph",
        "safety_period": 14,
        "irac_group": "4"  # Phenylamides
    },
    "Karat Daun Jagung": {
        "type": "Penyakit",
        "severity": "Medium",
        "target_crops": ["Jagung"],
        "active_ingredient": "Mancozeb",
        "dosage_per_ha": "2-3 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 65,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Propiconazole",
        "safety_period": 7,
        "irac_group": "M3"  # Dithiocarbamates
    },
    
    # ===== CABAI =====
    "Thrips": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Cabai", "Tomat"],
        "active_ingredient": "Abamectin",
        "dosage_per_ha": "250-500 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 5,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Spinosad",
        "safety_period": 3,
        "irac_group": "6"  # Avermectins
    },
    "Kutu Daun (Aphids)": {
        "type": "Hama",
        "severity": "Medium",
        "target_crops": ["Cabai", "Tomat", "Kentang"],
        "active_ingredient": "Imidakloprid",
        "dosage_per_ha": "200-300 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Acetamiprid",
        "safety_period": 7,
        "irac_group": "4A"  # Neonicotinoid
    },
    "Lalat Buah": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Cabai", "Tomat"],
        "active_ingredient": "Methyl Eugenol + Malathion",
        "dosage_per_ha": "50-100 ml",
        "water_volume": "200-400 L/ha",
        "spray_interval": 7,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 32,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Spinosad",
        "safety_period": 7,
        "irac_group": "1B"  # Organofosfat
    },
    "Antraknosa Cabai": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Cabai"],
        "active_ingredient": "Mankozeb + Carbendazim",
        "dosage_per_ha": "2-3 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Azoxystrobin",
        "safety_period": 7,
        "irac_group": "M3 + 1"  # Mix
    },
    "Layu Fusarium": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Cabai", "Tomat"],
        "active_ingredient": "Benomyl",
        "dosage_per_ha": "500-750 g",
        "water_volume": "400-600 L/ha",
        "spray_interval": 10,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 28,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Trichoderma",
        "safety_period": 14,
        "irac_group": "1"  # Benzimidazoles
    },
    
    # ===== TOMAT =====
    "Ulat Buah Tomat": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Tomat"],
        "active_ingredient": "Bacillus thuringiensis",
        "dosage_per_ha": "500-1000 g",
        "water_volume": "400-600 L/ha",
        "spray_interval": 5,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Indoxacarb",
        "safety_period": 1,
        "irac_group": "11A"  # Microbial
    },
    "Bercak Daun Tomat": {
        "type": "Penyakit",
        "severity": "Medium",
        "target_crops": ["Tomat"],
        "active_ingredient": "Chlorothalonil",
        "dosage_per_ha": "2-3 L",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 65,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Mancozeb",
        "safety_period": 7,
        "irac_group": "M5"  # Chloronitriles
    },
    
    # ===== KENTANG =====
    "Ulat Tanah": {
        "type": "Hama",
        "severity": "Medium",
        "target_crops": ["Kentang", "Jagung", "Kedelai"],
        "active_ingredient": "Klorpirifos",
        "dosage_per_ha": "1-2 L",
        "water_volume": "400-600 L/ha",
        "spray_interval": 14,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 28,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Fipronil",
        "safety_period": 14,
        "irac_group": "1B"  # Organofosfat
    },
    "Busuk Daun Kentang": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Kentang"],
        "active_ingredient": "Propineb",
        "dosage_per_ha": "2-3 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 5,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 25,
            "min_humidity": 70,
            "no_rain_hours": 8
        },
        "resistance_management": "Rotasi dengan Cymoxanil",
        "safety_period": 7,
        "irac_group": "M3"  # Dithiocarbamates
    },
    
    # ===== BAWANG MERAH =====
    "Ulat Bawang": {
        "type": "Hama",
        "severity": "Medium",
        "target_crops": ["Bawang Merah"],
        "active_ingredient": "Profenofos",
        "dosage_per_ha": "1-2 L",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Emamektin Benzoat",
        "safety_period": 7,
        "irac_group": "1B"  # Organofosfat
    },
    "Bercak Ungu Bawang": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Bawang Merah"],
        "active_ingredient": "Mankozeb",
        "dosage_per_ha": "2-3 kg",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 28,
            "min_humidity": 70,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Difenoconazole",
        "safety_period": 7,
        "irac_group": "M3"  # Dithiocarbamates
    },
    
    # ===== KEDELAI =====
    "Penggerek Polong Kedelai": {
        "type": "Hama",
        "severity": "High",
        "target_crops": ["Kedelai"],
        "active_ingredient": "Sipermetrin",
        "dosage_per_ha": "250-500 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Sore (16:00-18:00)",
        "weather_conditions": {
            "max_wind_speed": 8,
            "max_temp": 30,
            "min_humidity": 60,
            "no_rain_hours": 4
        },
        "resistance_management": "Rotasi dengan Indoxacarb",
        "safety_period": 7,
        "irac_group": "3A"  # Piretroid
    },
    "Karat Daun Kedelai": {
        "type": "Penyakit",
        "severity": "High",
        "target_crops": ["Kedelai"],
        "active_ingredient": "Azoxystrobin",
        "dosage_per_ha": "500-750 ml",
        "water_volume": "400-600 L/ha",
        "spray_interval": 7,
        "optimal_time": "Pagi (06:00-09:00)",
        "weather_conditions": {
            "max_wind_speed": 10,
            "max_temp": 30,
            "min_humidity": 65,
            "no_rain_hours": 6
        },
        "resistance_management": "Rotasi dengan Trifloxystrobin",
        "safety_period": 14,
        "irac_group": "11"  # Strobilurin

    }
}

# ========== WEATHER API ==========
def get_weather_forecast(lat=-6.2088, lon=106.8456):
    """Get 7-day weather forecast from Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m",
            "forecast_days": 7,
            "timezone": "Asia/Jakarta"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Parse hourly data
        hourly = data['hourly']
        df = pd.DataFrame({
            'time': pd.to_datetime(hourly['time']),
            'temperature': hourly['temperature_2m'],
            'humidity': hourly['relative_humidity_2m'],
            'precipitation_prob': hourly['precipitation_probability'],
            'wind_speed': hourly['wind_speed_10m']
        })
        
        return df
    except:
        # Fallback to dummy data if API fails
        return generate_dummy_weather()

def generate_dummy_weather():
    """Generate dummy weather data for demo"""
    dates = pd.date_range(start=datetime.now(), periods=168, freq='H')
    
    return pd.DataFrame({
        'time': dates,
        'temperature': np.random.uniform(24, 32, 168),
        'humidity': np.random.uniform(60, 90, 168),
        'precipitation_prob': np.random.uniform(0, 40, 168),
        'wind_speed': np.random.uniform(2, 12, 168)
    })

# ========== SPRAY OPTIMIZATION ==========
def calculate_spray_windows(weather_df, pest_conditions):
    """Calculate optimal spray windows based on weather"""
    spray_windows = []
    
    for idx, row in weather_df.iterrows():
        # Check if conditions are suitable
        suitable = True
        reasons = []
        
        # Wind speed
        if row['wind_speed'] > pest_conditions['max_wind_speed']:
            suitable = False
            reasons.append(f"Angin terlalu kencang ({row['wind_speed']:.1f} km/h)")
        
        # Temperature
        if row['temperature'] > pest_conditions['max_temp']:
            suitable = False
            reasons.append(f"Suhu terlalu tinggi ({row['temperature']:.1f}°C)")
        
        # Humidity
        if row['humidity'] < pest_conditions['min_humidity']:
            suitable = False
            reasons.append(f"Kelembaban terlalu rendah ({row['humidity']:.1f}%)")
        
        # Rain probability
        if row['precipitation_prob'] > 30:
            suitable = False
            reasons.append(f"Kemungkinan hujan tinggi ({row['precipitation_prob']:.0f}%)")
        
        # Time of day (only 6-9 AM and 4-6 PM)
        hour = row['time'].hour
        if not ((6 <= hour <= 9) or (16 <= hour <= 18)):
            suitable = False
            reasons.append("Bukan waktu optimal")
        
        spray_windows.append({
            'time': row['time'],
            'suitable': suitable,
            'score': 100 if suitable else 0,
            'reasons': reasons if not suitable else ["Kondisi optimal"],
            'temperature': row['temperature'],
            'humidity': row['humidity'],
            'wind_speed': row['wind_speed'],
            'precipitation_prob': row['precipitation_prob']
        })
    
    return pd.DataFrame(spray_windows)

def calculate_cost(area_ha, dosage_val, water_val, labor_wage, workers_count, work_days, equipment_price, pesticide_price=150000):
    """Calculate spraying cost"""
    # dosage_val in ml/gr per ha
    # water_val in L per ha
    
    # Calculate
    pesticide_needed = dosage_val * area_ha / 1000  # Convert ml to L (or gr to kg)
    water_needed = water_val * area_ha
    
    pesticide_cost = pesticide_needed * pesticide_price
    labor_cost = labor_wage * workers_count * work_days
    equipment_cost = area_ha * equipment_price
    
    total_cost = pesticide_cost + labor_cost + equipment_cost
    
    return {
        'pesticide_needed': pesticide_needed,
        'water_needed': water_needed,
        'pesticide_cost': pesticide_cost,
        'labor_cost': labor_cost,
        'equipment_cost': equipment_cost,
        'total_cost': total_cost
    }

# ========== MAIN APP ==========
st.title("💧 Strategi Penyemprotan Cerdas")
st.markdown("**Optimasi waktu, dosis, dan biaya penyemprotan dengan AI dan data cuaca real-time**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur Advanced:**
    - 🌤️ Integrasi cuaca real-time (7 hari forecast)
    - 🎯 Rekomendasi waktu optimal otomatis
    - 💰 Kalkulasi biaya lengkap
    - 📅 Jadwal penyemprotan bertahap
    - 🔄 Manajemen resistensi
    - ⚠️ Safety period calculator
    - 📊 Visualisasi kondisi cuaca
    
    **Input yang Diperlukan:**
    1. Pilih hama/penyakit target
    2. Luas lahan
    3. Lokasi (untuk data cuaca)
    4. Tanggal rencana penyemprotan
    
    **Output:**
    - Waktu optimal penyemprotan
    - Dosis & volume air
    - Estimasi biaya
    - Jadwal aplikasi
    - Rekomendasi resistensi
    """)

# Input Section
st.subheader("📝 Input Data Penyemprotan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Target & Lokasi**")
    
    pest_disease = st.selectbox(
        "Hama/Penyakit Target",
        options=list(PEST_DISEASE_DB.keys()),
        help="Pilih hama atau penyakit yang akan dikendalikan"
    )
    
    area_ha = st.number_input(
        "Luas Lahan (ha)",
        min_value=0.1,
        max_value=1000.0,
        value=1.0,
        step=0.1
    )
    
    # Map Input
    st.markdown("**Lokasi Lahan (Klik pada Peta)**")
    
    # Default to Central Java if no click yet
    default_lat, default_lon = -7.150975, 110.140259 
    
    if 'spray_coords' not in st.session_state:
        st.session_state.spray_coords = (default_lat, default_lon)
        
    m = folium.Map(location=[st.session_state.spray_coords[0], st.session_state.spray_coords[1]], zoom_start=7)
    m.add_child(folium.ClickForMarker(popup="Lokasi Lahan"))
    
    map_output = st_folium(m, height=300, width="100%", returned_objects=["last_clicked"])
    
    if map_output and map_output['last_clicked']:
        lat = map_output['last_clicked']['lat']
        lon = map_output['last_clicked']['lng']
        st.session_state.spray_coords = (lat, lon)
        
    st.caption(f"Koordinat Terpilih: {st.session_state.spray_coords[0]:.4f}, {st.session_state.spray_coords[1]:.4f}")


with col2:
    st.markdown("**Waktu & Harga**")
    
    start_date = st.date_input(
        "Tanggal Rencana Penyemprotan",
        value=datetime.now(),
        min_value=datetime.now()
    )
    
    pesticide_price = st.number_input(
        "Harga Pestisida (Rp/L atau Rp/kg)",
        min_value=0,
        value=150000,
        step=10000,
        help="Harga per liter atau kilogram"
    )
    
    harvest_date = st.date_input(
        "Rencana Panen",
        value=datetime.now() + timedelta(days=30),
        help="Untuk cek safety period"
    )
    
    # Correction: Manual Dosage Calibration
    st.markdown("---")
    st.markdown("**🧪 Kalibrasi Dosis**")
    
    # Get defaults
    default_pest_info = PEST_DISEASE_DB[pest_disease]
    def_dosage_str = default_pest_info['dosage_per_ha']
    def_water_str = default_pest_info['water_volume']
    
    # Try parse default number
    try:
        # Check units for conversion
        multiplier = 1.0
        lower_str = def_dosage_str.lower()
        if 'l' in lower_str and 'ml' not in lower_str: # Liter
            multiplier = 1000.0
        elif 'kg' in lower_str: # Kilogram
            multiplier = 1000.0
            
        raw_val = float(def_dosage_str.split('-')[0].replace(',','.').strip().split()[0]) # Split space to get number part safely
        def_dosage_val = raw_val * multiplier
    except:
        def_dosage_val = 500.0
        
    try:
        def_water_val = float(def_water_str.split('-')[0].replace(',','.').strip().split()[0])
    except:
        def_water_val = 400.0

    manual_dosage = st.number_input(
        "Dosis per Hektar (ml atau gram)",
        min_value=0.0,
        value=float(def_dosage_val),
        step=50.0,
        key="man_dosage",
        help="Sesuaikan dengan label produk yang Anda gunakan. Angka dikonversi ke ml/gr."
    )
    
    manual_water = st.number_input(
        "Volume Air per Hektar (Liter)",
        min_value=0.0,
        value=float(def_water_val),
        step=10.0,
        key="man_water",
        help="Volume semprot yang biasa Anda habiskan untuk 1 Ha"
    )
    
    # Operational Costs
    st.markdown("**Biaya Operasional**")
    
    st.caption("Tenaga Kerja (HOK)")
    c_hok1, c_hok2, c_hok3 = st.columns(3)
    with c_hok1:
        labor_wage = st.number_input("Upah Harian (Rp)", value=100000.0, step=10000.0, key="labor_wage")
    with c_hok2:
        workers_count = st.number_input("Jumlah Pekerja", min_value=1, value=1, step=1, key="workers_count")
    with c_hok3:
        work_days = st.number_input("Durasi (Hari)", min_value=1, value=1, step=1, key="work_days")
        
    st.caption("Peralatan")
    equipment_price = st.number_input("Sewa Alat (Rp/Ha)", value=20000.0, step=5000.0, key="eq_price")
    
    # Rotation history (simulation)
    st.markdown("**🛡️ Manajemen Resistensi**")
    last_spray_group = st.selectbox(
        "Grup Bahan Aktif Terakhir Dipakai",
        options=["Belum ada", "1A", "1B", "3A", "4A", "6", "M3", "11", "M1"],
        help="Pilih kode grup IRAC/FRAC dari kemasan pestisida sebelumnya"
    )


# Analyze button
if st.button("🔍 Analisis & Buat Strategi", type="primary", use_container_width=True):
    
    with st.spinner("Menganalisis kondisi cuaca dan membuat strategi optimal..."):
        # Get pest/disease info
        pest_info = PEST_DISEASE_DB[pest_disease]
        
        # Get weather forecast
        selected_lat, selected_lon = st.session_state.spray_coords
        weather_df = get_weather_forecast(lat=selected_lat, lon=selected_lon)
        
        # Calculate spray windows
        spray_windows = calculate_spray_windows(weather_df, pest_info['weather_conditions'])
        
        # Calculate cost
        cost_info = calculate_cost(
            area_ha, manual_dosage, manual_water, 
            labor_wage, workers_count, work_days, 
            equipment_price, pesticide_price
        )
    
    # Display Results
    st.markdown("---")
    st.subheader("📊 Hasil Analisis")
    
    # Pest/Disease Info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        st.metric(
            "Target",
            pest_disease,
            delta=f"{severity_colors[pest_info['severity']]} {pest_info['severity']}"
        )
    
    with col2:
        st.metric(
            "Tipe",
            pest_info['type'],
            help="Hama atau Penyakit"
        )
    
    with col3:
        st.metric(
            "Interval Semprot",
            f"{pest_info['spray_interval']} hari",
            help="Jarak antar aplikasi"
        )
    
    # Recommendations
    st.markdown("---")
    st.subheader("💊 Rekomendasi Pestisida")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Bahan Aktif:** {pest_info['active_ingredient']}
        
        **Dosis per Hektar:** {pest_info['dosage_per_ha']}
        
        **Volume Air:** {pest_info['water_volume']}
        
        **Waktu Optimal:** {pest_info['optimal_time']}
        """)
    
    with col2:
        st.markdown(f"""
        **Manajemen Resistensi (IRAC/FRAC):**
        - **Grup Saat Ini:** {pest_info.get('irac_group', 'N/A')}
        - **Strategi:** {pest_info['resistance_management']}
        
        **Safety Period:** {pest_info['safety_period']} hari sebelum panen
        
        **Total Kebutuhan:**
        - Pestisida: {cost_info['pesticide_needed']:.2f} L/kg
        - Air: {cost_info['water_needed']:.0f} L
        """)
    
    # Resistance Check
    st.markdown("---")
    st.subheader("🛡️ Analisis Risiko Kekebalan (Resistensi)")
    
    current_group = pest_info.get('irac_group', 'N/A')
    
    if last_spray_group != "Belum ada" and last_spray_group == current_group:
        st.error(f"""
        ⚠️ **RISIKO RESISTENSI TINGGI!**
        
        Anda berencana menggunakan pestisida **Grup {current_group}**, padahal sebelumnya juga menggunakan **Grup {last_spray_group}**.
        Penggunaan grup yang sama berturut-turut akan membuat hama menjadi KEBAL.
        
        **Saran:** GANTI bahan aktif dengan Grup yang berbeda (misalnya Grup {pest_info['resistance_management'].split()[-1] if 'Grup' in pest_info['resistance_management'] else 'Lainnya'}).
        """)
    else:
        st.success(f"""
        ✅ **Strategi Rotasi Aman**
        
        Grup pestisida saat ini: **{current_group}**
        Grup sebelumnya: **{last_spray_group}**
        
        Lanjutkan rotasi ini untuk mencegah hama menjadi kebal.
        """)
    
    # Safety period check
    days_to_harvest = (harvest_date - start_date.today()).days
    
    if days_to_harvest < pest_info['safety_period']:
        st.error(f"""
        ⚠️ **PERINGATAN SAFETY PERIOD!**
        
        Jarak ke panen: {days_to_harvest} hari
        Safety period minimum: {pest_info['safety_period']} hari
        
        **TIDAK AMAN untuk disemprot!** Tunda penyemprotan atau gunakan pestisida dengan safety period lebih pendek.
        """)
    else:
        st.success(f"✅ Aman untuk disemprot ({days_to_harvest} hari ke panen)")
    
    # Weather Analysis
    st.markdown("---")
    st.subheader("🌤️ Analisis Cuaca & Waktu Optimal")
    
    # Find optimal windows
    optimal_windows = spray_windows[spray_windows['suitable'] == True]
    
    if len(optimal_windows) > 0:
        st.success(f"✅ Ditemukan {len(optimal_windows)} waktu optimal dalam 7 hari ke depan")
        
        # Show top 5 recommendations
        st.markdown("**Top 5 Waktu Terbaik:**")
        
        for i, (idx, window) in enumerate(optimal_windows.head(5).iterrows(), 1):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{i}. {window['time'].strftime('%A, %d %B %Y - %H:%M')}**")
            with col2:
                st.write(f"🌡️ {window['temperature']:.1f}°C")
            with col3:
                st.write(f"💧 {window['humidity']:.0f}%")
            with col4:
                st.write(f"💨 {window['wind_speed']:.1f} km/h")
    else:
        st.warning("⚠️ Tidak ada waktu optimal dalam 7 hari ke depan. Pertimbangkan menunda penyemprotan.")
    
    # Weather visualization
    st.markdown("---")
    st.subheader("📈 Visualisasi Kondisi Cuaca")
    
    tab1, tab2, tab3 = st.tabs(["Suhu & Kelembaban", "Angin & Hujan", "Spray Windows"])
    
    with tab1:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weather_df['time'],
            y=weather_df['temperature'],
            name='Suhu (°C)',
            line=dict(color='#ef4444')
        ))
        
        fig.add_trace(go.Scatter(
            x=weather_df['time'],
            y=weather_df['humidity'],
            name='Kelembaban (%)',
            yaxis='y2',
            line=dict(color='#3b82f6')
        ))
        
        fig.update_layout(
            title="Suhu dan Kelembaban (7 Hari)",
            xaxis_title="Waktu",
            yaxis_title="Suhu (°C)",
            yaxis2=dict(
                title="Kelembaban (%)",
                overlaying='y',
                side='right'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weather_df['time'],
            y=weather_df['wind_speed'],
            name='Kecepatan Angin (km/h)',
            fill='tozeroy',
            line=dict(color='#10b981')
        ))
        
        fig.add_trace(go.Scatter(
            x=weather_df['time'],
            y=weather_df['precipitation_prob'],
            name='Probabilitas Hujan (%)',
            yaxis='y2',
            line=dict(color='#8b5cf6')
        ))
        
        fig.update_layout(
            title="Angin dan Probabilitas Hujan",
            xaxis_title="Waktu",
            yaxis_title="Kecepatan Angin (km/h)",
            yaxis2=dict(
                title="Probabilitas Hujan (%)",
                overlaying='y',
                side='right'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Spray suitability heatmap
        spray_windows['date'] = spray_windows['time'].dt.date
        spray_windows['hour'] = spray_windows['time'].dt.hour
        
        pivot = spray_windows.pivot_table(
            values='score',
            index='hour',
            columns='date',
            aggfunc='mean'
        )
        
        fig = px.imshow(
            pivot,
            labels=dict(x="Tanggal", y="Jam", color="Suitability"),
            color_continuous_scale='RdYlGn',
            aspect="auto"
        )
        
        fig.update_layout(
            title="Heatmap Waktu Optimal Penyemprotan",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Cost Analysis
    st.markdown("---")
    st.subheader("💰 Analisis Biaya")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Biaya Pestisida", f"Rp {cost_info['pesticide_cost']:,.0f}")
    with col2:
        st.metric("Biaya Tenaga Kerja", f"Rp {cost_info['labor_cost']:,.0f}")
    with col3:
        st.metric("Biaya Peralatan", f"Rp {cost_info['equipment_cost']:,.0f}")
    with col4:
        st.metric("Total Biaya", f"Rp {cost_info['total_cost']:,.0f}")
    
    # Cost breakdown chart
    fig = go.Figure(data=[go.Pie(
        labels=['Pestisida', 'Tenaga Kerja', 'Peralatan'],
        values=[cost_info['pesticide_cost'], cost_info['labor_cost'], cost_info['equipment_cost']],
        hole=.3
    )])
    
    fig.update_layout(title="Breakdown Biaya Penyemprotan", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Spray Schedule
    st.markdown("---")
    st.subheader("📅 Jadwal Penyemprotan Bertahap")
    
    # Calculate multiple spray dates
    num_sprays = min(4, days_to_harvest // pest_info['spray_interval'])
    
    if num_sprays > 0:
        schedule_data = []
        
        for i in range(num_sprays):
            spray_date = start_date + timedelta(days=i * pest_info['spray_interval'])
            
            schedule_data.append({
                'Aplikasi': f"Aplikasi {i+1}",
                'Tanggal': spray_date.strftime('%d %B %Y'),
                'Dosis': pest_info['dosage_per_ha'],
                'Volume Air': pest_info['water_volume'],
                'Biaya': f"Rp {cost_info['total_cost']:,.0f}"
            })
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        # Download schedule
        csv = df_schedule.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Jadwal (CSV)",
            data=csv,
            file_name=f"jadwal_penyemprotan_{pest_disease}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("Tidak cukup waktu untuk aplikasi bertahap sebelum panen")
    
    # Safety Tips
    st.markdown("---")
    st.subheader("⚠️ Tips Keselamatan")
    
    st.warning("""
    **Penting untuk Diperhatikan:**
    
    1. **APD (Alat Pelindung Diri):**
       - Gunakan masker respirator
       - Sarung tangan karet
       - Baju lengan panjang
       - Sepatu boot
    
    2. **Saat Penyemprotan:**
       - Semprot searah angin
       - Jangan makan/minum saat menyemprot
       - Hindari penyemprotan saat angin kencang
       - Pastikan tidak ada orang/hewan di area
    
    3. **Setelah Penyemprotan:**
       - Cuci tangan dan mandi
       - Cuci pakaian terpisah
       - Simpan pestisida di tempat aman
       - Buang kemasan bekas dengan benar
    
    4. **Safety Period:**
       - Tunggu minimal {0} hari sebelum panen
       - Jangan masuk area tanpa APD selama 24 jam
    """.format(pest_info['safety_period']))

# Footer
st.markdown("---")
st.caption("""
💧 **Strategi Penyemprotan Cerdas** - Optimasi waktu, dosis, dan biaya dengan data cuaca real-time.
Selalu ikuti petunjuk label pestisida dan konsultasikan dengan ahli untuk kasus khusus.
""")
