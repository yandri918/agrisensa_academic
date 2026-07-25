# Pestisida Nabati - Database Lengkap (M-48 Edition)
# Referensi: M-48 Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya (W. Setiawati et al., 2008)

import streamlit as st
import pandas as pd

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Pestisida Nabati M-48", page_icon="🌿", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ==========================================
# 🌿 DATABASE PESTISIDA NABATI (59 SPESIES - M-48)
# ==========================================

PESTISIDA_DATABASE = {
    "Ajeran (Bidens pilosa)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Kutu daun", "Kepik"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Vlavonoid, Terpenoid",
        "bahan": {"Tanaman ajeran": "1 kg", "Air": "10 liter", "Detergen": "20 ml"},
        "cara_pembuatan": ["Rebus seluruh bagian tanaman dengan air selama 30 menit", "Saring dan biarkan dingin", "Tambahkan detergen sebagai perekat"],
        "dosis_aplikasi": "Semprot langsung (tanpa pengenceran)"
    },
    "Akar Tuba (Derris elliptica)": {
        "kategori": "Insektisida + Moluskisida",
        "target_hama": ["Ulat", "Kutu", "Keong mas", "Tikus (sawah)"],
        "target_tanaman": ["Padi", "Sayuran"],
        "bahan_aktif": "Rotenon",
        "bahan": {"Akar tuba": "500 gram", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk akar tuba hingga hancur", "Rendam dalam air semalaman", "Saring air perasan"],
        "dosis_aplikasi": "Encerkan 1:5, semprotkan pada tanaman atau air sawah (untuk keong)"
    },
    "Bandotan (Ageratum conyzoides)": {
        "kategori": "Insektisida + Akarisida",
        "target_hama": ["Lalat buah", "Nyamuk", "Kutu", "Tungau"],
        "target_tanaman": ["Buah-buahan", "Sayuran"],
        "bahan_aktif": "Saponin, Flavonoid, Polifenol",
        "bahan": {"Daun bandotan": "1 kg", "Air": "5 liter", "Detergen": "10 ml"},
        "cara_pembuatan": ["Haluskan daun bandotan", "Rendam 24 jam dalam air", "Saring dan tambahkan detergen"],
        "dosis_aplikasi": "Encerkan 1:2"
    },
    "Baru Cina (Artemisia vulgaris)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat grayak", "Kutu daun"],
        "target_tanaman": ["Jagung", "Cabai"],
        "bahan_aktif": "Minyak atsiri, Artemisin",
        "bahan": {"Daun baru cina": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk halus", "Rebus sebentar atau rendam air panas", "Saring"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Bawang Merah (Allium cepa)": {
        "kategori": "Fungisida + ZPT",
        "target_hama": ["Jamur (Fusarium, Alternaria)", "Penyakit layu"],
        "target_tanaman": ["Cabai", "Tomat"],
        "bahan_aktif": "Quercetin, Allicin + Hormon Auxin",
        "bahan": {"Kulit/Umbi bawang merah": "200 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Blender bawang merah", "Rendam air 12 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5 (Bagus juga untuk perangsang akar)"
    },
    "Bawang Putih (Allium sativum)": {
        "kategori": "Insektisida + Fungisida",
        "target_hama": ["Kutu daun", "Thrips", "Ulat", "Jamur"],
        "target_tanaman": ["Bawang", "Cabai"],
        "bahan_aktif": "Allicin",
        "bahan": {"Bawang putih": "100 gram", "Air": "5 liter", "Minyak": "2 sdm", "Sabun": "1 sdt"},
        "cara_pembuatan": ["Haluskan bawang, rendam di minyak 24 jam", "Campur dengan air sabun", "Aduk rata"],
        "dosis_aplikasi": "Encerkan 1:20"
    },
    "Bayam Duri (Amaranthus spinosus)": {
        "kategori": "Insektisida",
        "target_hama": ["Larva Lepidoptera (Ulat)"],
        "target_tanaman": ["Sayuran daun"],
        "bahan_aktif": "Saponin, Tanin",
        "bahan": {"Daun bayam duri": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk daun", "Rendam dalam air selama 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:2"
    },
    "Bengkuang (Pachyrhizus erosus)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Thrips", "Kutu"],
        "target_tanaman": ["Palawija"],
        "bahan_aktif": "Rotenon (pada biji)",
        "bahan": {"Biji bengkuang": "500 gram", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk biji hingga halus", "Rendam air 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5, semprot sore hari"
    },
    "Bijanggut (Mentha spp.)": {
        "kategori": "Insektisida (Repellent)",
        "target_hama": ["Semut", "Kutu daun", "Lalat"],
        "target_tanaman": ["Tanaman hias", "Sayur"],
        "bahan_aktif": "Menthol (Minyak atsiri)",
        "bahan": {"Daun mint/bijanggut": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Remas-remas daun dalam air", "Diamkan semalaman", "Saring"],
        "dosis_aplikasi": "Semprot langsung sebagai pengusir"
    },
    "Brotowali (Tinospora rumphii)": {
        "kategori": "Insektisida",
        "target_hama": ["Wereng", "Ulat", "Kutu"],
        "target_tanaman": ["Padi"],
        "bahan_aktif": "Alkaloid (Rasa pahit)",
        "bahan": {"Batang brotowali": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Potong kecil batang", "Rebus atau rendam 3 hari", "Saring"],
        "dosis_aplikasi": "Encerkan 1:2"
    },
    "Bunga Pagoda (Clerodendrum japonicum)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat pemakan daun"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Saponin, Polifenol",
        "bahan": {"Akar/Daun": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk halus", "Rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Bunga Piretrum (Chrysanthemum cinerariaefolium)": {
        "kategori": "Insektisida (Kontak Kuat)",
        "target_hama": ["Hampir semua serangga lunak"],
        "target_tanaman": ["Semua tanaman"],
        "bahan_aktif": "Pyrethrin",
        "bahan": {"Bunga kering": "100 gram", "Alkohol": "200 ml", "Air": "10 liter"},
        "cara_pembuatan": ["Rendam bunga dalam alkohol", "Encerkan dengan air", "Saring"],
        "dosis_aplikasi": "Semprot langsung (Sore hari, hindari cahaya matahari langsung)"
    },
    "Bunga Pukul Empat (Mirabilis jalapa)": {
        "kategori": "Insektisida",
        "target_hama": ["Kutu daun (Aphids)"],
        "target_tanaman": ["Cabai", "Tomat"],
        "bahan_aktif": "Alkaloid, Trigonelline",
        "bahan": {"Daun/Biji": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk halus", "Rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:2"
    },
    "Cabai Merah (Capsicum annuum)": {
        "kategori": "Insektisida (Repellent)",
        "target_hama": ["Hama umum, Mamalia (tupai/tikus)"],
        "target_tanaman": ["Semua"],
        "bahan_aktif": "Capsaicin",
        "bahan": {"Cabai": "100 gram", "Air": "2 liter", "Sabun": "sedikit"},
        "cara_pembuatan": ["Blender cabai", "Rebus sebentar", "Saring dan tambah sabun"],
        "dosis_aplikasi": "Encerkan 1:5, semprotkan"
    },
    "Cemara Hantu (Melaleuca brachteata)": {
        "kategori": "Attractant (Pemikat)",
        "target_hama": ["Lalat Buah (Bactrocera spp.)"],
        "target_tanaman": ["Buah-buahan (Mangga, Jeruk)"],
        "bahan_aktif": "Minyak Atsiri (Methyl eugenol like)",
        "bahan": {"Daun cemara hantu": "Secukupnya"},
        "cara_pembuatan": ["Penyulingan minyak daun", "Atau remas daun dan masukkan perangkap"],
        "dosis_aplikasi": "Gunakan sebagai umpan dalam perangkap lalat buah"
    },
    "Cengkeh (Syzygium aromaticum)": {
        "kategori": "Fungisida + Bakterisida",
        "target_hama": ["Layu bakteri, Jamur akar, Nematoda"],
        "target_tanaman": ["Lada, Vanili, Pisang"],
        "bahan_aktif": "Eugenol",
        "bahan": {"Daun/Gagang cengkeh": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk/cacah", "Komposkan atau rendam", "Ambil airnya"],
        "dosis_aplikasi": "Encerkan 1:5, kocor di akar"
    },
    "Duku (Lansium domesticum)": {
        "kategori": "Insektisida (Nyamuk)",
        "target_hama": ["Nyamuk", "Serangga terbang"],
        "target_tanaman": ["Lingkungan rumah/kebun"],
        "bahan_aktif": "Lansic acid",
        "bahan": {"Kulit duku kering": "Secukupnya"},
        "cara_pembuatan": ["Keringkan kulit", "Bakar seperti obat nyamuk bakar"],
        "dosis_aplikasi": "Asap pengusir"
    },
    "Gadung (Dioscorea hispida)": {
        "kategori": "Rodentisida & Insektisida",
        "target_hama": ["Tikus", "Ulat krop"],
        "target_tanaman": ["Padi", "Palawija"],
        "bahan_aktif": "Dioscorine (Racun Saraf)",
        "bahan": {"Umbi gadung": "1 kg", "Dedak (untuk umpan)": "1 kg"},
        "cara_pembuatan": ["Parut umbi gadung", "Campur dengan dedak/ikan asin", "Bentuk pelet umpan"],
        "dosis_aplikasi": "Sebar umpan di lubang tikus (AWAS BERACUN BAGI MANUSIA)"
    },
    "Gamal (Gliricidia sepium)": {
        "kategori": "Rodentisida & Insektisida",
        "target_hama": ["Tikus", "Kutu daun"],
        "target_tanaman": ["Padi", "Kakao"],
        "bahan_aktif": "Dicoumarol (Anti-koagulan)",
        "bahan": {"Daun/Kulit batang": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk daun", "Rebus atau fermentasi", "Untuk tikus: campur ekstrak dengan umpan"],
        "dosis_aplikasi": "Encerkan 1:5 untuk semprot, atau jadikan umpan padat"
    },
    "Genteng Peujet (Quassia amara)": {
        "kategori": "Insektisida",
        "target_hama": ["Nematoda, Kutu, Ulat"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Quassin (Sangat pahit)",
        "bahan": {"Kayu/Kulit batang": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Rebus potongan kayu", "Saring airnya"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Iler (Coleus scutellarioides)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat"],
        "target_tanaman": ["Hias, Sayuran"],
        "bahan_aktif": "Minyak atsiri",
        "bahan": {"Daun iler": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk dan peras airnya"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Jahe (Zingiber officinale)": {
        "kategori": "Fungisida & Bakterisida",
        "target_hama": ["Layu bakteri, Jamur"],
        "target_tanaman": ["Padi (blas), Sayuran"],
        "bahan_aktif": "Zingerone, Shogaol",
        "bahan": {"Rimpang jahe": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Parut dan peras", "Campur air"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Jarak (Ricinus communis)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat grayak"],
        "target_tanaman": ["Jagung, Padi"],
        "bahan_aktif": "Risin (Racun protein)",
        "bahan": {"Biji jarak": "200 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk biji (HATI-HATI RACUN KERAS)", "Rebus dalam air", "Saring"],
        "dosis_aplikasi": "Encerkan 1:10. Jangan kena kulit!"
    },
    "Jeringau (Acorus calamus)": {
        "kategori": "Insektisida & Fungisida",
        "target_hama": ["Wereng, Walang sangit"],
        "target_tanaman": ["Padi"],
        "bahan_aktif": "Asaron",
        "bahan": {"Rimpang jeringau": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk rimpang", "Rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Kelor (Moringa oleifera)": {
        "kategori": "Pestisida & Pupuk",
        "target_hama": ["Memperkuat dinding sel (preventif)"],
        "target_tanaman": ["Semua"],
        "bahan_aktif": "Zeatin (Hormon), Antimikroba",
        "bahan": {"Daun kelor": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Blender daun", "Peras airnya (fermentasi 1 malam lebih baik)"],
        "dosis_aplikasi": "Encerkan 1:10 (Berfungsi sebagai pupuk daun juga)"
    },
    "Kenikir (Tagetes erecta)": {
        "kategori": "Nematisida & Insektisida",
        "target_hama": ["Nematoda akar, Kutu daun"],
        "target_tanaman": ["Cabai, Kentang"],
        "bahan_aktif": "Terthienyl (Akar)",
        "bahan": {"Seluruh tanaman": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Blender/tumbuk", "Rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Kocor ke tanah (nematoda) atau semprot daun (kutu)"
    },
    "Ketumbar (Coriandrum sativum)": {
        "kategori": "Insektisida (Acaricide)",
        "target_hama": ["Tungau (Mites), Kutu daun"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Linalool",
        "bahan": {"Biji ketumbar": "200 gram", "Air": "2 liter"},
        "cara_pembuatan": ["Tumbuk biji", "Rebus 10 menit", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Kipait (Tithonia diversifolia)": {
        "kategori": "Insektisida (Antifeedant)",
        "target_hama": ["Ulat pemakan daun"],
        "target_tanaman": ["Sayur, Padi"],
        "bahan_aktif": "Tagitinin (Pahit)",
        "bahan": {"Daun kipait": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk daun", "Rendam 1-2 hari", "Saring"],
        "dosis_aplikasi": "Semprot langsung (pekat)"
    },
    "Kirinyuh (Eupatorium odoratum/Chromolaena)": {
        "kategori": "Fungisida & Nematisida",
        "target_hama": ["Jamur akar, Nematoda"],
        "target_tanaman": ["Perkebunan, Horti"],
        "bahan_aktif": "Alkaloid, Fenol",
        "bahan": {"Daun kirinyuh": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk dan peras sarinya"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Kunyit (Curcuma domestica)": {
        "kategori": "Fungisida",
        "target_hama": ["Penyakit tepung (Oidium), Antraknosa"],
        "target_tanaman": ["Cabai, Tomat"],
        "bahan_aktif": "Kurkumin",
        "bahan": {"Rimpang kunyit": "500 gram", "Air": "5 liter", "Urine sapi (opsional)": "1 liter"},
        "cara_pembuatan": ["Parut kunyit", "Campur air (dan urine)", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Legundi (Vitex negundo)": {
        "kategori": "Insektisida & Fungisida",
        "target_hama": ["Gudang (kutu beras), Ulat"],
        "target_tanaman": ["Penyimpanan benih, Tanaman pangan"],
        "bahan_aktif": "Minyak atsiri",
        "bahan": {"Daun legundi": "Kering"},
        "cara_pembuatan": ["Keringkan daun", "Selipkan di karung beras/benih"],
        "dosis_aplikasi": "Letakkan di gudang"
    },
    "Lengkuas (Alpinia galanga)": {
        "kategori": "Fungisida",
        "target_hama": ["Jamur kulit, Penyakit tanaman"],
        "target_tanaman": ["Jahe-jahean, Sayur"],
        "bahan_aktif": "Galangin",
        "bahan": {"Rimpang lengkuas": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Parut, peras ambil airnya"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Lenglengan (Leucas aspera)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Minyak atsiri",
        "bahan": {"Seluruh tanaman": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk dan rendam"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Lidah Buaya (Aloe barbadensis)": {
        "kategori": "Bakterisida & Biostimulan",
        "target_hama": ["Bakteri busuk lunak"],
        "target_tanaman": ["Anggrek, Sayuran"],
        "bahan_aktif": "Saponin, Acemannan",
        "bahan": {"Jel lidah buaya": "500 ml", "Air": "2 liter"},
        "cara_pembuatan": ["Blender jel", "Campur air"],
        "dosis_aplikasi": "Encerkan 1:5, semprot daun"
    },
    "Mahoni (Swietenia mahagoni)": {
        "kategori": "Insektisida (Antifeedant)",
        "target_hama": ["Ulat, Penggerek batang"],
        "target_tanaman": ["Padi, Hutan"],
        "bahan_aktif": "Swietenin (Pahit)",
        "bahan": {"Biji mahoni": "500 gram", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk biji kering", "Rendam air panas", "Saring"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Mengkudu (Morinda citrifolia)": {
        "kategori": "Bakterisida & Insektisida",
        "target_hama": ["Kutu, Bakteri", "Nematoda"],
        "target_tanaman": ["Kopi, Sayur"],
        "bahan_aktif": "Antrakuinon",
        "bahan": {"Buah matang": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Hancurkan buah matang", "Fermentasi 3 hari", "Ambil air lindi"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Mimba (Azadirachta indica)": {
        "kategori": "Insektisida (Broad Spectrum)",
        "target_hama": ["Hampir semua serangga (Ulat, Wereng, Kutu)"],
        "target_tanaman": ["Semua"],
        "bahan_aktif": "Azadirachtin",
        "bahan": {"Biji/Daun mimba": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk biji (paling kuat) atau daun", "Rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Mindi (Melia azedarach)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Belalang"],
        "target_tanaman": ["Kedelai, Padi"],
        "bahan_aktif": "Melriantriol (mirip Mimba)",
        "bahan": {"Daun mindi": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk dan rendam 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Pacar Cina (Aglaia odorata)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat krop (Crocidolomia)"],
        "target_tanaman": ["Kubis-kubisan"],
        "bahan_aktif": "Rocaglamide",
        "bahan": {"Daun/Ranting": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk, rendam"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Paku Ekor Kuda (Equisetum arvense)": {
        "kategori": "Fungisida",
        "target_hama": ["Jamur karat, Embun tepung"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Silika (penguat dinding sel), Saponin",
        "bahan": {"Tanaman segar/kering": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Rebus tanaman", "Biarkan dingin"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Patah Tulang (Euphorbia tirucalli)": {
        "kategori": "Moluskisida & Insektisida",
        "target_hama": ["Keong Mas, Siput", "Kutu"],
        "target_tanaman": ["Padi"],
        "bahan_aktif": "Getah (Euphorbol) - Iritan/Racun",
        "bahan": {"Ranting patah tulang (bergetah)": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Cacah ranting hingga keluar getah", "Rendam air", "Saring"],
        "dosis_aplikasi": "Siramkan ke area yang ada keong (HATI-HATI GETAH BERBAHAYA BAGI MATA)"
    },
    "Pepaya (Carica papaya)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Kutu"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Papain",
        "bahan": {"Daun pepaya tua": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk daun", "Rendam 24 jam (dicampur sabun sedikit)", "Saring"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Petikan Kebo (Euphorbia hirta)": {
        "kategori": "Insektisida",
        "target_hama": ["Kutu daun"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Flavonoid, Saponin",
        "bahan": {"Seluruh tanaman": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk dan rendam"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Pongam/Ki Pahang (Pongamia pinnata)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Kutu, Wereng"],
        "target_tanaman": ["Padi, Palawija"],
        "bahan_aktif": "Karanjin",
        "bahan": {"Biji/Minyak biji": "100 ml", "Air": "10 liter", "Sabun": "Secukupnya"},
        "cara_pembuatan": ["Peras minyak biji", "Emulsikan dengan sabun dan air"],
        "dosis_aplikasi": "2-3 ml per liter air"
    },
    "Putri Malu (Mimosa pudica)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Mimosin",
        "bahan": {"Seluruh tanaman": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk halus", "Rendam"],
        "dosis_aplikasi": "Encerkan 1:3"
    },
    "Sambiloto (Andrographis paniculata)": {
        "kategori": "Insektisida (Pahit)",
        "target_hama": ["Ulat, Penggerek"],
        "target_tanaman": ["Semua"],
        "bahan_aktif": "Andrographolide",
        "bahan": {"Daun/batang": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk karena pahit sekali", "Rendam"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Selasih (Ocimum basilicum)": {
        "kategori": "Repellent & Fungisida",
        "target_hama": ["Lalat buah, Nyamuk"],
        "target_tanaman": ["Buah, Sayur"],
        "bahan_aktif": "Minyak atsiri (Eugenol)",
        "bahan": {"Daun selasih": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Penyulingan atau perasan daun"],
        "dosis_aplikasi": "Semprot sebagai repellent"
    },
    "Senopodii (Chenopodium ambrosioides)": {
        "kategori": "Insektisida",
        "target_hama": ["Kutu, Ulat"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Ascaridole",
        "bahan": {"Seluruh tanaman": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk dan rendam"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Serai Wangi (Cymbopogon nardus)": {
        "kategori": "Repellent & Insektisida",
        "target_hama": ["Kutu, Nyamuk, Lalat"],
        "target_tanaman": ["Semua"],
        "bahan_aktif": "Sitronelal, Geraniol",
        "bahan": {"Daun/Batang serai": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Blender dan peras", "Atau suling minyaknya"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Singawalang (Petiveria alliacea)": {
        "kategori": "Insektisida & Akarisida",
        "target_hama": ["Hama gudang, Kutu"],
        "target_tanaman": ["Gudang"],
        "bahan_aktif": "Senyawa Sulfur (Bau bawang)",
        "bahan": {"Daun/Akar": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk halus (bau menyengat)", "Rendam"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Sirih (Piper betle)": {
        "kategori": "Fungisida & Bakterisida",
        "target_hama": ["Antraknosa, Busuk daun"],
        "target_tanaman": ["Cabai"],
        "bahan_aktif": "Fenol, Kavikol",
        "bahan": {"Daun sirih": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Rebus daun sirih", "Saring"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Sirsak (Annona muricata)": {
        "kategori": "Insektisida (Kontak & Perut)",
        "target_hama": ["Thrips, Kutu, Ulat"],
        "target_tanaman": ["Cabai, Tomat"],
        "bahan_aktif": "Annonain",
        "bahan": {"Daun sirsak": "100 lembar", "Air": "5 liter", "Sabun": "20 ml"},
        "cara_pembuatan": ["Blender daun", "Rendam 24 jam", "Saring & tambah sabun"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Srikaya (Annona squamosa)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Kutu"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Squamocin (Biji)",
        "bahan": {"Biji srikaya": "200 gram", "Air": "2 liter"},
        "cara_pembuatan": ["Tumbuk biji hingga halus", "Rendam air", "saring"],
        "dosis_aplikasi": "Encerkan 1:10"
    },
    "Suren (Toona sureni)": {
        "kategori": "Insektisida & Repellent",
        "target_hama": ["Ulat, Wereng"],
        "target_tanaman": ["Padi, Sayur"],
        "bahan_aktif": "Surenin",
        "bahan": {"Daun/Kulit batang": "1 kg", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk/cacah", "Rendam air"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Tembakau (Nicotiana tabacum)": {
        "kategori": "Insektisida (Sangat Kuat)",
        "target_hama": ["Hampir semua hama serangga"],
        "target_tanaman": ["Padi (Jangan sayuran siap panen)"],
        "bahan_aktif": "Nikotin (Racun Saraf)",
        "bahan": {"Daun/Batang tembakau/Puntung rokok": "200 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Rebus atau rendam air panas", "Saring"],
        "dosis_aplikasi": "Encerkan 1:10 (Beracun bagi manusia, hati-hati residu)"
    },
    "Tembelekan (Lantana camara)": {
        "kategori": "Insektisida & Repellent",
        "target_hama": ["Kutu, Ulat"],
        "target_tanaman": ["Pagar hidup, Sayuran"],
        "bahan_aktif": "Lantanine",
        "bahan": {"Daun tembelekan": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk dan rendam"],
        "dosis_aplikasi": "Encerkan 1:5 (Tanaman ini juga alelopati/herbisida)"
    },
    "Tephrosia (Tephrosia vogelii)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Kutu (Helopeltis)"],
        "target_tanaman": ["Kakao, Sayur"],
        "bahan_aktif": "Rotenon (Daun)",
        "bahan": {"Daun tephrosia": "500 gram", "Air": "10 liter"},
        "cara_pembuatan": ["Tumbuk daun", "Rendam air semalaman"],
        "dosis_aplikasi": "Encerkan 1:5"
    },
    "Tomat (Lycopersicum esculentum)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat, Kutu"],
        "target_tanaman": ["Sawi, Kubis (Jangan pada tomat/terong - sekerabat)"],
        "bahan_aktif": "Tomatine (pada daun/batang)",
        "bahan": {"Daun tomat": "1 kg", "Air": "5 liter"},
        "cara_pembuatan": ["Cacah daun tomat", "Rendam air 24 jam", "Saring"],
        "dosis_aplikasi": "Encerkan 1:2"
    },
    "Ubi Kemili (Stemona tuberosa)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat"],
        "target_tanaman": ["Sayuran"],
        "bahan_aktif": "Stemonine",
        "bahan": {"Umbi kemili": "500 gram", "Air": "5 liter"},
        "cara_pembuatan": ["Tumbuk umbi", "Rendam air"],
        "dosis_aplikasi": "Encerkan 1:5"
    }
}

PESTISIDA_DATABASE["Pinang (Areca catechu)"] = {
    "kategori": "Moluskisida (Keong)",
    "target_hama": ["Keong Mas", "Cacing"],
    "target_tanaman": ["Padi"],
    "bahan_aktif": "Arecoline, Tanin",
    "bahan": {"Biji pinang muda": "500 gram", "Air": "10 liter"},
    "cara_pembuatan": ["Tumbuk biji pinang", "Rendam air", "Saring"],
    "dosis_aplikasi": "Siramkan ke sawah yang ada keong"
}

# ========== SIDEBAR INFO ==========
# ========== SIDEBAR INFO ==========
with st.sidebar:
    st.info("ℹ️ **Info Ilmiah:** Ingin tahu lebih dalam tentang bahan aktif seperti *Azadirachtin* atau *Rotenon*?")
    if st.button("🔬 Buka Direktori Bahan Aktif"):
        st.switch_page("pages/26_🔬_Direktori_Bahan_Aktif.py")
        
    st.markdown("---")
    st.header("📚 Referensi Lengkap")
    st.write("Untuk informasi lebih lengkap buka file ini:")
    
    import os
    
    # Try multiple possible paths for PDF
    pdf_paths = [
        "assets/pdfs/M-48_Pestisida_Nabati.pdf",
        os.path.join(os.path.dirname(__file__), "..", "..", "assets", "pdfs", "M-48_Pestisida_Nabati.pdf"),
        "agrisensa_streamlit/assets/pdfs/M-48_Pestisida_Nabati.pdf"
    ]
    
    pdf_found = False
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF M-48",
                        data=pdf_file,
                        file_name="M-48_Pestisida_Nabati.pdf",
                        mime="application/pdf"
                    )
                    pdf_found = True
                    break
            except Exception as e:
                continue
    
    if not pdf_found:
        st.warning("📄 File PDF tersedia di repository")
        st.markdown("[📥 Download dari GitHub](https://github.com/yandri918/streamlit_terbaru/raw/main/agrisensa_streamlit/assets/pdfs/M-48_Pestisida_Nabati.pdf)")

# ========== HELPER FUNCTIONS ==========
def calculate_dosage(luas_lahan, volume_per_ha, konsentrasi):
    """Kalkulator dosis pestisida"""
    total_volume = (luas_lahan / 10000) * volume_per_ha
    volume_pestisida = total_volume / (konsentrasi + 1)
    volume_air = total_volume - volume_pestisida
    return total_volume, volume_pestisida, volume_air

# ========== MAIN APP ==========
st.title("🌿 Pestisida Nabati - Database Lengkap (M-48)")
st.markdown("**Referensi: M-48 Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya**")

# Statistics
st.metric("Total Spesies Terdata", f"{len(PESTISIDA_DATABASE)} Tanaman")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌱 Cari Berdasarkan Tanaman",
    "🔍 Cari Solusi Hama",
    "📚 Ensiklopedia M-48",
    "🧮 Kalkulator Dosis"
])

# TAB 1: SEARCH BY PLANT (NEW)
with tab1:
    st.header("🌱 Cari Solusi untuk Tanaman Anda")
    st.info("Pilih jenis tanaman yang Anda tanam, kami akan carikan pestisida yang cocok.")
    
    # Logic: Collect all unique 'target_tanaman' from DB
    all_plants = set()
    for data in PESTISIDA_DATABASE.values():
        for t in data['target_tanaman']:
            # Normalize strings (remove spaces, etc if needed, but simple split is ok)
            # Some entries might be "Padi (Sawah)". Let's just collect all strings.
            t_clean = t.strip()
            all_plants.add(t_clean)
            
    # Add common groupings manually if needed, or just let user search generic
    # Let's clean up the list a bit (e.g. split comma separated if any remained, currently DB is list)
    
    selected_plant_filter = st.selectbox("Tanaman apa yang Anda budidayakan?", sorted(list(all_plants)))
    
    if selected_plant_filter:
        st.subheader(f"Rekomendasi Pestisida Nabati untuk: **{selected_plant_filter}**")
        
        # Filter DB
        found_count = 0
        for nama, data in PESTISIDA_DATABASE.items():
            # Check if selected plant matches any in the target list (substring match usually better for UX)
            # e.g. "Sayuran" should match "Sayuran daun"
            is_match = False
            for t in data['target_tanaman']:
                if selected_plant_filter.lower() in t.lower() or t.lower() in selected_plant_filter.lower():
                    is_match = True
                    break
            
            if is_match:
                found_count += 1
                with st.expander(f"**{nama}** - Target: {', '.join(data['target_hama'])}"):
                    st.caption(f"Kategori: {data['kategori']}")
                    st.write(f"**Bahan Aktif:** {data['bahan_aktif']}")
                    st.write(f"**Cara Buat:** {data['cara_pembuatan'][0]}...")
                    st.write(f"**Aplikasi:** {data['dosis_aplikasi']}")
        
        if found_count == 0:
            st.warning(f"Belum ada data spesifik untuk {selected_plant_filter}. Coba cari berdasarkan hama di tab sebelah.")

# TAB 2: SEARCH BY PEST
with tab2:
    st.header("🎯 Solusi Berdasarkan Hama")
    
    all_pests = set()
    for data in PESTISIDA_DATABASE.values():
        all_pests.update(data['target_hama'])
    
    selected_pest = st.selectbox(
        "Saya punya masalah dengan hama:",
        sorted(list(all_pests))
    )
    
    if selected_pest:
        st.subheader(f"Rekomendasi untuk Hama: **{selected_pest}**")
        for nama, data in PESTISIDA_DATABASE.items():
            if selected_pest in data['target_hama']:
                with st.expander(f"**{nama}** ({data['kategori']})"):
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.markdown(f"**Bahan Aktif:** {data['bahan_aktif']}")
                        st.warning("**Resep:**")
                        for k, v in data['bahan'].items():
                            st.markdown(f"- {k}: {v}")
                    with c2:
                        st.success("**Cara Buat:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(data['cara_pembuatan'])]))
                        st.info(f"**Aplikasi:** {data['dosis_aplikasi']}")

# TAB 3: FULL DATABASE
with tab3:
    st.header("📚 Ensiklopedia Pestisida M-48")
    search = st.text_input("Cari nama tanaman (misal: Gadung, Mimba)...")
    
    col_layout = st.columns(2)
    
    keys = sorted(PESTISIDA_DATABASE.keys())
    for i, nama in enumerate(keys):
        if search.lower() in nama.lower():
            data = PESTISIDA_DATABASE[nama]
            with col_layout[i % 2]:
                with st.container(border=True):
                    st.subheader(nama)
                    st.caption(data['kategori'])
                    st.markdown(f"**Taget:** {', '.join(data['target_hama'])}")
                    with st.expander("Lihat Detail Resep"):
                        st.markdown("**Bahan:**")
                        for k, v in data['bahan'].items():
                            st.write(f"- {k}: {v}")
                        st.markdown("**Pembuatan:**")
                        for step in data['cara_pembuatan']:
                            st.write(f"- {step}")
                        st.markdown(f"**Dosis:** {data['dosis_aplikasi']}")

# TAB 4: CALCULATOR
with tab4:
    st.header("🧮 Kalkulator Aplikasi")
    lahan = st.number_input("Luas Lahan (m2)", 100, 10000, 1000)
    vol = st.number_input("Volume Semprot Biasa (L/ha)", 200, 600, 400)
    ratio = st.slider("Rasio Pengenceran (1 bagian pestisida : X bagian air)", 1, 20, 5)
    
    if st.button("Hitung Kebutuhan"):
        tot, pest, air = calculate_dosage(lahan, vol, ratio)
        st.success(f"Anda butuh **{pest:.1f} Liter** ekstrak pestisida nabati dicampur dengan **{air:.1f} Liter** air.")


st.markdown("---")
st.caption("Sumber Data: Balai Penelitian Tanaman Sayuran (2008) - Modul M-48")
