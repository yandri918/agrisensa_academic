# Pusat Pengetahuan Pertanian
# Ensiklopedia lengkap nutrisi tanaman, pupuk, dan pengendalian hama alami
# Version: 1.0.1 (Bug Fix)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Pusat Pengetahuan", page_icon="📚", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== KNOWLEDGE DATABASE ==========

# PUPUK MAKRO
PUPUK_MAKRO = {
    "Urea (46% N)": {
        "kandungan": {"N": 46, "P": 0, "K": 0},
        "fungsi": "Pertumbuhan vegetatif (daun, batang)",
        "dosis": "200-300 kg/ha untuk padi, 250-350 kg/ha untuk jagung",
        "cara_aplikasi": "Tabur/kocor, 2-3 kali aplikasi",
        "waktu_aplikasi": "7-10 HST, 21-25 HST, 35-40 HST",
        "kelebihan": ["Kadar N tinggi", "Mudah larut", "Harga terjangkau"],
        "kekurangan": ["Mudah menguap", "Perlu aplikasi bertahap", "Dapat menurunkan pH tanah"],
        "tips": "Aplikasi pagi/sore, hindari siang hari. Campur dengan tanah untuk mengurangi penguapan."
    },
    "ZA (21% N, 24% S)": {
        "kandungan": {"N": 21, "P": 0, "K": 0, "S": 24},
        "fungsi": "Pertumbuhan + tambahan Sulfur",
        "dosis": "100-200 kg/ha",
        "cara_aplikasi": "Tabur/kocor",
        "waktu_aplikasi": "Fase vegetatif",
        "kelebihan": ["Mengandung S", "Tidak mudah menguap", "Cocok untuk tanah alkalin"],
        "kekurangan": ["Kadar N lebih rendah", "Dapat menurunkan pH"],
        "tips": "Baik untuk tanaman yang butuh sulfur (bawang, kubis)"
    },
    "SP-36 (36% P2O5)": {
        "kandungan": {"N": 0, "P": 36, "K": 0},
        "fungsi": "Pertumbuhan akar, bunga, buah",
        "dosis": "100-150 kg/ha",
        "cara_aplikasi": "Tabur saat tanam, kocor saat berbunga",
        "waktu_aplikasi": "Saat tanam + fase generatif",
        "kelebihan": ["Kadar P tinggi", "Efek jangka panjang", "Merangsang pembungaan"],
        "kekurangan": ["Tidak larut air", "Perlu waktu untuk tersedia"],
        "tips": "Aplikasi saat tanam untuk hasil maksimal. Campur dengan pupuk kandang."
    },
    "TSP (46% P2O5)": {
        "kandungan": {"N": 0, "P": 46, "K": 0},
        "fungsi": "Pertumbuhan akar dan buah",
        "dosis": "75-125 kg/ha",
        "cara_aplikasi": "Tabur saat tanam",
        "waktu_aplikasi": "Saat tanam",
        "kelebihan": ["Kadar P sangat tinggi", "Efisien"],
        "kekurangan": ["Harga lebih mahal", "Tidak larut air"],
        "tips": "Lebih efisien dari SP-36, cocok untuk lahan intensif"
    },
    "KCl (60% K2O)": {
        "kandungan": {"N": 0, "P": 0, "K": 60},
        "fungsi": "Kualitas hasil, ketahanan penyakit",
        "dosis": "100-200 kg/ha",
        "cara_aplikasi": "Tabur/kocor",
        "waktu_aplikasi": "Fase generatif",
        "kelebihan": ["Kadar K tinggi", "Mudah larut", "Meningkatkan kualitas"],
        "kekurangan": ["Mengandung Cl (tidak cocok untuk tembakau)"],
        "tips": "Aplikasi saat pembentukan buah untuk kualitas optimal"
    },
    "NPK 15-15-15": {
        "kandungan": {"N": 15, "P": 15, "K": 15},
        "fungsi": "Nutrisi seimbang untuk semua fase",
        "dosis": "200-400 kg/ha",
        "cara_aplikasi": "Tabur/kocor, 2-3 kali",
        "waktu_aplikasi": "Sepanjang musim tanam",
        "kelebihan": ["Praktis", "Seimbang", "Cocok untuk semua tanaman"],
        "kekurangan": ["Kurang spesifik", "Harga lebih mahal"],
        "tips": "Cocok untuk petani pemula, aplikasi mudah"
    },
    "NPK 16-16-16 (Phonska)": {
        "kandungan": {"N": 16, "P": 16, "K": 16},
        "fungsi": "Nutrisi lengkap untuk tanaman pangan",
        "dosis": "250-350 kg/ha",
        "cara_aplikasi": "Tabur, 2-3 kali",
        "waktu_aplikasi": "10 HST, 25 HST, 40 HST",
        "kelebihan": ["Subsidi pemerintah", "Lengkap", "Terjangkau"],
        "kekurangan": ["Stok terbatas", "Perlu kartu tani"],
        "tips": "Pupuk subsidi terbaik untuk padi dan palawija"
    }
}

# PUPUK MAKRO SEKUNDER (Ca, Mg, S)
PUPUK_MAKRO_SEKUNDER = {
    # MAGNESIUM (Mg)
    "Kieserite (MgSO₄)": {
        "kandungan": {"Mg": 27, "S": 22},
        "fungsi": "Sintesis klorofil, fotosintesis, aktivasi enzim",
        "defisiensi": "Klorosis interveinal pada daun tua, daun kemerahan/keunguan",
        "dosis": "50-100 kg/ha",
        "cara_aplikasi": "Tabur/kocor saat defisiensi Mg terdeteksi",
        "waktu_aplikasi": "Fase vegetatif atau saat gejala defisiensi muncul",
        "tanaman_peka": ["Sawit", "Kakao", "Karet", "Sayuran", "Buah"],
        "kelebihan": ["Kandungan Mg tinggi", "Bonus Sulfur", "Efek cepat"],
        "kekurangan": ["Harga relatif mahal", "Perlu import"],
        "tips": "Sangat penting untuk tanaman perkebunan di tanah masam"
    },
    "Magnesium Sulfat (Epsom Salt)": {
        "kandungan": {"Mg": 10, "S": 13},
        "fungsi": "Koreksi defisiensi Mg cepat, pembentukan klorofil",
        "defisiensi": "Daun kuning, pertumbuhan terhambat",
        "dosis": "20-50 kg/ha atau 2-5 g/L (semprot daun)",
        "cara_aplikasi": "Kocor/semprot daun",
        "waktu_aplikasi": "Saat gejala defisiensi muncul",
        "tanaman_peka": ["Sayuran", "Buah", "Tanaman hias", "Tomat", "Cabai"],
        "kelebihan": ["Larut air sempurna", "Efek sangat cepat", "Bisa semprot daun"],
        "kekurangan": ["Harga lebih mahal", "Efek tidak tahan lama"],
        "tips": "Ideal untuk koreksi cepat defisiensi Mg via semprot daun"
    },
    
    # KALSIUM (Ca)
    "Dolomit [CaMg(CO₃)₂]": {
        "kandungan": {"Ca": "18-22", "Mg": "10-13"},
        "fungsi": "Menaikkan pH tanah, sumber Ca dan Mg, memperbaiki struktur tanah",
        "defisiensi": "Ujung daun mati (tip burn), buah busuk ujung (blossom end rot)",
        "dosis": "500-2000 kg/ha (tergantung pH tanah)",
        "cara_aplikasi": "Tabur saat pengolahan tanah, 2-4 minggu sebelum tanam",
        "waktu_aplikasi": "Saat olah tanah, sebelum musim tanam",
        "tanaman_peka": ["Semua tanaman di tanah masam (pH <5.5)"],
        "kelebihan": ["Murah", "Bonus Ca+Mg", "Efek jangka panjang", "Memperbaiki struktur"],
        "kekurangan": ["Efek lambat (2-3 bulan)", "Perlu aplikasi rutin"],
        "tips": "Wajib untuk tanah masam! Aplikasi 2-4 minggu sebelum tanam"
    },
    "Kapur Pertanian (CaCO₃)": {
        "kandungan": {"Ca": "32-40"},
        "fungsi": "Menaikkan pH tanah, sumber kalsium",
        "defisiensi": "Pertumbuhan akar lemah, buah mudah busuk",
        "dosis": "500-2000 kg/ha",
        "cara_aplikasi": "Tabur saat pengolahan tanah",
        "waktu_aplikasi": "2-4 minggu sebelum tanam",
        "tanaman_peka": ["Semua tanaman di tanah masam (pH <5.5)"],
        "kelebihan": ["Sangat murah", "Mudah didapat", "Efek jangka panjang"],
        "kekurangan": ["Tidak mengandung Mg", "Efek lambat"],
        "tips": "Pilihan ekonomis untuk menaikkan pH tanah masam"
    },
    "Gypsum (CaSO₄·2H₂O)": {
        "kandungan": {"Ca": 23, "S": 18},
        "fungsi": "Sumber Ca+S untuk tanah alkalin, memperbaiki tanah sodic",
        "defisiensi": "Buah busuk ujung, akar lemah",
        "dosis": "200-500 kg/ha",
        "cara_aplikasi": "Tabur, cocok untuk tanah pH tinggi atau tanah sodic",
        "waktu_aplikasi": "Saat olah tanah",
        "tanaman_peka": ["Kacang tanah", "Sayuran", "Buah"],
        "kelebihan": ["Tidak menaikkan pH", "Cocok tanah alkalin", "Bonus Sulfur"],
        "kekurangan": ["Lebih mahal dari kapur", "Efek lebih lambat"],
        "tips": "Pilihan terbaik untuk tanah alkalin (pH >7) atau tanah sodic"
    },
    "Kalsium Nitrat [Ca(NO₃)₂]": {
        "kandungan": {"Ca": 19, "N": 15.5},
        "fungsi": "Sumber Ca dan N cepat tersedia, untuk fertigasi/hidroponik",
        "defisiensi": "Blossom end rot pada tomat, tip burn pada selada",
        "dosis": "100-200 kg/ha atau 1-2 g/L (fertigasi)",
        "cara_aplikasi": "Kocor/fertigasi, larut air sempurna",
        "waktu_aplikasi": "Sepanjang musim tanam (fertigasi)",
        "tanaman_peka": ["Tomat", "Cabai", "Selada", "Sayuran hidroponik"],
        "kelebihan": ["Larut air sempurna", "Efek sangat cepat", "Bonus N", "Ideal hidroponik"],
        "kekurangan": ["Harga mahal", "Perlu aplikasi rutin"],
        "tips": "Wajib untuk hidroponik dan mencegah blossom end rot!"
    },
    "Kalsium Klorida (CaCl₂)": {
        "kandungan": {"Ca": 36},
        "fungsi": "Koreksi defisiensi Ca cepat via semprot daun",
        "defisiensi": "Blossom end rot, bitter pit pada apel",
        "dosis": "2-5 g/L (semprot daun)",
        "cara_aplikasi": "Semprot daun, terutama saat pembentukan buah",
        "waktu_aplikasi": "Fase generatif, saat buah berkembang",
        "tanaman_peka": ["Tomat", "Cabai", "Apel", "Sayuran buah"],
        "kelebihan": ["Efek sangat cepat", "Semprot daun efektif", "Mencegah blossom end rot"],
        "kekurangan": ["Mengandung Cl (tidak untuk semua tanaman)", "Harga mahal"],
        "tips": "Semprot rutin saat pembentukan buah untuk cegah blossom end rot"
    },
    
    # SULFUR (S)
    "Sulfur Bentonit": {
        "kandungan": {"S": 90},
        "fungsi": "Menurunkan pH tanah alkalin (slow-release), sumber Sulfur",
        "defisiensi": "Daun muda kuning, pertumbuhan terhambat",
        "dosis": "100-300 kg/ha",
        "cara_aplikasi": "Tabur, efek bertahap 3-6 bulan",
        "waktu_aplikasi": "Saat olah tanah, 2-3 bulan sebelum tanam",
        "tanaman_peka": ["Sawit", "Karet", "Teh", "Tanaman asam-loving"],
        "kelebihan": ["Efek jangka panjang", "Menurunkan pH bertahap", "Aman"],
        "kekurangan": ["Efek lambat", "Perlu waktu 3-6 bulan"],
        "tips": "Ideal untuk menurunkan pH tanah alkalin secara bertahap"
    },
    "Sulfur Powder (Belerang)": {
        "kandungan": {"S": 99},
        "fungsi": "Menurunkan pH tanah, fungisida untuk embun tepung",
        "defisiensi": "Daun pucat, pertumbuhan lambat",
        "dosis": "50-200 kg/ha (tanah) atau 3-5 g/L (semprot)",
        "cara_aplikasi": "Tabur/semprot",
        "waktu_aplikasi": "Saat olah tanah atau saat serangan jamur",
        "tanaman_peka": ["Tanah alkalin", "Tanaman dengan embun tepung"],
        "kelebihan": ["Murni", "Fungisida alami", "Menurunkan pH"],
        "kekurangan": ["Efek lambat untuk pH", "Bisa fitotoksik jika berlebihan"],
        "tips": "Dosis 3-5 g/L efektif untuk embun tepung (powdery mildew)"
    },
    "Amonium Tiosulfat (ATS)": {
        "kandungan": {"N": 12, "S": 26},
        "fungsi": "Sumber N dan S cepat tersedia untuk fertigasi",
        "defisiensi": "Daun kuning, pertumbuhan terhambat",
        "dosis": "50-100 L/ha (diencerkan)",
        "cara_aplikasi": "Fertigasi, larut air sempurna",
        "waktu_aplikasi": "Sepanjang musim tanam (fertigasi)",
        "tanaman_peka": ["Jagung", "Gandum", "Sayuran (fertigasi)"],
        "kelebihan": ["Cair, mudah aplikasi", "Bonus N", "Efek cepat"],
        "kekurangan": ["Harga mahal", "Perlu sistem fertigasi"],
        "tips": "Ideal untuk sistem fertigasi modern"
    },
    
    # KOMBINASI Ca+Mg
    "CalMag (Ca+Mg kompleks)": {
        "kandungan": {"Ca": 15, "Mg": 3},
        "fungsi": "Sumber Ca dan Mg untuk hidroponik dan fertigasi",
        "defisiensi": "Blossom end rot, klorosis interveinal",
        "dosis": "1-3 g/L (fertigasi/hidroponik)",
        "cara_aplikasi": "Kocor/fertigasi, larut air sempurna",
        "waktu_aplikasi": "Sepanjang musim tanam",
        "tanaman_peka": ["Hidroponik", "Sayuran", "Buah"],
        "kelebihan": ["Larut sempurna", "Kombinasi ideal Ca+Mg", "Cocok hidroponik"],
        "kekurangan": ["Harga mahal", "Perlu aplikasi rutin"],
        "tips": "Wajib untuk sistem hidroponik! Cegah defisiensi Ca dan Mg"
    }
}

# PUPUK MIKRO
PUPUK_MIKRO = {
    "Boron (B)": {
        "fungsi": "Pembentukan bunga, buah, dan biji",
        "defisiensi": "Bunga rontok, buah kecil, pertumbuhan terhambat",
        "sumber": "Borax, Asam borat",
        "dosis": "0.5-1 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Kubis", "Brokoli", "Apel", "Anggur"],
        "tips": "Sangat penting untuk tanaman buah dan sayuran"
    },
    "Zinc (Zn)": {
        "fungsi": "Pembentukan klorofil, hormon pertumbuhan",
        "defisiensi": "Daun kecil, klorosis, pertumbuhan kerdil",
        "sumber": "ZnSO4 (Zinc Sulfat)",
        "dosis": "5-10 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Padi", "Jagung", "Kedelai"],
        "tips": "Penting untuk tanah alkalin dan berpasir"
    },
    "Mangan (Mn)": {
        "fungsi": "Fotosintesis, metabolisme nitrogen",
        "defisiensi": "Klorosis interveinal, bercak nekrotik",
        "sumber": "MnSO4 (Mangan Sulfat)",
        "dosis": "2-5 kg/ha atau 1-2 g/L (semprot)",
        "tanaman_peka": ["Kedelai", "Gandum", "Kentang"],
        "tips": "Defisiensi umum pada tanah alkalin"
    },
    "Tembaga (Cu)": {
        "fungsi": "Fotosintesis, pembentukan protein",
        "defisiensi": "Daun layu, ujung daun mati",
        "sumber": "CuSO4 (Tembaga Sulfat)",
        "dosis": "2-5 kg/ha atau 0.5-1 g/L (semprot)",
        "tanaman_peka": ["Jeruk", "Tomat", "Gandum"],
        "tips": "Hati-hati overdosis, bersifat toksik"
    },
    "Besi (Fe)": {
        "fungsi": "Pembentukan klorofil",
        "defisiensi": "Klorosis pada daun muda",
        "sumber": "FeSO4, Fe-EDTA",
        "dosis": "5-10 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Padi", "Kedelai", "Buah-buahan"],
        "tips": "Gunakan Fe-EDTA untuk tanah alkalin"
    },
    "Molibdenum (Mo)": {
        "fungsi": "Fiksasi nitrogen, metabolisme N",
        "defisiensi": "Daun kuning, pertumbuhan terhambat",
        "sumber": "Sodium molybdate",
        "dosis": "0.1-0.5 kg/ha",
        "tanaman_peka": ["Kedelai", "Kacang-kacangan", "Kubis"],
        "tips": "Penting untuk legum dan tanah asam"
    }
}

# PUPUK ORGANIK & HAYATI
PUPUK_ORGANIK = {
    "Kompos": {
        "kandungan": "N: 1-2%, P: 0.5-1%, K: 1-2%, C-Organik: 15-25%",
        "fungsi": "Memperbaiki struktur tanah, meningkatkan mikroba",
        "dosis": "5-10 ton/ha",
        "cara_buat": [
            "1. Kumpulkan bahan organik (jerami, daun, kotoran)",
            "2. Cacah bahan ukuran 2-5 cm",
            "3. Susun berlapis, siram EM4/MOL",
            "4. Tutup dengan terpal, balik setiap minggu",
            "5. Matang 4-6 minggu (warna hitam, tidak bau)"
        ],
        "kelebihan": ["Murah", "Ramah lingkungan", "Memperbaiki tanah jangka panjang"],
        "tips": "Campurkan berbagai bahan untuk kompos berkualitas"
    },
    "Pupuk Kandang": {
        "jenis": {
            "Ayam": "N: 3%, P: 2%, K: 1.5% (paling kaya nutrisi)",
            "Sapi": "N: 2%, P: 1%, K: 1.5% (paling aman)",
            "Kambing": "N: 2.5%, P: 1.5%, K: 2% (cocok untuk sayuran)"
        },
        "dosis": "10-20 ton/ha",
        "cara_aplikasi": "Fermentasi 2-4 minggu, tabur saat olah tanah",
        "kelebihan": ["Nutrisi lengkap", "Memperbaiki struktur tanah"],
        "tips": "Harus difermentasi dulu, jangan gunakan segar!"
    },
    "Kascing (Vermikompos)": {
        "kandungan": "N: 2%, P: 1.5%, K: 1.5%, Hormon pertumbuhan",
        "fungsi": "Nutrisi + hormon + mikroba menguntungkan",
        "dosis": "2-5 ton/ha",
        "cara_buat": [
            "1. Siapkan cacing tanah (Lumbricus rubellus)",
            "2. Buat media dari kotoran ternak + jerami",
            "3. Masukkan cacing, tutup dengan karung basah",
            "4. Siram setiap 2 hari",
            "5. Panen setelah 1-2 bulan"
        ],
        "kelebihan": ["Kualitas tinggi", "Mengandung hormon", "Mikroba aktif"],
        "tips": "Kascing adalah pupuk organik terbaik!"
    },
    "Biochar (Arang Hayati)": {
        "fungsi": "Meningkatkan retensi air dan nutrisi, rumah bagi mikroba tanah yang menguntungkan, serta membantu memperbaiki pH tanah.",
        "dosis": "1-3 ton/ha (atau 10% dari volume media tanam)",
        "cara_buat": [
            "Proses pirolisis (pembakaran biomassa kering seperti sekam padi, tongkol jagung, atau kayu dengan oksigen terbatas atau tanpa oksigen)."
        ],
        "kelebihan": [
            "Efek jangka panjang (>100 tahun) di dalam tanah", 
            "Sekuestrasi Karbon (mengunci karbon agar tidak lepas ke atmosfer)", 
            "Sangat efektif mengurangi pencucian (leaching) pupuk kimia"
        ],
        "kekurangan": [
            "Butuh proses aktivasi/loading nutrisi sebelum diaplikasikan",
            "Sifatnya basa kuat, perlu diperhatikan untuk tanah yang sudah alkali"
        ],
        "cara_aplikasi": "Dibenamkan ke tanah saat pengolahan lahan atau dicampur ke lubang tanam.",
        "tips": "**Penting:** Lakukan 'Aktivasi' dengan merendam Biochar dalam pupuk cair/POC selama 1-2 minggu sebelum diaplikasikan agar pori-porinya terisi nutrisi dan tidak 'menyedot' hara dari tanaman saat baru ditanam."
    },
    "Pupuk Hijau": {
        "tanaman": ["Kacang-kacangan", "Orok-orok", "Mucuna"],
        "fungsi": "Fiksasi N, biomassa organik",
        "cara_aplikasi": "Tanam → Potong saat berbunga → Benamkan ke tanah",
        "kelebihan": ["Gratis", "Fiksasi N alami", "Memperbaiki tanah"],
        "tips": "Ideal untuk rotasi tanaman"
    }
}

# POC, MOL & ZPT
POC_MOL_ZPT = {
    "POC (Pupuk Organik Cair)": {
        "bahan": "Kotoran ternak, urine, daun-daunan",
        "cara_buat": [
            "1. Campurkan kotoran + air (1:3)",
            "2. Tambahkan gula merah 1 kg/20L",
            "3. Tambahkan EM4 atau MOL",
            "4. Tutup rapat, buka setiap 3 hari",
            "5. Fermentasi 14 hari"
        ],
        "dosis": "5-10 L/ha (diencerkan 1:10)",
        "aplikasi": "Semprot daun atau kocor",
        "kelebihan": ["Cepat diserap", "Mudah dibuat", "Murah"],
        "tips": "Aplikasi pagi/sore untuk hasil maksimal"
    },
    "MOL (Mikroorganisme Lokal)": {
        "jenis": {
            "MOL Bonggol Pisang": {
                "bahan": "Bonggol pisang, gula merah, air",
                "fungsi": "Hormon pertumbuhan (auksin, giberelin)",
                "cara": "Cacah bonggol + gula + air, fermentasi 7-14 hari"
            },
            "MOL Rebung Bambu": {
                "bahan": "Rebung bambu, gula merah, air",
                "fungsi": "Pertumbuhan tunas dan akar",
                "cara": "Cacah rebung + gula + air, fermentasi 7 hari"
            },
            "MOL Buah-buahan": {
                "bahan": "Buah busuk, gula, air",
                "fungsi": "Mikroba pengurai, nutrisi",
                "cara": "Hancurkan buah + gula + air, fermentasi 14 hari"
            }
        },
        "dosis": "100-200 ml/L air",
        "aplikasi": "Semprot/kocor setiap 7-10 hari",
        "tips": "MOL bonggol pisang terbaik untuk pertumbuhan!"
    },
    "ZPT Alami (Zat Pengatur Tumbuh)": {
        "Air Kelapa": {
            "kandungan": "Sitokinin, auksin, giberelin",
            "fungsi": "Pertumbuhan akar, tunas, buah",
            "dosis": "100-200 ml/L air",
            "aplikasi": "Rendam benih, semprot tanaman muda"
        },
        "Bawang Merah": {
            "kandungan": "Auksin, vitamin B1",
            "fungsi": "Perakaran kuat",
            "cara": "Haluskan 250g bawang + 1L air, saring",
            "aplikasi": "Rendam stek/benih 30 menit"
        },
        "Kecambah Kacang Hijau": {
            "kandungan": "Giberelin tinggi",
            "fungsi": "Pertumbuhan tinggi, pembungaan",
            "cara": "Haluskan kecambah + air, saring",
            "aplikasi": "Semprot saat fase vegetatif"
        }
    }
}

# PESTISIDA NABATI
PESTISIDA_NABATI = {
    "Ekstrak Daun Mimba (Neem)": {
        "target": ["Ulat", "Kutu daun", "Thrips", "Tungau"],
        "bahan_aktif": "Azadirachtin",
        "cara_buat": [
            "1. Tumbuk 1 kg daun mimba segar",
            "2. Rendam dalam 10 L air + 10 ml detergen",
            "3. Diamkan 24 jam, aduk sesekali",
            "4. Saring, siap digunakan"
        ],
        "dosis": "Semprot langsung (tidak perlu diencerkan)",
        "interval": "Setiap 5-7 hari",
        "kelebihan": ["Sistemik", "Aman untuk manusia", "Efek jangka panjang"],
        "tips": "Aplikasi sore hari, mimba sangat efektif!"
    },
    "Ekstrak Bawang Putih": {
        "target": ["Bakteri", "Jamur", "Serangga penghisap"],
        "bahan_aktif": "Allicin (antibakteri kuat)",
        "cara_buat": [
            "1. Haluskan 500g bawang putih",
            "2. Rendam dalam 10 L air + 50 ml minyak goreng",
            "3. Diamkan 24 jam",
            "4. Saring, encerkan 1:5"
        ],
        "dosis": "Semprot 1:5 dengan air",
        "interval": "Setiap 3-5 hari",
        "kelebihan": ["Antibakteri kuat", "Antijamur", "Mudah didapat"],
        "tips": "Kombinasi dengan cabai untuk efek maksimal"
    },
    "Ekstrak Cabai Rawit": {
        "target": ["Ulat", "Belalang", "Kutu daun"],
        "bahan_aktif": "Capsaicin (iritan kuat)",
        "cara_buat": [
            "1. Haluskan 500g cabai rawit",
            "2. Rebus dengan 5 L air selama 30 menit",
            "3. Dinginkan, saring",
            "4. Tambahkan 50 ml detergen"
        ],
        "dosis": "Encerkan 1:3 dengan air",
        "interval": "Setiap 5 hari",
        "kelebihan": ["Efek repellent kuat", "Murah", "Mudah dibuat"],
        "tips": "Gunakan sarung tangan saat membuat!"
    },
    "Ekstrak Tembakau": {
        "target": ["Ulat", "Kutu", "Thrips"],
        "bahan_aktif": "Nikotin",
        "cara_buat": [
            "1. Rendam 200g tembakau kering dalam 5 L air",
            "2. Diamkan 48 jam",
            "3. Saring, tambahkan detergen"
        ],
        "dosis": "Encerkan 1:2",
        "interval": "Setiap 7 hari",
        "kelebihan": ["Sangat efektif", "Kontak dan sistemik"],
        "peringatan": "⚠️ Beracun! Gunakan APD, jangan untuk sayuran menjelang panen"
    },
    "Pestisida Nabati Kombinasi (Super Formula)": {
        "target": "Hama & penyakit umum",
        "bahan": [
            "500g daun mimba",
            "250g bawang putih",
            "250g cabai rawit",
            "100g lengkuas",
            "100g jahe",
            "50 ml minyak goreng",
            "50 ml detergen",
            "10 L air"
        ],
        "cara_buat": [
            "1. Haluskan semua bahan (kecuali air, minyak, detergen)",
            "2. Rendam dalam air 24 jam",
            "3. Saring, tambahkan minyak + detergen",
            "4. Aduk rata"
        ],
        "dosis": "Encerkan 1:3",
        "interval": "Setiap 5-7 hari",
        "kelebihan": ["Spektrum luas", "Sangat efektif", "Tahan lama"],
        "tips": "Formula terbaik untuk pengendalian terpadu!"
    },
    "Fermentasi Urine Sapi + Daun Pepaya": {
        "target": ["Ulat", "Penggerek", "Kutu"],
        "cara_buat": [
            "1. Campurkan 5 L urine sapi segar",
            "2. Tambahkan 1 kg daun pepaya yang dihaluskan",
            "3. Tambahkan 100g gula merah",
            "4. Fermentasi 7 hari dalam wadah tertutup"
        ],
        "dosis": "Encerkan 1:10",
        "interval": "Setiap 7 hari",
        "kelebihan": ["Murah", "Efektif", "Bonus nutrisi"],
        "tips": "Urine sapi juga mengandung nutrisi!"
    }
}


# ========== ADVANCED INTEL MODULES ==========

def show_mulders_chart():
    st.subheader("📊 Visualisasi Interaksi Nutrisi (Mulder's Chart)")
    st.markdown("""
    Bagan ini menunjukkan bagaimana satu unsur hara dapat memengaruhi penyerapan unsur hara lainnya.
    - **Antagonisme (Garis Merah):** Kelebihan satu unsur menghambat penyerapan unsur lain.
    - **Sinergisme (Garis Hijau):** Kehadiran satu unsur membantu penyerapan unsur lain.
    """)

    nutrients = ["N", "P", "K", "Ca", "Mg", "Fe", "Mn", "Zn", "Cu", "B", "Mo"]
    
    # Simple coordinates for a circle
    angles = np.linspace(0, 2*np.pi, len(nutrients), endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    fig = go.Figure()

    # Define interactions (Simplified example for visualization)
    interactions = [
        ("N", "P", "synergy"), ("N", "K", "synergy"), ("N", "Mg", "synergy"),
        ("K", "Mg", "antagonism"), ("K", "Ca", "antagonism"),
        ("P", "Zn", "antagonism"), ("P", "Fe", "antagonism"), ("P", "Cu", "antagonism"),
        ("Ca", "P", "antagonism"), ("Ca", "Mg", "antagonism"), ("Ca", "B", "antagonism"),
        ("Mg", "Ca", "antagonism"), ("Mg", "K", "antagonism"),
        ("Fe", "Mn", "antagonism"), ("Cu", "Mo", "antagonism")
    ]

    # Draw lines
    for start, end, type in interactions:
        idx_s = nutrients.index(start)
        idx_e = nutrients.index(end)
        color = "rgba(34, 197, 94, 0.6)" if type == "synergy" else "rgba(239, 68, 68, 0.6)"
        width = 2
        
        fig.add_trace(go.Scatter(
            x=[x[idx_s], x[idx_e]], y=[y[idx_s], y[idx_e]],
            mode='lines',
            line=dict(color=color, width=width),
            hoverinfo='none',
            showlegend=False
        ))

    # Add points
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers+text',
        text=nutrients,
        textposition="top center",
        marker=dict(size=25, color='#065f46', line=dict(width=2, color='white')),
        textfont=dict(color="black", size=14, family="Outfit"),
        hoverinfo='text',
        hovertext=nutrients
    ))

    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_ph_availability():
    st.subheader("🌍 Pengaruh pH Tanah terhadap Ketersediaan Hara")
    
    ph_range = np.linspace(4.0, 9.0, 50)
    
    # Simulated availability curves
    availability = {
        "N (Nitrogen)": np.exp(-(ph_range-6.5)**2 / 2.0),
        "P (Fosfor)": np.exp(-(ph_range-6.8)**2 / 0.8),
        "K (Kalium)": np.where(ph_range < 6, (ph_range-4)/2, 1.0),
        "Ca/Mg": np.where(ph_range < 7, (ph_range-4)/3, 1.0),
        "Mikro (Fe, Mn, Zn)": np.where(ph_range > 6, 1 - (ph_range-6)/3, 1.0),
        "Mo (Molibdenum)": np.where(ph_range < 7, (ph_range-4)/4, 1.0)
    }
    
    fig = px.line(pd.DataFrame(availability, index=ph_range), 
                 labels={"index": "pH Tanah", "value": "Ketersediaan (Relatif)"},
                 color_discrete_sequence=px.colors.qualitative.Safe)
    
    fig.add_vrect(x0=6.0, x1=7.0, fillcolor="rgba(34, 197, 94, 0.2)", layer="below", line_width=0, 
                  annotation_text="Rentang Ideal (6.0 - 7.0)")
    
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

def show_mixture_simulator():
    st.subheader("🧪 Simulator Pencampuran Pupuk")
    st.markdown("Cek apakah dua jenis pupuk aman untuk dicampurkan dalam satu tangki/wadah.")
    
    col1, col2 = st.columns(2)
    pupuk_list = ["Urea", "ZA", "SP-36/TSP", "KCl", "NPK", "Kalsium Nitrat", "Magnesium Sulfat", "Pupuk Organik Cair"]
    
    with col1:
        p1 = st.selectbox("Pilih Pupuk A", pupuk_list, index=0)
    with col2:
        p2 = st.selectbox("Pilih Pupuk B", pupuk_list, index=5)
        
    # Compatibility Logic
    compatibility = "Safe"
    reason = "Aman untuk dicampur."
    
    # Specific Cases
    dangerous = [
        ("Kalsium Nitrat", "SP-36/TSP"), # Presipitasi kalsium fosfat
        ("Kalsium Nitrat", "Magnesium Sulfat"), # Presipitasi kalsium sulfat (gipsum)
        ("Urea", "ZA"), # Menjadi sangat lembab (higroskopis)
    ]
    
    caution = [
        ("Urea", "SP-36/TSP"), # Bisa menggumpal jika disimpan lama
        ("ZA", "Kapur/Dolomit"), # Kehilangan N dalam bentuk amonia
    ]
    
    for pair in dangerous:
        if (p1 == pair[0] and p2 == pair[1]) or (p1 == pair[1] and p2 == pair[0]):
            compatibility = "Dangerous"
            reason = "Terjadi presipitasi (pengendapan) yang dapat menyumbat nozzle atau mengurangi efektivitas."
    
    for pair in caution:
        if (p1 == pair[0] and p2 == pair[1]) or (p1 == pair[1] and p2 == pair[0]):
            compatibility = "Caution"
            reason = "Segera gunakan setelah dicampur. Jangan disimpan dalam kondisi tercampur."

    if compatibility == "Safe":
        st.success(f"✅ **{p1} + {p2}**: {reason}")
    elif compatibility == "Caution":
        st.warning(f"⚠️ **{p1} + {p2}**: {reason}")
    else:
        st.error(f"❌ **{p1} + {p2}**: {reason}")


def show_deficiency_detector():
    st.subheader("🔍 Pendeteksi Defisiensi Cerdas")
    st.info("Jawab beberapa pertanyaan di bawah ini untuk mengidentifikasi kemungkinan kekurangan nutrisi.")
    
    # Step 1: Location of symptoms
    location = st.radio(
        "Di mana gejala pertama kali muncul?",
        ["Daun Tua (Bagian Bawah)", "Daun Muda (Bagian Atas/Pucuk)", "Bunga/Buah/Akar"],
        horizontal=True
    )
    
    if location == "Daun Tua (Bagian Bawah)":
        st.markdown("**Analisis Daun Tua:** Unsur hara yang bersifat mobil (N, P, K, Mg) akan dipindahkan ke daun muda jika terjadi kekurangan.")
        symptom = st.radio(
            "Apa gejala utamanya?",
            [
                "Kuning merata (Klorosis)", 
                "Tepi daun kering/terbakar (Necrosis)",
                "Warna ungu/merah tua",
                "Bercak kuning di antara tulang daun (Interveinal)"
            ]
        )
        
        if symptom == "Kuning merata (Klorosis)":
            st.error("💡 **Kemungkinan: Defisiensi NITROGEN (N)**")
            st.write("Tanaman butuh asupan N cepat (Urea/ZA/POC).")
        elif symptom == "Tepi daun kering/terbakar (Necrosis)":
            st.error("💡 **Kemungkinan: Defisiensi KALIUM (K)**")
            st.write("Tanaman butuh KCl atau pupuk daun tinggi K.")
        elif symptom == "Warna ungu/merah tua":
            st.error("💡 **Kemungkinan: Defisiensi FOSFOR (P)**")
            st.write("Tanaman butuh SP-36/TSP atau MAP/DAP.")
        elif symptom == "Bercak kuning di antara tulang daun (Interveinal)":
            st.error("💡 **Kemungkinan: Defisiensi MAGNESIUM (Mg)**")
            st.write("Aplikasi Magnesium Sulfat atau Kapur Dolomit.")
            
    elif location == "Daun Muda (Bagian Atas/Pucuk)":
        st.markdown("**Analisis Daun Muda:** Unsur hara imobil (Ca, S, Fe, Zn, Mn, B, Cu) tidak bisa pindah, sehingga gejala muncul di pucuk.")
        symptom = st.radio(
            "Apa gejala utamanya?",
            [
                "Pucuk kuning pucat (tulang daun tetap hijau)", 
                "Pucuk kuning merata",
                "Pucuk kerdil/cacat/mati",
                "Daun muda putih bersih"
            ]
        )
        
        if symptom == "Pucuk kuning pucat (tulang daun tetap hijau)":
            st.error("💡 **Kemungkinan: Defisiensi BESI (Fe)**")
            st.write("Hampir sering terjadi di tanah pH tinggi. Gunakan Fe-EDTA.")
        elif symptom == "Pucuk kuning merata":
            st.error("💡 **Kemungkinan: Defisiensi SULFUR (S)**")
            st.write("Mirip N tapi di daun muda. Gunakan ZA atau pupuk mengandung S.")
        elif symptom == "Pucuk kerdil/cacat/mati":
            st.error("💡 **Kemungkinan: Defisiensi BORON (B) atau KALSIUM (Ca)**")
            st.write("Cek buah; jika busuk pantat (blossom end rot) itu Ca. Jika titik tumbuh mati itu B.")
        elif symptom == "Daun muda putih bersih":
            st.error("💡 **Kemungkinan: Defisiensi MIKRO (Zn/Mn)**")
            st.write("Gunakan pupuk mikro lengkap.")

    elif location == "Bunga/Buah/Akar":
        st.markdown("**Analisis Organ Khusus:**")
        symptom = st.radio(
            "Gejala apa yang ditemukan?",
            ["Buah busuk ujung (Blossom End Rot)", "Bunga rontok parah", "Akar pendek/kerdil"]
        )
        if symptom == "Buah busuk ujung (Blossom End Rot)":
            st.error("💡 **Kemungkinan: Defisiensi KALSIUM (Ca)**")
        else:
            st.info("Kombinasi defisiensi P, B, dan K sering menyebabkan masalah pada organ generatif.")

def show_pest_action_matrix():
    st.subheader("🛡️ Matriks Aksi Pengendalian Alami")
    st.markdown("Pilih Target Hama untuk melihat solusi pengendalian nabati yang paling efektif.")
    
    # Combined data from knowledge and pestisida nabati
    action_data = {
        "Ulat (Grayak/Krop)": ["Mimba", "Tembakau", "Cabai Rawit", "Sirsak", "Sambiloto"],
        "Kutu Daun/Aphids": ["Bawang Putih", "Mimba", "Minyak Kelapa/Sabun", "Tembakau"],
        "Thrips/Tungau": ["Mimba", "Bawang Putih", "Tembakau"],
        "Wereng Padi": ["Mimba", "Brotowali", "Tembakau"],
        "Lalat Buah": ["Cemara Hantu (Atraktan)", "Selasih", "Minyak Nimba"],
        "Jamur/Fungi": ["Kunyit", "Lengkuas", "Sirih", "Jahe", "Bawang Putih"],
        "Bakteri": ["Sirih", "Bawang Putih", "Lidah Buaya"],
        "Keong Mas": ["Akar Tuba", "Biji Jarak", "Batik/Pinang Muda"],
        "Tikus": ["Gadung", "Gamal"]
    }
    
    selected_target = st.selectbox("🎯 Target Gangguan:", list(action_data.keys()))
    
    if selected_target:
        solutions = action_data[selected_target]
        st.markdown(f"**Solusi Nabati untuk {selected_target}:**")
        
        cols = st.columns(len(solutions) if len(solutions) < 4 else 4)
        for i, sol in enumerate(solutions):
            with cols[i % 4]:
                st.info(f"🌿 **{sol}**")
                if st.button(f"Lihat Resep {sol}", key=f"btn_res_{sol}_{i}"):
                    # Logic to switch or show recipe (for now just a link mention)
                    st.success(f"Gunakan Tab 'Pestisida Nabati' dan cari '{sol}'")

# ========== MAIN APP ==========
st.title("📚 Pusat Pengetahuan Pertanian")
st.markdown("**Ensiklopedia lengkap nutrisi tanaman, pupuk, dan pengendalian hama alami**")

# Category tabs
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧠 Intelijen Nutrisi",
    "🌾 Pupuk Makro",
    "⚛️ Pupuk Makro Sekunder",
    "⚗️ Pupuk Mikro",
    "🌱 Pupuk Organik & Hayati",
    "💧 POC, MOL & ZPT",
    "🌿 Pestisida Nabati"
])

# TAB 0: INTEL NUTRISI (NEW)
with tab0:
    st.header("🧠 Intelijen Nutrisi & Pupuk")
    st.info("Gunakan modul interaktif ini untuk memahami interaksi kimia dalam tanah dan tanaman.")
    
    col_a, col_b = st.columns([1, 1.2])
    
    with col_a:
        show_ph_availability()
        st.divider()
        show_mixture_simulator()
        st.divider()
        show_pest_action_matrix()
        
    with col_b:
        show_mulders_chart()
        st.divider()
        show_deficiency_detector()
        with st.expander("ℹ️ Cara Membaca Mulder's Chart"):
            st.markdown("""
            - **Antagonisme**: Jika kadar satu unsur terlalu tinggi, ia akan 'menekan' ketersediaan unsur lain. Misalnya, kadar **Kalium (K)** yang sangat tinggi dapat menghambat penyerapan **Magnesium (Mg)**.
            - **Sinergisme**: Unsur yang saling membantu. Misalnya, **Nitrogen (N)** membantu penyerapan **Magnesium (Mg)**.
            - **Penting**: Pemupukan harus berimbang. Menambah satu jenis pupuk secara berlebihan justru bisa menyebabkan tanaman 'kelaparan' unsur lain.
            """)

# TAB 1: PUPUK MAKRO
with tab1:
    st.header("🌾 Pupuk Makro")
    st.markdown("Pupuk dengan kandungan NPK tinggi untuk pertumbuhan optimal")
    
    # Search
    search_makro = st.text_input("🔍 Cari pupuk makro...", key="search_makro")
    
    # Filter
    filtered_makro = {k: v for k, v in PUPUK_MAKRO.items() 
                      if search_makro.lower() in k.lower()}
    
    for nama, data in filtered_makro.items():
        with st.expander(f"**{nama}**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Kandungan:**
                - N: {data['kandungan']['N']}%
                - P: {data['kandungan']['P']}%
                - K: {data['kandungan']['K']}%
                
                **Fungsi:** {data['fungsi']}
                
                **Dosis:** {data['dosis']}
                
                **Cara Aplikasi:** {data['cara_aplikasi']}
                
                **Waktu Aplikasi:** {data['waktu_aplikasi']}
                """)
            
            with col2:
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
                st.warning("**Kekurangan:**\n" + "\n".join([f"⚠️ {k}" for k in data['kekurangan']]))
                st.info(f"💡 **Tips:** {data['tips']}")

# TAB 2: PUPUK MAKRO SEKUNDER
with tab2:
    st.header("⚛️ Pupuk Makro Sekunder (Ca, Mg, S)")
    st.markdown("""
    Unsur hara makro sekunder sangat penting untuk:
    - **Kalsium (Ca)**: Struktur dinding sel, pertumbuhan akar, kualitas buah
    - **Magnesium (Mg)**: Pusat molekul klorofil, fotosintesis, aktivasi enzim
    - **Sulfur (S)**: Pembentukan protein, vitamin, enzim
    """)
    
    # Search
    search_sekunder = st.text_input("🔍 Cari pupuk makro sekunder...", key="search_sekunder")
    
    # Category filter
    kategori_sekunder = st.radio(
        "Filter berdasarkan unsur:",
        ["Semua", "Magnesium (Mg)", "Kalsium (Ca)", "Sulfur (S)", "Kombinasi"],
        horizontal=True
    )
    
    # Filter logic
    filtered_sekunder = {}
    for nama, data in PUPUK_MAKRO_SEKUNDER.items():
        # Search filter
        if search_sekunder and search_sekunder.lower() not in nama.lower():
            continue
        
        # Category filter
        if kategori_sekunder != "Semua":
            if kategori_sekunder == "Magnesium (Mg)" and "Mg" not in data['kandungan']:
                continue
            elif kategori_sekunder == "Kalsium (Ca)" and "Ca" not in data['kandungan']:
                continue
            elif kategori_sekunder == "Sulfur (S)" and "S" not in data['kandungan'] and "Mg" in data['kandungan']:
                continue
            elif kategori_sekunder == "Kombinasi" and len(data['kandungan']) < 2:
                continue
        
        filtered_sekunder[nama] = data
    
    st.write(f"**Menampilkan {len(filtered_sekunder)} produk**")
    
    for nama, data in filtered_sekunder.items():
        with st.expander(f"**{nama}**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Kandungan:**")
                for unsur, persen in data['kandungan'].items():
                    st.markdown(f"- {unsur}: {persen}%")
                
                st.markdown(f"\n**Fungsi:** {data['fungsi']}")
                
                st.markdown(f"\n**Gejala Defisiensi:**")
                st.markdown(f"⚠️ {data['defisiensi']}")
                
                st.markdown(f"\n**Dosis:** {data['dosis']}")
                
                st.markdown(f"\n**Cara Aplikasi:** {data['cara_aplikasi']}")
                
                st.markdown(f"\n**Waktu Aplikasi:** {data['waktu_aplikasi']}")
            
            with col2:
                st.markdown("**Tanaman Peka:**")
                for tanaman in data['tanaman_peka']:
                    st.markdown(f"🌱 {tanaman}")
                
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
                st.warning("**Kekurangan:**\n" + "\n".join([f"⚠️ {k}" for k in data['kekurangan']]))
                st.info(f"💡 **Tips:** {data['tips']}")
    
    # Info box
    st.markdown("---")
    st.info("""
    **📌 Catatan Penting:**
    
    **Kalsium (Ca):**
    - Tanah masam (pH <5.5): Gunakan Dolomit atau Kapur Pertanian
    - Tanah alkalin (pH >7): Gunakan Gypsum
    - Hidroponik/Fertigasi: Gunakan Kalsium Nitrat atau CalMag
    - Mencegah Blossom End Rot: Semprot Kalsium Klorida saat pembentukan buah
    
    **Magnesium (Mg):**
    - Defisiensi umum pada tanah masam dan berpasir
    - Gejala: Klorosis interveinal pada daun tua
    - Koreksi cepat: Semprot Magnesium Sulfat (Epsom Salt) 2-5 g/L
    
    **Sulfur (S):**
    - Penting untuk tanaman Brassica (kubis, brokoli) dan Allium (bawang)
    - Menurunkan pH tanah: Gunakan Sulfur Bentonit atau Sulfur Powder
    - Fungisida alami: Sulfur Powder efektif untuk embun tepung
    """)

# TAB 3: PUPUK MIKRO
with tab3:
    st.header("⚗️ Pupuk Mikro")
    st.markdown("Unsur hara mikro penting untuk pertumbuhan optimal")
    
    for nama, data in PUPUK_MIKRO.items():
        with st.expander(f"**{nama}**"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Fungsi:** {data['fungsi']}
                
                **Gejala Defisiensi:**
                {data['defisiensi']}
                
                **Sumber:** {data['sumber']}
                """)
            
            with col2:
                st.markdown(f"""
                **Dosis:** {data['dosis']}
                
                **Tanaman Peka:**
                {', '.join(data['tanaman_peka'])}
                """)
                
                st.info(f"💡 {data['tips']}")

# TAB 4: PUPUK ORGANIK
with tab4:
    st.header("🌱 Pupuk Organik & Hayati")
    st.markdown("Pupuk alami untuk kesehatan tanah jangka panjang")
    
    for nama, data in PUPUK_ORGANIK.items():
        with st.expander(f"**{nama}**", expanded=False):
            if "kandungan" in data:
                st.markdown(f"**Kandungan:** {data['kandungan']}")
            
            if "jenis" in data:
                st.markdown("**Jenis:**")
                for jenis, desc in data['jenis'].items():
                    st.markdown(f"- **{jenis}:** {desc}")
            
            if "fungsi" in data:
                st.markdown(f"**Fungsi:** {data['fungsi']}")
            
            if "tanaman" in data:
                st.markdown(f"**Tanaman:** {', '.join(data['tanaman'])}")
            
            if "dosis" in data:
                st.markdown(f"**Dosis:** {data['dosis']}")
            
            if "cara_buat" in data:
                st.markdown("**Cara Membuat:**")
                for step in data['cara_buat']:
                    st.markdown(f"{step}")
            
            if "cara_aplikasi" in data:
                st.markdown(f"**Cara Aplikasi:** {data['cara_aplikasi']}")
            
            if "kelebihan" in data:
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
            
            if "kekurangan" in data:
                st.warning("**Kekurangan:**\n" + "\n".join([f"⚠️ {k}" for k in data['kekurangan']]))
            
            st.info(f"💡 **Tips:** {data['tips']}")

# TAB 5: POC, MOL & ZPT
with tab5:
    st.header("💧 POC, MOL & ZPT Alami")
    st.markdown("Pupuk cair dan zat pengatur tumbuh alami")
    
    for kategori, items in POC_MOL_ZPT.items():
        st.subheader(kategori)
        
        if kategori == "MOL (Mikroorganisme Lokal)":
            for jenis_mol, data_mol in items['jenis'].items():
                with st.expander(jenis_mol):
                    st.markdown(f"**Bahan:** {data_mol['bahan']}")
                    st.markdown(f"**Fungsi:** {data_mol['fungsi']}")
                    st.markdown(f"**Cara:** {data_mol['cara']}")
            
            st.markdown(f"**Dosis Umum:** {items['dosis']}")
            st.markdown(f"**Aplikasi:** {items['aplikasi']}")
            st.info(f"💡 {items['tips']}")
            
        elif kategori == "ZPT Alami (Zat Pengatur Tumbuh)":
            for zpt_name, zpt_data in items.items():
                with st.expander(zpt_name):
                    st.markdown(f"**Kandungan:** {zpt_data['kandungan']}")
                    st.markdown(f"**Fungsi:** {zpt_data['fungsi']}")
                    if 'cara' in zpt_data:
                        st.markdown(f"**Cara:** {zpt_data['cara']}")
                    if 'dosis' in zpt_data:
                        st.markdown(f"**Dosis:** {zpt_data['dosis']}")
                    st.markdown(f"**Aplikasi:** {zpt_data['aplikasi']}")
        else:
            with st.expander("Detail"):
                st.markdown(f"**Bahan:** {items['bahan']}")
                st.markdown("**Cara Membuat:**")
                for step in items['cara_buat']:
                    st.markdown(step)
                st.markdown(f"**Dosis:** {items['dosis']}")
                st.markdown(f"**Aplikasi:** {items['aplikasi']}")
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in items['kelebihan']]))
                st.info(f"💡 {items['tips']}")

# TAB 6: PESTISIDA NABATI
with tab6:
    st.header("🌿 Pestisida Nabati")
    st.markdown("Pengendalian hama & penyakit dengan bahan alami")
    
    st.warning("""
    **⚠️ Penting:**
    - Gunakan APD (masker, sarung tangan)
    - Aplikasi pagi/sore hari
    - Hindari saat hujan
    - Simpan di tempat aman
    - Jauhkan dari jangkauan anak-anak
    """)
    
    for nama, data in PESTISIDA_NABATI.items():
        with st.expander(f"**{nama}**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Target Hama:**")
                if isinstance(data['target'], list):
                    for target in data['target']:
                        st.markdown(f"- {target}")
                else:
                    st.markdown(data['target'])
                
                if 'bahan_aktif' in data:
                    st.markdown(f"\n**Bahan Aktif:** {data['bahan_aktif']}")
                
                if 'bahan' in data:
                    st.markdown("\n**Bahan:**")
                    for bahan in data['bahan']:
                        st.markdown(f"- {bahan}")
            
            with col2:
                st.markdown(f"**Dosis:** {data['dosis']}")
                st.markdown(f"**Interval:** {data['interval']}")
                
                if 'kelebihan' in data:
                    st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
            
            st.markdown("**Cara Membuat:**")
            for i, step in enumerate(data['cara_buat'], 1):
                st.markdown(step)
            
            if 'tips' in data:
                st.info(f"💡 **Tips:** {data['tips']}")
            
            if 'peringatan' in data:
                st.error(data['peringatan'])

# Footer
st.markdown("---")
st.caption("""
📚 **Pusat Pengetahuan Pertanian** - Ensiklopedia lengkap untuk pertanian berkelanjutan.

💡 **Disclaimer:** Informasi ini bersifat edukatif. Sesuaikan dengan kondisi lokal dan konsultasikan dengan ahli untuk kasus spesifik.

🌱 **Tips:** Kombinasikan pupuk organik dan anorganik untuk hasil optimal dan kesehatan tanah jangka panjang!
""")
