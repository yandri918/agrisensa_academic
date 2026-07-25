# AgriSensa Knowledge - Ensiklopedia Pertanian Digital
# Comprehensive agricultural knowledge base
# Version: 1.0.0

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="AgriSensa Knowledge", page_icon="📖", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== SESSION STATE ==========
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'read_articles' not in st.session_state:
    st.session_state.read_articles = []

# ========== KNOWLEDGE DATABASE ==========

# 1. DASAR-DASAR PERTANIAN
DASAR_PERTANIAN = {
    "sistem_pertanian": {
        "title": "Sistem-Sistem Pertanian Modern",
        "content": """
        ### 🌾 Sistem Pertanian Konvensional
        - Menggunakan input kimia (pupuk, pestisida)
        - Fokus pada produktivitas tinggi
        - Mekanisasi pertanian
        - **Kelebihan**: Produktivitas tinggi, efisien
        - **Kekurangan**: Degradasi tanah, polusi
        
        ### 🌱 Pertanian Organik
        - Tanpa input kimia sintetis
        - Menggunakan pupuk organik dan pestisida nabati
        - Fokus pada kesehatan tanah
        - **Kelebihan**: Ramah lingkungan, produk sehat
        - **Kekurangan**: Produktivitas lebih rendah, harga mahal
        
        ### 💧 Hidroponik
        - Tanaman tumbuh di media air bernutrisi
        - Tanpa tanah
        - Sistem: NFT, DFT, Wick, Drip
        - **Kelebihan**: Hemat air 90%, bebas hama tanah, produktivitas tinggi
        - **Kekurangan**: Investasi awal tinggi, butuh keahlian
        
        ### 🐟 Aquaponik
        - Kombinasi budidaya ikan dan tanaman
        - Kotoran ikan = nutrisi tanaman
        - Sistem sirkular
        - **Kelebihan**: Dua produk sekaligus, efisien
        - **Kekurangan**: Kompleks, butuh monitoring ketat
        
        ### 🏢 Vertical Farming
        - Pertanian bertingkat dalam gedung
        - Controlled environment
        - LED grow lights
        - **Kelebihan**: Hemat lahan, produksi sepanjang tahun
        - **Kekurangan**: Biaya energi tinggi, investasi besar
        """,
        "tags": ["sistem", "dasar", "pemula"],
        "difficulty": "beginner",
        "read_time": 5
    },
    "siklus_tanaman": {
        "title": "Siklus Pertumbuhan Tanaman",
        "content": """
        ### 📊 Fase Pertumbuhan Tanaman
        
        **1. Fase Perkecambahan (0-7 hari)**
        - Benih menyerap air (imbibisi)
        - Radikula muncul (akar primer)
        - Kotiledon membuka
        - **Kebutuhan**: Kelembaban tinggi, suhu hangat
        
        **2. Fase Vegetatif (7-40 hari)**
        - Pertumbuhan daun, batang, akar
        - Fotosintesis aktif
        - Pembentukan biomassa
        - **Kebutuhan**: N tinggi, cahaya penuh, air cukup
        
        **3. Fase Generatif (40-70 hari)**
        - Pembentukan bunga
        - Penyerbukan dan pembuahan
        - Pembentukan buah/biji
        - **Kebutuhan**: P dan K tinggi, suhu optimal
        
        **4. Fase Pematangan (70-90 hari)**
        - Buah/biji matang
        - Akumulasi gula/pati
        - Perubahan warna
        - **Kebutuhan**: Air dikurangi, K tinggi
        
        **5. Fase Penuaan**
        - Daun menguning
        - Fotosintesis menurun
        - Siap panen
        """,
        "tags": ["siklus", "pertumbuhan", "dasar"],
        "difficulty": "beginner",
        "read_time": 4
    },
    "faktor_pertumbuhan": {
        "title": "Faktor-Faktor Pertumbuhan Tanaman",
        "content": """
        ### ☀️ Cahaya
        - **Intensitas**: 10,000-50,000 lux untuk sayuran
        - **Durasi**: Tanaman hari panjang (>12 jam) vs hari pendek (<12 jam)
        - **Kualitas**: Spektrum merah (pertumbuhan) vs biru (pembungaan)
        
        ### 💧 Air
        - **Kebutuhan**: 400-800 L/kg biomassa
        - **Fungsi**: Fotosintesis, transportasi nutrisi, turgiditas
        - **Defisit**: Layu, pertumbuhan terhambat
        - **Kelebihan**: Akar busuk, defisiensi oksigen
        
        ### 🌡️ Suhu
        - **Optimal**: 20-30°C untuk kebanyakan tanaman
        - **Minimum**: <10°C = dormansi
        - **Maksimum**: >35°C = stress panas
        - **DIF (Day-Night)**: Perbedaan suhu siang-malam penting untuk kualitas
        
        ### 💨 Kelembaban
        - **Optimal**: 60-80% RH
        - **Rendah**: Transpirasi berlebih, stress air
        - **Tinggi**: Penyakit jamur, edema
        
        ### 🌬️ CO2
        - **Atmosfer**: 400 ppm
        - **Optimal**: 800-1200 ppm (greenhouse)
        - **Fungsi**: Bahan baku fotosintesis
        
        ### 🧪 Nutrisi
        - **Makro**: N, P, K, Ca, Mg, S
        - **Mikro**: Fe, Mn, Zn, Cu, B, Mo, Cl
        - **pH optimal**: 5.5-6.5 (hidroponik), 6.0-7.0 (tanah)
        """,
        "tags": ["faktor", "lingkungan", "dasar"],
        "difficulty": "intermediate",
        "read_time": 6
    }
}

# 2. DATABASE TANAMAN
DATABASE_TANAMAN = {
    "padi": {
        "title": "Padi (Oryza sativa)",
        "latin": "Oryza sativa",
        "family": "Poaceae",
        "content": """
        ### 📋 Profil Tanaman
        - **Nama Latin**: Oryza sativa
        - **Famili**: Poaceae (rumput-rumputan)
        - **Asal**: Asia Tenggara
        - **Umur**: 110-130 hari
        
        ### 🌍 Syarat Tumbuh
        - **Iklim**: Tropis, curah hujan 1500-2000 mm/tahun
        - **Ketinggian**: 0-1500 mdpl
        - **Suhu**: 22-32°C
        - **pH Tanah**: 5.5-7.0
        - **Jenis Tanah**: Liat, lempung (sawah)
        
        ### 🌱 Panduan Budidaya
        **Persiapan Lahan:**
        1. Bajak dan garu sawah
        2. Buat petakan dengan pematang
        3. Genangi air 5-10 cm
        
        **Penanaman:**
        - Bibit umur 18-25 hari
        - Jarak tanam: 25x25 cm atau 20x20 cm
        - 2-3 bibit per lubang
        
        **Pemupukan:**
        - **Dasar**: 100 kg Phonska/ha
        - **Susulan 1 (21 HST)**: 100 kg Urea + 50 kg Phonska/ha
        - **Susulan 2 (35 HST)**: 100 kg Urea/ha
        
        **Pengairan:**
        - Fase vegetatif: Genangan 5-10 cm
        - Fase generatif: Genangan 3-5 cm
        - 2 minggu sebelum panen: Dikeringkan
        
        ### 🐛 Hama & Penyakit
        - **Hama**: Wereng, penggerek batang, tikus
        - **Penyakit**: Blast, hawar daun, busuk batang
        
        ### 📊 Hasil Panen
        - **Produktivitas**: 5-7 ton GKP/ha
        - **Waktu Panen**: 110-130 HST (gabah kuning 80-90%)
        - **Rendemen**: 62-65% (GKP → beras)
        """,
        "tags": ["padi", "pangan", "sawah"],
        "difficulty": "intermediate",
        "read_time": 8
    },
    "cabai": {
        "title": "Cabai Merah (Capsicum annuum)",
        "latin": "Capsicum annuum",
        "family": "Solanaceae",
        "content": """
        ### 📋 Profil Tanaman
        - **Nama Latin**: Capsicum annuum
        - **Famili**: Solanaceae
        - **Asal**: Amerika Tengah dan Selatan
        - **Umur**: 90-120 hari
        
        ### 🌍 Syarat Tumbuh
        - **Ketinggian**: 200-2000 mdpl
        - **Suhu**: 20-30°C
        - **pH Tanah**: 6.0-7.0
        - **Curah Hujan**: 600-1250 mm/tahun
        - **Jenis Tanah**: Gembur, drainase baik
        
        ### 🌱 Panduan Budidaya
        **Persemaian:**
        1. Rendam benih 6 jam
        2. Semai di tray/polybag
        3. Pindah tanam umur 25-30 hari (4-6 daun)
        
        **Penanaman:**
        - Jarak tanam: 60x70 cm atau 50x70 cm
        - Buat bedengan tinggi 30 cm, lebar 100 cm
        - Mulsa plastik hitam perak
        
        **Pemupukan:**
        - **Dasar**: 10 ton pupuk kandang + 200 kg Phonska/ha
        - **Susulan**: 5 g NPK/tanaman setiap 2 minggu
        - **Tambahan**: KNO3 2 g/L (semprot daun)
        
        **Perawatan:**
        - Pasang ajir/turus
        - Pemangkasan tunas air
        - Penyiraman rutin (pagi/sore)
        
        ### 🐛 Hama & Penyakit
        - **Hama**: Thrips, kutu daun, ulat grayak
        - **Penyakit**: Antraknosa, layu fusarium, virus keriting
        
        ### 📊 Hasil Panen
        - **Produktivitas**: 15-25 ton/ha
        - **Panen**: Mulai 75 HST, interval 3-5 hari
        - **Kriteria**: Warna merah 80-100%
        - **Harga**: Rp 20,000-60,000/kg (fluktuatif)
        """,
        "tags": ["cabai", "hortikultura", "sayuran"],
        "difficulty": "advanced",
        "read_time": 8
    },
    "tomat": {
        "title": "Tomat (Solanum lycopersicum)",
        "latin": "Solanum lycopersicum",
        "family": "Solanaceae",
        "content": """
        ### 📋 Profil Tanaman
        - **Nama Latin**: Solanum lycopersicum
        - **Famili**: Solanaceae
        - **Umur**: 60-90 hari
        - **Tipe**: Determinate (terbatas) vs Indeterminate (tidak terbatas)
        
        ### 🌍 Syarat Tumbuh
        - **Ketinggian**: 700-1500 mdpl (dataran tinggi lebih baik)
        - **Suhu**: 20-27°C
        - **pH**: 6.0-6.8
        - **Cahaya**: Full sun (8+ jam/hari)
        
        ### 🌱 Budidaya
        **Persemaian**: 25-30 hari
        **Jarak Tanam**: 60x60 cm (determinate), 75x75 cm (indeterminate)
        
        **Pemupukan:**
        - NPK 16-16-16: 300 kg/ha (dasar)
        - KNO3 + Ca: Semprot setiap minggu (cegah blossom end rot)
        
        **Perawatan Khusus:**
        - Pruning (pemangkasan tunas samping)
        - Staking (ajir setinggi 2 m)
        - Pollination assistance (getar bunga)
        
        ### 📊 Hasil
        - **Produktivitas**: 20-40 ton/ha
        - **Harga**: Rp 8,000-15,000/kg
        """,
        "tags": ["tomat", "sayuran", "hortikultura"],
        "difficulty": "intermediate",
        "read_time": 6
    }
}

# 3. ILMU TANAH
ILMU_TANAH = {
    "jenis_tanah": {
        "title": "Jenis-Jenis Tanah di Indonesia",
        "content": """
        ### 🗺️ Klasifikasi Tanah Indonesia
        
        **1. Tanah Aluvial**
        - **Lokasi**: Dataran rendah, delta sungai
        - **Karakteristik**: Subur, tekstur liat-lempung
        - **Cocok untuk**: Padi sawah, palawija
        - **Contoh**: Pantura Jawa, Sumatera Timur
        
        **2. Tanah Andosol (Vulkanik)**
        - **Lokasi**: Sekitar gunung berapi
        - **Karakteristik**: Gembur, kaya mineral, pH asam
        - **Cocok untuk**: Sayuran, kopi, teh
        - **Contoh**: Jawa Barat, Jawa Tengah
        
        **3. Tanah Latosol**
        - **Lokasi**: Dataran tinggi
        - **Karakteristik**: Merah/kuning, miskin hara, pH asam
        - **Cocok untuk**: Perkebunan (karet, kelapa sawit)
        - **Perlakuan**: Perlu kapur dan pupuk organik
        
        **4. Tanah Podsolik**
        - **Lokasi**: Daerah beriklim basah
        - **Karakteristik**: Asam, miskin hara
        - **Cocok untuk**: Karet, kelapa sawit
        - **Perlakuan**: Pengapuran intensif
        
        **5. Tanah Gambut**
        - **Lokasi**: Rawa-rawa (Kalimantan, Sumatera)
        - **Karakteristik**: Organik tinggi, pH sangat asam (3-4)
        - **Cocok untuk**: Kelapa sawit, sagu
        - **Perlakuan**: Drainase, kapur dolomit
        
        **6. Tanah Regosol**
        - **Lokasi**: Pantai, gunung
        - **Karakteristik**: Pasir, miskin hara
        - **Cocok untuk**: Kelapa, jambu mete
        """,
        "tags": ["tanah", "jenis", "klasifikasi"],
        "difficulty": "intermediate",
        "read_time": 7
    },
    "ph_tanah": {
        "title": "pH Tanah dan Pengelolaannya",
        "content": """
        ### 🧪 Skala pH dan Pengaruhnya
        
        **pH < 5.5 (Sangat Asam)**
        - **Masalah**: Keracunan Al, Fe, Mn; defisiensi P, Ca, Mg
        - **Tanaman toleran**: Teh, kopi, nanas
        - **Perbaikan**: Kapur dolomit 2-4 ton/ha
        
        **pH 5.5-6.5 (Sedikit Asam) ✅ OPTIMAL**
        - **Ketersediaan nutrisi maksimal**
        - **Cocok untuk**: Kebanyakan tanaman
        
        **pH 6.5-7.5 (Netral)**
        - **Baik untuk**: Padi, jagung, kedelai
        
        **pH > 7.5 (Alkalin)**
        - **Masalah**: Defisiensi Fe, Mn, Zn, Cu
        - **Tanaman toleran**: Asparagus, bit
        - **Perbaikan**: Sulfur 200-500 kg/ha, pupuk asam
        
        ### 📏 Cara Mengukur pH
        1. **pH Meter Digital**: Akurat, cepat
        2. **Kertas Lakmus**: Murah, kurang akurat
        3. **Soil Test Kit**: Praktis, cukup akurat
        
        ### 🔧 Cara Memperbaiki pH
        
        **Menaikkan pH (Tanah Asam):**
        - Kapur pertanian (CaCO3): 1-3 ton/ha
        - Dolomit (CaMg(CO3)2): 1-2 ton/ha (bonus Mg)
        - Aplikasi 2-3 bulan sebelum tanam
        
        **Menurunkan pH (Tanah Alkalin):**
        - Sulfur: 200-500 kg/ha
        - Pupuk asam (ZA, amonium sulfat)
        - Bahan organik (kompos, gambut)
        """,
        "tags": ["pH", "tanah", "pengelolaan"],
        "difficulty": "intermediate",
        "read_time": 6
    }
}

# 3.5. PUPUK MAKRO SEKUNDER
PUPUK_MAKRO_SEKUNDER = {
    "kalsium": {
        "title": "Kalsium (Ca) - Unsur Hara Sekunder Penting",
        "content": """
        ### 🧪 Fungsi Kalsium dalam Tanaman
        
        **Peran Struktural:**
        - Komponen dinding sel (kalsium pektat)
        - Memperkuat struktur tanaman
        - Meningkatkan ketahanan terhadap penyakit
        
        **Peran Fisiologis:**
        - Aktivasi enzim
        - Permeabilitas membran sel
        - Pembelahan dan pemanjangan sel
        - Perkembangan akar
        - Kualitas buah (mencegah blossom end rot)
        
        ### 🔍 Gejala Defisiensi Kalsium
        
        **Pada Daun Muda:**
        - Daun muda keriput dan menggulung
        - Tepi daun nekrosis (mati)
        - Pertumbuhan terhambat
        
        **Pada Buah:**
        - Blossom end rot (tomat, cabai)
        - Bitter pit (apel)
        - Tip burn (selada, kubis)
        - Buah mudah busuk
        
        **Tanaman Rentan:**
        - Tomat, cabai, melon
        - Selada, kubis, sawi
        - Apel, anggur
        
        ### 🌾 Jenis Pupuk Kalsium
        
        **1. Kapur Pertanian (CaCO₃)**
        - **Kandungan Ca**: 32-40%
        - **Fungsi**: Menaikkan pH + sumber Ca
        - **Dosis**: 500-2000 kg/ha
        - **Aplikasi**: 2-4 minggu sebelum tanam
        - **Cocok untuk**: Tanah asam (pH <5.5)
        
        **2. Dolomit (CaMg(CO₃)₂)**
        - **Kandungan**: Ca 20-22%, Mg 10-13%
        - **Keunggulan**: Bonus magnesium
        - **Dosis**: 1-2 ton/ha
        - **Cocok untuk**: Tanah asam + defisiensi Mg
        
        **3. Gypsum (CaSO₄·2H₂O)**
        - **Kandungan**: Ca 23%, S 18%
        - **Keunggulan**: Tidak menaikkan pH
        - **Dosis**: 200-500 kg/ha
        - **Cocok untuk**: Tanah alkalis, tanah sodic
        - **Bonus**: Sumber sulfur
        
        **4. Kalsium Nitrat (Ca(NO₃)₂)**
        - **Kandungan**: Ca 19%, N 15.5%
        - **Keunggulan**: Larut air, cepat tersedia
        - **Dosis**: 100-200 kg/ha atau 1-2 g/L
        - **Aplikasi**: Fertigasi, hidroponik
        - **Cocok untuk**: Koreksi cepat, sayuran
        
        **5. Kalsium Klorida (CaCl₂)**
        - **Kandungan**: Ca 36%
        - **Aplikasi**: Semprot daun 2-5 g/L
        - **Fungsi**: Mencegah blossom end rot
        - **Frekuensi**: 7-10 hari sekali
        
        ### 📊 Kebutuhan Kalsium per Tanaman
        - **Tomat**: 150-200 kg Ca/ha
        - **Cabai**: 100-150 kg Ca/ha
        - **Kubis**: 200-250 kg Ca/ha
        - **Apel**: 80-120 kg Ca/ha
        
        ### 💡 Tips Aplikasi
        1. Untuk tanah asam: Gunakan kapur/dolomit
        2. Untuk tanah alkalis: Gunakan gypsum
        3. Untuk koreksi cepat: Kalsium nitrat (kocor/fertigasi)
        4. Untuk buah: Semprot kalsium klorida saat berbuah
        5. Jangan campur dengan pupuk fosfat (mengendap)
        """,
        "tags": ["kalsium", "Ca", "pupuk", "sekunder"],
        "difficulty": "intermediate",
        "read_time": 8
    },
    "magnesium": {
        "title": "Magnesium (Mg) - Jantung Klorofil",
        "content": """
        ### 🧪 Fungsi Magnesium dalam Tanaman
        
        **Peran Utama:**
        - **Inti klorofil** (atom pusat molekul klorofil)
        - Fotosintesis - tanpa Mg, tidak ada fotosintesis
        - Aktivator 300+ enzim
        - Metabolisme karbohidrat
        - Sintesis protein dan lemak
        - Transfer energi (ATP)
        
        ### 🔍 Gejala Defisiensi Magnesium
        
        **Karakteristik Khas:**
        - **Klorosis interveinal** (tulang daun hijau, daging daun kuning)
        - Dimulai dari **daun tua** (Mg mobile)
        - Daun bawah kuning → oranye → merah → nekrosis
        - Fotosintesis menurun drastis
        - Hasil panen turun 30-50%
        
        **Tanaman Rentan:**
        - Sawit, kakao, karet (perkebunan)
        - Tomat, cabai, terong
        - Kentang, ubi
        - Tanaman di tanah asam atau berpasir
        
        **Kondisi Pemicu:**
        - Tanah asam (pH <5.5)
        - Tanah berpasir (pencucian tinggi)
        - Kelebihan K (antagonis dengan Mg)
        - Curah hujan tinggi
        
        ### 🌾 Jenis Pupuk Magnesium
        
        **1. Kieserite (MgSO₄·H₂O)**
        - **Kandungan**: Mg 16%, S 22%
        - **Kelarutan**: Sedang
        - **Dosis**: 50-100 kg/ha
        - **Keunggulan**: Bonus sulfur
        - **Cocok untuk**: Sawit, kakao, karet
        - **Harga**: Rp 4,500/kg
        
        **2. Magnesium Sulfat/Epsom Salt (MgSO₄·7H₂O)**
        - **Kandungan**: Mg 9.8%, S 13%
        - **Kelarutan**: Sangat tinggi
        - **Dosis Tanah**: 20-50 kg/ha
        - **Dosis Semprot**: 2-5 g/L
        - **Keunggulan**: Cepat tersedia, bisa semprot daun
        - **Cocok untuk**: Sayuran, buah, koreksi cepat
        - **Harga**: Rp 8,000/kg
        
        **3. Dolomit (CaMg(CO₃)₂)**
        - **Kandungan**: Mg 10-13%, Ca 20-22%
        - **Fungsi**: Menaikkan pH + sumber Mg+Ca
        - **Dosis**: 1-2 ton/ha
        - **Cocok untuk**: Tanah asam
        - **Harga**: Rp 600/kg
        
        ### 📊 Kebutuhan Magnesium
        - **Sawit**: 40-60 kg Mg/ha/tahun
        - **Kakao**: 30-50 kg Mg/ha/tahun
        - **Tomat**: 20-30 kg Mg/ha
        - **Cabai**: 15-25 kg Mg/ha
        
        ### 💡 Strategi Aplikasi
        
        **Untuk Tanah Asam:**
        1. Dolomit 1-2 ton/ha (pengolahan tanah)
        2. Kieserite 50-100 kg/ha (maintenance)
        
        **Untuk Koreksi Cepat:**
        1. Epsom salt 20-30 kg/ha (kocor)
        2. Atau semprot daun 3-5 g/L, 7-10 hari sekali
        
        **Untuk Perkebunan:**
        1. Kieserite 100-200 kg/ha/tahun
        2. Aplikasi 2-3 kali per tahun
        3. Tabur di piringan pohon
        
        ### ⚠️ Perhatian
        - Jangan over-aplikasi K (antagonis Mg)
        - Rasio K:Mg ideal = 2:1 sampai 4:1
        - Monitor warna daun secara rutin
        """,
        "tags": ["magnesium", "Mg", "pupuk", "sekunder", "klorofil"],
        "difficulty": "intermediate",
        "read_time": 8
    },
    "sulfur": {
        "title": "Sulfur (S) - Unsur Pembentuk Protein",
        "content": """
        ### 🧪 Fungsi Sulfur dalam Tanaman
        
        **Peran Struktural:**
        - Komponen asam amino (sistein, metionin)
        - Pembentukan protein (15-20% protein mengandung S)
        - Komponen vitamin (B1, biotin)
        - Komponen koenzim A
        
        **Peran Fisiologis:**
        - Sintesis klorofil (bukan komponen, tapi esensial)
        - Fiksasi nitrogen (legum)
        - Pembentukan minyak (biji-bijian)
        - Aroma dan rasa (bawang, kubis)
        - Ketahanan terhadap penyakit
        
        ### 🔍 Gejala Defisiensi Sulfur
        
        **Mirip Defisiensi Nitrogen, tapi:**
        - Klorosis dimulai dari **daun muda** (S immobile)
        - Daun muda kuning pucat, hijau muda
        - Batang kurus dan kaku
        - Pertumbuhan terhambat
        - Pembungaan terlambat
        - Kadar protein rendah
        
        **Tanaman Rentan:**
        - Brassica (kubis, sawi, brokoli)
        - Bawang, bawang putih
        - Kedelai, kacang tanah
        - Jagung, padi
        - Tanaman di tanah berpasir
        
        **Kondisi Pemicu:**
        - Tanah berpasir (pencucian tinggi)
        - Tanah rendah bahan organik
        - Curah hujan tinggi
        - Penggunaan pupuk tanpa S (Urea vs ZA)
        
        ### 🌾 Jenis Pupuk Sulfur
        
        **1. Sulfur Elemental (S⁰)**
        - **Kandungan**: S 90-99%
        - **Bentuk**: Powder, bentonit
        - **Dosis**: 50-200 kg/ha
        - **Keunggulan**: Konsentrasi tinggi, slow-release
        - **Fungsi tambahan**: Menurunkan pH tanah
        - **Waktu efektif**: 3-6 bulan (perlu oksidasi)
        - **Harga**: Rp 5,000/kg
        
        **2. Sulfur Bentonit**
        - **Kandungan**: S 90% + bentonit
        - **Keunggulan**: Slow-release, tidak mudah tercuci
        - **Dosis**: 100-300 kg/ha
        - **Cocok untuk**: Perkebunan (sawit, karet, teh)
        - **Harga**: Rp 3,500/kg
        
        **3. ZA (Amonium Sulfat)**
        - **Kandungan**: N 21%, S 24%
        - **Keunggulan**: Cepat tersedia, bonus N
        - **Dosis**: 200-300 kg/ha
        - **Cocok untuk**: Padi, tebu, tembakau
        - **Harga**: Rp 1,800/kg
        
        **4. Gypsum (CaSO₄·2H₂O)**
        - **Kandungan**: S 18%, Ca 23%
        - **Keunggulan**: Bonus Ca, tidak ubah pH
        - **Dosis**: 200-500 kg/ha
        - **Cocok untuk**: Kacang tanah, legum
        - **Harga**: Rp 1,200/kg
        
        **5. Kieserite (MgSO₄·H₂O)**
        - **Kandungan**: S 22%, Mg 16%
        - **Keunggulan**: Bonus Mg
        - **Dosis**: 50-100 kg/ha
        - **Cocok untuk**: Sawit, kakao
        - **Harga**: Rp 4,500/kg
        
        **6. Amonium Tiosulfat (ATS)**
        - **Kandungan**: N 12%, S 26%
        - **Bentuk**: Cair
        - **Keunggulan**: Sangat larut, fertigasi
        - **Dosis**: 50-100 L/ha
        - **Cocok untuk**: Jagung, gandum, fertigasi
        - **Harga**: Rp 15,000/kg
        
        ### 📊 Kebutuhan Sulfur
        - **Padi**: 10-15 kg S/ha
        - **Jagung**: 15-25 kg S/ha
        - **Kedelai**: 20-30 kg S/ha
        - **Kubis**: 30-50 kg S/ha
        - **Bawang**: 40-60 kg S/ha
        - **Sawit**: 20-40 kg S/ha/tahun
        
        ### 💡 Strategi Aplikasi
        
        **Untuk Tanah Asam:**
        - Hindari sulfur elemental (makin asam)
        - Gunakan gypsum atau ZA
        
        **Untuk Tanah Alkalis:**
        - Sulfur elemental 100-300 kg/ha
        - Efek: Menurunkan pH + sumber S
        
        **Untuk Tanaman Brassica:**
        - S sangat penting untuk kualitas
        - ZA 200-300 kg/ha atau
        - Gypsum 300-500 kg/ha
        
        **Untuk Perkebunan:**
        - Sulfur bentonit 100-200 kg/ha/tahun
        - Aplikasi 1-2 kali per tahun
        
        ### ⚠️ Perhatian
        - Sulfur elemental butuh waktu 3-6 bulan efektif
        - Aplikasi berlebihan dapat menurunkan pH drastis
        - Rasio N:S ideal = 7:1 sampai 15:1
        """,
        "tags": ["sulfur", "S", "pupuk", "sekunder", "protein"],
        "difficulty": "intermediate",
        "read_time": 9
    }
}

# 4. MANAJEMEN AIR
MANAJEMEN_AIR = {
    "sistem_irigasi": {
        "title": "Sistem Irigasi Modern",
        "content": """
        ### 💧 Jenis-Jenis Sistem Irigasi
        
        **1. Irigasi Tetes (Drip Irrigation)**
        - **Prinsip**: Air menetes langsung ke zona akar
        - **Efisiensi**: 90-95%
        - **Kelebihan**: Hemat air, presisi, minim gulma
        - **Kekurangan**: Investasi tinggi, butuh filter
        - **Cocok untuk**: Sayuran, buah, greenhouse
        - **Biaya**: Rp 15-30 juta/ha
        
        **2. Irigasi Sprinkler**
        - **Prinsip**: Air disemprotkan seperti hujan
        - **Efisiensi**: 70-85%
        - **Kelebihan**: Cocok untuk lahan luas, merata
        - **Kekurangan**: Evaporasi tinggi, butuh tekanan
        - **Cocok untuk**: Rumput, palawija
        - **Biaya**: Rp 20-40 juta/ha
        
        **3. Irigasi Permukaan (Surface)**
        - **Prinsip**: Air mengalir di permukaan tanah
        - **Efisiensi**: 40-60%
        - **Kelebihan**: Murah, sederhana
        - **Kekurangan**: Boros air, tidak merata
        - **Cocok untuk**: Padi sawah
        
        **4. Irigasi Bawah Permukaan (Subsurface)**
        - **Prinsip**: Pipa tetes ditanam di bawah tanah
        - **Efisiensi**: 95%+
        - **Kelebihan**: Sangat efisien, tahan lama
        - **Kekurangan**: Mahal, instalasi kompleks
        - **Cocok untuk**: Perkebunan premium
        
        ### 📊 Kebutuhan Air Tanaman
        - **Padi**: 1200-1500 mm/musim
        - **Jagung**: 400-600 mm/musim
        - **Cabai**: 600-800 mm/musim
        - **Tomat**: 400-600 mm/musim
        
        ### ⏰ Jadwal Penyiraman
        - **Pagi**: 06:00-08:00 (terbaik)
        - **Sore**: 16:00-18:00
        - **Hindari**: Siang hari (evaporasi tinggi)
        """,
        "tags": ["irigasi", "air", "sistem"],
        "difficulty": "intermediate",
        "read_time": 7
    }
}

# 5. HAMA & PENYAKIT
HAMA_PENYAKIT = {
    "wereng_coklat": {
        "title": "Wereng Coklat Padi",
        "content": """
        ### 🐛 Identifikasi
        - **Nama Latin**: Nilaparvata lugens
        - **Tanaman Inang**: Padi
        - **Gejala**: 
          - Daun menguning dari bawah
          - Hopperburn (tanaman mengering seperti terbakar)
          - Koloni di pangkal batang
        
        ### 🔬 Siklus Hidup
        - Telur (5-7 hari) → Nimfa (14-21 hari) → Dewasa (20-30 hari)
        - 1 generasi: 25-35 hari
        - Betina bertelur 300-500 butir
        
        ### 🛡️ Pengendalian
        
        **Preventif:**
        - Varietas tahan (Inpari 32, Inpari 42)
        - Jarak tanam tidak terlalu rapat
        - Hindari pemupukan N berlebihan
        - Sanitasi: Bersihkan jerami
        
        **Mekanis:**
        - Perangkap lampu
        - Jaring serangga
        
        **Biologis:**
        - Predator: Laba-laba, kepik
        - Parasitoid: Anagrus nilaparvatae
        
        **Kimia (jika populasi tinggi):**
        - Imidakloprid 200 SL: 0.5 ml/L
        - Buprofezin 25 WP: 2 g/L
        - Aplikasi sore hari, semprot pangkal batang
        
        ### 🚨 Ambang Pengendalian
        - **Vegetatif**: 10 ekor/rumpun
        - **Generatif**: 5 ekor/rumpun
        """,
        "tags": ["hama", "wereng", "padi"],
        "difficulty": "intermediate",
        "read_time": 5
    }
}

# 6. MIKROBIOLOGI PERTANIAN & BIOTEKNOLOGI (HIPOCI CIANJUR)
MIKROBIOLOGI_PERTANIAN = {
    "mikroba_pangan": {
        "title": "Mikrobia Pangan & Fermentasi",
        "content": """
        ### 🧀 Produk Susu & Keju
        1. **Lactobacillus bulgaricus & Streptococcus thermophillus**: Pembuatan **Yogurt**. Mengubah laktosa menjadi asam laktat.
        2. **Lactobacillus lactis**: Pembuatan **Keju** (penggumpalan susu).
        3. **Lactobacillus citrovorum**: Memberi **aroma khas** pada mentega dan keju.
        4. **Lactobacillus casei / Streptococcus cremoris**: Pematangan Keju.
        5. **Leuconostoc mesenteroides**: Penghasil sukrosa (dextran) untuk tekstur.
        6. **Penicillium camemberti & P. roqueforti**: Jamur untuk meningkatkan kualitas/aroma keju (Blue Cheese).
        
        ### 🍞 Roti, Tape & Alkohol
        7. **Saccharomyces cerevisiae**: Pembuatan **Roti** (pengembang) dan **Tape**.
        8. **Saccharomyces fibulegera**: Fermentasi tape dan pakan ternak.
        9. **Saccharomyces ellipsoideus**: Fermentasi anggur menjadi **Wine**.
        
        ### 🥢 Produk Kedelai & Tradisional
        10. **Rhizopus oryzae**: Pembuatan **Tempe**.
        11. **Aspergillus oryzae & A. sojae**: Pembuatan **Kecap** & Tauco.
        12. **Aspergillus wentii**: Pembuatan Kecap.
        13. **Neurospora sithopila**: Pembuatan **Oncom** (warna merah/oranye).
        14. **Acetobacter xylinum**: Pembuatan **Nata de Coco** (selulosa bakteri).
        15. **Acetobacter aceti**: Pembuatan **Asam Cuka**.
        16. **Lactobacillus sp.**: Pembuatan **Terasi**.
        17. **Pediococcus cerevisiae**: Pembuatan **Sosis** (fermentasi daging).
        18. **Lactobacillus plantarum**: Asinan Kubis (Sauerkraut).
        19. **Pseudomonas sp. & Propionibacterium sp.**: Penghasil Vitamin B12.
        """,
        "tags": ["mikroba", "pangan", "fermentasi"],
        "difficulty": "beginner",
        "read_time": 5
    },
    "mikroba_pertanian_lingkungan": {
        "title": "Mikrobia Pupuk Hayati & Lingkungan",
        "content": """
        ### 🌱 Penyubur Tanah & Biofertilizer
        1. **Nitrosomonas & Nitrosococcus**: Mengubah Amonia (NH3) menjadi Nitrit (NO2).
        2. **Nitrobacter**: Mengubah Nitrit (NO2) menjadi Nitrat (NO3) yang siap diserap tanaman.
        3. **Rhizobium sp.**: Menambat Nitrogen bebas dari udara (simbiosis kacang-kacangan).
        4. **Pseudomonas sp.**: Melindungi tanaman dari kematian akibat suhu dingin (Ice-nucleation bacteria).
        
        ### 🛡️ Biopestisida (Pengendali Hama)
        5. **Bacillus thuringiensis (Bt)**: Menghasilkan kristal protein (indotoksin) yang meracuni pencernaan **ulat hama**.
        6. **Amanita muscaria**: Jamur penghasil toksin muskarin untuk membunuh lalat (berasal dari kotoran ternak).
        
        ### 🏭 Industri & Tambang
        7. **Thiobacillus ferrooxidans**: **Bioleaching**. Memisahkan tembaga (Cu) dan emas dari bijih logam kadar rendah.
        8. **Methanobacterium omelianskii & M. ruminatum**: Menguraikan limbah organik (asam cuka) menjadi **Biogas (Metana & CO2)**.
        9. **E. coli**: Indikator kualitas air dan makanan (pencemaran tinja).
        """,
        "tags": ["mikroba", "pupuk hayati", "lingkungan"],
        "difficulty": "intermediate",
        "read_time": 6
    },
    "mikroba_medis_industri": {
        "title": "Mikrobia Medis & Industri Antibiotik",
        "content": """
        ### 💊 Penghasil Antibiotik
        1. **Penicillium notatum & P. chrysogenum**: Penghasil **Penisilin** (antibiotik pertama).
        2. **Cephalosporium**: Penghasil Penisilin N.
        3. **Streptomyces griseus**: Penghasil **Streptomisin** (untuk TBC, efektif lawan bakteri kebal penisilin).
        4. **Bacillus brevis**: Penghasil Tirotrisin.
        5. **Bacillus subtilis**: Penghasil Basitrasin.
        6. **Bacillus polymyxa**: Penghasil Polimixin.
        
        ### 🧪 Industri Kimia
        7. **Corynebacterium glutamicum**: Memproduksi **Asam Glutamat** (bahan baku Vetsin/MSG).
        8. **Aspergillus niger**: Penghasil **Asam Sitrat** (pengawet/rasa asam) dan fermentasi pakan.
        9. **Spirulina & Chlorella**: Mikroalga sumber **Protein Sel Tunggal (PST)** / Superfood.
        """,
        "tags": ["mikroba", "antibiotik", "industri"],
        "difficulty": "advanced",
        "read_time": 7
    }
}

# 6. GREENHOUSE FLORIKULTURA (NEW)
GREENHOUSE_FLORIKULTURA = {
    "bunga_potong_jepang": {
        "title": "Bunga Potong Jepang (Japanese Cut Flowers)",
        "content": """
        ### 🌸 Pengantar
        Bunga potong Jepang (seperti Eustoma/Lisianthus, Krisan, dan Lili) dikenal karena kualitas premium, kelopak tebal, dan daya simpan vas (vase life) yang lama. 
        Budidaya di greenhouse memerlukan kontrol iklim mikro yang presisi.

        ### 🎨 Varietas Populer
        
        **1. Varietas Putih (White - Shiro)**
        - **Karakter**: Simbol kesucian, sering untuk pernikahan & upacara.
        - **Contoh**: *Eustoma 'Voyage White'*, *Chrysanthemum 'Sei White'*.
        - **Pasar**: Sangat stabil tinggi.
        
        **2. Varietas Pink (Pink - Pinku)**
        - **Karakter**: Simbol kelembutan & cinta.
        - **Contoh**: *Eustoma 'Celeb Pink'*, *Gerbera 'Prestige'*.
        - **Pasar**: Valentine, Hari Ibu, Hadiah.
        
        **3. Varietas Kuning (Yellow - Kiiro)**
        - **Karakter**: Simbol keceriaan, persahabatan, atau penghormatan (tergantung budaya).
        - **Contoh**: *Chrysanthemum 'Sei Yellow'*, *Oncidium*.
        - **Pasar**: Dekorasi musim panas, festival.

        ### 🌤️ Manajemen Musim (Summer vs Winter)
        
        **A. Musim Panas (Summer / Natsu)**
        - **Tantangan**: Suhu tinggi (>30°C) menyebabkan tangkai pendek, petal burn, dan hama Thrips.
        - **Strategi Greenhouse**:
            1. **Shading Net (Paranet)**: Gunakan kerapatan 50-70% aluminet (memantulkan panas).
            2. **Exhaust Fan + Pad**: Wajib menyala untuk menurunkan suhu 5-7°C.
            3. **Irrigation**: Pulse irrigation (sedikit tapi sering), pagi & siang. Meningkatkan kelembaban.
            4. **Hama**: Waspada Thrips & Tungau. Gunakan *predatory mites* (kontrol biologis).
            
        **B. Musim Dingin (Winter / Fuyu)**
        - **Tantangan**: Suhu rendah (<10°C) melambatkan pertumbuhan & *blinding* (kuncup gagal mekar).
        - **Strategi Greenhouse**:
            1. **Heater (Pemanas)**: Jaga suhu malam >12°C stabil.
            2. **Supplemental Lighting**: Tambah durasi cahaya (day extension) hingga 14-16 jam untuk mencegah *rosetting* (tidur).
            3. **CO2 Enrichment**: Injeksi CO2 saat ventilasi tertutup meningkatkan fotosintesis 20%.
            4. **Penyakit**: Waspada Botrytis (busuk abu-abu) karena kelembaban tinggi. Sirkulasi udara (HAF Fan) wajib 24 jam.

        ### 🏭 Teknologi Greenhouse Jepang
        - **Kontrol Iklim Otomatis**: Sensor suhu & RH terhubung ke jendela atap/samping.
        - **Irigasi Tetes Presisi**: Berbasis VPD (Vapor Pressure Deficit).
        - **Media Tanam**: Rockwool atau Cocopeat steril (bukan tanah langsung).
        """,
        "tags": ["bunga", "greenhouse", "florikultura", "jepang"],
        "difficulty": "advanced",
        "read_time": 10
    }
}

# ========== HELPER FUNCTIONS ==========

def search_knowledge(query):
    """Search across all knowledge base"""
    results = []
    query = query.lower()
    
    all_categories = {
        "Dasar Pertanian": DASAR_PERTANIAN,
        "Database Tanaman": DATABASE_TANAMAN,
        "Ilmu Tanah": ILMU_TANAH,
        "Pupuk Makro Sekunder": PUPUK_MAKRO_SEKUNDER,
        "Manajemen Air": MANAJEMEN_AIR,
        "Hama & Penyakit": HAMA_PENYAKIT,
        "Greenhouse Florikultura": GREENHOUSE_FLORIKULTURA
    }

    
    for cat_name, category in all_categories.items():
        for article_id, article in category.items():
            if (query in article['title'].lower() or 
                query in article['content'].lower() or
                any(query in tag for tag in article.get('tags', []))):
                results.append({
                    'category': cat_name,
                    'id': article_id,
                    'title': article['title'],
                    'difficulty': article.get('difficulty', 'N/A'),
                    'read_time': article.get('read_time', 'N/A')
                })
    
    return results

def display_article(article):
    """Display article with metadata"""
    st.markdown(f"# {article['title']}")
    
    # Metadata
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        difficulty_color = {
            'beginner': '🟢',
            'intermediate': '🟡',
            'advanced': '🔴'
        }
        st.caption(f"{difficulty_color.get(article.get('difficulty', ''), '⚪')} {article.get('difficulty', 'N/A').title()}")
    with col2:
        st.caption(f"⏱️ {article.get('read_time', 'N/A')} menit")
    with col3:
        if article.get('tags'):
            st.caption(f"🏷️ {', '.join(article['tags'][:3])}")
    with col4:
        article_id = st.session_state.get('current_article_id', '')
        if article_id in st.session_state.bookmarks:
            if st.button("⭐ Hapus Bookmark", key=f"unbookmark_{article_id}"):
                st.session_state.bookmarks.remove(article_id)
                st.rerun()
        else:
            if st.button("☆ Bookmark", key=f"bookmark_{article_id}"):
                st.session_state.bookmarks.append(article_id)
                st.rerun()
    
    st.markdown("---")
    
    # Content
    st.markdown(article['content'])
    
    # Mark as read
    if article_id and article_id not in st.session_state.read_articles:
        st.session_state.read_articles.append(article_id)

# ========== MAIN APP ==========

st.title("📖 AgriSensa Knowledge")
st.markdown("**Ensiklopedia Pertanian Digital - Panduan Lengkap dari Dasar hingga Mahir**")

# Search bar
st.markdown("---")
search_query = st.text_input("🔍 Cari topik, tanaman, atau kata kunci...", placeholder="Contoh: padi, pH tanah, irigasi tetes")

if search_query:
    results = search_knowledge(search_query)
    if results:
        st.success(f"Ditemukan {len(results)} artikel")
        for result in results:
            with st.expander(f"📄 {result['title']} ({result['category']})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"Kategori: {result['category']} | Tingkat: {result['difficulty']} | {result['read_time']} menit")
                with col2:
                    if st.button("Baca", key=f"read_{result['id']}"):
                        st.session_state.current_article_id = result['id']
                        st.session_state.current_category = result['category']
                        st.rerun()
    else:
        st.warning("Tidak ada hasil ditemukan. Coba kata kunci lain.")

st.markdown("---")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🌱 Dasar Pertanian",
    "🌾 Database Tanaman",
    "🧪 Ilmu Tanah",
    "💧 Manajemen Air",
    "🐛 Hama & Penyakit",
    "🧬 Pupuk Makro Sekunder",
    "🌸 Greenhouse",
    "🦠 Mikrobiologi",
    "⭐ Bookmark Saya"
])

# TAB 1: DASAR PERTANIAN
with tab1:
    st.header("🌱 Dasar-Dasar Pertanian")
    
    article_choice = st.selectbox(
        "Pilih Topik:",
        options=list(DASAR_PERTANIAN.keys()),
        format_func=lambda x: DASAR_PERTANIAN[x]['title']
    )
    
    if article_choice:
        st.session_state.current_article_id = f"dasar_{article_choice}"
        display_article(DASAR_PERTANIAN[article_choice])

# TAB 2: DATABASE TANAMAN
with tab2:
    st.header("🌾 Database Tanaman")
    st.markdown("Panduan lengkap budidaya berbagai komoditas pertanian")
    
    # Filter
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.multiselect(
            "Filter berdasarkan jenis:",
            ["pangan", "hortikultura", "sayuran", "perkebunan"],
            default=[]
        )
    
    # Display plants
    for plant_id, plant in DATABASE_TANAMAN.items():
        if not filter_type or any(t in plant.get('tags', []) for t in filter_type):
            with st.expander(f"🌿 {plant['title']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"**{plant.get('latin', '')}** | {plant.get('family', '')}")
                    st.caption(f"Tingkat: {plant.get('difficulty', 'N/A')} | ⏱️ {plant.get('read_time', 'N/A')} menit")
                with col2:
                    if st.button("Baca Lengkap", key=f"plant_{plant_id}"):
                        st.session_state.current_article_id = f"plant_{plant_id}"
                        display_article(plant)

# TAB 3: ILMU TANAH
with tab3:
    st.header("🧪 Ilmu Tanah")
    
    article_choice = st.selectbox(
        "Pilih Topik:",
        options=list(ILMU_TANAH.keys()),
        format_func=lambda x: ILMU_TANAH[x]['title'],
        key="tanah_select"
    )
    
    if article_choice:
        st.session_state.current_article_id = f"tanah_{article_choice}"
        display_article(ILMU_TANAH[article_choice])

# TAB 4: MANAJEMEN AIR
with tab4:
    st.header("💧 Manajemen Air")
    
    article_choice = st.selectbox(
        "Pilih Topik:",
        options=list(MANAJEMEN_AIR.keys()),
        format_func=lambda x: MANAJEMEN_AIR[x]['title'],
        key="air_select"
    )
    
    if article_choice:
        st.session_state.current_article_id = f"air_{article_choice}"
        display_article(MANAJEMEN_AIR[article_choice])

# TAB 5: HAMA & PENYAKIT
with tab5:
    st.header("🐛 Hama & Penyakit")
    
    article_choice = st.selectbox(
        "Pilih Hama/Penyakit:",
        options=list(HAMA_PENYAKIT.keys()),
        format_func=lambda x: HAMA_PENYAKIT[x]['title'],
        key="hama_select"
    )
    
    if article_choice:
        st.session_state.current_article_id = f"hama_{article_choice}"
        display_article(HAMA_PENYAKIT[article_choice])

# TAB 6: PUPUK MAKRO SEKUNDER
with tab6:
    st.header("🧬 Pupuk Makro Sekunder")
    st.markdown("**Panduan Lengkap Unsur Hara Makro Sekunder: Kalsium, Magnesium, dan Sulfur**")
    
    article_choice = st.selectbox(
        "Pilih Unsur Hara:",
        options=list(PUPUK_MAKRO_SEKUNDER.keys()),
        format_func=lambda x: PUPUK_MAKRO_SEKUNDER[x]['title'],
        key="pupuk_sekunder_select"
    )
    
    if article_choice:
        st.session_state.current_article_id = f"pupuk_sekunder_{article_choice}"
        display_article(PUPUK_MAKRO_SEKUNDER[article_choice])

# TAB 7: GREENHOUSE FLORIKULTURA
with tab7:
    st.header("🌸 Greenhouse Florikultura")
    st.markdown("**Teknologi Budidaya Bunga Potong Premium (Jepang)**")
    
    article_choice = st.selectbox(
        "Pilih Topik:",
        options=list(GREENHOUSE_FLORIKULTURA.keys()),
        format_func=lambda x: GREENHOUSE_FLORIKULTURA[x]['title'],
        key="greenhouse_select"
    )
    
    if article_choice:
        st.session_state.current_article_id = f"greenhouse_{article_choice}"
        display_article(GREENHOUSE_FLORIKULTURA[article_choice])

# TAB 8: MIKROBIOLOGI (NEW)
with tab8:
    st.header("🦠 Mikrobiologi Pertanian & Bioteknologi")
    st.info("Referensi: 'Aneka Mikrobia dan Peranannya' - Hipoci Cianjur (Om Mukhlis, 2014)")
    
    c1, c2 = st.columns(2)
    
    with c1:
        with st.expander("🌱 Pertanian & Lingkungan (Biofertilizer)"):
            st.markdown(MIKROBIOLOGI_PERTANIAN['mikroba_pertanian_lingkungan']['content'])
            
        with st.expander("💊 Medis & Industri (Antibiotik)"):
            st.markdown(MIKROBIOLOGI_PERTANIAN['mikroba_medis_industri']['content'])
            
    with c2:
        with st.expander("🧀 Pangan & Fermentasi (Food Tech)"):
            st.markdown(MIKROBIOLOGI_PERTANIAN['mikroba_pangan']['content'])
            
    st.warning("💡 **Insight:** Mikroba seperti *Rhizobium* dan *Bacillus thuringiensis* adalah kunci pertanian organik modern.")

# TAB 9: BOOKMARKS
with tab9:
    st.header("⭐ Artikel yang Saya Bookmark")
    
    if st.session_state.bookmarks:
        st.success(f"Anda memiliki {len(st.session_state.bookmarks)} bookmark")
        
        for bookmark_id in st.session_state.bookmarks:
            # Find article
            # (Simplified - in production, implement proper lookup)
            st.info(f"📌 {bookmark_id}")
    else:
        st.info("Belum ada bookmark. Klik tombol ☆ pada artikel untuk menambahkan bookmark.")

# Sidebar - Statistics
with st.sidebar:
    st.markdown("### 📊 Statistik Anda")
    st.metric("Artikel Dibaca", len(st.session_state.read_articles))
    st.metric("Bookmark", len(st.session_state.bookmarks))
    
    st.markdown("---")
    st.markdown("### 📚 Kategori")
    st.markdown("""
    - 🌱 Dasar Pertanian (3 artikel)
    - 🌾 Database Tanaman (3 artikel)
    - 🧪 Ilmu Tanah (2 artikel)
    - 💧 Manajemen Air (1 artikel)
    - 🐛 Hama & Penyakit (1 artikel)
    - 🧬 Pupuk Makro Sekunder (3 artikel)
    
    **Total: 13 artikel** (akan terus bertambah!)
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("Gunakan fitur search untuk menemukan topik dengan cepat!")

# Footer
st.markdown("---")
st.caption("""
📖 **AgriSensa Knowledge v1.0** - Ensiklopedia Pertanian Digital

💡 **Catatan**: Informasi ini bersifat edukatif dan umum. Sesuaikan dengan kondisi lokal Anda dan konsultasikan dengan penyuluh pertanian untuk kasus spesifik.

🌱 **Coming Soon**: Lebih banyak tanaman, video tutorial, kalkulator interaktif, dan fitur AI Q&A!
""")
