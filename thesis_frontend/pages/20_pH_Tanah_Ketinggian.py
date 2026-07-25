# Panduan pH Tanah & Ketinggian Optimal
# Database lengkap pH dan altimeter untuk berbagai jenis tanaman

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="AgriSensa Advanced pH & Altitude", page_icon="🌍", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# Custom CSS for Eco-Light Theme and Advanced UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f9f0 0%, #ffffff 100%);
        color: #263238;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(39, 174, 96, 0.15);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.12);
        background: rgba(255, 255, 255, 0.95);
    }
    .parameter-box {
        background: #f1f8f5;
        border-radius: 12px;
        padding: 20px;
        border-left: 6px solid #2ecc71;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    h1, h2, h3 {
        color: #1b5e20 !important;
        font-family: 'Inter', sans-serif;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.5);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }
    .scientific-tag {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        border: 1px solid #c8e6c9;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATABASE TANAMAN ==========

TANAMAN_DATABASE = {
    # PADI & PALAWIJA
    "Padi": {
        "kategori": "Pangan Utama",
        "ph_optimal": "5.5-7.0",
        "ph_range": "5.0-7.5",
        "ph_ideal": 6.0,
        "ketinggian_optimal": "0-1500 mdpl",
        "ketinggian_ideal": "0-600 mdpl",
        "suhu_optimal": "22-32°C",
        "curah_hujan": "1500-2000 mm/tahun",
        "jenis_tanah": "Aluvial, Latosol, Grumosol",
        "drainase": "Tergenang (sawah) atau baik (gogo)",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "A, B1, B2",
        "pola_tanam": "Padi - Padi - Palawija",
        "gejala_ph_rendah": ["Daun menguning (klorosis)", "Pertumbuhan kerdil", "Akar pendek dan berwarna coklat", "Keracunan Al dan Fe"],
        "gejala_ph_tinggi": ["Daun pucat kekuningan", "Defisiensi Fe, Mn, Zn", "Pertumbuhan terhambat"],
        "perbaikan_ph_rendah": ["Kapur pertanian (CaCO3) 1-2 ton/ha", "Dolomit 1-2 ton/ha", "Aplikasi 2-4 minggu sebelum tanam"],
        "perbaikan_ph_tinggi": ["Belerang (S) 200-500 kg/ha", "Pupuk organik 5-10 ton/ha", "Gypsum (CaSO4) 500-1000 kg/ha"],
        "tips": "Padi toleran pH luas, tapi optimal di pH 6.0. Sawah tergenang menaikkan pH tanah masam.",
        "referensi": "Balittanah (2023), Jurnal Ilmu Tanah dan Lingkungan (IPB)"
    },
    
    "Jagung": {
        "kategori": "Pangan Utama",
        "ph_optimal": "5.5-7.5",
        "ph_range": "5.0-8.0",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-1800 mdpl",
        "ketinggian_ideal": "50-600 mdpl",
        "suhu_optimal": "21-34°C",
        "curah_hujan": "85-200 mm/bulan",
        "jenis_tanah": "Latosol, Grumosol, Andosol",
        "drainase": "Baik, tidak tahan genangan",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "C1, C2, D1",
        "pola_tanam": "Padi - Jagung - Palawija/Bera",
        "gejala_ph_rendah": ["Daun bawah menguning", "Tongkol kecil dan tidak penuh", "Keracunan aluminium", "Akar pendek"],
        "gejala_ph_tinggi": ["Klorosis interveinal", "Defisiensi Zn dan Fe", "Biji tidak berkembang sempurna"],
        "perbaikan_ph_rendah": ["Kapur 1-3 ton/ha (pH <5.5)", "Dolomit untuk tambahan Mg", "Aplikasi saat olah tanah"],
        "perbaikan_ph_tinggi": ["Belerang 300-600 kg/ha", "Kompos 10 ton/ha", "Pupuk asam (ZA, urea)"],
        "tips": "Jagung sangat responsif terhadap pengapuran. pH 6.5 optimal untuk hasil maksimal.",
        "referensi": "Balitsereal Maros, Jurnal Akta Agrosia"
    },
    
    "Kedelai": {
        "kategori": "Pangan & Protein",
        "ph_optimal": "6.0-7.5",
        "ph_range": "5.5-8.0",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-1500 mdpl",
        "ketinggian_ideal": "100-400 mdpl",
        "suhu_optimal": "23-30°C",
        "curah_hujan": "100-200 mm/bulan",
        "jenis_tanah": "Latosol, Grumosol, Aluvial",
        "drainase": "Baik, tidak tahan genangan",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "C2, C3, D2",
        "pola_tanam": "Padi - Palawija - Kedelai",
        "gejala_ph_rendah": ["Bintil akar sedikit (fiksasi N terganggu)", "Daun kuning pucat", "Polong sedikit dan hampa", "Keracunan Al and Mn"],
        "gejala_ph_tinggi": ["Klorosis Fe (daun muda kuning)", "Pertumbuhan lambat", "Polong kecil"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1.5-2 ton/ha (untuk Mg)", "Inokulasi rhizobium untuk fiksasi N"],
        "perbaikan_ph_tinggi": ["Belerang 200-400 kg/ha", "Pupuk organik 5-8 ton/ha", "Fe-EDTA untuk atasi klorosis"],
        "tips": "pH 6.5 penting untuk fiksasi N optimal. Rhizobium tidak aktif di pH <5.5.",
        "referensi": "Balitkabi Malang, Jurnal Agronomi Indonesia"
    },
    
    # SAYURAN
    "Cabai": {
        "kategori": "Sayuran Buah",
        "ph_optimal": "6.0-7.0",
        "ph_range": "5.5-7.5",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-1400 mdpl",
        "ketinggian_ideal": "200-800 mdpl",
        "suhu_optimal": "24-28°C",
        "curah_hujan": "600-1250 mm/tahun",
        "jenis_tanah": "Latosol, Andosol, Grumosol",
        "drainase": "Sangat baik, tidak tahan genangan",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "B1, B2, C1",
        "pola_tanam": "Sesuai musim hujan (tanam awal MH)",
        "gejala_ph_rendah": ["Daun menguning", "Bunga rontok", "Buah kecil dan sedikit", "Rentan layu bakteri (pH <5.5)"],
        "gejala_ph_tinggi": ["Klorosis Fe dan Mn", "Buah pucat", "Pertumbuhan lambat"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1-1.5 ton/ha", "Aplikasi 3-4 minggu sebelum tanam"],
        "perbaikan_ph_tinggi": ["Belerang 200-400 kg/ha", "Kompos 10-15 ton/ha", "Mulsa organik"],
        "tips": "pH 6.5 optimal untuk cabai. pH <5.5 meningkatkan risiko layu bakteri!",
        "referensi": "Balitsa Lembang, Jurnal Hortikultura"
    },
    
    "Tomat": {
        "kategori": "Sayuran Buah",
        "ph_optimal": "6.0-7.0",
        "ph_range": "5.5-7.5",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-1500 mdpl",
        "ketinggian_ideal": "700-1200 mdpl",
        "suhu_optimal": "20-27°C",
        "curah_hujan": "750-1250 mm/tahun",
        "jenis_tanah": "Andosol, Latosol, Grumosol",
        "drainase": "Sangat baik",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "B1, B2, C1",
        "pola_tanam": "Dataran Tinggi - Sepanjang Tahun",
        "gejala_ph_rendah": ["Blossom end rot (ujung buah busuk)", "Daun keriting", "Buah pecah-pecah", "Rentan layu bakteri"],
        "gejala_ph_tinggi": ["Klorosis Fe (daun muda kuning)", "Buah kecil", "Warna buah pucat"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit untuk tambahan Ca dan Mg", "Aplikasi Ca(NO3)2 untuk cegah blossom end rot"],
        "perbaikan_ph_tinggi": ["Belerang 200-400 kg/ha", "Kompos 10-15 ton/ha", "Fe-EDTA semprot daun"],
        "tips": "pH 6.5 + Ca cukup = tidak ada blossom end rot. Tomat dataran tinggi lebih manis!",
        "referensi": "Balitsa, Jurnal Agroteknologi UGM"
    },
    
    "Kentang": {
        "kategori": "Sayuran Umbi",
        "ph_optimal": "5.0-6.5",
        "ph_range": "4.8-7.0",
        "ph_ideal": 5.5,
        "ketinggian_optimal": "1000-3000 mdpl",
        "ketinggian_ideal": "1000-1500 mdpl",
        "suhu_optimal": "15-20°C",
        "curah_hujan": "1500-2500 mm/tahun",
        "jenis_tanah": "Andosol, Latosol",
        "drainase": "Sangat baik, gembur",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Sangat Tinggi (>10%)",
        "oldeman_type": "B1, B2",
        "pola_tanam": "Rotasi dengan Sayuran Daun",
        "gejala_ph_rendah": ["Keracunan Al and Mn", "Umbi kecil", "Pertumbuhan lambat"],
        "gejala_ph_tinggi": ["Kudis kentang (scab) meningkat (pH >6.5)", "Klorosis Fe", "Umbi cacat"],
        "perbaikan_ph_rendah": ["Kapur 0.5-1 ton/ha (HATI-HATI!)", "Target pH 5.5, JANGAN >6.0", "Dolomit ringan"],
        "perbaikan_ph_tinggi": ["Belerang 300-500 kg/ha", "Pupuk asam (ZA)", "Kompos matang"],
        "tips": "PENTING! Kentang suka pH asam (5.5). pH >6.5 = kudis kentang meningkat!",
        "referensi": "Balitbangtan, CIP (International Potato Center)"
    },
    
    "Bawang Merah": {
        "kategori": "Sayuran Umbi",
        "ph_optimal": "6.0-7.0",
        "ph_range": "5.5-7.5",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-900 mdpl",
        "ketinggian_ideal": "0-400 mdpl",
        "suhu_optimal": "25-32°C",
        "curah_hujan": "300-500 mm/musim",
        "jenis_tanah": "Aluvial, Latosol, Grumosol",
        "drainase": "Sangat baik, bedengan tinggi",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "D1, D2, E",
        "pola_tanam": "Musim Kemarau (MK) dengan Irigasi",
        "gejala_ph_rendah": ["Umbi kecil", "Daun kuning", "Rentan penyakit akar"],
        "gejala_ph_tinggi": ["Defisiensi mikronutrien", "Umbi tidak mengeras", "Daya simpan rendah"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1-1.5 ton/ha", "Aplikasi 2-3 minggu sebelum tanam"],
        "perbaikan_ph_tinggi": ["Belerang 200-300 kg/ha", "Kompos 10 ton/ha", "Pupuk organik matang"],
        "tips": "pH 6.5 + drainase sempurna = umbi besar dan tahan simpan. Hindari genangan!",
        "referensi": "Balitsa, Jurnal Hortikultura"
    },

    "Melon": {
        "kategori": "Buah Semusim",
        "ph_optimal": "6.0-7.0",
        "ph_range": "5.5-7.5",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-800 mdpl",
        "ketinggian_ideal": "200-500 mdpl",
        "suhu_optimal": "24-30°C",
        "curah_hujan": "200-300 mm/musim",
        "jenis_tanah": "Andosol, Latosol, Liat Berpasir",
        "drainase": "Sangat baik",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "D1, D2",
        "pola_tanam": "Musim Kemarau (lebih manis)",
        "gejala_ph_rendah": ["Pertumbuhan kerdil", "Buah pecah", "Kadar gula (Brix) rendah"],
        "gejala_ph_tinggi": ["Klorosis Mn", "Defisiensi Boron", "Jaring melon tidak sempurna"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit untuk Ca/Mg", "Aplikasi saat pengolahan bedengan"],
        "perbaikan_ph_tinggi": ["Asam humat", "ZA", "Kompos matang"],
        "tips": "Melon butuh sinar matahari penuh dan pH stabil 6.5 untuk kemanisan maksimal.",
        "referensi": "Kementerian Pertanian, Jurnal Agroteknologi UPN"
    },
    
    # BUAH-BUAHAN
    "Jeruk": {
        "kategori": "Buah Tahunan",
        "ph_optimal": "5.5-6.5",
        "ph_range": "5.0-7.0",
        "ph_ideal": 6.0,
        "ketinggian_optimal": "0-1200 mdpl",
        "ketinggian_ideal": "200-800 mdpl",
        "suhu_optimal": "25-30°C",
        "curah_hujan": "1500-2500 mm/tahun",
        "jenis_tanah": "Latosol, Andosol, Podsolik",
        "drainase": "Baik, tidak tahan genangan",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "B2, C2",
        "pola_tanam": "Tanaman Tahunan",
        "gejala_ph_rendah": ["Daun kuning (klorosis)", "Buah kecil dan asam", "Akar pendek", "Rentan penyakit akar"],
        "gejala_ph_tinggi": ["Klorosis Fe (daun muda kuning)", "Defisiensi Zn dan Mn", "Buah pucat"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1.5-2 ton/ha", "Aplikasi bertahap, 2x/tahun"],
        "perbaikan_ph_tinggi": ["Belerang 300-500 kg/ha", "Kompos 15-20 ton/ha", "Fe-EDTA and Zn-EDTA semprot"],
        "tips": "pH 6.0 optimal untuk jeruk manis. Jeruk nipis toleran pH lebih rendah (5.5).",
        "referensi": "Balitjestro Batu, Jurnal Hortikultura"
    },
    
    "Pisang": {
        "kategori": "Buah Tahunan",
        "ph_optimal": "5.5-7.0",
        "ph_range": "5.0-7.5",
        "ph_ideal": 6.5,
        "ketinggian_optimal": "0-1300 mdpl",
        "ketinggian_ideal": "0-700 mdpl",
        "suhu_optimal": "27-30°C",
        "curah_hujan": "2000-2500 mm/tahun",
        "jenis_tanah": "Latosol, Aluvial, Andosol",
        "drainase": "Baik, tahan genangan ringan",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "A, B1, C1",
        "pola_tanam": "Tumpang Sari Awal - Monokultur Lanjut",
        "gejala_ph_rendah": ["Daun kuning kemerahan", "Buah kecil", "Tandan sedikit", "Keracunan Al"],
        "gejala_ph_tinggi": ["Klorosis Fe", "Pertumbuhan lambat", "Buah pucat"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1.5-2 ton/ha", "Aplikasi melingkar di sekitar pohon"],
        "perbaikan_ph_tinggi": ["Belerang 200-400 kg/ha", "Kompos 20-30 ton/ha", "Mulsa organik tebal"],
        "tips": "Pisang toleran pH luas. pH 6.5 + K tinggi = buah besar dan manis!",
        "referensi": "Balitbu Solok, Jurnal Agronomi"
    },

    "Durian": {
        "kategori": "Buah Tahunan",
        "ph_optimal": "6.0-6.5",
        "ph_range": "5.5-7.5",
        "ph_ideal": 6.2,
        "ketinggian_optimal": "0-1000 mdpl",
        "ketinggian_ideal": "0-600 mdpl",
        "suhu_optimal": "24-30°C",
        "curah_hujan": "1500-2500 mm/tahun",
        "jenis_tanah": "Latosol, Andosol, Podsolik Merah Kuning",
        "drainase": "Sangat baik, tidak tahan genangan",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "B1, B2, C1",
        "pola_tanam": "Tanaman Sela saat Muda",
        "gejala_ph_rendah": ["Pertumbuhan lambat", "Klorosis tepi daun", "Rentan kanker batang (Phytophthora)"],
        "gejala_ph_tinggi": ["Defisiensi Boron (buah busuk ujung)", "Klorosis besi", "Erosi bunga"],
        "perbaikan_ph_rendah": ["Dolomit 2-4 kg/pohon", "Kapur pertanian", "Pupuk Organik Cair"],
        "perbaikan_ph_tinggi": ["Asam amino", "ZA", "Belerang jika tanah alkali"],
        "tips": "Durian butuh sinkronisasi pH dan Ca/Mg untuk tekstur buah yang creamy.",
        "referensi": "Balitbu Solok, Jurnal Hortikultura Indonesia"
    },
    
    # PERKEBUNAN
    "Kopi": {
        "kategori": "Perkebunan",
        "ph_optimal": "5.5-6.5",
        "ph_range": "5.0-7.0",
        "ph_ideal": 6.0,
        "ketinggian_optimal": "700-1700 mdpl",
        "ketinggian_ideal": "1000-1500 mdpl (Arabica), 400-800 mdpl (Robusta)",
        "suhu_optimal": "18-25°C (Arabica)",
        "curah_hujan": "1500-3000 mm/tahun",
        "jenis_tanah": "Andosol, Latosol",
        "drainase": "Sangat baik",
        "ktk_requirement": "Sedang (15-25 cmol/kg)",
        "bo_requirement": "Tinggi (>5%)",
        "oldeman_type": "B1, B2, C1",
        "pola_tanam": "Sistem Agroforestri",
        "gejala_ph_rendah": ["Daun kuning", "Buah kecil dan sedikit", "Akar pendek", "Keracunan Al"],
        "gejala_ph_tinggi": ["Klorosis Fe (daun muda kuning)", "Defisiensi Zn", "Kualitas biji menurun"],
        "perbaikan_ph_rendah": ["Kapur 1-2 ton/ha", "Dolomit 1.5-2 ton/ha", "Aplikasi 2x/tahun"],
        "perbaikan_ph_tinggi": ["Belerang 300-500 kg/ha", "Kompos 15-20 ton/ha", "Mulsa organik"],
        "tips": "Kopi Arabica dataran tinggi (>1000 mdpl) = kualitas premium. pH 6.0 optimal!",
        "referensi": "Puslitkoka Jember, World Coffee Research"
    },
    
    "Teh": {
        "kategori": "Perkebunan",
        "ph_optimal": "4.5-5.5",
        "ph_range": "4.0-6.0",
        "ph_ideal": 5.0,
        "ketinggian_optimal": "800-2000 mdpl",
        "ketinggian_ideal": "1200-1600 mdpl",
        "suhu_optimal": "13-25°C",
        "curah_hujan": "2000-3000 mm/tahun",
        "jenis_tanah": "Andosol, Latosol",
        "drainase": "Sangat baik",
        "ktk_requirement": "Tinggi (>25 cmol/kg)",
        "bo_requirement": "Sangat Tinggi (>10%)",
        "oldeman_type": "A, B1",
        "pola_tanam": "Monokultur pada Lereng",
        "gejala_ph_rendah": ["Keracunan Al and Mn (jarang, teh suka asam)", "Akar coklat"],
        "gejala_ph_tinggi": ["Klorosis Fe berat", "Daun kuning", "Kualitas daun menurun", "Pertumbuhan terhambat"],
        "perbaikan_ph_rendah": ["JARANG PERLU!", "Jika pH <4.0: kapur ringan 0.5 ton/ha"],
        "perbaikan_ph_tinggi": ["Belerang 500-1000 kg/ha", "Pupuk asam (ZA, urea)", "Kompos asam (pinus, oak)"],
        "tips": "TEH SUKA ASAM! pH 5.0 optimal. Dataran tinggi + pH asam = teh berkualitas!",
        "referensi": "Puslit Teh dan Kina Gambung, Jurnal Teh Kina"
    },

    "Kelapa Sawit": {
        "kategori": "Perkebunan",
        "ph_optimal": "4.0-6.0",
        "ph_range": "3.5-7.0",
        "ph_ideal": 5.0,
        "ketinggian_optimal": "0-500 mdpl",
        "ketinggian_ideal": "0-200 mdpl",
        "suhu_optimal": "25-32°C",
        "curah_hujan": "2000-3000 mm/tahun",
        "jenis_tanah": "Podsolik Merah Kuning, Aluvial, Gambut",
        "drainase": "Baik, butuh water management (gambut)",
        "ktk_requirement": "Rendah-Sedang (<20 cmol/kg)",
        "bo_requirement": "Sedang (2-5%)",
        "oldeman_type": "A, B1",
        "pola_tanam": "Monokultur Skala Luas",
        "gejala_ph_rendah": ["Bercak oranye (Curvularia)", "Defisiensi Magnesium", "Produksi TBS menurun"],
        "gejala_ph_tinggi": ["Defisiensi Boron (hook leaf)", "Defisiensi Cu dan Zn", "Klorosis pelepah muda"],
        "perbaikan_ph_rendah": ["Dolomit 2-5 kg/pohon/tahun", "Rock Phosphate", "Abu janjang kosong"],
        "perbaikan_ph_tinggi": ["Pupuk bersifat asam (ZA)", "Aplikasi mikronutrien Cu/Zn/B"],
        "tips": "Sawit sangat toleran pH rendah, terutama di lahan gambut dengan manajemen air baik.",
        "referensi": "PPKS Medan, Jurnal Kelapa Sawit"
    }
}

# ========== HELPER FUNCTIONS ==========

def safe_parse_altitude(alt_str):
    """Safely parse altitude strings with multiple ranges or text"""
    import re
    try:
        # Find all X-Y patterns
        matches = re.findall(r'(\d+)\s*-\s*(\d+)', alt_str)
        if matches:
            # Flatten all numbers and find overall min/max
            nums = [float(val) for match in matches for val in match]
            return min(nums), max(nums)
        
        # Fallback to single numbers
        nums = re.findall(r'(\d+)', alt_str)
        if nums:
            vals = [float(n) for n in nums]
            return min(vals), max(vals)
    except:
        pass
    return 0.0, 3000.0

def get_ph_color(ph_value):
    """Get color based on pH value"""
    if ph_value < 4.5:
        return "#FF0000"  # Sangat asam - merah
    elif ph_value < 5.5:
        return "#FF6B00"  # Asam - oranye
    elif ph_value < 6.5:
        return "#FFD700"  # Agak asam - kuning
    elif ph_value < 7.5:
        return "#00FF00"  # Netral - hijau
    elif ph_value < 8.5:
        return "#00BFFF"  # Agak basa - biru muda
    else:
        return "#0000FF"  # Basa - biru

def calculate_lime_requirement(ph_current, ph_target, texture="Lempung"):
    """Calculate lime requirement (ton/ha)"""
    ph_diff = ph_target - ph_current
    
    # Base requirement by texture
    base_rates = {
        "Pasir": 0.5,
        "Lempung berpasir": 0.75,
        "Lempung": 1.0,
        "Lempung berliat": 1.25,
        "Liat": 1.5
    }
    
    base_rate = base_rates.get(texture, 1.0)
    lime_needed = ph_diff * base_rate
    
    return max(0, lime_needed)

# ========== MAIN APP ==========

st.title("🌍 Panduan pH Tanah & Ketinggian Optimal")
st.markdown("**Database lengkap pH dan altimeter untuk berbagai jenis tanaman**")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Cari & Rekomendasi",
    "📊 Database Lengkap",
    "🧮 Kalkulator pH",
    "📖 Panduan pH Tanah",
    "🏔️ Panduan Ketinggian",
    "📄 Jurnal & Referensi"
])

# TAB 1: SEARCH & RECOMMENDATION
with tab1:
    st.header("🔍 Cari & Rekomendasi Pintar")
    
    # Climate Education Expander
    with st.expander("🎓 Edukasi: Memahami Iklim & Kesesuaian Lahan", expanded=False):
        st.markdown("""
        ### 🇮🇩 1. Klasifikasi Iklim Oldeman (Spesifik Indonesia)
        Klasifikasi ini didasarkan pada jumlah **Bulan Basah (BB)** dan **Bulan Kering (BK)** berturut-turut.
        - **Bulan Basah (BB)**: Curah hujan > 200 mm/bulan (Cukup untuk padi sawah).
        - **Bulan Lembab (BL)**: Curah hujan 100 - 200 mm/bulan.
        - **Bulan Kering (BK)**: Curah hujan < 100 mm/bulan (Hanya cocok untuk palawija).

        | Tipe | Penjelasan Strategis | Pola Tanam Rekomendasi |
        | :--- | :--- | :--- |
        | **A** | Sangat basah, air tersedia sepanjang tahun. | Padi - Padi - Padi |
        | **B** | Basah, air cukup untuk padi hampir setahun. | Padi - Padi - Palawija |
        | **C** | Cukup basah, air terbatas di musim kemarau. | Padi - Palawija - Palawija |
        | **D** | Sedang, air sangat terbatas. | Padi Gogo - Palawija |
        | **E** | Kering, hanya mengandalkan tadah hujan pendek. | Palawija - Pemberaan |

        ---
        ### 🌍 2. Zona Iklim Global (Latitudinal)
        Pembagian iklim berdasarkan posisi geografis dan suhu rata-rata tahunan.
        
        1. **Tropis (0° - 23.5° LU/LS)**:
           - Matahari tegak lurus, suhu stabil (20-30°C).
           - Tanaman: Sawit, Karet, Pisang, Padi, Kakao.
        
        2. **Subtropis (23.5° - 40° LU/LS)**:
           - Memiliki 4 musim, perbedaan suhu musim nyata.
           - Tanaman: Gandum, Jeruk, Teh, Kapas, Kedelai.
        
        3. **Sedang (40° - 66.5° LU/LS)**:
           - Curah hujan sepanjang tahun, musim dingin bersalju.
           - Tanaman: Apel, Persik, Gandum Musim Dingin.
        
        4. **Kutub (> 66.5° LU/LS)**:
           - Suhu sangat rendah, tidak cocok untuk agrikultur skala besar.
        """)

    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.markdown("### 🛠️ Input Kondisi Lahan")
        user_ph = st.slider("pH Tanah Saat Ini", 3.0, 9.0, 6.0, 0.1)
        user_alt = st.number_input("Ketinggian Lahan (mdpl)", 0, 3000, 500)
        user_oldeman = st.selectbox("Tipe Iklim Oldeman", ["A", "B1", "B2", "C1", "C2", "C3", "D1", "D2", "E"])
        user_bo = st.selectbox("Bahan Organik", ["Rendah (<2%)", "Sedang (2-5%)", "Tinggi (>5%)"])
        
        show_matching = st.button("🚀 Analisis Kesesuaian Lahan", use_container_width=True, type="primary")
    
    with col_result:
        if not show_matching:
            st.info("Pilih tanaman di bawah atau klik tombol di samping untuk mencari rekomendasi tanaman yang paling cocok untuk lahan Anda.")
            selected_plant = st.selectbox(
                "Atau Pilih Tanaman Spesifik:",
                sorted(list(TANAMAN_DATABASE.keys()))
            )
        else:
            st.markdown("### 🏆 Rekomendasi Tanaman Terbaik")
            
            # Suitability Algorithm
            recommendations = []
            for name, d in TANAMAN_DATABASE.items():
                score = 0
                
                # pH Score (40%)
                ph_range = d['ph_range'].split('-')
                p_min, p_max = float(ph_range[0]), float(ph_range[1])
                if d['ph_ideal'] - 0.5 <= user_ph <= d['ph_ideal'] + 0.5:
                    score += 40
                elif p_min <= user_ph <= p_max:
                    score += 20
                
                # Altitude Score (30%) - USE ROBUST PARSER
                a_min, a_max = safe_parse_altitude(d['ketinggian_optimal'])
                ai_min, ai_max = safe_parse_altitude(d['ketinggian_ideal'])
                
                if ai_min <= user_alt <= ai_max:
                    score += 30
                elif a_min <= user_alt <= a_max:
                    score += 15
                
                # Climate Score (20%) - Precise Match
                allowed_climates = [x.strip() for x in d.get('oldeman_type', '').split(',')]
                if user_oldeman in allowed_climates:
                    score += 20
                
                # BO Score (10%) - Precise Match
                user_bo_clean = user_bo.split(' ')[0]
                if user_bo_clean in d.get('bo_requirement', ''):
                    score += 10
                
                recommendations.append({"name": name, "score": score})
            
            # Sort by score
            recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
            
            # Display Top 3 in glass cards
            for i, rec in enumerate(recommendations[:3]):
                match_color = "#2ecc71" if rec['score'] > 70 else "#f1c40f" if rec['score'] > 40 else "#e74c3c"
                text_color = "#1b5e20" if rec['score'] > 70 else "#7d6608" if rec['score'] > 40 else "#7b241c"
                
                st.markdown(f"""
                <div class="glass-card" style="border-left: 8px solid {match_color}; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin:0; color: {text_color}; font-size: 1.2em;">{i+1}. {rec['name']}</h4>
                        <span style="background: {match_color}; color: white; padding: 4px 15px; border-radius: 30px; font-size: 0.85em; font-weight: bold;">{rec['score']}% MATCH</span>
                    </div>
                    <p style="margin-top: 10px; font-size: 0.95em; color: #34495e; line-height: 1.4;">{TANAMAN_DATABASE[rec['name']]['tips']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            selected_plant = st.selectbox("Lihat Detail Tanaman:", [r['name'] for r in recommendations])
    
    if selected_plant:
        data = TANAMAN_DATABASE[selected_plant]
        
        # UI Header with Refined Glassmorphism
        st.markdown(f"""
        <div class="glass-card" style="background: white; border-bottom: 4px solid #2ecc71;">
            <h2 style='color: #1b5e20; margin: 0;'>{selected_plant}</h2>
            <p style='color: #7f8c8d; font-size: 1.1em; margin-top: 5px;'>Kategori: <span class="scientific-tag">{data['kategori']}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("pH Ideal", data['ph_ideal'])
            st.caption(f"Range: {data['ph_optimal']}")
        
        with col2:
            st.metric("Ketinggian Ideal", data['ketinggian_ideal'])
            st.caption(f"Range: {data['ketinggian_optimal']}")
        
        with col3:
            st.metric("Suhu Optimal", data['suhu_optimal'])
        
        st.markdown("---")
        
        # Advanced Parameters Section
        st.markdown("### 🔬 Parameter Ilmiah Lanjutan")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class='parameter-box' style='background: #f1f8e9; border-left: 6px solid #2ecc71;'>
                <small style='color: #2e7d32; font-weight: bold;'>KTK (CEC)</small><br>
                <b style='color: #1b5e20; font-size: 1.1em;'>{data.get('ktk_requirement', 'N/A')}</b>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class='parameter-box' style='background: #e3f2fd; border-left: 6px solid #2ecc71; border-left-color: #3498db;'>
                <small style='color: #1565c0; font-weight: bold;'>Bahan Organik (BO)</small><br>
                <b style='color: #0d47a1; font-size: 1.1em;'>{data.get('bo_requirement', 'N/A')}</b>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class='parameter-box' style='background: #fff3e0; border-left: 6px solid #2ecc71; border-left-color: #e67e22;'>
                <small style='color: #ef6c00; font-weight: bold;'>Iklim Oldeman</small><br>
                <b style='color: #e65100; font-size: 1.1em;'>Tipe {data.get('oldeman_type', 'N/A')}</b>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"**Pola Tanam Rekomendasi:** <span class='scientific-tag'>{data.get('pola_tanam', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown("---")
        
        # pH Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧪 Informasi pH")
            st.markdown(f"**pH Optimal:** {data['ph_optimal']}")
            st.markdown(f"**pH Ideal:** {data['ph_ideal']}")
            st.markdown(f"**Range Toleransi:** {data['ph_range']}")
            
            st.markdown("**Gejala pH Terlalu Rendah:**")
            for gejala in data['gejala_ph_rendah']:
                st.markdown(f"- {gejala}")
            
            st.markdown("**Gejala pH Terlalu Tinggi:**")
            for gejala in data['gejala_ph_tinggi']:
                st.markdown(f"- {gejala}")
        
        with col2:
            st.markdown("### 🌱 Perbaikan pH")
            
            st.success("**Jika pH Terlalu Rendah (Asam):**")
            for tindakan in data['perbaikan_ph_rendah']:
                st.markdown(f"• {tindakan}")
            
            st.warning("**Jika pH Terlalu Tinggi (Basa):**")
            for tindakan in data['perbaikan_ph_tinggi']:
                st.markdown(f"• {tindakan}")
        
        st.markdown("---")
        
        # Additional Info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏔️ Informasi Lingkungan")
            st.markdown(f"**Ketinggian Optimal:** {data['ketinggian_optimal']}")
            st.markdown(f"**Ketinggian Ideal:** {data['ketinggian_ideal']}")
            st.markdown(f"**Curah Hujan:** {data['curah_hujan']}")
        
        with col2:
            st.markdown("### 🌾 Informasi Tanah")
            st.markdown(f"**Jenis Tanah Cocok:** {data['jenis_tanah']}")
            st.markdown(f"**Drainase:** {data['drainase']}")
        
        st.info(f"💡 **Tips:** {data['tips']}")
        st.markdown(f"📚 **Referensi:** *{data.get('referensi', 'N/A')}*")

# TAB 2: FULL DATABASE
with tab2:
    st.header("📊 Database Lengkap Tanaman")
    
    # Create DataFrame
    df_data = []
    for nama, data in TANAMAN_DATABASE.items():
        df_data.append({
            "Tanaman": nama,
            "Kategori": data['kategori'],
            "pH Ideal": data['ph_ideal'],
            "pH Range": data['ph_optimal'],
            "Ketinggian Ideal": data['ketinggian_ideal'],
            "CEC": data.get('ktk_requirement', 'N/A'),
            "Organic Matter": data.get('bo_requirement', 'N/A'),
            "Oldeman": data.get('oldeman_type', 'N/A'),
            "Suhu": data['suhu_optimal']
        })
    
    df = pd.DataFrame(df_data)
    
    # Filter by category
    categories = ["Semua"] + sorted(df['Kategori'].unique().tolist())
    selected_category = st.selectbox("Filter Kategori:", categories)
    
    if selected_category != "Semua":
        df_filtered = df[df['Kategori'] == selected_category]
    else:
        df_filtered = df
    
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    
    # Advanced 3D Visualization
    st.markdown("---")
    st.subheader("🌋 Visualisasi 3D Kesesuaian Lingkungan")
    st.caption("Memetakan pH vs Ketinggian vs Potensi Keberhasilan")
    
    # Generate mesh for 3D visualization
    fig_3d = go.Figure()
    
    for idx, row in df_filtered.iterrows():
        # Get pH ranges
        ph_range = row['pH Range'].split('-')
        ph_min, ph_max = float(ph_range[0]), float(ph_range[1])
        
        # Get Altitude ranges - USE ROBUST PARSER
        alt_data = TANAMAN_DATABASE[row['Tanaman']]
        alt_min, alt_max = safe_parse_altitude(alt_data['ketinggian_optimal'])
        
        # Add a 3D bubble for each plant
        fig_3d.add_trace(go.Scatter3d(
            x=[row['pH Ideal']],
            y=[(alt_min + alt_max)/2],
            z=[10], # Simulated success score
            mode='markers+text',
            name=row['Tanaman'],
            marker=dict(
                size=12,
                color=get_ph_color(row['pH Ideal']),
                opacity=0.8
            ),
            text=[row['Tanaman']],
            textposition="top center",
            hovertemplate=f"<b>{row['Tanaman']}</b><br>pH: {row['pH Ideal']}<br>Alt: {(alt_min+alt_max)/2} mdpl<extra></extra>"
        ))

    fig_3d.update_layout(
        scene=dict(
            xaxis_title='pH Tanah',
            yaxis_title='Ketinggian (mdpl)',
            zaxis_title='Potensi Hasil',
            xaxis=dict(range=[3, 9], gridcolor='#ecf0f1'),
            yaxis=dict(range=[0, 2000], gridcolor='#ecf0f1'),
            zaxis=dict(range=[0, 15], gridcolor='#ecf0f1'),
            bgcolor='rgba(255,255,255,0.8)'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)

    # Original Bar Chart
    st.markdown("---")
    st.subheader("📊 Range pH Optimal")
    
    fig = go.Figure()
    
    for idx, row in df_filtered.iterrows():
        ph_range = row['pH Range'].split('-')
        ph_min = float(ph_range[0])
        ph_max = float(ph_range[1])
        
        fig.add_trace(go.Bar(
            name=row['Tanaman'],
            x=[row['Tanaman']],
            y=[ph_max - ph_min],
            base=[ph_min],
            marker_color=get_ph_color(row['pH Ideal']),
            text=f"pH {row['pH Ideal']}",
            textposition='inside',
            hovertemplate=f"<b>{row['Tanaman']}</b><br>pH: {row['pH Range']}<br>Ideal: {row['pH Ideal']}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Range pH Optimal per Tanaman",
        xaxis_title="Tanaman",
        yaxis_title="pH",
        yaxis=dict(range=[3.5, 8.5]),
        showlegend=False,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: pH CALCULATOR
with tab3:
    st.header("🧮 Kalkulator Kebutuhan Kapur")
    
    st.markdown("""
    Kalkulator ini membantu menghitung kebutuhan kapur untuk memperbaiki pH tanah.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        ph_current = st.number_input(
            "pH Tanah Saat Ini",
            min_value=3.0,
            max_value=9.0,
            value=5.0,
            step=0.1,
            help="Hasil uji pH tanah"
        )
        
        ph_target = st.number_input(
            "pH Target",
            min_value=4.0,
            max_value=8.0,
            value=6.5,
            step=0.1,
            help="pH yang diinginkan"
        )
    
    with col2:
        texture = st.selectbox(
            "Tekstur Tanah",
            ["Pasir", "Lempung berpasir", "Lempung", "Lempung berliat", "Liat"],
            index=2
        )
        
        luas_lahan = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=1000.0,
            value=1.0,
            step=0.1
        )
    
    if st.button("💧 Hitung Kebutuhan Kapur", type="primary"):
        if ph_current >= ph_target:
            st.warning("⚠️ pH saat ini sudah lebih tinggi atau sama dengan pH target. Tidak perlu pengapuran!")
        else:
            lime_per_ha = calculate_lime_requirement(ph_current, ph_target, texture)
            total_lime = lime_per_ha * luas_lahan
            
            st.success("### 📊 Hasil Perhitungan")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Kebutuhan per Hektar", f"{lime_per_ha:.2f} ton")
            
            with col2:
                st.metric("Total Kebutuhan", f"{total_lime:.2f} ton")
            
            with col3:
                st.metric("Kenaikan pH", f"+{ph_target - ph_current:.1f}")
            
            st.info(f"""
            **Rekomendasi Aplikasi:**
            
            1. **Jenis Kapur:**
               - Kapur pertanian (CaCO3) - umum
               - Dolomit (CaMg(CO3)2) - jika tanah kekurangan Mg
               - Kapur tohor (CaO) - lebih reaktif, dosis 60% dari perhitungan
            
            2. **Cara Aplikasi:**
               - Sebar merata di permukaan tanah
               - Aduk dengan tanah (kedalaman 15-20 cm)
               - Aplikasi 2-4 minggu sebelum tanam
               - Jika dosis >2 ton/ha, bagi 2x aplikasi
            
            3. **Waktu Aplikasi:**
               - Saat olah tanah
               - Musim kemarau (kapur lebih cepat bereaksi)
               - Ulangi setiap 2-3 tahun
            
            4. **Monitoring:**
               - Cek pH 4 minggu setelah aplikasi
               - Sesuaikan dosis jika perlu
               - Target pH tercapai dalam 2-3 bulan
            """)
            
            # Cost estimation
            st.markdown("---")
            st.markdown("### 💰 Estimasi Biaya")
            
            harga_kapur = st.number_input(
                "Harga Kapur per Ton (Rp)",
                min_value=100000,
                max_value=2000000,
                value=500000,
                step=50000
            )
            
            biaya_total = total_lime * harga_kapur
            biaya_per_ha = lime_per_ha * harga_kapur
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Biaya per Hektar", f"Rp {biaya_per_ha:,.0f}")
            
            with col2:
                st.metric("Total Biaya", f"Rp {biaya_total:,.0f}")

# TAB 4: pH GUIDE
with tab4:
    st.header("📖 Panduan Lengkap pH Tanah")
    
    st.markdown("""
    ## 🔬 Apa itu pH Tanah?
    
    pH tanah adalah ukuran keasaman atau kebasaan tanah, dengan skala 0-14:
    - **pH < 7:** Asam
    - **pH = 7:** Netral
    - **pH > 7:** Basa (Alkalin)
    
    ---
    
    ## 📊 Klasifikasi pH Tanah
    
    | pH Range | Klasifikasi | Warna Indikator |
    |----------|-------------|-----------------|
    | < 4.5 | Sangat Asam | 🔴 Merah |
    | 4.5 - 5.5 | Asam | 🟠 Oranye |
    | 5.5 - 6.5 | Agak Asam | 🟡 Kuning |
    | 6.5 - 7.5 | Netral | 🟢 Hijau |
    | 7.5 - 8.5 | Agak Basa | 🔵 Biru Muda |
    | > 8.5 | Basa | 🔵 Biru Tua |
    
    **pH Optimal untuk Kebanyakan Tanaman: 6.0 - 7.0**
    
    ---
    
    ## ⚗️ Pengaruh pH terhadap Ketersediaan Hara
    
    ### pH Rendah (Asam) < 5.5:
    
    **Ketersediaan Tinggi (Bisa Toksik):**
    - ⬆️ Aluminium (Al) - TOKSIK untuk akar
    - ⬆️ Besi (Fe) - bisa berlebihan
    - ⬆️ Mangan (Mn) - bisa toksik
    
    **Ketersediaan Rendah (Defisiensi):**
    - ⬇️ Nitrogen (N)
    - ⬇️ Fosfor (P) - terikat Al dan Fe
    - ⬇️ Kalium (K)
    - ⬇️ Kalsium (Ca)
    - ⬇️ Magnesium (Mg)
    - ⬇️ Molibdenum (Mo)
    
    **Dampak:**
    - Pertumbuhan akar terhambat
    - Fiksasi N terganggu (untuk legum)
    - Aktivitas mikroba rendah
    - Tanaman kerdil dan kuning
    
    ---
    
    ### pH Tinggi (Basa) > 7.5:
    
    **Ketersediaan Rendah (Defisiensi):**
    - ⬇️ Besi (Fe) - klorosis daun muda
    - ⬇️ Mangan (Mn)
    - ⬇️ Zinc (Zn)
    - ⬇️ Tembaga (Cu)
    - ⬇️ Boron (B)
    - ⬇️ Fosfor (P) - terikat Ca
    
    **Dampak:**
    - Klorosis Fe (daun kuning, tulang hijau)
    - Pertumbuhan lambat
    - Buah/biji kecil
    - Kualitas hasil menurun
    
    ---
    
    ### pH Optimal (6.0 - 7.0):
    
    **Keuntungan:**
    - ✅ Semua hara tersedia optimal
    - ✅ Aktivitas mikroba maksimal
    - ✅ Struktur tanah baik
    - ✅ Tidak ada toksisitas
    - ✅ Hasil panen maksimal
    
    ---
    
    ## 🧪 Cara Mengukur pH Tanah
    
    ### 1. pH Meter Digital (Akurat)
    - Masukkan probe ke tanah lembab
    - Baca hasil di layar
    - Akurasi: ±0.1 pH
    - Harga: Rp 200.000 - 2.000.000
    
    ### 2. pH Tester Tanah (Sedang)
    - Tusukkan probe ke tanah
    - Baca skala warna
    - Akurasi: ±0.5 pH
    - Harga: Rp 50.000 - 200.000
    
    ### 3. Kertas Lakmus (Murah)
    - Campur tanah + air suling (1:2)
    - Celupkan kertas lakmus
    - Cocokkan warna dengan skala
    - Akurasi: ±1.0 pH
    - Harga: Rp 10.000 - 50.000
    
    ### 4. Uji Laboratorium (Paling Akurat)
    - Kirim sampel ke lab tanah
    - Hasil lengkap: pH, hara, tekstur
    - Akurasi: ±0.05 pH
    - Biaya: Rp 50.000 - 200.000/sampel
    - Rekomendasi: **Balai Penelitian Tanah** atau **Lab Tanah Fakultas Pertanian**
    
    ---
    
    ## 🔧 Cara Memperbaiki pH Tanah
    
    ### Menaikkan pH (Tanah Asam → Netral)
    
    **1. Kapur Pertanian (CaCO3)**
    - Dosis: 1-3 ton/ha
    - Kenaikan: +0.5-1.5 pH
    - Waktu reaksi: 2-3 bulan
    - Bonus: Tambahan Ca
    
    **2. Dolomit (CaMg(CO3)2)**
    - Dosis: 1-3 ton/ha
    - Kenaikan: +0.5-1.5 pH
    - Waktu reaksi: 2-3 bulan
    - Bonus: Tambahan Ca dan Mg
    - **Pilih ini jika tanah kekurangan Mg!**
    
    **3. Kapur Tohor (CaO)**
    - Dosis: 0.6-2 ton/ha (60% dari kapur biasa)
    - Kenaikan: +0.5-1.5 pH
    - Waktu reaksi: 1-2 bulan (lebih cepat)
    - Hati-hati: Lebih reaktif, bisa merusak akar jika over
    
    **4. Abu Kayu**
    - Dosis: 2-5 ton/ha
    - Kenaikan: +0.3-0.8 pH
    - Bonus: K, Ca, Mg
    - Organik dan murah!
    
    **Cara Aplikasi:**
    - Sebar merata saat olah tanah
    - Aduk dengan tanah (15-20 cm)
    - 2-4 minggu sebelum tanam
    - Jangan bersamaan dengan pupuk N (urea hilang)
    
    ---
    
    ### Menurunkan pH (Tanah Basa → Netral)
    
    **1. Belerang (S)**
    - Dosis: 200-1000 kg/ha
    - Penurunan: -0.5-1.5 pH
    - Waktu reaksi: 3-6 bulan (lambat)
    - Mekanisme: S → H2SO4 (asam sulfat)
    
    **2. Pupuk Asam**
    - ZA (Amonium Sulfat): Efek asam sedang
    - Urea: Efek asam ringan
    - Amonium Nitrat: Efek asam kuat
    
    **3. Kompos/Pupuk Organik**
    - Dosis: 10-20 ton/ha
    - Penurunan: -0.3-0.8 pH
    - Waktu reaksi: 2-4 bulan
    - Bonus: Perbaiki struktur tanah
    
    **4. Gypsum (CaSO4)**
    - Dosis: 500-2000 kg/ha
    - Penurunan: -0.2-0.5 pH
    - Bonus: Tambahan Ca dan S
    - Cocok untuk tanah sodic (Na tinggi)
    
    **5. Mulsa Organik Asam**
    - Serbuk gergaji pinus
    - Daun oak
    - Jarum pinus
    - Efek: Penurunan bertahap
    
    **Cara Aplikasi:**
    - Sebar merata
    - Aduk dengan tanah
    - Aplikasi bertahap (jangan sekaligus)
    - Monitor pH setiap 2 bulan
    
    ---
    
    ## ⚠️ Hal Penting yang Harus Diperhatikan
    
    1. **Jangan Over-Aplikasi!**
       - Kelebihan kapur → pH terlalu tinggi → defisiensi mikronutrien
       - Kelebihan belerang → pH terlalu rendah → toksisitas Al
    
    2. **Aplikasi Bertahap**
       - Jika butuh >2 ton kapur/ha → bagi 2x aplikasi
       - Jarak 2-3 bulan antar aplikasi
    
    3. **Waktu yang Tepat**
       - Kapur: 2-4 minggu sebelum tanam
       - Belerang: 3-6 bulan sebelum tanam (reaksi lambat)
    
    4. **Jangan Campur dengan Pupuk N**
       - Kapur + Urea = N hilang (volatilisasi)
       - Beri jarak 2-3 minggu
    
    5. **Monitoring Rutin**
       - Cek pH setiap 6 bulan
       - Ulangi pengapuran setiap 2-3 tahun
    
    6. **Sesuaikan dengan Tanaman**
       - Kentang, teh → suka pH asam (5.0-5.5)
       - Kedelai, bawang → suka pH netral (6.5-7.0)
       - Lihat database tanaman!
    
    ---
    
    ## 💡 Tips Praktis
    
    1. **Uji pH Sebelum Tanam**
       - Investasi kecil, manfaat besar
       - Hemat pupuk (efisiensi meningkat)
    
    2. **Perbaikan pH = Investasi Jangka Panjang**
       - Efek kapur bertahan 2-3 tahun
       - Hasil panen meningkat 20-50%
    
    3. **Kombinasi dengan Pupuk Organik**
       - Organik + kapur = struktur tanah bagus
       - Organik + belerang = pH turun stabil
    
    4. **Rotasi Tanaman**
       - Tanaman suka asam → tanaman suka netral
       - Bantu stabilkan pH tanah
    
    5. **Drainase Penting!**
       - Tanah tergenang → pH naik
       - Drainase baik → pH stabil
    """)

# TAB 5: ALTITUDE GUIDE
with tab5:
    st.header("🏔️ Panduan Ketinggian (Altimeter)")
    
    st.markdown("""
    ## 🌍 Pengaruh Ketinggian terhadap Pertanian
    
    Ketinggian tempat (altimeter) sangat mempengaruhi:
    - 🌡️ Suhu udara
    - 💧 Kelembaban
    - ☀️ Intensitas cahaya
    - 🌧️ Curah hujan
    - 🌱 Jenis tanaman yang cocok
    
    **Prinsip Umum:**
    - Setiap naik 100 m → suhu turun 0.6°C
    - Dataran tinggi → suhu dingin, kelembaban tinggi
    - Dataran rendah → suhu panas, kelembaban rendah
    
    ---
    
    ## 📊 Klasifikasi Ketinggian
    
    ### 1. Dataran Rendah (0-700 mdpl)
    
    **Karakteristik:**
    - Suhu: 24-32°C
    - Kelembaban: Sedang-tinggi
    - Curah hujan: 1500-3000 mm/tahun
    
    **Tanaman Cocok:**
    - **Pangan:** Padi sawah, jagung, kedelai
    - **Sayuran:** Cabai, terong, kangkung, bayam
    - **Buah:** Pisang, pepaya, mangga, nanas, durian
    - **Perkebunan:** Kelapa sawit, karet, kakao, tebu
    
    **Keuntungan:**
    - Pertumbuhan cepat
    - Produktivitas tinggi
    - Akses mudah
    
    **Tantangan:**
    - Hama lebih banyak
    - Penyakit lebih aktif
    - Kualitas buah kurang manis (untuk beberapa jenis)
    
    ---
    
    ### 2. Dataran Sedang (700-1500 mdpl)
    
    **Karakteristik:**
    - Suhu: 18-24°C
    - Kelembaban: Tinggi
    - Curah hujan: 2000-3500 mm/tahun
    
    **Tanaman Cocok:**
    - **Pangan:** Padi gogo, jagung, kedelai
    - **Sayuran:** Tomat, cabai, bawang daun, kacang panjang
    - **Buah:** Jeruk, alpukat, markisa, salak
    - **Perkebunan:** Kopi robusta, kakao, vanili
    
    **Keuntungan:**
    - Suhu ideal untuk banyak tanaman
    - Kualitas hasil baik
    - Hama lebih sedikit dari dataran rendah
    
    **Tantangan:**
    - Curah hujan tinggi → penyakit jamur
    - Akses lebih sulit
    - Biaya transportasi lebih mahal
    
    ---
    
    ### 3. Dataran Tinggi (1500-3000 mdpl)
    
    **Karakteristik:**
    - Suhu: 10-18°C
    - Kelembaban: Sangat tinggi
    - Curah hujan: 2500-4000 mm/tahun
    
    **Tanaman Cocok:**
    - **Pangan:** Kentang, ubi jalar
    - **Sayuran:** Kubis, brokoli, wortel, selada, bawang putih, seledri
    - **Buah:** Strawberry, apel, anggur (varietas tertentu)
    - **Perkebunan:** Kopi arabica, teh, cengkeh
    
    **Keuntungan:**
    - Kualitas premium (kopi, teh, sayuran)
    - Hama sangat sedikit
    - Harga jual tinggi
    - Udara sejuk
    
    **Tantangan:**
    - Pertumbuhan lambat
    - Biaya produksi tinggi
    - Akses sangat sulit
    - Risiko frost (beku) di >2000 mdpl
    
    ---
    
    ## 🌡️ Pengaruh Suhu terhadap Tanaman
    
    ### Tanaman Suhu Panas (>25°C)
    - Padi, jagung, kedelai
    - Cabai, terong
    - Pisang, mangga, durian
    - Kelapa sawit, karet
    
    ### Tanaman Suhu Sedang (18-25°C)
    - Tomat, bawang
    - Jeruk, alpukat
    - Kopi robusta, kakao
    
    ### Tanaman Suhu Dingin (<18°C)
    - Kentang, kubis, wortel
    - Strawberry, apel
    - Kopi arabica, teh
    
    ---
    
    ## 💡 Tips Memilih Tanaman Berdasarkan Ketinggian
    
    1. **Sesuaikan dengan Lokasi**
       - Cek ketinggian lahan dengan GPS/altimeter
       - Pilih tanaman sesuai klasifikasi
       - Jangan paksa tanaman dataran tinggi di dataran rendah (dan sebaliknya)
    
    2. **Pertimbangkan Ekonomi**
       - Dataran tinggi: Tanaman premium (harga tinggi)
       - Dataran rendah: Tanaman volume (produktivitas tinggi)
    
    3. **Akses Pasar**
       - Dataran tinggi: Sayuran segar (cepat rusak) → pasar dekat
       - Dataran rendah: Komoditas tahan lama → pasar jauh OK
    
    4. **Kombinasi Ketinggian + pH**
       - Kopi arabica: 1000-1500 mdpl + pH 6.0 = premium
       - Kentang: >1000 mdpl + pH 5.5 = hasil maksimal
       - Lihat database tanaman untuk kombinasi optimal!
    
    5. **Adaptasi Iklim Mikro**
       - Lembah: Lebih dingin dari sekitar
       - Lereng: Lebih hangat, drainase baik
       - Puncak: Paling dingin, angin kencang
    
    ---
    
    ## 📍 Cara Mengukur Ketinggian
    
    ### 1. GPS Smartphone
    - Buka aplikasi GPS (Google Maps, dll)
    - Lihat elevation/altitude
    - Akurasi: ±10-50 meter
    - Gratis!
    
    ### 2. Altimeter Digital
    - Alat khusus ukur ketinggian
    - Akurasi: ±5-10 meter
    - Harga: Rp 500.000 - 5.000.000
    
    ### 3. Peta Topografi
    - Lihat kontur peta
    - Akurasi: ±25 meter
    - Gratis (online)
    
    ### 4. Barometer
    - Ukur tekanan udara
    - Konversi ke ketinggian
    - Akurasi: ±10-20 meter
    
    ---
    
    ## 🌾 Contoh Kasus Sukses
    
    ### Kopi Arabica Gayo (Aceh)
    - Ketinggian: 1200-1600 mdpl
    - pH: 5.5-6.5
    - Hasil: Kopi specialty grade 1
    - Harga: 3-5x kopi biasa
    
    ### Kentang Dieng (Jawa Tengah)
    - Ketinggian: 2000-2500 mdpl
    - pH: 5.0-5.5
    - Hasil: 25-30 ton/ha
    - Kualitas: Premium
    
    ### Bawang Merah Brebes (Jawa Tengah)
    - Ketinggian: 0-100 mdpl
    - pH: 6.0-7.0
    - Hasil: 15-20 ton/ha
    - Sentra produksi nasional
    
    ### Teh Puncak (Jawa Barat)
    - Ketinggian: 1200-1800 mdpl
    - pH: 4.5-5.5
    - Hasil: Teh berkualitas tinggi
    - Ekspor premium
    """)

# TAB 6: JOURNALS & REFERENCES
with tab6:
    st.header("📄 Referensi Jurnal & Basis Data Ilmiah")
    st.markdown("""
    Penyusunan database ini didasarkan pada berbagai literatur ilmiah, jurnal penelitian, dan standar teknis dari institusi pertanian terkemuka untuk memastikan akurasi data parameter agronomi.
    
    ### 🏛️ Institusi Sumber Data
    - **Balittanah (Balai Penelitian Tanah):** Standar klasifikasi pH dan kesuburan tanah Indonesia.
    - **Puslitkoka (Pusat Penelitian Kopi dan Kakao):** Parameter spesifik tanaman perkebunan.
    - **Balitbangtan (Badan Penelitian dan Pengembangan Pertanian):** Deskripsi varietas dan syarat tumbuh tanaman pangan.
    - **IPB University & UGM:** Publikasi jurnal agronomi dan ilmu tanah.
    
    ### 📚 Literatur Jurnal Utama
    1. **Oldeman, L.R. (1975):** *An Agroclimatic Map of Java*. Contributions from the Central Research Institute for Agriculture. (Dasar klasifikasi iklim Oldeman).
    2. **Hardjowigeno, S. (2003):** *Ilmu Tanah*. Akademika Pressindo. (Referensi utama sifat kimia tanah dan pH).
    3. **Djaenudin, D., dkk. (2003):** *Kriteria Kesesuaian Lahan untuk Komoditas Pertanian*. Balai Penelitian Tanah. (Dasar algoritma scoring kesesuaian).
    4. **Setyahadi, V. (2015):** *Analisis Kation dan Kapasitas Tukar Kation*. Jurnal Tanah Tropika.
    
    ### 🔬 Parameter Ilmiah yang Digunakan
    - **KTK (Kapasitas Tukar Kation):** Mengukur kemampuan tanah menjerap kation hara. KTK tinggi berarti kemampuan menahan hara tinggi.
    - **Tipe Iklim Oldeman:** Menggunakan data Bulan Basah (BB) dan Bulan Kering (BK) berturut-turut untuk menentukan pola tanam padi-palawija.
    - **Base Saturation (Kejenuhan Basa):** Persentase kation basa terhadap total KTK, berkorelasi kuat dengan pH tanah.
    """)
    
    st.info("💡 **Catatan:** Data dalam aplikasi ini adalah generalisasi untuk tujuan edukasi. Untuk implementasi presisi, sangat direkomendasikan melakukan uji sampel tanah di laboratorium bersertifikat.")

# Footer
st.markdown("---")
st.caption("""
🌍 **AgriSensa Advanced pH & Altitude Edition** - Database Ilmiah Terintegrasi

💡 **Integrasi Terpadu:**
- 🗺️ **Peta Data Tanah** - Analisis pH Spasial
- 🧮 **Kalkulator Pupuk** - Koreksi Kebutuhan Hara
- 🌤️ **Cuaca Pertanian** - Sinkronisasi Oldeman & Curah Hujan

⚠️ **Disclaimer:** Data ini berbasis jurnal ilmiah namun bersifat generalisasi. Hasil lapangan dapat bervariasi tergantung varietas dan mikro-iklim. Lakukan uji lab tanah secara berkala.

🌱 **Visi AgriSensa:** Pertanian Presisi berbasis Data Ilmiah untuk Kedaulatan Pangan.
""")
