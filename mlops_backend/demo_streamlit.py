import streamlit as st
import requests
import json
from PIL import Image
import io

# ==========================================
# 🎨 CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="AgriSensa MLOps Client",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
    <style>
    .main {
        background-color: #f9fbf9;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: scale(1.02);
    }
    .card {
        padding: 20px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e8f5e9;
        margin-bottom: 20px;
    }
    .header-title {
        font-family: 'Outfit', sans-serif;
        color: #1b5e20;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/color/96/sprout.png", width=80)
st.sidebar.markdown("<h2 class='header-title'>AgriSensa MLOps</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Base API URL setting
API_BASE_URL = st.sidebar.text_input("🔗 API Base URL", value="http://127.0.0.1:8000")

# Check Health Status
try:
    health_resp = requests.get(f"{API_BASE_URL}/health", timeout=2)
    if health_resp.status_code == 200:
        status_data = health_resp.json()
        st.sidebar.success(f"🟢 Connected (v{status_data.get('version', '1.0.0')})")
    else:
        st.sidebar.warning("🟡 Degraded connection status")
except Exception:
    st.sidebar.error("🔴 Offline (Pastikan API server menyala)")

st.sidebar.info("""
**Endpoints Demo:**
1. 🌾 Crop Recommendation
2. 📈 Yield Prediction
3. 🍂 Leaf Health (BWD)
""")

# ==========================================
# 🚀 MAIN APP DASHBOARD
# ==========================================
st.markdown("<h1 class='header-title'>🌱 AgriSensa MLOps Client Demo</h1>", unsafe_allow_html=True)
st.markdown("Aplikasi frontend demo untuk berinteraksi dengan API MLOps AgriSensa secara dinamis.")

tab1, tab2, tab3 = st.tabs([
    "🌾 Rekomendasi Tanaman", 
    "📈 Prediksi Hasil Panen", 
    "🍂 Analisis Citra Daun (BWD)"
])

# ==========================================
# 🌾 TAB 1: CROP RECOMMENDATION
# ==========================================
with tab1:
    st.markdown("### Prediksi Rekomendasi Komoditas Terbaik")
    st.write("Masukkan kandungan hara tanah dan kondisi cuaca untuk menentukan komoditas paling optimal.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🧪 **Kandungan Hara Tanah (NPK)**")
        n_val = st.number_input("Nitrogen (N) - mg/kg", min_value=0.0, max_value=200.0, value=90.0)
        p_val = st.number_input("Fosfor (P) - mg/kg", min_value=0.0, max_value=200.0, value=42.0)
        k_val = st.number_input("Kalium (K) - mg/kg", min_value=0.0, max_value=200.0, value=43.0)
        ph_val = st.slider("Derajat Keasaman (pH)", min_value=3.0, max_value=10.0, value=6.5, step=0.1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("⛅ **Kondisi Lingkungan / Cuaca**")
        temp_val = st.number_input("Suhu Rata-rata (°C)", min_value=0.0, max_value=50.0, value=25.0)
        hum_val = st.slider("Kelembaban (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        rain_val = st.number_input("Curah Hujan Tahunan (mm)", min_value=0.0, max_value=10000.0, value=200.0)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Dapatkan Rekomendasi 🌾"):
        payload = {
            "n_value": n_val,
            "p_value": p_val,
            "k_value": k_val,
            "temperature": temp_val,
            "humidity": hum_val,
            "ph": ph_val,
            "rainfall": rain_val
        }
        
        with st.spinner("Menghubungi engine MLOps..."):
            try:
                response = requests.post(f"{API_BASE_URL}/api/ml/recommend-crop", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    rec = data["recommended_crop"]
                    
                    st.success("Analisis rekomendasi komoditas berhasil!")
                    
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric(label="Rekomendasi Tanaman", value=rec["crop"])
                    with col_res2:
                        st.metric(label="Confidence Level", value=f"{rec['confidence']}%")
                        
                    if "details" in rec and rec["details"]:
                        st.markdown("#### Panduan Budidaya Singkat:")
                        st.json(rec["details"])
                else:
                    st.error(f"Error API ({response.status_code}): {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Gagal melakukan koneksi ke server API MLOps: {e}")

# ==========================================
# 📈 TAB 2: YIELD PREDICTION
# ==========================================
with tab2:
    st.markdown("### Prediksi Estimasi Hasil Panen & SHAP Explainer")
    st.write("Masukkan kandungan unsur hara untuk memprediksi tonase panen per hektar (ton/ha) serta melihat visualisasi faktor pengaruh.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🧪 **Kandungan Hara Tanah**")
        n_yield = st.number_input("Nitrogen (N) - kg/ha", min_value=0.0, max_value=500.0, value=120.0, key="ny")
        p_yield = st.number_input("Fosfor (P) - kg/ha", min_value=0.0, max_value=500.0, value=75.0, key="py")
        k_yield = st.number_input("Kalium (K) - kg/ha", min_value=0.0, max_value=500.0, value=75.0, key="ky")
        ph_yield = st.slider("Tingkat pH Tanah", min_value=3.0, max_value=10.0, value=6.2, step=0.1, key="phy")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("⛅ **Faktor Lingkungan**")
        temp_yield = st.number_input("Suhu Lingkungan (°C)", min_value=0.0, max_value=50.0, value=26.5, key="tempy")
        rain_yield = st.number_input("Curah Hujan (mm)", min_value=0.0, max_value=5000.0, value=1800.0, key="rainy")
        
        opt_mode = st.radio("Metode Analisis", ["Standar", "Advanced (Dengan SHAP Explainer)"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Prediksi Hasil Panen 📈"):
        payload = {
            "nitrogen": n_yield,
            "phosphorus": p_yield,
            "potassium": k_yield,
            "temperature": temp_yield,
            "rainfall": rain_yield,
            "ph": ph_yield
        }
        
        endpoint = "/api/ml/predict-yield-advanced" if opt_mode == "Advanced (Dengan SHAP Explainer)" else "/api/ml/predict-yield"
        
        with st.spinner("Memproses prediksi MLOps..."):
            try:
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    yield_val = data["predicted_yield_ton_ha"]
                    
                    st.success("Hasil estimasi panen berhasil dihitung!")
                    st.metric(label="Estimasi Hasil Panen", value=f"{yield_val:.2f} Ton / Ha")
                    
                    if "shap_values" in data:
                        st.markdown("#### 🔍 Kontribusi Variabel (SHAP Values)")
                        st.write("Menunjukkan seberapa besar kontribusi masing-masing parameter tanah/cuaca terhadap hasil akhir:")
                        
                        # Display SHAP contributions in a nice format
                        for feature, val in data["shap_values"].items():
                            val_rounded = round(val, 4)
                            direction = "🔼 Meningkatkan" if val > 0 else "🔽 Menurunkan"
                            st.write(f"- **{feature.capitalize()}**: {direction} hasil panen sebesar **{abs(val_rounded)}**")
                else:
                    st.error(f"Error API ({response.status_code}): {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Gagal melakukan koneksi ke server API MLOps: {e}")

# ==========================================
# 🍂 TAB 3: LEAF HEALTH ANALYSIS (BWD)
# ==========================================
with tab3:
    st.markdown("### Analisis Warna Daun (Bagan Warna Daun)")
    st.write("Unggah foto daun padi/tanaman Anda untuk mengukur skala warna hijau (BWD) secara otomatis dan mendeteksi potensi serangan hama/penyakit.")
    
    uploaded_file = st.file_uploader("Pilih gambar daun...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar yang diunggah", width=350)
        
        if st.button("Mulai Analisis Citra Daun 🍂"):
            # Prepare file to send
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            files = {"file": (uploaded_file.name, img_byte_arr, uploaded_file.type)}
            
            with st.spinner("Memproses gambar menggunakan OpenCV Headless..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/api/analysis/bwd", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.success("Analisis citra daun selesai!")
                        
                        col_bwd1, col_bwd2, col_bwd3 = st.columns(3)
                        with col_bwd1:
                            st.metric(label="Skala Warna Daun (BWD)", value=f"{data['bwd_value']:.2f} / 4.0")
                        with col_bwd2:
                            st.metric(label="Status Kesehatan Daun", value=data["health_status"])
                        with col_bwd3:
                            st.metric(label="Deteksi Infeksi", value="Tinggi" if data["has_disease"] else "Aman")
                            
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.write("📋 **Rekomendasi Pemupukan & Aksi:**")
                        st.info(data["recommendation"])
                        
                        # Extra diagnostics if disease detected
                        if data["has_disease"]:
                            st.warning(f"⚠️ **Detail Penyakit Terdeteksi:** {data['disease_details']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"Error API ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Gagal melakukan koneksi ke server API MLOps: {e}")
