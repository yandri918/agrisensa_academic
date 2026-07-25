# Peta Data Tanah - Streamlit Version
# Interactive soil map with polygon drawing, NPK data, and weather integration

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import requests

# ========== CONFIGURATION ==========
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Peta Data Tanah - AgriSensa",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================







# ========== DATA STORAGE ==========
POLYGONS_FILE = "soil_map_polygons.json"
NPK_DATA_FILE = "soil_map_npk_data.json"
MARKERS_FILE = "soil_map_markers.json"

def load_json(filename, default=[]):
    """Load JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(filename, data):
    """Save JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== WEATHER SERVICE ==========
def get_weather_data(lat, lon):
    """Get weather data from Open-Meteo API (free, no API key needed)"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'Asia/Jakarta'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_soil_data(lat, lon):
    """Get soil data from Open-Meteo Soil API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'soil_temperature_0cm,soil_moisture_0_to_1cm',
            'timezone': 'Asia/Jakarta'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Get latest values
            if 'hourly' in data:
                return {
                    'soil_temperature': data['hourly']['soil_temperature_0cm'][0] if data['hourly']['soil_temperature_0cm'] else None,
                    'soil_moisture': data['hourly']['soil_moisture_0_to_1cm'][0] if data['hourly']['soil_moisture_0_to_1cm'] else None
                }
    except:
        pass
    return None

# ========== NPK ANALYSIS ==========
def analyze_npk(n, p, k):
    """Analyze NPK values (all in ppm)"""
    def classify_value(value, low, high):
        if value < low:
            return "Rendah", "🔴"
        elif value <= high:
            return "Sedang", "🟡"
        else:
            return "Tinggi", "🟢"
    
    # Thresholds in ppm
    # N: 2000-5000 ppm (0.2-0.5%)
    # P: 10-25 ppm
    # K: 2000-4000 ppm (0.2-0.4%)
    n_status, n_icon = classify_value(n, 2000, 5000)
    p_status, p_icon = classify_value(p, 10, 25)
    k_status, k_icon = classify_value(k, 2000, 4000)
    
    return {
        'n': {'value': n, 'status': n_status, 'icon': n_icon, 'unit': 'ppm'},
        'p': {'value': p, 'status': p_status, 'icon': p_icon, 'unit': 'ppm'},
        'k': {'value': k, 'status': k_status, 'icon': k_icon, 'unit': 'ppm'}
    }

def get_fertilizer_recommendation(n, p, k):
    """Get fertilizer recommendations based on NPK (all in ppm)"""
    recommendations = []
    
    if n < 2000:
        recommendations.append("🔹 Tambahkan pupuk Urea (45-0-0) untuk meningkatkan Nitrogen")
    if p < 10:
        recommendations.append("🔹 Tambahkan pupuk SP-36 (0-36-0) untuk meningkatkan Fosfor")
    if k < 2000:
        recommendations.append("🔹 Tambahkan pupuk KCl (0-0-60) untuk meningkatkan Kalium")
    
    if not recommendations:
        recommendations.append("✅ Kandungan NPK sudah baik, lakukan pemeliharaan rutin")
    
    return recommendations

# ========== CUSTOM CSS (Premium Glassmorphism) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }

    .main {
        background-color: #f8fafc;
    }

    /* Header & Hero */
    .header-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.3);
    }

    /* Command Center KPI Cards */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 200px;
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #10b981;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }
    .kpi-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Info Boxes & Modules */
    .info-box {
        background: white;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        padding: 20px;
        margin-bottom: 20px;
    }
    .analysis-pill {
        display: inline-flex;
        align-items: center;
        background: #f1f5f9;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 0.85rem;
        color: #475569;
        font-weight: 600;
        margin-right: 10px;
        border: 1px solid #e2e8f0;
    }

    /* Form Styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px !important;
    }
    
    .status-success { color: #10b981; font-weight: 700; }
    .status-warning { color: #f59e0b; font-weight: 700; }
    .status-danger { color: #ef4444; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    # Header Hero
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; color:white; font-size:2.8rem;">🗺️ Soil Command Center v2.0</h1>
        <p style="margin:0; opacity:0.9; font-size:1.1rem; font-weight:300;">GIS AgriSensa: Integrasi Spasial, Kimiawi, dan Iklim Mikro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🍱 Navigation")
    menu = st.sidebar.radio(
        "Pilih Fitur:",
        ["🗺️ Peta Interaktif", "📊 Data NPK", "🌤️ Cuaca & Iklim", "📈 Statistik"]
    )
    
    # Load data
    polygons = load_json(POLYGONS_FILE)
    npk_data = load_json(NPK_DATA_FILE)
    markers = load_json(MARKERS_FILE)
    
    # ========== PAGE: INTERACTIVE MAP ==========
    if menu == "🗺️ Peta Interaktif":
        st.subheader("🌐 GIS Master View")
        
        # Instructions
        with st.expander("📖 Panduan GIS Command Center", expanded=False):
            st.markdown("""
            - 🖱️ **Klik Kiri**: Pilih titik untuk analisis cuaca & tanah instan.
            - 📑 **Layer Control**: Ganti ke mode Satelit untuk melihat vegetasi asli.
            - 📐 **Drawing Tools**: Gambar poligon untuk menghitung luas lahan & estimasi NPK.
            - 🔄 **Sinkronisasi**: Hubungkan data titik NPK langsung ke modul RAB.
            """)
        
        # Map center
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            # Create map
            m = folium.Map(location=[-6.2088, 106.8456], zoom_start=12, tiles=None)
            folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
            folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)
            folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
            
            # Add existing polygons
            for polygon in polygons:
                coords = polygon.get('coordinates', [])
                if coords:
                    if isinstance(coords[0], dict):
                        coords = [[c['lat'], c['lng']] for c in coords]
                    folium.Polygon(
                        locations=coords,
                        popup=f"<b>{polygon['name']}</b>",
                        color='#059669', fill=True, fillColor='#10b981', fillOpacity=0.3
                    ).add_to(m)
            
            # Add NPK markers with status colors
            for npk in npk_data:
                lat, lon = npk.get('latitude'), npk.get('longitude')
                if lat and lon:
                    n, p, k = npk.get('n_value', 0), npk.get('p_value', 0), npk.get('k_value', 0)
                    # Simple metric for icon color
                    avg_status = (n/3500 + p/17.5 + k/3000) / 3
                    color = 'green' if avg_status > 0.8 else 'orange' if avg_status > 0.4 else 'red'
                    
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"NPK: {n}/{p}/{k} ppm",
                        icon=folium.Icon(color=color, icon='flask', prefix='fa')
                    ).add_to(m)
            
            folium.LayerControl().add_to(m)
            from folium.plugins import Draw
            Draw(export=True, position='topleft').add_to(m)
            
            map_data = st_folium(m, width="100%", height=600)
            
        with col_m2:
            st.markdown("### 🛰️ Real-time Analysis")
            if map_data and map_data.get('last_clicked'):
                clicked = map_data['last_clicked']
                lat, lon = clicked['lat'], clicked['lng']
                
                # Fetch Weather & Soil Data
                with st.spinner("Fetching Satellite Data..."):
                    weather = get_weather_data(lat, lon)
                    soil = get_soil_data(lat, lon)
                
                st.markdown(f"""
                <div class="info-box">
                    <p style="margin:0; font-size:0.8rem; color:#64748b;">LOKASI TERDETEKSI</p>
                    <p style="margin:0; font-weight:700;">{lat:.4f}, {lon:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if weather and 'current' in weather:
                    w_curr = weather['current']
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("🌡️ Temp", f"{w_curr['temperature_2m']}°C")
                    with c2:
                        st.metric("🌧️ Hujan", f"{w_curr['precipitation']} mm")
                
                if soil:
                    st.markdown("---")
                    st.markdown("**🌱 Kondisi Tanah (Real-time)**")
                    s1, s2 = st.columns(2)
                    with s1:
                        st.metric("🌡️ Soil Temp", f"{soil.get('soil_temperature', '-')}°C")
                    with s2:
                        st.metric("💧 Soil Moist", f"{soil.get('soil_moisture', '-')}%")
                
                st.markdown("---")
                st.subheader("⚡ Quick Actions")
                if st.button("➕ Tambah Data NPK", use_container_width=True):
                    st.session_state['add_npk_lat'] = lat
                    st.session_state['add_npk_lon'] = lon
                
                if st.button("🚀 Lanjut ke Simulasi RAB", use_container_width=True):
                    # Find nearest NPK
                    nearest_dist = float('inf')
                    nearest_data = None
                    for record in npk_data:
                        try:
                            dist = haversine(lat, lon, float(record['latitude']), float(record['longitude']))
                            if dist < nearest_dist:
                                nearest_dist = dist
                                nearest_data = record
                        except: continue
                    
                    context = {
                        'source': f"GIS Target ({lat:.4f})",
                        'ph': float(nearest_data.get('ph', 6.0)) if nearest_data else 6.0,
                        'texture': nearest_data.get('soil_type', 'Lempung') if nearest_data else 'Lempung',
                        'n_ppm': float(nearest_data.get('n_value', 0)) if nearest_data else 0,
                        'p_ppm': float(nearest_data.get('p_value', 0)) if nearest_data else 0,
                        'k_ppm': float(nearest_data.get('k_value', 0)) if nearest_data else 0
                    }
                    st.session_state['rab_context'] = context
                    st.success(f"Context siap! Jarak data terdekat: {nearest_dist:.0f}m")
                    st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
            else:
                st.info("Silakan klik titik mana saja di peta untuk memulai analisis spasial.")


        # Add NPK Data Form
        if 'add_npk_lat' in st.session_state:
            st.markdown("---")
            st.subheader("📊 Tambah Data NPK")
            
            with st.form("npk_form"):
                st.info("💡 **Semua nilai NPK dalam satuan ppm (mg/kg)** - sesuai dengan alat ukur standar")
                col1, col2 = st.columns(2)
                with col1:
                    n_value = st.number_input("Nitrogen (ppm)", min_value=0.0, max_value=10000.0, step=10.0, 
                                             help="Range normal: 2000-5000 ppm")
                    p_value = st.number_input("Fosfor (ppm)", min_value=0.0, max_value=100.0, step=1.0,
                                             help="Range normal: 10-25 ppm")
                    k_value = st.number_input("Kalium (ppm)", min_value=0.0, max_value=10000.0, step=10.0,
                                             help="Range normal: 2000-4000 ppm")
                with col2:
                    ph = st.number_input("pH Tanah", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                                        help="Range ideal: 6.0-7.0")
                    soil_type = st.selectbox("Jenis Tanah", ["Lempung", "Pasir", "Liat", "Humus", "Gambut"])
                    notes = st.text_area("Catatan", placeholder="Contoh: Hasil uji lab tanggal 4 Des 2024")
                
                submitted = st.form_submit_button("💾 Simpan Data NPK")
                
                if submitted:
                    npk_record = {
                        'id': str(uuid.uuid4()),
                        'latitude': st.session_state['add_npk_lat'],
                        'longitude': st.session_state['add_npk_lon'],
                        'n_value': n_value,
                        'p_value': p_value,
                        'k_value': k_value,
                        'ph': ph,
                        'soil_type': soil_type,
                        'notes': notes,
                        'created_at': datetime.now().isoformat()
                    }
                    npk_data.append(npk_record)
                    save_json(NPK_DATA_FILE, npk_data)
                    
                    # --- AUTO-LOG TO JOURNAL ---
                    try:
                        from utils.journal_utils import log_to_journal
                        log_to_journal(
                            category="🌍 Peta Tanah",
                            title=f"Uji Tanah: {soil_type}",
                            notes=f"Hasil NPK: {n_value}/{p_value}/{k_value} ppm. pH: {ph}. Lokasi: {st.session_state['add_npk_lat']:.4f}, {st.session_state['add_npk_lon']:.4f}",
                            priority="Sedang"
                        )
                    except Exception as e:
                        pass
                        
                    st.success("✅ Data NPK berhasil disimpan!")
                    del st.session_state['add_npk_lat']
                    del st.session_state['add_npk_lon']
                    st.rerun()
    
    # ========== PAGE: NPK DATA ==========
    elif menu == "📊 Data NPK":
        st.subheader("📜 Database Kimiawi Tanah")
        
        if not npk_data:
            st.info("Belum ada data NPK. Gunakan peta interaktif untuk menambah data.")
        else:
            # Statistics Dashboard
            df = pd.DataFrame(npk_data)
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-value">{len(npk_data)}</div>
                    <div class="kpi-label">Total Sampel</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{df['n_value'].mean():.0f}</div>
                    <div class="kpi-label">Rata N (ppm)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{df['p_value'].mean():.1f}</div>
                    <div class="kpi-label">Rata P (ppm)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{df['k_value'].mean():.0f}</div>
                    <div class="kpi-label">Rata K (ppm)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display data with premium cards
            for npk in npk_data:
                analysis = analyze_npk(npk['n_value'], npk['p_value'], npk['k_value'])
                
                with st.container():
                    st.markdown(f"""
                    <div class="info-box">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                            <h4 style="margin:0; color:#1e293b;">📍 Lahan {npk.get('soil_type', 'Tanpa Nama')}</h4>
                            <span style="font-size:0.8rem; color:#94a3b8;">UID: {npk['id'][:8]}</span>
                        </div>
                        <div style="margin-bottom:15px;">
                            <span class="analysis-pill">🧪 pH: <b>{npk.get('ph', '-')}</b></span>
                            <span class="analysis-pill">🗺️ {npk['latitude']:.4f}, {npk['longitude']:.4f}</span>
                            <span class="analysis-pill">📅 {npk['created_at'][:10]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**Status Nutrisi**")
                        st.write(f"{analysis['n']['icon']} N: {analysis['n']['value']:.0f} ppm")
                        st.write(f"{analysis['p']['icon']} P: {analysis['p']['value']:.1f} ppm")
                        st.write(f"{analysis['k']['icon']} K: {analysis['k']['value']:.0f} ppm")
                    
                    with c2:
                        st.markdown("**Rekomendasi Utama**")
                        recs = get_fertilizer_recommendation(npk['n_value'], npk['p_value'], npk['k_value'])
                        for rec in recs[:2]: # Show top 2
                            st.caption(rec)
                    
                    with c3:
                        st.markdown("**Integrasi & Aksi**")
                        if st.button("🚀 Kirim ke RAB", key=f"send_rab_{npk['id']}", use_container_width=True):
                            st.session_state['rab_context'] = {
                                'source': 'Peta Data Tanah',
                                'ph': float(npk.get('ph', 6.0)),
                                'texture': npk.get('soil_type', 'Lempung'),
                                'n_ppm': float(npk.get('n_value', 0)),
                                'p_ppm': float(npk.get('p_value', 0)),
                                'k_ppm': float(npk.get('k_value', 0))
                            }
                            st.success("Terkirim!")
                        
                        if st.button("🗑️ Hapus", key=f"del_npk_{npk['id']}", use_container_width=True):
                            npk_data = [n for n in npk_data if n['id'] != npk['id']]
                            save_json(NPK_DATA_FILE, npk_data)
                            st.rerun()
                    st.markdown("---")
    
    # ========== PAGE: WEATHER ==========
    elif menu == "🌤️ Cuaca & Iklim":
        st.subheader("🌦️ Analisis Iklim Mikro & Tanah")
        
        with st.container():
            st.markdown("""
            <div class="info-box">
                <p style="margin:0;">Lakukan pengecekan cuaca dan kondisi tanah secara real-time untuk optimalisasi jadwal pemupukan dan irigasi.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                weather_lat = st.number_input("Latitude", value=-6.2088, format="%.6f", key="weather_lat")
            with col2:
                weather_lon = st.number_input("Longitude", value=106.8456, format="%.6f", key="weather_lon")
            
            if st.button("🔍 Ambil Data Komprehensif", type="primary", use_container_width=True):
                with st.spinner("Mengambil data cuaca & tanah..."):
                    weather = get_weather_data(weather_lat, weather_lon)
                    soil = get_soil_data(weather_lat, weather_lon)
                    
                    if weather and 'current' in weather:
                        st.markdown(f"""
                        <div class="kpi-container">
                            <div class="kpi-card">
                                <div class="kpi-value">{weather['current']['temperature_2m']}°C</div>
                                <div class="kpi-label">Suhu Udara</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value">{weather['current']['relative_humidity_2m']}%</div>
                                <div class="kpi-label">Kelembaban</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value">{weather['current']['precipitation']}mm</div>
                                <div class="kpi-label">Curah Hujan</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if soil:
                            st.markdown(f"""
                            <div class="kpi-container">
                                <div class="kpi-card" style="border-left:4px solid #10b981;">
                                    <div class="kpi-value" style="color:#059669;">{soil.get('soil_temperature', '-')}°C</div>
                                    <div class="kpi-label">Suhu Tanah</div>
                                </div>
                                <div class="kpi-card" style="border-left:4px solid #10b981;">
                                    <div class="kpi-value" style="color:#059669;">{soil.get('soil_moisture', '-')}%</div>
                                    <div class="kpi-label">Kelembaban Tanah</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if 'daily' in weather:
                            st.markdown("---")
                            st.subheader("📅 Prakiraan 7 Hari Terintegrasi")
                            forecast_df = pd.DataFrame({
                                'Tanggal': weather['daily']['time'],
                                'Suhu Max (°C)': weather['daily']['temperature_2m_max'],
                                'Suhu Min (°C)': weather['daily']['temperature_2m_min'],
                                'Curah Hujan (mm)': weather['daily']['precipitation_sum']
                            })
                            st.dataframe(forecast_df, use_container_width=True)
                    else:
                        st.error("❌ Gagal menjangkau sensor satelit.")
    
    # ========== PAGE: STATISTICS ==========
    elif menu == "📈 Statistik":
        st.subheader("📈 Analisis Spasial & Distribusi")
        
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-value">{len(polygons)}</div>
                <div class="kpi-label">Area Lahan</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{len(npk_data)}</div>
                <div class="kpi-label">Titik NPK</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{len(markers)}</div>
                <div class="kpi-label">Lain-lain</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if npk_data:
            df = pd.DataFrame(npk_data)
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🧪 Profil Nutrisi Rata-rata (ppm)**")
                st.bar_chart(df[['n_value', 'p_value', 'k_value']].mean(), color="#10b981")
            
            with c2:
                st.markdown("**📈 Tren Variabilitas Kimiawi**")
                st.line_chart(df[['n_value', 'p_value', 'k_value']])
            
            st.markdown("---")
            st.subheader("📍 Sebaran pH Tanah")
            st.area_chart(df['ph'], color="#3b82f6")

def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371000 # Radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi, d_lam = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

if __name__ == "__main__":
    main()
