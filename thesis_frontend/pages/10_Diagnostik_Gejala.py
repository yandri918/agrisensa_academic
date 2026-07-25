# Diagnostik Gejala Cerdas v2.0
# AI-Powered Plant Pathology & Decision Support

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
import uuid
from datetime import datetime
import google.generativeai as genai

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Diagnostik Gejala Cerdas", page_icon="🔍", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DISEASE DATABASE V2.0 (Weighted) ==========
# Importance weights: 0.1 (low/generic) to 1.0 (pathognomonic/specific)
DISEASE_DATABASE = {
    "Blas Padi (Blast)": {
        "symptoms": {
            "Bercak coklat belah ketupat": 1.0,
            "Pusat bercak berwarna abu-abu": 0.8,
            "Daun mengering/terbakar": 0.4,
            "Leher malai membusuk (neck blast)": 0.9
        },
        "causes": "Jamur Pyricularia oryzae",
        "treatment": [
            "Aplikasi fungisida sistemik (Trisiklazol/Propikonazol)",
            "Aplikasi saat anakan maksimum dan awal berbunga",
            "Kurangi dosis Nitrogen (Urea) sementara"
        ],
        "prevention": ["Gunakan varietas tahan (Inpari 32/42)", "Jarak tanam Legowo", "Perlakuan benih"],
        "severity": "Tinggi"
    },
    "Hawar Daun Bakteri (Kresek)": {
        "symptoms": {
            "Garis kuning/jingga di tepi daun": 0.9,
            "Eksudat bakteri (butiran kuning)": 1.0,
            "Daun melintir dan layu": 0.7,
            "Warna daun pucat keabu-abuan": 0.3
        },
        "causes": "Bakteri Xanthomonas oryzae pv. oryzae",
        "treatment": [
            "Semprot bakterisida/antibiotik pertanian (Kasugamisin)",
            "Aplikasi tembaga hidroksida",
            "Buang sumber infeksi dari lahan"
        ],
        "prevention": ["Benih bersertifikat", "Hindari pemupukan N berlebih", "Pengaturan air"],
        "severity": "Tinggi"
    },
    "Bule Jagung (Downy Mildew)": {
        "symptoms": {
            "Garis khlorotik/putih memanjang": 1.0,
            "Lapisan spora putih di bawah daun": 0.9,
            "Pertumbuhan kerdil": 0.5,
            "Daun kaku dan tegak": 0.7
        },
        "causes": "Jamur Peronosclerospora maydis",
        "treatment": [
            "Cabut dan musnahkan tanaman sakit segara (Erradikasi)",
            "Aplikasi fungisida Metalaksil pada tanaman sekitar",
            "Proteksi preventif"
        ],
        "prevention": ["Seed treatment dengan Metalaksil", "Waktu tanam serempak", "Rotasi tanaman"],
        "severity": "Sangat Tinggi"
    },
    "Virus Kuning (Bule Cabai)": {
        "symptoms": {
            "Daun menguning terang (mosaik)": 1.0,
            "Daun mengerut/mengecil": 0.8,
            "Tanaman kerdil dan tidak berbuah": 0.7,
            "Terdapat kutu kebul di bawah daun": 0.6
        },
        "causes": "Gemini Virus (Vektor: Bemisia tabaci)",
        "treatment": [
            "Tidak ada obat virus (Fokus kendali vektor)",
            "Semprot insektisida Abamektin/Imidakloprid",
            "Aplikasi pupuk mikro untuk daya tahan"
        ],
        "prevention": ["Gunakan mulsa perak", "Gunakan bibit sehat", "Tanaman barrier"],
        "severity": "Sangat Tinggi"
    },
    "Busuk Buah Antraknosa": {
        "symptoms": {
            "Bercak coklat kehitaman melingkar": 1.0,
            "Buah mengkerut dan kering": 0.8,
            "Spora berwarna oranye/merah muda": 0.9,
            "Bercak melekuk (sunken)": 0.7
        },
        "causes": "Jamur Colletotrichum spp.",
        "treatment": [
            "Semprot fungisida berbahan aktif Mankozeb/Kabit",
            "Buang buah yang busuk jauh dari lahan",
            "Kurangi kelembaban tajuk"
        ],
        "prevention": ["Jarak tanam longgar", " Drainase baik", "Varietas toleran"],
        "severity": "Tinggi"
    }
}

# ========== DESIGN SYSTEM (Premium Glassmorphism) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }

    .main { background-color: #f8fafc; }

    .header-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
        overflow-x: auto;
        padding-bottom: 10px;
    }

    .kpi-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        min-width: 180px;
        flex: 1;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }

    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #059669; }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }

    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.8rem;">🔍 Diagnostik Gejala v2.0</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:1.1rem; font-weight:300;">
            Sistem Pakar Patologi Tanaman: Weighted Bayesian Inference & AI Reasoning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar API Configuration
    with st.sidebar:
        st.header("⚙️ Konfigurasi Intelijen")
        api_key = st.text_input("Gemini API Key", type="password")
        if not api_key:
            if "GOOGLE_API_KEY" in st.secrets: api_key = st.secrets["GOOGLE_API_KEY"]
        
        st.divider()
        st.markdown("### 📊 Parameter Analisis")
        confidence_threshold = st.slider("Ambang Keyakinan (%)", 5, 50, 20)
        
    # Navigation
    menu = st.sidebar.selectbox("Navigasi", ["🎯 Diagnosis Utama", "📜 Riwayat Diagnostik", "📚 Database Penyakit"])


    if menu == "🎯 Diagnosis Utama":
        st.markdown("### 1. Observasi Gejala")
        st.info("💡 Pilih semua gejala yang Anda temukan pada tanaman. Algoritma kami akan menghitung probabilitas diagnosis secara real-time.")
        
        # Collect all unique symptoms
        all_symptoms = []
        for d in DISEASE_DATABASE.values():
            all_symptoms.extend(list(d['symptoms'].keys()))
        all_symptoms = sorted(list(set(all_symptoms)))
        
        col_inp, col_info = st.columns([2, 1])
        with col_inp:
            selected_symptoms = st.multiselect(
                "Pilih Gejala Teramati:",
                options=all_symptoms,
                format_func=lambda x: f"🔍 {x}",
                placeholder="Cari gejala (misal: bercak, kuning...)"
            )
        
        with col_info:
            if selected_symptoms:
                st.write(f"**Total Gejala Terpilih:** {len(selected_symptoms)}")
                if st.button("🧮 Jalankan Analisis Intelijen", type="primary", use_container_width=True):
                    # Bayesian Logic (Weighted)
                    results = []
                    diseases = list(DISEASE_DATABASE.keys())
                    prior = 1.0 / len(diseases)
                    
                    total_unnormalized = 0
                    disease_scores = {}
                    
                    for disease_name, info in DISEASE_DATABASE.items():
                        # P(S | D) = Product of (weight if symptom present, else 0.1 penalty)
                        likelihood = 1.0
                        for s_db, weight in info['symptoms'].items():
                            if s_db in selected_symptoms:
                                likelihood *= weight
                            else:
                                # Smaller penalty for missing non-critical symptoms
                                likelihood *= (1.0 - weight) * 0.5 + 0.05
                        
                        posterior = prior * likelihood
                        disease_scores[disease_name] = posterior
                        total_unnormalized += posterior
                    
                    # Normalize & Format
                    for d_name in diseases:
                        score = disease_scores[d_name]
                        prob = score / total_unnormalized if total_unnormalized > 0 else 0
                        results.append({"name": d_name, "prob": prob, "info": DISEASE_DATABASE[d_name]})
                    
                    results.sort(key=lambda x: x['prob'], reverse=True)
                    st.session_state['diagnosis_v2_results'] = results
                    st.session_state['diagnosis_v2_symptoms'] = selected_symptoms
                    
                    # --- AUTO-LOG TO JOURNAL ---
                    try:
                        from utils.journal_utils import log_to_journal
                        top_res = results[0]
                        log_to_journal(
                            category="🔍 Diagnostik AI",
                            title=f"Diagnosis AI: {top_res['name']}",
                            notes=f"Keyakinan: {top_res['prob']*100:.1f}%. Gejala terdeteksi: {', '.join(selected_symptoms)}.",
                            priority="Tinggi" if top_res['info']['severity'] in ["Tinggi", "Sangat Tinggi"] else "Sedang"
                        )
                    except Exception as e:
                        pass
                        
                    st.rerun()

        # Display Results
        if 'diagnosis_v2_results' in st.session_state:
            results = st.session_state['diagnosis_v2_results']
            symptoms = st.session_state['diagnosis_v2_symptoms']
            top = results[0]
            
            st.markdown("---")
            st.subheader("🎯 Hasil Analisis Intelijen")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                # Top Result Card
                severity_map = {"Rendah": "🟢", "Sedang": "🟡", "Tinggi": "🟠", "Sangat Tinggi": "🔴"}
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style="color:#059669; margin-top:0;">{top['name']}</h2>
                    <div style="font-size:3rem; font-weight:700; color:#065f46;">{top['prob']*100:.1f}%</div>
                    <p style="color:#64748b; font-weight:600;">KEYAKINAN DIAGNOSIS</p>
                    <div style="margin-top:20px; padding:10px; border-radius:10px; background:#f1f5f9;">
                        <b>Tingkat Keparahan:</b> {severity_map.get(top['info']['severity'], '⚪')} {top['info']['severity']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                # Chart
                df_chart = pd.DataFrame(results[:5])
                fig = go.Figure(go.Bar(
                    x=df_chart['prob'], y=df_chart['name'],
                    orientation='h',
                    marker_color='#10b981',
                    text=[f"{p*100:.1f}%" for p in df_chart['prob']],
                    textposition='auto',
                ))
                fig.update_layout(
                    title="Probabilitas Alternatif",
                    height=300, margin=dict(l=0, r=0, t=30, b=0),
                    yaxis_autorange="reversed"
                )
                st.plotly_chart(fig, use_container_width=True)

            # AI Reasoning Panel
            st.markdown("### 🤖 Reasoning AI (Google Gemini)")
            if api_key and top['prob'] > 0.1:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"""
                    Sebagai ahli patologi tanaman, jelaskan mengapa gejala {symptoms} 
                    diduga kuat sebagai {top['name']} (probabilitas {top['prob']*100:.1f}%).
                    Berikan saran penanganan teknis dan estimasi dampak ekonomi jika tidak ditangani.
                    Gunakan Bahasa Indonesia yang profesional namun mudah dimengerti petani.
                    """
                    with st.spinner("AI sedang menyusun penjelasan..."):
                        response = model.generate_content(prompt)
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #059669; background: #f0fdf4;">
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Gagal memuat Reasoning AI: {str(e)}")
            else:
                st.info("Tambahkan API Key di sidebar untuk mendapatkan penjelasan naratif dari AI.")

            # Recommendations
            st.markdown("### 💊 Protokol Penanganan & Pencegahan")
            r1, r2 = st.columns(2)
            with r1:
                st.markdown("**Tindakan Kuratif (Pengobatan):**")
                for t in top['info']['treatment']:
                    st.write(f"✅ {t}")
            with r2:
                st.markdown("**Tindakan Preventif (Pencegahan):**")
                for p in top['info']['prevention']:
                    st.write(f"🛡️ {p}")

    elif menu == "📜 Riwayat Diagnostik":
        st.subheader("📜 Riwayat Analisis Lahan")
        st.info("Fitur ini akan menampilkan sejarah diagnosis berdasarkan lokasi lahan Anda.")
        st.warning("Penyimpanan riwayat sedang dalam pengembangan (Alpha v2.3).")

    elif menu == "📚 Database Penyakit":
        st.subheader("📚 Ensiklopedia Penyakit & Hama")
        for name, info in DISEASE_DATABASE.items():
            with st.expander(f"🔍 {name} - Severity: {info['severity']}"):
                st.markdown(f"**Penyebab:** {info['causes']}")
                st.markdown("**Gejala Utama:**")
                for s, w in info['symptoms'].items():
                    st.write(f"- {s} (Bobot: {w})")
                st.divider()
                st.markdown("**Treatment:**")
                for t in info['treatment']: st.write(f"- {t}")

if __name__ == "__main__":
    main()
