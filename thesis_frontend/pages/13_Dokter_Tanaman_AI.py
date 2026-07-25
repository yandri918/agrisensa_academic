import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from datetime import datetime

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Dokter Tanaman AI (Gemini)", page_icon="🌿", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== CONFIGURATION ==========
st.sidebar.header("⚙️ Konfigurasi AI")

# Try to get key from secrets or environment, else from sidebar
api_key = st.sidebar.text_input("Google AI Studio API Key", type="password", help="Dapatkan key gratis di: https://aistudio.google.com/app/apikey")

if not api_key:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    elif "GOOGLE_API_KEY" in os.environ:
        api_key = os.environ["GOOGLE_API_KEY"]

# ========== GEMINI LOGIC ==========
def get_gemini_models(api_key):
    """Fetch available Gemini models from API"""
    try:
        genai.configure(api_key=api_key)
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return models
    except Exception as e:
        return []

def analyze_with_gemini(image, key, model_name='models/gemini-1.5-flash'):
    """
    Analyze image using Google Gemini
    """
    if not key:
        return None, "API Key belum diisi."
        
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel(model_name)
        
        prompt = """
        You are an expert agricultural plant pathologist. Analyze this image of a plant.
        Identify if there is any disease, pest, or nutrient deficiency.
        
        IMPORTANT: Provide the response strictly in INDONESIAN language (Bahasa Indonesia).
        
        Return the result strictly in this JSON format:
        {
            "is_healthy": boolean,
            "diagnosis": "Nama penyakit/hama/defisiensi atau 'Sehat' jika tidak ada (Dalam Bahasa Indonesia)",
            "confidence": float (0.0 to 1.0),
            "severity": "None" | "Low" | "Medium" | "High" | "Critical",
            "symptoms_observed": ["Daftar", "gejala", "visual", "yang", "terlihat"],
            "explanation": "Penjelasan singkat mengapa Anda membuat diagnosis ini berdasarkan bukti visual (Dalam Bahasa Indonesia).",
            "treatment_recommendations": {
                "immediate": ["Tindakan 1", "Tindakan 2"],
                "short_term": ["Tindakan 1", "Tindakan 2"],
                "prevention": ["Tindakan 1", "Tindakan 2"]
            }
        }
        Do not allow markdown formatting in the response, just raw JSON.
        """
        
        with st.spinner(f"🤖 Meminta analisis ke {model_name}..."):
            # Gemini 1.5 Flash/Pro supports image directly in list
            # Legacy models might act differently, but 'generateContent' is standard for newer ones
            response = model.generate_content([prompt, image])
            text_response = response.text.replace('```json', '').replace('```', '').strip()
            
            try:
                data = json.loads(text_response)
                return data, None
            except json.JSONDecodeError:
                return None, f"Gagal memproses respons AI: {text_response}"
                
    except Exception as e:
        return None, str(e)

# ========== MAIN APP ==========
st.title("🌿 Dokter Tanaman AI (Gemini)")
st.caption("Didukung oleh Google Gemini - Multimodal Analysis")

# Sidebar Info
with st.sidebar:
    st.info("💡 **Tips:** Pastikan API Key Anda memiliki akses ke model yang dipilih.")
    st.divider()

    # Model Selection Logic
    available_models = []
    if api_key:
        available_models = get_gemini_models(api_key)
    
    # Default options if fetch fails
    default_options = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro-vision"]
    
    # Merge found models
    options = available_models if available_models else default_options
    
    selected_model = st.selectbox(
        "Pilih Model AI", 
        options, 
        index=0 if options else 0,
        help="Pilih model yang tersedia di akun Anda. Gunakan 'flash' untuk kecepatan, 'pro' untuk akurasi."
    )
    
    st.divider()
    st.markdown("[Dapatkan API Key Gratis](https://aistudio.google.com/app/apikey)")

# Input Section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload Foto")
    input_method = st.radio("Metode:", ["Upload File", "Kamera"], horizontal=True)
    
    image = None
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Pilih foto daun/tanaman", type=['jpg', 'png', 'jpeg'])
        if uploaded_file:
            image = Image.open(uploaded_file)
    else:
        camera_photo = st.camera_input("Ambil foto")
        if camera_photo:
            image = Image.open(camera_photo)

with col2:
    if image:
        st.image(image, caption="Preview Citra", use_container_width=True)
        
        if not api_key:
            st.warning("⚠️ Masukkan Google API Key di Sidebar untuk memulai analisis.")
            
        if api_key and st.button("🔍 Analisis Sekarang", type="primary", use_container_width=True):
            result, error = analyze_with_gemini(image, api_key, model_name=selected_model)
            
            if error:
                st.error(f"Terjadi Kesalahan: {error}")
            elif result:
                st.session_state['last_diagnosis'] = result

# ========== RESULTS DISPLAY ==========
if 'last_diagnosis' in st.session_state:
    data = st.session_state['last_diagnosis']
    
    st.divider()
    st.subheader("🎯 Hasil Diagnosis")
    
    # Header Card
    severity_color = {
        "None": "green", "Low": "blue", "Medium": "orange", 
        "High": "red", "Critical": "darkred"
    }.get(data['severity'], "grey")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(f"### :{severity_color}[{data['diagnosis']}]")
        st.markdown(f"**Gejala:** {', '.join(data['symptoms_observed'])}")
    with c2:
        st.metric("Tingkat Keparahan", data['severity'])
    with c3:
        st.metric("AI Confidence", f"{data['confidence']*100:.0f}%")
        
    # Explanation
    st.info(f"💡 **Analisis AI:** {data['explanation']}")
    
    # Treatment
    st.subheader("💊 Rekomendasi Penanganan")
    t1, t2, t3 = st.tabs(["⚡ Tindakan Segera", "📅 Jangka Pendek", "🛡️ Pencegahan"])
    
    with t1:
        for item in data['treatment_recommendations'].get('immediate', []):
            st.markdown(f"- {item}")
            
    with t2:
        for item in data['treatment_recommendations'].get('short_term', []):
            st.markdown(f"- {item}")
            
    with t3:
        for item in data['treatment_recommendations'].get('prevention', []):
            st.markdown(f"- {item}")
            
    # Save Log
    if st.button("💾 Simpan ke Riwayat"):
        st.success("Data disimpan ke log lokal (simulasi).")
