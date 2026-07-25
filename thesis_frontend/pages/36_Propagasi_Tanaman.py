import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Teknologi Propagasi Tanaman - AgriSensa",
    page_icon="🧬",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🧬 Teknologi Propagasi & Pembibitan")
st.markdown("**Plant Propagation: Seni & Sains Menggandakan Tanaman**")

# Main tabs
tab_intro, tab_vegetatif, tab_kultur, tab_nursery, tab_kalkulator, tab_bonsai = st.tabs([
    "📖 Prinsip Dasar",
    "🌿 Vegetatif Makro",
    "🧪 Kultur Jaringan",
    "🏡 Manajemen Nursery",
    "🧮 Kalkulator Bibit",
    "🌳 Seni Bonsai"
])

# ===== TAB 1: PRINSIP DASAR =====
with tab_intro:
    st.header("📖 Prinsip Dasar Propagasi")
    
    st.markdown("""
    ### Apa itu Propagasi?
    
    **Propagasi Tanaman** adalah proses perbanyakan tanaman untuk melestarikan sifat-sifat unggul (kloning) atau menghasilkan varietas baru (breeding).
    
    **Dua Metode Utama:**
    
    1.  **Seksual (Generatif):**
        *   Menggunakan **Biji**.
        *   **Keunggulan:** Murah, mudah, sistem akar kuat (akar tunggang).
        *   **Kelemahan:** Sifat anakan heterogen (tidak sama persis dengan induk), masa juvenil lama (lama berbuah).
        *   **Aplikasi:** Tanaman pangan (padi, jagung), batang bawah (rootstock).
        
    2.  **Aseksual (Vegetatif):**
        *   Menggunakan bagian tubuh tanaman (batang, daun, sel).
        *   **Keunggulan:** Sifat anakan **IDENTIK/KLON** dengan induk (True-to-Type), cepat berbuah.
        *   **Kelemahan:** Akar serabut (mudah roboh), rentan menularkan penyakit sistemik (virus).
        *   **Aplikasi:** Buah-buahan unggul (Durian, Mangga), Tanaman hias, Kehutanan.
    
    ---
    
    ### Konsep "Totipotensi"
    
    Dasar dari propagasi vegetatif adalah **TOTIPOTENSI SEL**, yaitu kemampuan setiap sel hidup tanaman untuk membelah diri (regenerasi) menjadi tanaman utuh yang sempurna jika diberi kondisi yang tepat.
    
    *   **Auxin:** Hormon pemicu akar.
    *   **Cytokinin:** Hormon pemicu tunas.
    *   **Rasio Auxin/Cytokinin:** Menentukan arah pertumbuhan (Akar vs Tunas).
    """)

# ===== TAB 2: VEGETATIF MAKRO =====
with tab_vegetatif:
    st.header("🌿 Propagasi Vegetatif Konvensional")
    
    st.markdown("""
    Teknik perbanyakan tanpa laboratorium, namun membutuhkan keahlian tangan (skill).
    
    ### 1. GRAFTING (Sambung Pucuk)
    Menyambungkan batang atas (**Scion**) yang unggul buahnya dengan batang bawah (**Rootstock**) yang kuat akarnya.
    
    *   **Tanaman:** Alpukat, Durian, Mangga, Kakao.
    *   **Kunci Keberhasilan:**
        1.  **Kambium Bertemu:** Sayatan harus rata dan kambium scion menempel pas dengan rootstock.
        2.  **Kelembaban:** Sambungan harus ditali rapat dan disungkup plastik (parafilm) agar tidak kering.
        3.  **Sterilitas:** Pisau harus tajam dan bersih (steril alkohol).
    *   **Jenis:**
        *   *V-Graft:* Sayatan bentuk V (paling umum).
        *   *Cleft Graft:* Sayatan celah.
    
    ### 2. BUDDING (Okulasi / Tempel Mata Tunas)
    Menempelkan satu mata tunas (bud) ke batang bawah.
    
    *   **Tanaman:** Jeruk, Karet, Mawar.
    *   **Kelebihan:** Hemat bahan entres (1 mata = 1 bibit).
    *   **Teknik:**
        *   *T-Budding:* Sayatan kulit rootstock bentuk T.
        *   *Chip Budding:* Sayatan keping (chip).
    
    ### 3. CUTTING (Stek)
    Memotong bagian tanaman (batang/daun) untuk diakarkan.
    
    *   **Tanaman:** Singkong (batang), Anggur (batang), Sansiviera (daun).
    *   **Tips:**
        *   Gunakan ZPT (Zat Pengatur Tumbuh) Auxin (Rootone-F/Bawang Merah) pada pangkal stek.
        *   Media harus porous (pasir/sekam bakar) agar tidak busuk.
        *   Kelembaban tinggi (sungkup).
    
    ### 4. LAYERING (Cangkok)
    Menumbuhkan akar pada batang yang masih menempel di pohon induk.
    
    *   **Tanaman:** Jambu Air, Mangga (skala hobi).
    *   **Kelebihan:** Tingkat keberhasilan tinggi karena nutrisi masih disuplai induk.
    *   **Kelemahan:** Merusak pohon induk jika terlalu banyak, akar serabut lemah.
    *   **Teknik:** Kerat kulit batang sampai kambium hilang (bersih/kering) → Bungkus media (kokopeat/tanah).
    """)

# ===== TAB 3: KULTUR JARINGAN =====
with tab_kultur:
    st.header("🧪 Kultur Jaringan (Tissue Culture)")
    
    st.markdown("""
    **Definisi:** Membudidayakan jaringan tanaman (eksplan) dalam kondisi steril di media buatan yang kaya nutrisi.
    
    **Keunggulan:**
    1.  **Massal:** 1 eksplan bisa jadi 10,000 bibit dalam 1 tahun.
    2.  **Bebas Penyakit:** Menggunakan meristem (pucuk) yang bebas virus.
    3.  **Seragam:** Kualitas bibit sama persis.
    
    ---
    
    ### Tahapan Kultur Jaringan
    
    #### 1. Persiapan Media (Kitchen Stage)
    Media paling umum: **Murashige & Skoog (MS)**.
    *   **Makro:** N, P, K, Ca, Mg, S (konsentrasi tinggi).
    *   **Mikro:** Fe, Mn, Zn, B, Cu, Mo, Co.
    *   **Vitamin:** Thiamine, Pyridoxine.
    *   **Gula:** Sumber energi (karena belum fotosintesis).
    *   **Agar:** Pemadat.
    *   **ZPT:** Auxin/Cytokinin (tergantung tujuan).
    *   **pH:** 5.8 (Kritis!)
    
    #### 2. Sterilisasi Eksplan (Critical Stage)
    Membunuh jamur/bakteri di permukaan eksplan tanpa membunuh sel tanaman.
    *   **Bahan:** Alkohol 70%, Pemutih (NaOCl/Bayclin), Fungisida, Bakterisida.
    *   **Tempat:** Di dalam Laminar Air Flow (LAF).
    
    #### 3. Inisiasi (Initiation)
    Menanam eksplan steril ke media. Tujuan: Eksplan hidup dan bebas kontaminasi.
    
    #### 4. Multiplikasi (Multiplication)
    Memperbanyak tunas.
    *   **ZPT:** Tinggi **Cytokinin** (BAP/Kinetin) untuk memacu percabangan tunas.
    *   *Subkultur:* Memindah/memecah rumpun setiap 3-4 minggu.
    
    #### 5. Pengakaran (Rooting)
    Menumbuhkan akar pada tunas yang sudah banyak.
    *   **ZPT:** Tinggi **Auxin** (IBA/NAA).
    *   Kadang ditambahkan arang aktif (charcoal) untuk menyerap racun fenol.
    
    #### 6. Aklimatisasi (Hardening)
    Memindah bibit botol (heterotrof/manja) ke lingkungan luar (autotrof).
    *   **Tahap Paling Rawan!**
    *   Keluarkan dari botol → Cuci bersih agar (gula mengundang jamur) → Tanam di cocopeat/sekam bakar steril → Sungkup plastik (kelembaban >90%) → Buka sungkup bertahap.
    """)

# ===== TAB 4: MANAJEMEN NURSERY =====
with tab_nursery:
    st.header("🏡 Manajemen Pembibitan (Nursery Management)")
    
    st.markdown("""
    Nursery yang baik menjamin bibit siap tanam (field-ready) dengan survival rate tinggi.
    
    ### Fasilitas Nursery
    
    1.  **Mother Plant Area (blok Pohon Induk):**
        *   Sumber mata entres/scion.
        *   Harus varietas unggul tervalidasi dan bebas penyakit.
    
    2.  **Production House (Rumah Produksi):**
        *   Tempat grafting/sowing.
        *   Atap UV plastik + Net 50%.
        *   Lantai semen/paving (kebersihan).
    
    3.  **Shade House (Area Pembesaran):**
        *   Naungan paranet (shading net).
        *   *Fase Awal:* Paranet 75% (cahaya 25%).
        *   *Fase Lanjut:* Paranet 50% (cahaya 50%).
    
    4.  **Open Area (Hardening off):**
        *   Full sun (cahaya 100%).
        *   Tempat bibit dilatih panas sebelum ke ladang (2-4 minggu sebelum jual).
    
    ---
    
    ### Media Tanam Standar
    
    Rumus umum: **Topsoil : Pupuk Kandang : Sekam = 1 : 1 : 1**
    *   **Topsoil:** Perekat dan penyimpan hara.
    *   **Pupuk Kandang:** Nutrisi.
    *   **Sekam/Pasir:** Porositas (drainase).
    
    *Catatan:* Untuk polybag kecil, hindari tanah liat murni (padat). Gunakan campuran cocopeat/sekam bakar.
    """)

# ===== TAB 5: KALKULATOR BIBIT =====
with tab_kalkulator:
    st.header("🧮 Kalkulator Kebutuhan Benih & Bibit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameter")
        luas_lahan = st.number_input("Luas Lahan (hektar)", value=1.0)
        jarak_tanam_x = st.number_input("Jarak Tanam Antar Baris (m)", value=3.0)
        jarak_tanam_y = st.number_input("Jarak Tanam Dalam Baris (m)", value=3.0)
        
        st.write("---")
        st.caption("Khusus Benih (Biji):")
        bobot_1000_butir = st.number_input("Bobot 1000 butir (gram)", value=25.0)
        daya_kecambah = st.slider("Daya Kecambah (%)", 50, 100, 85)
        cadangan = st.slider("Cadangan Penyulaman (%)", 0, 50, 10)
    
    with col2:
        st.subheader("Hasil Perhitungan")
        
        # Hitung populasi
        luas_m2 = luas_lahan * 10000
        populasi_teoritis = luas_m2 / (jarak_tanam_x * jarak_tanam_y)
        
        jumlah_bibit_sebar = populasi_teoritis * (1 + cadangan/100)
        
        st.metric("Total Populasi Tanaman (Teoritis)", f"{int(populasi_teoritis):,} pohon")
        st.metric(f"Kebutuhan Bibit (+Cadangan {cadangan}%)", f"{int(jumlah_bibit_sebar):,} bibit")
        
        # Hitung berat benih
        # (Jumlah bibit / (DK/100)) * berat per butir
        jumlah_butir_dibutuhkan = jumlah_bibit_sebar / (daya_kecambah/100)
        berat_benih_gr = jumlah_butir_dibutuhkan * (bobot_1000_butir / 1000)
        berat_benih_kg = berat_benih_gr / 1000
        
        st.info(f"Jika menanam dari biji:")
        st.metric("Estimasi Berat Benih Dibutuhkan", f"{berat_benih_kg:.2f} kg")
        st.caption(f"Asumsi: Daya kecambah {daya_kecambah}%, Bobot 1000 butir {bobot_1000_butir}g")

# ===== TAB 6: SENI BONSAI =====
with tab_bonsai:
    st.header("🌳 Seni & Sains Bonsai")
    
    st.markdown("""
    **Bonsai (盆栽)** adalah seni mengerdilkan tanaman dalam pot dangkal dengan tujuan meniru bentuk pohon tua di alam bebas.
    
    ---
    
    ### 5 Gaya Dasar (Basic Styles)
    
    1.  **Chokkan (Formal Upright):**
        *   Batang tegak lurus, meruncing ke atas (tapering).
        *   Dahan kiri-kanan seimbang.
        *   Kesan: Agung, kokoh, resmi.
    
    2.  **Moyogi (Informal Upright):**
        *   Batang tegak tapi berliuk (S-shape).
        *   Puncak pohon (apex) segaris dengan pangkal batang.
        *   Gaya paling populer dan natural.
    
    3.  **Shakan (Slanting):**
        *   Batang miring (45 derajat) seperti tertiup angin.
        *   Akar dominan di sisi berlawanan arah miring (penyeimbang).
    
    4.  **Kengai (Cascade):**
        *   Batang menjuntai ke bawah pot, seperti pohon di tebing curam.
        *   Apex berada di bawah dasar pot.
    
    5.  **Bunjin (Literati):**
        *   Batang kurus, tinggi, meliuk, minim dahan.
        *   Meniru lukisan tinta Cina kuno.
        *   Kesan: Elegan, puitis, struggle for life.
    
    ---
    
    ### Teknik Pembentukan
    
    #### 1. Pruning (Pemangkasan)
    *   **Maintenance Pruning:** Menjaga bentuk, membuang tunas liar.
    *   **Structural Pruning:** Memotong dahan besar untuk membentuk rangka dasar.
    *   *Tips:* Selalu gunakan gunting tajam (konkave cutter) agar luka cepat menutup kambium.
    
    #### 2. Wiring (Pengawatan)
    *   Membelitkan kawat (Aluminium/Tembaga) ke dahan untuk mengubah arah tumbuhnya.
    *   *Aturan:* Sudut kawat 45 derajat. Jangan menjepit dahan (implant). Lepas kawat sebelum melukai kulit (3-6 bulan).
    
    #### 3. Deadwood (Kayu Mati)
    *   **Jin:** Dahan yang dikupas kulitnya (kesan dahan mati tersambar petir).
    *   **Shari:** Batang yang dikupas sebagian kulitnya (kesan pohon tua lapuk).
    *   Gunakan Lime Sulfur untuk memutihkan dan mengawetkan kayu mati.
    
    ---
    
    ### Manajemen Akar & Repotting
    
    Bonsai bisa hidup ratusan tahun di pot kecil karena teknik **Repotting**.
    
    *   **Kapan:** Setiap 1-3 tahun (tergantung spesies & umur), saat akar sudah penuh (pot-bound).
    *   **Caranya:**
        1.  Keluarkan pohon.
        2.  Urai akar.
        3.  Potong 30% akar (terutama akar tunggang tebal). Sisakan akar serabut halus (feeder roots).
        4.  Ganti media baru (Akadama/Pasir Malang + Humus).
    
    *   **Fungsi:** Meremajakan sistem perakaran, memberi ruang tumbuh baru.
    
    ---
    
    ### Kriteria Tanaman Bonsai
    1.  **Berkayu keras (Woody):** Kambium aktif.
    2.  **Daun bisa mengecil:** Makin sering pruning, daun makin kecil.
    3.  **Umur panjang.**
    4.  **Spesies Populer:** Beringin (*Ficus*), Santigi (*Pemphis acidula*), Anting Putri (*Wrightia religiosa*), Cemara Udang (*Casuarina*).
    """)

