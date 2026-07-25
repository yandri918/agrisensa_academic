# Katalog Pupuk & Harga
# Module 25 - Comprehensive Fertilizer Catalog
# Version: 1.0.0

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Katalog Pupuk & Harga", page_icon="🧪", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATABASE INITIALIZATION ==========

# Default Data
FERTILIZER_DATABASE_DEFAULT = {
    # UREA
    "Urea Pusri": {
        "category": "Urea",
        "brand": "PT Pupuk Sriwidjaja (Pusri)",
        "formula": "CO(NH₂)₂",
        "n_content": 46,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen tunggal untuk fase vegetatif",
        "usage": "Padi, jagung, sayuran",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor, 2-3 kali aplikasi"
    },
    "Urea Petrokimia": {
        "category": "Urea",
        "brand": "PT Petrokimia Gresik",
        "formula": "CO(NH₂)₂",
        "n_content": 46,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen untuk pertumbuhan vegetatif",
        "usage": "Padi, jagung, tebu",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor, split application"
    },
    "Urea Kaltim": {
        "category": "Urea",
        "brand": "PT Pupuk Kalimantan Timur",
        "formula": "CO(NH₂)₂",
        "n_content": 46,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen butiran (granul) berkualitas tinggi",
        "usage": "Padi, jagung, hortalikultura",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor"
    },
    
    # NPK PHONSKA
    "NPK Phonska (Subsidi)": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "15-10-12",
        "n_content": 15,
        "p_content": 10,
        "k_content": 12,
        "price_per_kg": 2300,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk subsidi untuk tanaman pangan",
        "usage": "Padi, jagung, kedelai",
        "dosage": "250-400 kg/ha",
        "application": "Tabur saat tanam"
    },
    "NPK Phonska Plus": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "15-15-15+9S+0.1Zn",
        "n_content": 15,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 3200,
        "package_sizes": ["25 kg", "50 kg"],
        "description": "Pupuk majemuk non-subsidi dengan tambahan Sulfur dan Zinc",
        "usage": "Padi, jagung, hortikultura",
        "dosage": "200-350 kg/ha",
        "application": "Tabur/kocor"
    },
    "NPK Mutiara 16-16-16": {
        "category": "NPK",
        "brand": "Yara / PT Meroke Tetap Jaya",
        "formula": "16-16-16",
        "n_content": 16,
        "p_content": 16,
        "k_content": 16,
        "price_per_kg": 18000,
        "package_sizes": ["1 kg", "5 kg", "50 kg"],
        "description": "Pupuk majemuk impor berkualitas tinggi untuk hortikultura",
        "usage": "Sayuran, buah-buahan, tanaman hias",
        "dosage": "200-500 kg/ha",
        "application": "Tabur/kocor"
    },
    "NPK Pelangi 16-16-16": {
        "category": "NPK",
        "brand": "PT Pupuk Kalimantan Timur",
        "formula": "16-16-16",
        "n_content": 16,
        "p_content": 16,
        "k_content": 16,
        "price_per_kg": 12000,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk dengan teknologi blend merata",
        "usage": "Padi, jagung, perkebunan",
        "dosage": "250-400 kg/ha",
        "application": "Tabur"
    },
    
    # NPK GROWER
    "NPK Meroke Grower 15-09-20": {
        "category": "NPK",
        "brand": "PT Meroke Tetap Jaya",
        "formula": "15-09-20+TE",
        "n_content": 15,
        "p_content": 9,
        "k_content": 20,
        "price_per_kg": 19500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk untuk fase generatif/pembesaran buah",
        "usage": "Cabai, tomat, melon, jeruk",
        "dosage": "300-500 kg/ha",
        "application": "Kocor/tabur"
    },
    
    # SP-36 & TSP
    "SP-36 Petro": {
        "category": "Fosfat",
        "brand": "PT Petrokimia Gresik",
        "formula": "P₂O₅ 36%",
        "n_content": 0,
        "p_content": 36,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk sumber fosfat utama untuk perakaran",
        "usage": "Padi, jagung, kedelai",
        "dosage": "100-150 kg/ha",
        "application": "Tabur saat tanam"
    },
    "TSP 46": {
        "category": "Fosfat",
        "brand": "Import",
        "formula": "P₂O₅ 46%",
        "n_content": 0,
        "p_content": 46,
        "k_content": 0,
        "price_per_kg": 15000,
        "package_sizes": ["50 kg"],
        "description": "Triple Super Phosphate kandungan P sangat tinggi",
        "usage": "Perkebunan, holtikultura",
        "dosage": "100-200 kg/ha",
        "application": "Tabur"
    },
    
    # KCl / MOP
    "KCl Mahkota": {
        "category": "Kalium",
        "brand": "PT Wilmar Nabati Indonesia",
        "formula": "K₂O 60%",
        "n_content": 0,
        "p_content": 0,
        "k_content": 60,
        "price_per_kg": 9500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk sumber kalium untuk ketahanan penyakit",
        "usage": "Padi, sawit, jagung",
        "dosage": "100-200 kg/ha",
        "application": "Tabur"
    },
    "ZK (Kalium Sulfat)": {
        "category": "Kalium",
        "brand": "PT Petrokimia Gresik",
        "formula": "K₂O 50% + S 17%",
        "n_content": 0,
        "p_content": 0,
        "k_content": 50,
        "price_per_kg": 16000,
        "package_sizes": ["25 kg", "50 kg"],
        "description": "Pupuk kalium bebas klor, sangat baik untuk tembakau & jeruk",
        "usage": "Tembakau, kentang, wortel, jeruk",
        "dosage": "150-250 kg/ha",
        "application": "Tabur/kocor"
    },

    # KHUSUS HIDROPONIK
    "AB Mix Sayuran Daun": {
        "category": "Hidroponik",
        "brand": "Lokal Premium",
        "formula": "Pekatan A + Pekatan B",
        "n_content": 10,
        "p_content": 5,
        "k_content": 15,
        "price_per_kg": 45000,
        "package_sizes": ["1 set (5 liter)"],
        "description": "Nutrisi lengkap untuk sayuran daun hidroponik",
        "usage": "Selada, sawi, pakcoy, kangkung",
        "dosage": "5 ml A + 5 ml B per 1 liter air",
        "application": "Sirkulasi/NFT/Wick"
    },
    "AB Mix Buah": {
        "category": "Hidroponik",
        "brand": "Lokal Premium",
        "formula": "Pekatan A + Pekatan B",
        "n_content": 8,
        "p_content": 8,
        "k_content": 22,
        "price_per_kg": 55000,
        "package_sizes": ["1 set (5 liter)"],
        "description": "Nutrisi lengkap untuk sayuran buah hidroponik",
        "usage": "Melon, tomat, cabai, stroberi",
        "dosage": "5 ml A + 5 ml B per 1 liter air",
        "application": "Sirkulasi/Drip Irigasi"
    },
    
    # HAYATI & ORGANIK
    "EM4 Pertanian": {
        "category": "Hayati",
        "brand": "PT Songgolangit Persada",
        "formula": "Lactobacillus, ragi, fotosintetik",
        "n_content": 0.1,
        "p_content": 0.1,
        "k_content": 0.1,
        "price_per_kg": 25000, # per liter
        "package_sizes": ["1 liter"],
        "description": "Mikroorganisme efektif untuk dekomposisi dan kesehatan tanah",
        "usage": "Semua tanaman, pembuatan kompos",
        "dosage": "1-2 ml per liter air",
        "application": "Semprot tanah/siraman"
    },
    "Biotara": {
        "category": "Hayati",
        "brand": "PT Pupuk Indonesia",
        "formula": "Trichoderma + N-Fixer",
        "n_content": 1,
        "p_content": 1,
        "k_content": 1,
        "price_per_kg": 22000,
        "package_sizes": ["1 kg"],
        "description": "Pupuk hayati khusus untuk lahan rawa/asam",
        "usage": "Padi rawa, jagung",
        "dosage": "25-50 kg/ha",
        "application": "Tabur bersama pupuk kimia"
    },
    
    # KEBOMAS & PREMIUM
    "NPK Kebomas 15-15-15": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "15-15-15",
        "n_content": 15,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 9500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk untuk tanaman pangan dan hortikultura",
        "usage": "Padi, jagung, kedelai",
        "dosage": "250-400 kg/ha",
        "application": "Tabur"
    },
    "NPK YaraMila Winner": {
        "category": "NPK Premium",
        "brand": "Yara International",
        "formula": "15-09-20+TE",
        "n_content": 15,
        "p_content": 9,
        "k_content": 20,
        "price_per_kg": 22000,
        "package_sizes": ["50 kg"],
        "description": "Pupuk premium dengan teknologi prill, larut air sempurna",
        "usage": "Buah-buahan, sayuran bernilai tinggi",
        "dosage": "300-500 kg/ha",
        "application": "Kocor/tabur"
    },
    
    # ZA
    "ZA Petrokimia": {
        "category": "ZA",
        "brand": "PT Petrokimia Gresik",
        "formula": "(NH₄)₂SO₄",
        "n_content": 21,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 4500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen plus sulfur 24%",
        "usage": "Padi, tebu, hortikultura",
        "dosage": "150-250 kg/ha",
        "application": "Tabur"
    },
    "ZA Pusri": {
        "category": "ZA",
        "brand": "PT Pupuk Sriwidjaja",
        "formula": "(NH₄)₂SO₄",
        "n_content": 21,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 4500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen amonium tinggi sulfur",
        "usage": "Padi, jagung, sayuran",
        "dosage": "150-250 kg/ha",
        "application": "Tabur"
    },
    
    # KCl / MOP Variants
    "KCl Putih (MOP)": {
        "category": "Kalium",
        "brand": "Import",
        "formula": "K₂O 60%",
        "n_content": 0,
        "p_content": 0,
        "k_content": 60,
        "price_per_kg": 11000,
        "package_sizes": ["50 kg"],
        "description": "Kalium Klorida berkualitas tunggi untuk hasil optimal",
        "usage": "Padi, jagung, buah",
        "dosage": "100-200 kg/ha",
        "application": "Tabur"
    },
    
    # ORGANIK
    "Petroganik": {
        "category": "Organik",
        "brand": "PT Petrokimia Gresik",
        "formula": "Organik Granul",
        "n_content": 2,
        "p_content": 1,
        "k_content": 2,
        "price_per_kg": 1200,
        "package_sizes": ["40 kg"],
        "description": "Pupuk organik granul untuk memperbaiki struktur tanah",
        "usage": "Semua tanaman",
        "dosage": "500-1000 kg/ha",
        "application": "Tabur saat olah tanah"
    },
    "NASA POC": {
        "category": "Organik Cair",
        "brand": "PT Natural Nusantara",
        "formula": "Organik Cair",
        "n_content": 3,
        "p_content": 2,
        "k_content": 2,
        "price_per_kg": 45000,
        "package_sizes": ["500 ml", "3 liter"],
        "description": "Pupuk organik cair multiguna",
        "usage": "Semua tanaman",
        "dosage": "3-5 tutup botol per tangki",
        "application": "Semprot daun"
    },
    "DI GROW Hijau/Putih (Growth)": {
        "category": "Organik Cair",
        "brand": "Dynapharm",
        "formula": "Biostimulan Vegetatif",
        "n_content": 4,
        "p_content": 2,
        "k_content": 2,
        "price_per_kg": 175000, # per Liter
        "package_sizes": ["500 ml", "1 Liter", "4 Liter"],
        "description": "Growth Booster dari ekstrak rumput laut Atlantik Utara untuk fase vegetatif.",
        "usage": "Padi, cabai, sayuran, bawang",
        "dosage": "3-5 ml per liter air",
        "application": "Semprot daun (7-10 hari sekali)"
    },
    "DI GROW Merah (Fruits)": {
        "category": "Organik Cair",
        "brand": "Dynapharm",
        "formula": "Biostimulan Generatif",
        "n_content": 2,
        "p_content": 4,
        "k_content": 5,
        "price_per_kg": 185000, # per Liter
        "package_sizes": ["500 ml", "1 Liter", "4 Liter"],
        "description": "Fruit & Flower Booster untuk merangsang pembuahan dan mencegah rontok.",
        "usage": "Melon, buah-buahan, tanaman berbunga",
        "dosage": "3-5 ml per liter air",
        "application": "Semprot daun (7-10 hari sekali)"
    },
    
    # MIKRO & SEKUNDER
    "Gandasil D": {
        "category": "Mikro",
        "brand": "Kalbe",
        "formula": "N-P-K + Mikro",
        "n_content": 20,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 35000, # per 500g biasanya
        "package_sizes": ["100g", "500g"],
        "description": "Pupuk daun untuk fase vegetatif",
        "usage": "Sayuran, tanaman hias",
        "dosage": "2-3 g/liter",
        "application": "Semprot"
    },
    "Gandasil B": {
        "category": "Mikro",
        "brand": "Kalbe",
        "formula": "N-P-K + Mikro",
        "n_content": 6,
        "p_content": 20,
        "k_content": 30,
        "price_per_kg": 35000,
        "package_sizes": ["100g", "500g"],
        "description": "Pupuk daun untuk fase generatif (buah)",
        "usage": "Buah, bunga",
        "dosage": "2-3 g/liter",
        "application": "Semprot"
    },
    "Dolomit Super": {
        "category": "Sekunder",
        "brand": "Lokal",
        "formula": "CaMg(CO₃)₂",
        "n_content": 0,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 800,
        "package_sizes": ["50 kg", "Curah"],
        "description": "Kapur pertanian untuk menaikkan pH tanah",
        "usage": "Tanah masam",
        "dosage": "1-2 ton/ha",
        "application": "Tabur"
    },
    "Kieserite (Magnesium)": {
        "category": "Sekunder",
        "brand": "Import",
        "formula": "MgSO₄",
        "n_content": 0,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 6500,
        "package_sizes": ["50 kg"],
        "description": "Sumber Magnesium dan Sulfur cepat serap",
        "usage": "Tanaman tahunan, buah",
        "dosage": "100-200 kg/ha",
        "application": "Tabur"
    },
    
    # KHUSUS GENERATIF & PEMBUNGAAN
    "KNO3 Merah (DGW)": {
        "category": "Kalium Nitrat",
        "brand": "DGW",
        "formula": "15-0-14",
        "n_content": 15,
        "p_content": 0,
        "k_content": 14,
        "price_per_kg": 35000,
        "package_sizes": ["2 kg", "25 kg"],
        "description": "Pupuk kalium nitrat untuk fase vegetatif",
        "usage": "Cabai, tomat, bawang merah",
        "dosage": "2-5 g/liter air",
        "application": "Kocor/semprot"
    },
    "KNO3 Putih (Pak Tani)": {
        "category": "Kalium Nitrat",
        "brand": "Saprotan Utama (Pak Tani)",
        "formula": "13-0-45",
        "n_content": 13,
        "p_content": 0,
        "k_content": 45,
        "price_per_kg": 45000,
        "package_sizes": ["2 kg", "25 kg"],
        "description": "Pupuk kalium nitrat kristal untuk fase generatif/pembuahan",
        "usage": "Melon, semangka, jeruk, kentang",
        "dosage": "3-10 g/liter air",
        "application": "Kocor/semprot"
    },
    "MKP (Pak Tani)": {
        "category": "Fosfat Kalium",
        "brand": "Saprotan Utama (Pak Tani)",
        "formula": "0-52-34",
        "n_content": 0,
        "p_content": 52,
        "k_content": 34,
        "price_per_kg": 55000,
        "package_sizes": ["1 kg"],
        "description": "Mono Kalium Fosfat, larut air 100% untuk merangsang pembungaan",
        "usage": "Tanaman buah, hortikultura",
        "dosage": "2-4 g/liter air",
        "application": "Semprot/kocor"
    },
    "Meroke MAP": {
        "category": "Fosfat Amonium",
        "brand": "PT Meroke Tetap Jaya",
        "formula": "12-61-0",
        "n_content": 12,
        "p_content": 61,
        "k_content": 0,
        "price_per_kg": 48000,
        "package_sizes": ["1 kg", "25 kg"],
        "description": "Mono Amonium Fosfat untuk sistem perakaran dan energi tanaman",
        "usage": "Semua jenis tanaman",
        "dosage": "2-5 g/liter air",
        "application": "Sistem fertigasi/hidroponik"
    },
}

PESTICIDE_DATABASE_DEFAULT = {
    # INSEKTISIDA
    "Curacron 500EC": {
        "category": "Insektisida",
        "brand": "Syngenta",
        "active_ingredient": "Profenofos 500 g/l",
        "target_pests": ["Ulat Grayak", "Kutu Daun", "Thrips", "Penggerek Batang", "Lalat Buah"],
        "price": 125000,
        "unit": "500 ml",
        "description": "Insektisida racun kontak dan lambung spektrum luas.",
        "usage": "Cabai, Bawang Merah, Tomat, Kubis",
        "dosage": "1-2 ml/liter air"
    },
    "Regent 50SC": {
        "category": "Insektisida",
        "brand": "BASF",
        "active_ingredient": "Fipronil 50 g/l",
        "target_pests": ["Wereng Coklat", "Penggerek Batang", "Thrips", "Rayap"],
        "price": 85000,
        "unit": "100 ml",
        "description": "Insektisida sistemik racun kontak dan lambung dengan efek ZPT.",
        "usage": "Padi, Cabai, Jagung, Kelapa Sawit",
        "dosage": "1-2 ml/liter air"
    },
    "Prevathon 50SC": {
        "category": "Insektisida",
        "brand": "FMC",
        "active_ingredient": "Kloramtraniliprol 50 g/l",
        "target_pests": ["Ulat Grayak", "Penggerek Batang", "Ulat Krop"],
        "price": 195000,
        "unit": "250 ml",
        "description": "Insektisida sistemik translaminar, sangat efektif memutus siklus ulat.",
        "usage": "Padi, Bawang Merah, Kubis, Cabai",
        "dosage": "3 ml/liter air"
    },
    "Alika 247ZC": {
        "category": "Insektisida",
        "brand": "Syngenta",
        "active_ingredient": "Lambda cyhalothrin + Thiamethoxam",
        "target_pests": ["Kutu Daun", "Kutu Kebul", "Ulat Grayak", "Wereng"],
        "price": 95000,
        "unit": "100 ml",
        "description": "Insektisida campur, knockdown cepat dan proteksi lama.",
        "usage": "Cabai, Tomat, Kentang, Mangga",
        "dosage": "0.5-1 ml/liter air"
    },
    "Decis 25EC": {
        "category": "Insektisida",
        "brand": "Bayer",
        "active_ingredient": "Deltametrin 25 g/l",
        "target_pests": ["Ulat", "Belalang", "Lalat Buah", "Kutu Daun"],
        "price": 55000,
        "unit": "100 ml",
        "description": "Insektisida racun kontak dan lambung golongan piretroid yang legendaris.",
        "usage": "Sayuran, Jagung, Kedelai",
        "dosage": "1 ml/liter air"
    },
    "Confidor 200SL": {
        "category": "Insektisida",
        "brand": "Bayer",
        "active_ingredient": "Imidakloprid 200 g/l",
        "target_pests": ["Thrips", "Kutu Daun", "Wereng", "Lalat Bibit"],
        "price": 115000,
        "unit": "100 ml",
        "description": "Insektisida sistemik spesialis hama penghisap.",
        "usage": "Cabai, Tomat, Padi, Semangka",
        "dosage": "0.5-1 ml/liter air"
    },
    "Dursban 200EC": {
        "category": "Insektisida",
        "brand": "Corteva",
        "active_ingredient": "Klorpirifos 200 g/l",
        "target_pests": ["Ulat Tanpa Daun", "Kumbang Badak", "Rayap"],
        "price": 110000,
        "unit": "500 ml",
        "description": "Insektisida racun kontak, lambung dan pernapasan (fumigan).",
        "usage": "Kelapa Sawit, Jagung, Kakao",
        "dosage": "2-3 ml/liter air"
    },
    
    # RAINBOW PRODUCTS (NEW)
    "Onrole 20 SG": {
        "category": "Insektisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Dinotefuran 20%",
        "target_pests": ["Wereng Coklat", "Penggerek Batang Padi"],
        "price": 45000,
        "unit": "100 gr",
        "description": "Insektisida racun kontak dan lambung sistemik untuk wereng.",
        "usage": "Padi",
        "dosage": "150-300 g/ha"
    },
    "Abinsec 18 EC": {
        "category": "Insektisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Abamectin 18 g/l",
        "target_pests": ["Thrips", "Kutu Daun", "Tungau"],
        "price": 65000,
        "unit": "250 ml",
        "description": "Insektisida racun kontak dan lambung spektrum luas.",
        "usage": "Cabai, Tomat, Jeruk",
        "dosage": "0.5-1 ml/liter air"
    },

    # FUNGISIDA
    "Amistartop 325SC": {
        "category": "Fungisida",
        "brand": "Syngenta",
        "active_ingredient": "Azoksistrobin + Difenokonazol",
        "target_pests": ["Busuk Daun", "Antraknosa", "Blas Padi", "Bercak Daun"],
        "price": 285000,
        "unit": "250 ml",
        "description": "Fungisida sistemik premium dengan ZPT pemacu pertumbuhan.",
        "usage": "Padi, Bawang Merah, Cabai, Tomat",
        "dosage": "0.5-1 ml/liter air"
    },
    "Antracol 70WP": {
        "category": "Fungisida",
        "brand": "Bayer",
        "active_ingredient": "Propineb 70%",
        "target_pests": ["Busuk Daun", "Bercak Daun", "Embun Tepung"],
        "price": 115000,
        "unit": "1 kg",
        "description": "Fungisida kontak protektif dengan kandungan Zinc (Zn).",
        "usage": "Sayuran, Buah, Tanaman Hias",
        "dosage": "2-3 g/liter air"
    },
    "Score 250EC": {
        "category": "Fungisida",
        "brand": "Syngenta",
        "active_ingredient": "Difenokonazol 250 g/l",
        "target_pests": ["Busuk Buah", "Bercak Ungu", "Bercak Daun Alternaria"],
        "price": 175000,
        "unit": "250 ml",
        "description": "Fungisida sistemik ZPT, sangat baik untuk pematangan buah.",
        "usage": "Padi, Semangka, Tomat, Cabai",
        "dosage": "0.5 ml/liter air"
    },
    "Dithane M-45": {
        "category": "Fungisida",
        "brand": "Corteva",
        "active_ingredient": "Mankozeb 80%",
        "target_pests": ["Busuk Daun", "Cacar Daun", "Karat Daun"],
        "price": 125000,
        "unit": "1 kg",
        "description": "Fungisida kontak multiguna spektrum luas.",
        "usage": "Kentang, Bawang, Cabai, Tomat",
        "dosage": "2-4 g/liter air"
    },
    "Nativo 75WG": {
        "category": "Fungisida",
        "brand": "Bayer",
        "active_ingredient": "Tebuconazole + Trifloxystrobin",
        "target_pests": ["Blas Padi", "Gosong Palsu", "Antraknosa"],
        "price": 65000,
        "unit": "50 gr",
        "description": "Fungisida sistemik kombinasi dua bahan aktif untuk padi bening.",
        "usage": "Padi, Cabai, Bawang Merah",
        "dosage": "150-200 g/hektar"
    },
    "Raineb 70 WP": {
        "category": "Fungisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Propineb 70%",
        "target_pests": ["Hawar Pelepah", "Busuk Daun", "Bercak Daun"],
        "price": 85000,
        "unit": "1 kg",
        "description": "Fungisida kontak protektif untuk penyakit jamur.",
        "usage": "Padi, Sayuran",
        "dosage": "2-3 g/liter air"
    },
    "Raincozeb 80 WP": {
        "category": "Fungisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Mancozeb 80%",
        "target_pests": ["Hawar Daun", "Busuk Buah", "Karat Daun"],
        "price": 95000,
        "unit": "1 kg",
        "description": "Fungisida kontak protektif berwarna kuning/biru.",
        "usage": "Hortikultura, Perkebunan",
        "dosage": "2-4 g/liter air"
    },
    "Bakterisida Agrimycin": {
        "category": "Bakterisida",
        "brand": "Pfizer/Agro",
        "active_ingredient": "Streptomisin sulfat",
        "target_pests": ["Layu Bakteri", "Hawar Daun Bakteri"],
        "price": 45000,
        "unit": "20 gr",
        "description": "Antibiotik pertanian untuk mengendalikan serangan bakteri.",
        "usage": "Tomat, Cabai, Padi (Kresek)",
        "dosage": "1-2 g/liter air"
    },

    # HERBISIDA
    "Roundup 486SL": {
        "category": "Herbisida",
        "brand": "Bayer",
        "active_ingredient": "Glifosat Isopropilamina 486 g/l",
        "target_pests": ["Alang-alang", "Rumput Liar", "Gulma Berdaun Lebar"],
        "price": 145000,
        "unit": "1 Liter",
        "description": "Herbisida sistemik purna tumbuh nomor 1, mati sampai akar.",
        "usage": "Perkebunan (Sawit/Karet), Persiapan Lahan",
        "dosage": "5-10 ml/liter air"
    },
    "Gramoxone 276SL": {
        "category": "Herbisida",
        "brand": "Syngenta",
        "active_ingredient": "Paraquat Diklorida 276 g/l",
        "target_pests": ["Gulma Hijau", "Rumput Teki", "Gulma Berdaun Lebar"],
        "price": 95000,
        "unit": "1 Liter",
        "description": "Herbisida kontak purna tumbuh, rumput gosong dalam hitungan jam.",
        "usage": "Lahan tanpa tanaman, Pematang Sawah",
        "dosage": "10-20 ml/liter air"
    },
    "Garlon 670EC": {
        "category": "Herbisida",
        "brand": "Corteva",
        "active_ingredient": "Triklofir Butoksi Etil Ester",
        "target_pests": ["Gulma Berkayu", "Tunggul Pohon", "Semak Belukar"],
        "price": 285000,
        "unit": "500 ml",
        "description": "Herbisida khusus untuk mematikan tanaman berkayu dan semak besar.",
        "usage": "Perkebunan Kelapa Sawit, Lahan Non-Crop",
        "dosage": "1-2 liter/hektar"
    },
    "Maizcare 550 SC": {
        "category": "Herbisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Atrazine 500 g/l + Mesotrione 50 g/l",
        "target_pests": ["Gulma Berdaun Lebar", "Gulma Rumput"],
        "price": 135000,
        "unit": "1 Liter",
        "description": "Herbisida selektif untuk mengendalikan gulma pada tanaman jagung.",
        "usage": "Jagung",
        "dosage": "1.5-2 liter/ha"
    },
    "Lava 276 SL": {
        "category": "Herbisida",
        "brand": "Rainbow Agrosciences",
        "active_ingredient": "Paraquat Diklorida 276 g/l",
        "target_pests": ["Gulma Umum", "Rumput Liar"],
        "price": 85000,
        "unit": "1 Liter",
        "description": "Herbisida kontak purna tumbuh yang sangat cepat membakar gulma.",
        "usage": "Lahan tanpa tanaman, persiapan lahan",
        "dosage": "10-20 ml/liter air"
    },
}

# Session State Init
DB_VERSION = "1.6" # Increment to force refresh

if 'db_version' not in st.session_state or st.session_state.db_version != DB_VERSION:
    st.session_state.fertilizer_db = FERTILIZER_DATABASE_DEFAULT.copy()
    st.session_state.pesticide_db = PESTICIDE_DATABASE_DEFAULT.copy()
    st.session_state.db_version = DB_VERSION

# Global variables for convenience (points to session state)
FERTILIZER_DATABASE = st.session_state.fertilizer_db
PESTICIDE_DATABASE_COMMERCIAL = st.session_state.pesticide_db




# ========== HELPER FUNCTIONS ==========

def get_categories():
    """Get unique categories"""
    return sorted(list(set([v["category"] for v in FERTILIZER_DATABASE.values()])))

def get_brands():
    """Get unique brands"""
    return sorted(list(set([v["brand"] for v in FERTILIZER_DATABASE.values()])))

def filter_fertilizers(category=None, brand=None, search_term=None, price_range=None):
    """Filter fertilizers based on criteria"""
    filtered = {}
    
    for name, data in FERTILIZER_DATABASE.items():
        # Category filter
        if category and category != "Semua" and data["category"] != category:
            continue
        
        # Brand filter
        if brand and brand != "Semua" and data["brand"] != brand:
            continue
        
        # Search filter
        if search_term:
            search_lower = search_term.lower()
            if not (search_lower in name.lower() or 
                   search_lower in data["description"].lower() or
                   search_lower in data["usage"].lower()):
                continue
        
        # Price filter
        if price_range:
            if not (price_range[0] <= data["price_per_kg"] <= price_range[1]):
                continue
        
        filtered[name] = data
    
    return filtered

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
        text-align: center;
        margin-bottom: 1rem;
    }
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .product-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: #10b981;
    }
    .product-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    .product-brand {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    .product-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #dc2626;
        margin: 1rem 0;
    }
    .formula-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .category-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<h1 class="main-header">🧪 Katalog Pupuk & Harga</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Referensi harga pupuk terkini dari berbagai produsen terpercaya di Indonesia</p>', unsafe_allow_html=True)

# ========== SIDEBAR FILTERS ==========

# Calculate totals for sidebar stats
total_products = len(FERTILIZER_DATABASE)
total_pests = len(PESTICIDE_DATABASE_COMMERCIAL)

with st.sidebar:
    st.markdown("### 🔍 Filter & Pencarian")
    
    # Search
    search_term = st.text_input("🔎 Cari Pupuk", placeholder="Nama, deskripsi, atau penggunaan...")
    
    # Category filter
    categories = ["Semua"] + get_categories()
    selected_category = st.selectbox("Kategori", categories)
    
    # Brand filter
    brands = ["Semua"] + get_brands()
    selected_brand = st.selectbox("Produsen", brands)
    
    # Price range
    st.markdown("**Range Harga (Rp/kg atau unit):**")
    price_range = st.slider(
        "Pilih range harga",
        min_value=0,
        max_value=250000,
        value=(0, 250000),
        step=500,
        format="Rp %d"
    )
    
    # Sort by
    sort_by = st.selectbox(
        "Urutkan Berdasarkan",
        ["Nama (A-Z)", "Nama (Z-A)", "Harga (Termurah)", "Harga (Termahal)", "Kandungan N", "Kandungan P", "Kandungan K"]
    )
    
    st.metric("Total Produk", total_products)
    
    st.markdown("---")
    st.markdown("### 💰 Update Harga Reference")
    st.caption("Ubah harga untuk acuan perhitungan terkini")
    
    # Fertilizer Price Update
    with st.expander("📦 Edit Harga Pupuk"):
        prod_to_edit = st.selectbox("Pilih Pupuk:", sorted(list(st.session_state.fertilizer_db.keys())), key="edit_fert_select")
        current_price = st.session_state.fertilizer_db[prod_to_edit]['price_per_kg']
        new_price = st.number_input("Harga Baru (Rp/kg):", value=float(current_price), step=100.0, key="new_fert_price")
        if st.button("Update Harga Pupuk"):
            st.session_state.fertilizer_db[prod_to_edit]['price_per_kg'] = int(new_price)
            st.success(f"Harga {prod_to_edit} diperbarui!")
            st.rerun()

    # Pesticide Price Update
    with st.expander("💊 Edit Harga Pestisida"):
        pest_to_edit = st.selectbox("Pilih Pestisida:", sorted(list(st.session_state.pesticide_db.keys())), key="edit_pest_select")
        curr_pest_price = st.session_state.pesticide_db[pest_to_edit]['price']
        new_pest_price = st.number_input("Harga Baru (Rp):", value=float(curr_pest_price), step=500.0, key="new_pest_price")
        if st.button("Update Harga Pestisida"):
            st.session_state.pesticide_db[pest_to_edit]['price'] = int(new_pest_price)
            st.success(f"Harga {pest_to_edit} diperbarui!")
            st.rerun()

    if st.button("🔄 Reset ke Harga Default", type="secondary"):
        st.session_state.fertilizer_db = FERTILIZER_DATABASE_DEFAULT.copy()
        st.session_state.pesticide_db = PESTICIDE_DATABASE_DEFAULT.copy()
        st.success("Harga telah dikembalikan ke default.")
        st.rerun()
    
    st.markdown("---")
    st.caption(f"🛡️ AgriSensa Fertilizer DB v{DB_VERSION}")
    st.caption("Data diperbarui otomatis jika ada versi baru.")

# ========== MAIN CONTENT ==========

# Apply filters
filtered_fertilizers = filter_fertilizers(
    category=selected_category if selected_category != "Semua" else None,
    brand=selected_brand if selected_brand != "Semua" else None,
    search_term=search_term if search_term else None,
    price_range=price_range
)

# Sort
if sort_by == "Nama (A-Z)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items()))
elif sort_by == "Nama (Z-A)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), reverse=True))
elif sort_by == "Harga (Termurah)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["price_per_kg"]))
elif sort_by == "Harga (Termahal)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["price_per_kg"], reverse=True))
elif sort_by == "Kandungan N":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["n_content"], reverse=True))
elif sort_by == "Kandungan P":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["p_content"], reverse=True))
elif sort_by == "Kandungan K":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["k_content"], reverse=True))

# Display results
st.markdown(f"### Menampilkan {len(filtered_fertilizers)} produk")

if len(filtered_fertilizers) == 0:
    st.warning("Tidak ada produk yang sesuai dengan filter Anda. Coba ubah kriteria pencarian.")
else:
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Katalog Pupuk", "💊 Pestisida & Obat", "📊 Perbandingan Harga", "📚 Panduan Pemupukan"])
    
    # TAB 1: PRODUCT CATALOG (FERTILIZER)
    with tab1:
        # Display products in grid
        cols_per_row = 2
        products_list = list(filtered_fertilizers.items())
        
        for i in range(0, len(products_list), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j in range(cols_per_row):
                if i + j < len(products_list):
                    name, data = products_list[i + j]
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class="product-card">
                            <div class="product-name">{name}</div>
                            <div class="product-brand">📍 {data['brand']}</div>
                            <div>
                                <span class="category-badge">{data['category']}</span>
                                <span class="formula-badge">{data['formula']}</span>
                            </div>
                            <div class="product-price">Rp {data['price_per_kg']:,}/kg</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📋 Detail Produk"):
                            st.markdown(f"**Deskripsi:** {data['description']}")
                            st.markdown(f"**Kandungan:**")
                            st.markdown(f"- N: {data['n_content']}%")
                            st.markdown(f"- P₂O₅: {data['p_content']}%")
                            st.markdown(f"- K₂O: {data['k_content']}%")
                            st.markdown(f"**Penggunaan:** {data['usage']}")
                            st.markdown(f"**Dosis:** {data['dosage']}")
                            st.markdown(f"**Aplikasi:** {data['application']}")
                            st.markdown(f"**Kemasan:** {', '.join(data['package_sizes'])}")
    
    # TAB 2: PESTICIDE CATALOG (NEW)
    with tab2:
        st.markdown("### 💊 Katalog Pestisida (Insektisida, Fungisida, dll)")
        
        # Grid layout for pesticides
        pest_cols_per_row = 2
        pesticide_list = list(PESTICIDE_DATABASE_COMMERCIAL.items())
        
        # Optional: Add filters specific to pesticides if needed, now showing all
        
        for i in range(0, len(pesticide_list), pest_cols_per_row):
            cols = st.columns(pest_cols_per_row)
            for j in range(pest_cols_per_row):
                if i + j < len(pesticide_list):
                    name, data = pesticide_list[i + j]
                    
                    with cols[j]:
                         # Color code per category
                        cat_color = "#ef4444" # red default
                        cat_bg = "#fee2e2"
                        if "Fungisida" in data['category']:
                            cat_color = "#3b82f6" # blue
                            cat_bg = "#dbeafe"
                        elif "Herbisida" in data['category']:
                             cat_color = "#854d0e" # brown
                             cat_bg = "#fef9c3"
                             
                        st.markdown(f"""
                        <div class="product-card">
                            <div style="display:flex; justify-content:space-between; align-items:start;">
                                <div class="product-name">{name}</div>
                                <span style="background:{cat_bg}; color:{cat_color}; padding: 0.2rem 0.6rem; border-radius:10px; font-size:0.8rem; font-weight:bold;">{data['category']}</span>
                            </div>
                            <div class="product-brand">🏭 {data['brand']} | 🧪 {data['active_ingredient']}</div>
                            <div class="product-desc" style="font-size:0.9rem; color:#4b5563; margin:0.5rem 0;" >{data['description']}</div>
                            <hr style="margin:0.5rem 0;">
                            <div>
                                <div style="font-size:0.85rem;">🐛 <b>Target:</b> {', '.join(data['target_pests'][:4])}</div>
                            </div>
                            <div class="product-price">Rp {data['price']:,} <span style="font-size:0.9rem; color:#6b7280; font-weight:normal;">/ {data['unit']}</span></div>
                             <button style="background-color:#10b981; color:white; border:none; padding:0.5rem 1rem; border-radius:5px; cursor:pointer; width:100%;">🛒 Cek Ketersediaan</button>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander(f"📖 Dosis & Cara Pakai {name}"):
                            st.info(f"**Dosis:** {data['dosage']}")
                            st.write(f"**Tanaman:** {data['usage']}")
                            st.caption("*Baca label kemasan sebelum menggunakan.*")
                            
    # TAB 3: PRICE COMPARISON
    with tab3:
        st.markdown("### 💰 Perbandingan Harga")
        
        # Create comparison table
        comparison_data = []
        for name, data in filtered_fertilizers.items():
            comparison_data.append({
                "Nama Produk": name,
                "Kategori": data["category"],
                "Produsen": data["brand"],
                "Formula": data["formula"],
                "N (%)": data["n_content"],
                "P (%)": data["p_content"],
                "K (%)": data["k_content"],
                "Harga/kg": f"Rp {data['price_per_kg']:,}"
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Price chart by category
        st.markdown("### 📊 Grafik Harga per Kategori")
        
        category_prices = {}
        for name, data in filtered_fertilizers.items():
            cat = data["category"]
            if cat not in category_prices:
                category_prices[cat] = []
            category_prices[cat].append(data["price_per_kg"])
        
        chart_data = []
        for cat, prices in category_prices.items():
            chart_data.append({
                "Kategori": cat,
                "Harga Rata-rata": sum(prices) / len(prices),
                "Harga Terendah": min(prices),
                "Harga Tertinggi": max(prices)
            })
        
        df_chart = pd.DataFrame(chart_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Rata-rata',
            x=df_chart['Kategori'],
            y=df_chart['Harga Rata-rata'],
            marker_color='#10b981'
        ))
        fig.add_trace(go.Bar(
            name='Terendah',
            x=df_chart['Kategori'],
            y=df_chart['Harga Terendah'],
            marker_color='#3b82f6'
        ))
        fig.add_trace(go.Bar(
            name='Tertinggi',
            x=df_chart['Kategori'],
            y=df_chart['Harga Tertinggi'],
            marker_color='#ef4444'
        ))
        
        fig.update_layout(
            title="Perbandingan Harga Pupuk per Kategori",
            xaxis_title="Kategori",
            yaxis_title="Harga (Rp/kg)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: GUIDES
    with tab4:
        st.header("📚 Panduan Singkat")
        col1, col2 = st.columns(2)
        with col1:
             st.markdown("""
             **Tips Membeli Pupuk:**
             1. **Cek Nomor Pendaftaran:** Pastikan pupuk memiliki nomor pendaftaran Kementan RI.
             2. **Kemasan:** Cek kondisi kemasan, jahitan karung asli biasanya rapi dan ada logo produsen.
             3. **Bentuk Fisik:** Kenali warna dan bentuk butiran pupuk asli. Urea biasanya prill/granul putih/pink (subsidi).
             """)
        with col2:
             st.markdown("""
             **Tips Membeli Pestisida:**
             1. **Kenali Masalahnya:** Jangan beli insektisida untuk penyakit jamur!
             2. **Rotasi Bahan Aktif:** Jangan gunakan produk yang sama terus menerus untuk menghindari resistensi.
             3. **Perhatikan Warna Label:** Hijau (Aman), Biru (Cukup Aman), Kuning (Berbahaya), Merah (Sangat Berbahaya).
             """)
        st.markdown("### 📚 Panduan Pemupukan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🌾 Pupuk untuk Padi
            
            **Rekomendasi:**
            - **Dasar:** Urea 200 kg + SP-36 100 kg + KCl 100 kg
            - **Alternatif:** NPK Phonska 300 kg + Urea 100 kg
            - **Organik:** Petroganik 500 kg (saat olah tanah)
            
            **Waktu Aplikasi:**
            1. Saat tanam: SP-36 + 1/3 Urea + 1/2 KCl
            2. 21 HST: 1/3 Urea + 1/2 KCl
            3. 42 HST: 1/3 Urea
            
            ---
            
            #### 🌽 Pupuk untuk Jagung
            
            **Rekomendasi:**
            - **Dasar:** Urea 300 kg + SP-36 150 kg + KCl 100 kg
            - **Alternatif:** NPK 16-16-16 350 kg + Urea 150 kg
            
            **Waktu Aplikasi:**
            1. Saat tanam: SP-36 + 1/3 Urea + KCl
            2. 21 HST: 1/3 Urea
            3. 42 HST: 1/3 Urea
            
            ---
            
            #### 🌶️ Pupuk untuk Cabai
            
            **Rekomendasi:**
            - **Dasar:** Urea 200 kg + SP-36 200 kg + KCl 250 kg
            - **Alternatif:** NPK Grower 15-9-20 400 kg
            - **Daun:** Gandasil B 2 kg/ha (semprot)
            
            **Waktu Aplikasi:**
            - Setiap 2 minggu sekali
            - Fokus K tinggi saat berbuah
            """)
        
        with col2:
            st.markdown("""
            #### 🍅 Pupuk untuk Tomat
            
            **Rekomendasi:**
            - **Dasar:** Urea 150 kg + SP-36 200 kg + KCl 200 kg
            - **Alternatif:** NPK 15-15-15 300 kg + KCl 100 kg
            - **Daun:** Gandasil B 2 kg/ha
            
            **Waktu Aplikasi:**
            - Setiap 2 minggu sekali
            - Tingkatkan K saat berbuah
            
            ---
            
            #### 🥬 Pupuk untuk Sayuran Daun
            
            **Rekomendasi:**
            - **Dasar:** Urea 150 kg + NPK 15-15-15 200 kg
            - **Organik:** Kompos 5 ton/ha
            - **Daun:** Gandasil D 2 kg/ha
            
            **Waktu Aplikasi:**
            - Setiap 1-2 minggu
            - Fokus N tinggi untuk daun
            
            ---
            
            #### 💡 Tips Pemupukan
            
            1. **Waktu Aplikasi:**
               - Pagi (06:00-09:00) atau sore (15:00-18:00)
               - Hindari saat hujan atau panas terik
            
            2. **Cara Aplikasi:**
               - Tabur: Jarak 5-10 cm dari batang
               - Kocor: Larutkan dalam air
               - Semprot: Pagi/sore, hindari matahari terik
            
            3. **Penyimpanan:**
               - Tempat kering dan teduh
               - Tutup rapat setelah digunakan
               - Jauhkan dari jangkauan anak-anak
            """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("""
🧪 **Katalog Pupuk & Harga v1.0**

💡 **Catatan**: Harga dapat berubah sewaktu-waktu tergantung lokasi dan distributor. 
Gunakan sebagai referensi dan konfirmasi harga dengan toko pertanian terdekat.

📊 **Sumber**: PT Pupuk Indonesia, Petrokimia Gresik, dan berbagai distributor resmi

⚠️ **Disclaimer**: Selalu ikuti petunjuk penggunaan pada kemasan. Konsultasikan dengan penyuluh pertanian untuk rekomendasi spesifik.
""")
