# AgriSensa Command Center - Professional Dashboard
# Modern UI with Glassmorphism and Advanced Navigation

import streamlit as st
from datetime import datetime

# Auth import
from utils.auth import is_authenticated, login, logout, get_current_user, show_user_info_sidebar

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="AgriSensa Command Center",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/agrisensa',
        'About': "© 2025 AgriSensa Intelligence Systems"
    }
)


# ========== MODERN UI STYLING ==========
st.markdown("""
<style>
    /* GLOBAL THEME */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* BACKGROUND ANIMATION */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(16, 185, 129, 0.1) 0%, rgb(0, 0, 0, 0) 40%),
                    radial-gradient(circle at 90% 80%, rgb(5, 150, 105, 0.1) 0%, rgb(0, 0, 0, 0) 40%);
    }

    /* HERO SECTION */
    .hero-container {
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(236, 253, 245, 0.8) 0%, rgba(255, 255, 255, 0.4) 100%);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 3rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-align: center !important;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #4b5563;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        text-align: center !important;
        line-height: 1.6;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        cursor: default;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: #ecfdf5;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.5;
    }
    
    /* METRICS BADGE */
    .metric-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background: #ecfdf5;
        border-radius: 50px;
        color: #059669;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    /* EDUCATION CERTIFICATION BADGE */
    .edu-cert-badge {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(245, 158, 11, 0.25) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(251, 191, 36, 0.4);
        border-radius: 16px;
        margin: 1.5rem auto;
        box-shadow: 0 8px 32px rgba(251, 191, 36, 0.2);
        transition: all 0.3s ease;
    }
    .edu-cert-badge:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 40px rgba(251, 191, 36, 0.3);
    }
    .edu-cert-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .edu-cert-content {
        text-align: left;
    }
    .edu-cert-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #92400e;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .edu-cert-level {
        font-size: 1.25rem;
        font-weight: 800;
        color: #78350f;
        margin-bottom: 2px;
    }
    .edu-cert-desc {
        font-size: 0.8rem;
        color: #a16207;
    }
    .edu-cert-stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
    }
    .edu-stat {
        font-size: 0.7rem;
        color: #92400e;
        background: rgba(251, 191, 36, 0.2);
        padding: 4px 10px;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ========== TRANSLATION DICTIONARY ==========
TRANSLATIONS = {
    "ID": {
        "hero_title": "AgriSensa Intelligence",
        "hero_subtitle": "Superapp Pertanian Modern yang mengintegrasikan IoT, Analisis Satelit, dan Kecerdasan Buatan untuk revolusi ketahanan pangan.",
        "badges": ["🚀 v4.0.0 (Dec 2025)", "⚡ AI Powered", "🌍 Enterprise Grade"],
        "section_main": "🛠️ Modul Operasional Utama",
        "section_secondary": "📚 Pusat Pengetahuan & Analisis",
        "cards": {
            "planner": {"title": "Harvest Planner", "desc": "Perencanaan panen berbasis AI, cuaca, dan target profitabilitas presisi.", "btn": "Buka Planner"},
            "vision": {"title": "AgriSensa Vision", "desc": "Diagnosis hama & penyakit tanaman instan menggunakan kamera HP/Drone.", "btn": "Mulai Scan"},
            "gis": {"title": "GIS Intelligence", "desc": "Pemetaan lahan interaktif, kesesuaian tanah, dan analisis topografi.", "btn": "Buka Peta"},
            "climate": {"title": "Smart Climate", "desc": "Prediksi cuaca mikro real-time untuk penjadwalan pertanian yang akurat.", "btn": "Cek Cuaca"}
        },
        "groups": {
            "nutrition": {"title": "💊 Manajemen Nutrisi", "sub": "Kalkulator Pupuk, Analisis NPK, Katalog Harga", "btn": "Akses Modul Pupuk"},
            "protection": {"title": "🛡️ Proteksi Tanaman", "sub": "Pestisida Nabati, Bahan Aktif, Dokter Tanaman", "btn": "Cek Hama & Penyakit"},
            "business": {"title": "📈 Bisnis & Riset", "sub": "Analisis Usaha Tani, Statistik Penelitian", "btn": "Analisis Profit (RAB)"}
        },
        "tip": "💡 **Tip Hari Ini:** Gunakan fitur *AgriSensa Vision* di pagi hari untuk pencahayaan terbaik.",
        "status": "System Status: 🟢 Online"
    },
    "EN": {
        "hero_title": "AgriSensa Intelligence",
        "hero_subtitle": "Modern Agriculture Superapp integrating IoT, Satellite Analysis, and Artificial Intelligence for food security revolution.",
        "badges": ["🚀 v4.0.0 (Dec 2025)", "⚡ AI Powered", "🌍 Enterprise Grade"],
        "section_main": "🛠️ Core Operational Modules",
        "section_secondary": "📚 Knowledge & Analysis Center",
        "cards": {
            "planner": {"title": "Harvest Planner", "desc": "AI-based harvest planning, weather integration, and precision profitability targets.", "btn": "Open Planner"},
            "vision": {"title": "AgriSensa Vision", "desc": "Instant pest & disease diagnosis using Mobile Camera/Drone.", "btn": "Start Scan"},
            "gis": {"title": "GIS Intelligence", "desc": "Interactive land mapping, soil suitability, and topographic analysis.", "btn": "Open Map"},
            "climate": {"title": "Smart Climate", "desc": "Real-time micro-weather prediction for accurate agricultural scheduling.", "btn": "Check Weather"}
        },
        "groups": {
            "nutrition": {"title": "💊 Nutrition Management", "sub": "Fertilizer Calculator, NPK Analysis, Price Catalog", "btn": "Access Fertilizer Module"},
            "protection": {"title": "🛡️ Plant Protection", "sub": "Botanical Pesticides, Active Ingredients, AI Plant Doctor", "btn": "Check Pests & Diseases"},
            "business": {"title": "📈 Business & Research", "sub": "Farm Business Analysis, Research Statistics", "btn": "Profit Analysis (RAB)"}
        },
        "tip": "💡 **Tip of the Day:** Use *AgriSensa Vision* in the morning for best lighting conditions.",
        "status": "System Status: 🟢 Online"
    }
}

def show_login_page():
    """Show beautiful login page with registration."""
    from utils.auth import register
    
    st.markdown("""
    <style>
        .login-hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-radius: 24px;
            margin-bottom: 2rem;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
    </style>
    <div class="login-hero">
        <div class="login-title">🌾 AgriSensa</div>
        <p style="color: #065f46; margin-top: 0.5rem;">Smart Agriculture Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Tabs for Login and Register
        tab_login, tab_register = st.tabs(["🔐 Login", "📝 Daftar Baru"])
        
        with tab_login:
            st.markdown("### Masuk ke Akun Anda")
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="admin / demo / petani")
                password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
                
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
                
                if login_btn:
                    if username and password:
                        success, message = login(username, password)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.warning("Masukkan username dan password")
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #6b7280; font-size: 0.85rem;">
                <strong>Demo Accounts:</strong><br>
                👨‍💼 admin / admin123<br>
                👤 demo / demo123<br>
                👨‍🌾 petani / petani123
            </div>
            """, unsafe_allow_html=True)
        
        with tab_register:
            st.markdown("### Buat Akun Baru")
            st.info("📝 Daftar gratis untuk mengakses semua fitur AgriSensa!")
            
            with st.form("register_form"):
                reg_name = st.text_input("👤 Nama Lengkap *", placeholder="contoh: Budi Tani")
                reg_username = st.text_input("📛 Username *", placeholder="minimal 3 karakter")
                reg_email = st.text_input("📧 Email", placeholder="email@example.com (opsional)")
                reg_password = st.text_input("🔑 Password *", type="password", placeholder="minimal 6 karakter")
                reg_password2 = st.text_input("🔑 Konfirmasi Password *", type="password", placeholder="ulangi password")
                
                register_btn = st.form_submit_button("✨ Daftar Sekarang", use_container_width=True, type="primary")
                
                if register_btn:
                    if reg_password != reg_password2:
                        st.error("❌ Password tidak cocok!")
                    elif not reg_name or not reg_username or not reg_password:
                        st.warning("⚠️ Lengkapi semua field yang wajib (*)")
                    else:
                        success, message = register(reg_username, reg_password, reg_name, reg_email)
                        if success:
                            st.success(f"🎉 {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        # Features preview
        st.markdown("---")
        st.markdown("#### ✨ Fitur Premium AgriSensa")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("✅ 55+ Modul Pertanian")
            st.markdown("✅ AI Plant Doctor")
            st.markdown("✅ GIS & Pemetaan")
        with col_f2:
            st.markdown("✅ Analisis Cuaca")
            st.markdown("✅ Kalkulator Pupuk")
            st.markdown("✅ Database Lengkap")



def main():
    # === CHECK AUTHENTICATION ===
    # DISABLED by User Request (No mandatory login)
    # if not is_authenticated():
    #     show_login_page()
    #     return
    
    # === SHOW USER INFO IN SIDEBAR ===
    show_user_info_sidebar()
    
    # === LANGUAGE SELECTOR ===
    lang_code = st.sidebar.selectbox("🌐 Language / Bahasa", ["Bahasa Indonesia", "English"], index=0)
    lang = "ID" if lang_code == "Bahasa Indonesia" else "EN"
    
    T = TRANSLATIONS[lang]

    # ========== ONBOARDING SYSTEM ==========
    import random
    
    # Initialize user profile in session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'role': None,
            'experience': None,
            'focus': [],
            'onboarding_complete': False,
            'visited_modules': [],
            'tip_index': random.randint(0, 9)
        }
    
    # Tips database
    TIPS_DATABASE = [
        "💡 Gunakan **AgriSensa Vision** di pagi hari untuk pencahayaan terbaik saat scan penyakit.",
        "🌱 Nilai **Brix tinggi** (>12°) menandakan tanaman sehat dan tahan hama.",
        "💧 Irigasi **defisit terkontrol** di fase pematangan buah meningkatkan kadar gula.",
        "🌾 Rasio **C/N ideal** untuk kompos cepat matang adalah 25-30:1.",
        "🐔 FCR broiler ideal < 1.6 menandakan efisiensi pakan yang baik.",
        "📊 Cek **Dashboard KPI** secara rutin untuk monitoring performa usaha tani.",
        "🔬 **Mikoriza** dapat meningkatkan penyerapan fosfor hingga 10x lipat.",
        "🌡️ Suhu optimal fotosintesis C3 (padi) adalah 25-30°C.",
        "♻️ Kotoran ternak bisa bernilai Rp 8.000-15.000/kg jika diolah jadi vermikompos.",
        "🗺️ Gunakan **GIS Intelligence** untuk analisis kesesuaian lahan sebelum tanam."
    ]
    
    # Role-based module recommendations
    MODULE_RECOMMENDATIONS = {
        'petani': {
            'title': '🌾 Rekomendasi untuk Petani',
            'modules': [
                {'name': '🧮 Kalkulator Pupuk', 'page': '3_🧮_Kalkulator_Pupuk', 'desc': 'Hitung kebutuhan pupuk presisi'},
                {'name': '🌤️ Cuaca Pertanian', 'page': '27_🌤️_Cuaca_Pertanian', 'desc': 'Prediksi cuaca untuk jadwal tanam'},
                {'name': '🔍 Diagnostik Gejala', 'page': '10_🔍_Diagnostik_Gejala', 'desc': 'Identifikasi penyakit tanaman'},
                {'name': '💰 Analisis Usaha Tani', 'page': '28_💰_Analisis_Usaha_Tani', 'desc': 'Hitung RAB dan profitabilitas'}
            ]
        },
        'penyuluh': {
            'title': '👨‍🏫 Rekomendasi untuk Penyuluh',
            'modules': [
                {'name': '📢 Ruang Kerja PPL', 'page': '45_📢_Ruang_Kerja_PPL_Final', 'desc': 'Dashboard tugas & laporan'},
                {'name': '🎓 Kurikulum Pelatihan', 'page': '53_🎓_Kurikulum_Pelatihan', 'desc': 'Modul pelatihan terstruktur'},
                {'name': '🌿 Dokter Tanaman AI', 'page': '13_🌿_Dokter_Tanaman_AI', 'desc': 'Diagnosa penyakit dengan AI'},
                {'name': '📚 Pusat Pengetahuan', 'page': '17_📚_Pusat_Pengetahuan', 'desc': 'Referensi pengetahuan pertanian'}
            ]
        },
        'akademisi': {
            'title': '🎓 Rekomendasi untuk Akademisi',
            'modules': [
                {'name': '🌱 Fisiologi Tumbuhan', 'page': '29_🌱_Fisiologi_Tumbuhan', 'desc': 'Hormon & proses fisiologis'},
                {'name': '🧬 Genetika Pemuliaan', 'page': '31_🧬_Genetika_Pemuliaan', 'desc': 'Pemuliaan tanaman'},
                {'name': '🔬 Asisten Penelitian', 'page': '12_🔬_Asisten_Penelitian', 'desc': 'Bantuan riset ilmiah'},
                {'name': '📚 Pusat Pengetahuan', 'page': '17_📚_Pusat_Pengetahuan', 'desc': 'Ensiklopedia pertanian'}
            ]
        },
        'mahasiswa': {
            'title': '📚 Rekomendasi untuk Mahasiswa',
            'modules': [
                {'name': '📚 Pusat Pengetahuan', 'page': '17_📚_Pusat_Pengetahuan', 'desc': 'Mulai belajar dari sini'},
                {'name': '🌱 Fisiologi Tumbuhan', 'page': '29_🌱_Fisiologi_Tumbuhan', 'desc': 'Dasar fisiologi'},
                {'name': '🧮 Kalkulator Pupuk', 'page': '3_🧮_Kalkulator_Pupuk', 'desc': 'Latihan perhitungan'},
                {'name': '🔍 Diagnostik Gejala', 'page': '10_🔍_Diagnostik_Gejala', 'desc': 'Belajar identifikasi'}
            ]
        }
    }

    
    # ===== ONBOARDING MODAL (First-time user) =====
    if not st.session_state.user_profile['onboarding_complete']:
        st.markdown("""
        <style>
            .onboarding-modal {
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border-radius: 24px;
                padding: 2rem;
                border: 2px solid #10b981;
                margin-bottom: 2rem;
                box-shadow: 0 20px 60px rgba(16, 185, 129, 0.2);
            }
            .onboarding-title {
                font-size: 2rem;
                font-weight: 800;
                color: #064e3b;
                text-align: center;
                margin-bottom: 0.5rem;
            }
            .onboarding-subtitle {
                text-align: center;
                color: #047857;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="onboarding-modal">
            <div class="onboarding-title">👋 Selamat Datang di AgriSensa!</div>
            <div class="onboarding-subtitle">Bantu kami personalisasi pengalaman Anda dengan menjawab 3 pertanyaan singkat</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("onboarding_form"):
            st.markdown("### 1️⃣ Apa peran Anda?")
            role = st.radio(
                "Pilih satu:",
                ["🌾 Petani / Pelaku Usaha Tani", "👨‍🏫 Penyuluh Pertanian (PPL)", 
                 "🎓 Akademisi / Peneliti", "📚 Mahasiswa / Pelajar"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.markdown("### 2️⃣ Tingkat pengalaman Anda?")
            experience = st.radio(
                "Pilih satu:",
                ["🌱 Pemula (baru mulai)", "🌿 Menengah (1-5 tahun)", "🌳 Expert (>5 tahun)"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.markdown("### 3️⃣ Fokus komoditas Anda? (bisa pilih lebih dari satu)")
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                focus_padi = st.checkbox("🌾 Padi")
                focus_jagung = st.checkbox("🌽 Jagung")
            with col_f2:
                focus_sayur = st.checkbox("🥬 Sayuran")
                focus_buah = st.checkbox("🍎 Buah-buahan")
            with col_f3:
                focus_perkebunan = st.checkbox("🌴 Perkebunan")
                focus_hortikultura = st.checkbox("🌸 Hortikultura")
            with col_f4:
                focus_peternakan = st.checkbox("🐄 Peternakan")
                focus_perikanan = st.checkbox("🐟 Perikanan")
            
            submitted = st.form_submit_button("🚀 Mulai Jelajahi AgriSensa", type="primary", use_container_width=True)
            
            if submitted:
                # Parse role
                role_map = {
                    "🌾 Petani / Pelaku Usaha Tani": "petani",
                    "👨‍🏫 Penyuluh Pertanian (PPL)": "penyuluh",
                    "🎓 Akademisi / Peneliti": "akademisi",
                    "📚 Mahasiswa / Pelajar": "mahasiswa"
                }
                exp_map = {
                    "🌱 Pemula (baru mulai)": "pemula",
                    "🌿 Menengah (1-5 tahun)": "menengah",
                    "🌳 Expert (>5 tahun)": "expert"
                }
                
                # Build focus list
                focus_list = []
                if focus_padi: focus_list.append("padi")
                if focus_jagung: focus_list.append("jagung")
                if focus_sayur: focus_list.append("sayuran")
                if focus_buah: focus_list.append("buah")
                if focus_perkebunan: focus_list.append("perkebunan")
                if focus_hortikultura: focus_list.append("hortikultura")
                if focus_peternakan: focus_list.append("peternakan")
                if focus_perikanan: focus_list.append("perikanan")
                
                # Save to session
                st.session_state.user_profile = {
                    'role': role_map.get(role, 'petani'),
                    'experience': exp_map.get(experience, 'pemula'),
                    'focus': focus_list if focus_list else ['umum'],
                    'onboarding_complete': True,
                    'visited_modules': ['Home'],
                    'tip_index': random.randint(0, len(TIPS_DATABASE)-1)
                }
                
                st.balloons()
                st.rerun()
        
        # Stop rendering rest of page until onboarding complete
        st.stop()
    
    # ===== TIP OF THE DAY (for returning users) =====
    tip_index = st.session_state.user_profile.get('tip_index', 0)
    current_tip = TIPS_DATABASE[tip_index % len(TIPS_DATABASE)]
    
    st.info(current_tip)
    
    # ===== PERSONALIZED WELCOME =====
    user_role = st.session_state.user_profile.get('role', 'petani')
    user_exp = st.session_state.user_profile.get('experience', 'pemula')
    user_focus = st.session_state.user_profile.get('focus', [])
    
    role_emoji = {'petani': '🌾', 'penyuluh': '👨‍🏫', 'akademisi': '🎓', 'mahasiswa': '📚'}
    role_display = {'petani': 'Petani', 'penyuluh': 'Penyuluh', 'akademisi': 'Akademisi', 'mahasiswa': 'Mahasiswa'}
    exp_display = {'pemula': 'Pemula', 'menengah': 'Menengah', 'expert': 'Expert'}
    
    # Show personalized welcome in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**{role_emoji.get(user_role, '👤')} Profil Anda**")
        st.markdown(f"- Role: **{role_display.get(user_role, 'Pengguna')}**")
        st.markdown(f"- Level: **{exp_display.get(user_exp, 'Pemula')}**")
        if user_focus:
            st.markdown(f"- Fokus: {', '.join(user_focus[:3])}")
        
        if st.button("🔄 Reset Profil", use_container_width=True):
            st.session_state.user_profile['onboarding_complete'] = False
            st.rerun()

    # === HERO SECTION ===
    st.markdown(f"""
        <div class="hero-container" style="display: flex; flex-direction: column; align-items: center; text-align: center; justify-content: center;">
            <div style="margin-bottom: 1rem; display: flex; justify-content: center; gap: 10px;">
                <span class="metric-badge">{T['badges'][0]}</span>
                <span class="metric-badge">{T['badges'][1]}</span>
                <span class="metric-badge">{T['badges'][2]}</span>
            </div>
            <h1 class="hero-title" style="text-align: center; margin: 0 auto; width: 100%;">{T['hero_title']}</h1>
            <p class="hero-subtitle" style="text-align: center; margin: 10px auto; width: 80%; display: block;">
                {T['hero_subtitle']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== PERSONALIZED RECOMMENDATIONS =====
    recommendations = MODULE_RECOMMENDATIONS.get(user_role, MODULE_RECOMMENDATIONS['petani'])
    
    st.markdown(f"### {recommendations['title']}")
    st.markdown("*Modul yang direkomendasikan berdasarkan profil Anda:*")
    
    rec_cols = st.columns(4)
    for i, module in enumerate(recommendations['modules']):
        with rec_cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{module['name'].split()[0]}</div>
                <div style="font-weight: 600; color: #065f46; font-size: 0.9rem;">{module['name'].split(' ', 1)[1] if len(module['name'].split()) > 1 else module['name']}</div>
                <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">{module['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Buka", key=f"rec_{i}", use_container_width=True):
                st.switch_page(f"pages/{module['page']}.py")
    
    st.markdown("---")

    # === EDUCATION CERTIFICATION BADGE (QR Code) ===
    import qrcode
    from io import BytesIO
    import base64
    
    # Create QR code with certification info
    cert_url = "https://github.com/yandri918/agrisensa-streamlit"
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(f"{cert_url}\n\n🎓 S1-S2 Agriculture Level\n📚 56+ Modul\n📝 300K+ Karakter\n🔬 Referensi Ilmiah")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#064e3b", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    cert_col1, cert_col2, cert_col3 = st.columns([1, 1, 1])
    with cert_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #ecfdf5, #d1fae5); border-radius: 16px; border: 1px solid #10b981;">
            <img src="data:image/png;base64,{qr_base64}" style="width: 120px; height: 120px; margin-bottom: 8px;">
            <div style="font-size: 0.7rem; color: #065f46; font-weight: 600;">🎓 S1-S2 Agriculture Level</div>
            <div style="font-size: 0.6rem; color: #047857;">Scan untuk verifikasi</div>
        </div>
        """, unsafe_allow_html=True)


    # === SATELLITE APPS PORTAL ===
    st.markdown("---")
    st.markdown("### 🚀 Hub Aplikasi Satelit")
    st.markdown("Akses aplikasi spesifik untuk kebutuhan pertanian Anda:")

    # Get URLs from secrets or default to localhost
    # Official Satellite URLs (Default)
    DEFAULT_URLS = {
        "commodities": "https://budidaya.streamlit.app/",
        "tech": "https://teknology.streamlit.app/",
        "biz": "https://busines.streamlit.app/",
        "eco": "https://ekosistem.streamlit.app/",
        "livestock": "https://livestoc.streamlit.app/Peternakan_Perikanan"
    }

    # Get URLs from secrets or use default
    def get_url(key, port):
        # Check if secrets exist and have the key
        try:
            if "satellites" in st.secrets:
                return st.secrets["satellites"].get(key, DEFAULT_URLS.get(key, f"http://localhost:{port}"))
        except FileNotFoundError:
            pass
        # Fallback to default production URL or localhost
        return DEFAULT_URLS.get(key, f"http://localhost:{port}")

    url_comm = get_url("commodities", 8502)
    url_tech = get_url("tech", 8503)
    url_biz = get_url("biz", 8504)
    url_eco = get_url("eco", 8505)
    url_live = get_url("livestock", 8506)

    sat1, sat2, sat3 = st.columns(3)

    with sat1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🌾</div>
            <div class="card-title">AgriSensa Commodities</div>
            <div class="card-desc">Panduan spesifik Padi, Sayur, Buah, Sawit, & Jamur.</div>
            <a href="{url_comm}" target="_blank" style="text-decoration: none;">
                <div style="background: #10b981; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with sat2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🛰️</div>
            <div class="card-title">AgriSensa Tech</div>
            <div class="card-desc">Advanced Tools: IoT, Drone, GIS, & Genetika.</div>
            <a href="{url_tech}" target="_blank" style="text-decoration: none;">
                <div style="background: #3b82f6; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with sat3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">📈</div>
            <div class="card-title">AgriSensa Biz</div>
            <div class="card-desc">Analisis Bisnis, Keuangan, & Rantai Pasok.</div>
            <a href="{url_biz}" target="_blank" style="text-decoration: none;">
                <div style="background: #8b5cf6; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    sat4, sat5, sat6 = st.columns(3)
    with sat4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">♻️</div>
            <div class="card-title">AgriSensa Eco</div>
            <div class="card-desc">Lingkungan, Konservasi, & Pengolahan Sampah.</div>
            <a href="{url_eco}" target="_blank" style="text-decoration: none;">
                <div style="background: #f59e0b; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with sat5:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🐟</div>
            <div class="card-title">AgriSensa Livestock</div>
            <div class="card-desc">Manajemen Peternakan & Perikanan.</div>
            <a href="{url_live}" target="_blank" style="text-decoration: none;">
                <div style="background: #0ea5e9; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
    with sat6:
        url_krisan = "https://budidayakrisan.streamlit.app/"
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🌸</div>
            <div class="card-title">AgriSensa Chrysanthemum</div>
            <div class="card-desc">Panduan Spesifik Budidaya Krisan & Tanaman Hias.</div>
            <a href="{url_krisan}" target="_blank" style="text-decoration: none;">
                <div style="background: #db2777; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; font-weight: 600;">
                    Buka Aplikasi ↗
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # === QUICK ACTIONS GRID ===
    st.subheader(T['section_main'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🎯</div>
            <div class="card-title">{T['cards']['planner']['title']}</div>
            <div class="card-desc">{T['cards']['planner']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        # Fix: Module is in AgriSensa Tech, redirect to URL
        if st.button(T['cards']['planner']['btn'], key="btn_planner", use_container_width=True):
            # Use javascript to open new tab because it's external app
             st.markdown(f'<meta http-equiv="refresh" content="0;url={url_tech}/Perencana_Panen_AI">', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🛸</div>
            <div class="card-title">{T['cards']['vision']['title']}</div>
            <div class="card-desc">{T['cards']['vision']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['vision']['btn'], key="btn_vision", use_container_width=True):
            st.switch_page("pages/31_🛸_AgriSensa_Vision.py")

    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🗺️</div>
            <div class="card-title">{T['cards']['gis']['title']}</div>
            <div class="card-desc">{T['cards']['gis']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['gis']['btn'], key="btn_gis", use_container_width=True):
            st.switch_page("pages/29_🛰️_AgriSensa_GIS.py")
            
    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🌤️</div>
            <div class="card-title">{T['cards']['climate']['title']}</div>
            <div class="card-desc">{T['cards']['climate']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['climate']['btn'], key="btn_weather", use_container_width=True):
             st.switch_page("pages/27_🌤️_Cuaca_Pertanian.py")

    # === SECONDARY FEATURES ===
    st.markdown("---")
    st.subheader(T['section_secondary'])
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['nutrition']['title']}")
            st.caption(T['groups']['nutrition']['sub'])
            if st.button(T['groups']['nutrition']['btn'], use_container_width=True):
                 st.switch_page("pages/3_🧮_Kalkulator_Pupuk.py")
            st.markdown("- [Katalog Pupuk & Harga](pages/25_🧪_Katalog_Pupuk_Harga.py)")
            st.markdown("- [Rekomendasi Terpadu](pages/14_🎯_Rekomendasi_Terpadu.py)")

    with c2:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['protection']['title']}")
            st.caption(T['groups']['protection']['sub'])
            if st.button(T['groups']['protection']['btn'], use_container_width=True):
                 st.switch_page("pages/19_🐛_Panduan_Hama_Penyakit.py")
            st.markdown("- [Direktori Bahan Aktif](pages/26_🔬_Direktori_Bahan_Aktif.py)")
            st.markdown("- [Resep Pestisida Nabati](pages/18_🌿_Pestisida_Nabati.py)")

    with c3:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['business']['title']}")
            st.caption(T['groups']['business']['sub'])
            if st.button(T['groups']['business']['btn'], use_container_width=True):
                 st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
            st.markdown("- [Asisten Penelitian AI](pages/12_🔬_Asisten_Penelitian.py)")
            st.markdown("- [Prediksi Tren Harga](pages/6_📈_Analisis_Tren_Harga.py)")

    # === SYSTEM STATUS ===
    st.markdown("---")
    col_stat1, col_stat2 = st.columns([3, 1])
    
    with col_stat1:
        st.info(T['tip'])
        
    with col_stat2:
        st.markdown(f"""
        <div style="text-align: right; color: #9ca3af; font-size: 0.8rem;">
            {T['status']}<br>
            Server Time: {datetime.now().strftime('%H:%M WIB')}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
