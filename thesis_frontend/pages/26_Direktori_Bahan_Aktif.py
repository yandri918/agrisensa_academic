# Direktori Bahan Aktif Pestisida
# Module 26 - Comprehensive Pesticide Active Ingredient Directory
# Version: 1.1.0 (Updated with Botanical Ingredients)
# Based on: WHO, FAO, EPA, and peer-reviewed scientific journals

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Direktori Bahan Aktif Pestisida", page_icon="🔬", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ==========================================
# ACTIVE INGREDIENT DATABASE
# ==========================================
# Data compiled from WHO Pesticide Specifications, FAO guidelines, and scientific literature

ACTIVE_INGREDIENTS = {
    # --- BOTANICALS (NEW) ---
    "Azadirachtin": {
        "category": "Botanical",
        "chemical_class": "Limonoid (Tetranortriterpenoid)",
        "cas_number": "11141-17-6",
        "mode_of_action": "Antifeedant, IGR (Insect Growth Regulator), Repellent",
        "moa_detail": "Mengganggu sistem hormonal (ecdysone) serangga, menghambat pergantian kulit (molting), dan mengurangi nafsu makan.",
        "target_pests": "Ulat, wereng, kutu daun, lalat putih, thrips",
        "crops": "Padi, sayuran, palawija, tanaman hias",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "0-3 hari",
        "environmental_fate": "Biodegradable, cepat terurai oleh sinar UV (waktu paruh < 4 hari). Aman untuk cacing tanah.",
        "safety_precautions": "Relatif aman, namun hindari kontak mata langsung. Aman bagi musuh alami.",
        "resistance_risk": "Sangat Rendah (mekanisme kompleks menyulitkan resistensi)",
        "references": "Mordue (Luntz) & Blackwell (1993), Schmutterer (1990)"
    },
    
    "Rotenon": {
        "category": "Botanical",
        "chemical_class": "Isoflavonoid",
        "cas_number": "83-79-4",
        "mode_of_action": "Respiration inhibitor (Mitochondrial Complex I)",
        "moa_detail": "Menghambat transport elektron pada mitokondria, menyebabkan kegagalan produksi energi (ATP) dan kelumpuhan saraf.",
        "target_pests": "Ikan liar (piscicide), ulat, kutu, kumbang",
        "crops": "Sayuran, tambak (persiapan lahan)",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "132-1500 mg/kg (tikus)",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "1-3 hari (cepat terurai)",
        "environmental_fate": "Sangat toksik bagi ikan dan kehidupan air. Cepat terurai oleh cahaya dan udara.",
        "safety_precautions": "Sangat berbahaya bagi ikan! Jangan gunakan dekat perairan alami. Gunakan masker.",
        "resistance_risk": "Rendah",
        "references": "O'Brien (2014), EPA (2007)"
    },

    "Eugenol": {
        "category": "Botanical",
        "chemical_class": "Phenylpropene (Minyak Atsiri)",
        "cas_number": "97-53-0",
        "mode_of_action": "Neurotoxin (Octopamine blocker), Membrane disruptor",
        "moa_detail": "Merusak membran sel jamur/bakteri dan memblokir reseptor octopamine pada serangga.",
        "target_pests": "Jamur (fungisida), bakteri, serangga gudang, nyamuk",
        "crops": "Cengkeh, penyimpanan benih, sayuran",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": "2680 mg/kg (tikus)",
        "ld50_dermal": "Aman (iritasi ringan)",
        "phi": "0-1 hari",
        "environmental_fate": "Volatil (mudah menguap), residu sangat rendah.",
        "safety_precautions": "Dapat menyebabkan iritasi kulit/mata pada konsentrasi tinggi.",
        "resistance_risk": "Rendah",
        "references": "Rani et al. (2018)"
    },

    "Pyrethrin": {
        "category": "Botanical",
        "chemical_class": "Pyrethroid (Alami)",
        "cas_number": "8003-34-7",
        "mode_of_action": "Sodium channel modulator (Knock-down effect)",
        "moa_detail": "Menjaga saluran natrium tetap terbuka, menyebabkan eksitasi saraf berulang dan kelumpuhan instan.",
        "target_pests": "Nyamuk, lalat, semut, kutu daun, ulat (semua serangga lunak)",
        "crops": "Hortikultura, tanaman hias, rumah tangga",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "1030 mg/kg (tikus)",
        "ld50_dermal": ">1500 mg/kg",
        "phi": "0-1 hari",
        "environmental_fate": "Sangat cepat terurai oleh sinar matahari (photodegradable). Toksik bagi ikan.",
        "safety_precautions": "Aplikasi sore hari. Bahaya bagi ikan dan lebah (kontak langsung).",
        "resistance_risk": "Sedang (jika digunakan berlebihan tanpa rotasi)",
        "references": "Casida (1980)"
    },

    "Nicotine": {
        "category": "Botanical",
        "chemical_class": "Alkaloid",
        "cas_number": "54-11-5",
        "mode_of_action": "Nicotinic acetylcholine receptor agonist",
        "moa_detail": "Meniru acetylcholine di sinaps saraf, menyebabkan kejang hebat lalu kelumpuhan.",
        "target_pests": "Thrips, kutu daun, ulat, serangga penghisap",
        "crops": "Tembakau, sayuran (hati-hati residu)",
        "toxicity_class": "WHO Class Ib (Highly Hazardous)",
        "ld50_oral": "50 mg/kg (tikus) - Sangat Toksik!",
        "ld50_dermal": "50 mg/kg (mudah terserap kulit)",
        "phi": "7-14 hari (persisten)",
        "environmental_fate": "Cukup stabil. Berbahaya bagi mamalia dan burung.",
        "safety_precautions": "SANGAT BERBAHAYA. Wajib APD lengkap (masker, sarung tangan). Jangan kena kulit.",
        "resistance_risk": "Sedang",
        "references": "Tomizawa & Casida (2003)"
    },

    "Capsaicin": {
        "category": "Botanical",
        "chemical_class": "Capsaicinoid",
        "cas_number": "404-86-4",
        "mode_of_action": "Repellent, Metabolic disrupter",
        "moa_detail": "Iritasi kuat pada jaringan lunak dan saraf sensorik. Mengganggu metabolisme serangga.",
        "target_pests": "Hama vertebrata (tikus, tupai), serangga umum",
        "crops": "Semua tanaman",
        "toxicity_class": "WHO Class U (Tapi iritan kuat)",
        "ld50_oral": "118 mg/kg (tikus)",
        "ld50_dermal": ">512 mg/kg",
        "phi": "0-1 hari",
        "environmental_fate": "Biodegradable.",
        "safety_precautions": "Hindari kontak mata/kulit. Menyebabkan rasa panas terbakar.",
        "resistance_risk": "Rendah",
        "references": "Cater (2009)"
    },

    "Citronellal": {
        "category": "Botanical",
        "chemical_class": "Monoterpenoid (Minyak Atsiri)",
        "cas_number": "106-23-0",
        "mode_of_action": "Repellent",
        "moa_detail": "Mengganggu reseptor penciuman serangga, mencegah mereka menemukan inang.",
        "target_pests": "Nyamuk, lalat, kutu",
        "crops": "Hias, pekarangan",
        "toxicity_class": "WHO Class U",
        "ld50_oral": "2420 mg/kg",
        "ld50_dermal": ">2500 mg/kg",
        "phi": "0 hari",
        "environmental_fate": "Sangat volatil.",
        "safety_precautions": "Aman. Bisa menyebabkan iritasi mata.",
        "resistance_risk": "Rendah",
        "references": "Trongtokit et al. (2005)"
    },
    
    "Andrographolide": {
        "category": "Botanical",
        "chemical_class": "Diterpenoid Lactone",
        "cas_number": "5508-58-7",
        "mode_of_action": "Antifeedant, Chemosterilant",
        "moa_detail": "Sangat pahit, mencegah serangga makan. Dapat mengganggu kesuburan serangga.",
        "target_pests": "Ulat pemakan daun, penggerek",
        "crops": "Sayuran",
        "toxicity_class": "WHO Class U",
        "ld50_oral": ">1000 mg/kg",
        "ld50_dermal": "Aman",
        "phi": "1-3 hari",
        "environmental_fate": "Cepat terurai.",
        "safety_precautions": "Rasa sangat pahit.",
        "resistance_risk": "Rendah",
        "references": "Hermawan et al. (1997)"
    },

    # --- SYNTHETICS (EXISTING) ---
    # INSECTICIDES - ORGANOPHOSPHATES
    "Klorpirifos": {
        "category": "Insektisida",
        "chemical_class": "Organofosfat",
        "cas_number": "2921-88-2",
        "mode_of_action": "Acetylcholinesterase inhibitor",
        "moa_detail": "Menghambat enzim acetylcholinesterase, menyebabkan akumulasi acetylcholine di sinaps saraf",
        "target_pests": "Wereng, penggerek batang, ulat, trips, kutu daun",
        "crops": "Padi, jagung, sayuran, buah",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "135-163 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg (tikus)",
        "phi": "14-21 hari",
        "environmental_fate": "Persistensi sedang di tanah (DT50: 10-120 hari), dapat mencemari air permukaan",
        "safety_precautions": "Gunakan APD lengkap, hindari kontak kulit, jangan aplikasi dekat sumber air",
        "resistance_risk": "Tinggi - rotasi dengan bahan aktif berbeda sangat dianjurkan",
        "references": "WHO (2009), EPA (2020)"
    },
    
    "Profenofos": {
        "category": "Insektisida",
        "chemical_class": "Organofosfat",
        "cas_number": "41198-08-7",
        "mode_of_action": "Acetylcholinesterase inhibitor",
        "moa_detail": "Menghambat enzim acetylcholinesterase pada sistem saraf serangga",
        "target_pests": "Penggerek buah, ulat grayak, trips, kutu daun",
        "crops": "Cabai, tomat, bawang, kubis",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "358 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg (kelinci)",
        "phi": "7-14 hari",
        "environmental_fate": "Persistensi rendah-sedang (DT50: 1-7 hari di tanah)",
        "safety_precautions": "Gunakan masker dan sarung tangan, hindari inhalasi",
        "resistance_risk": "Tinggi",
        "references": "FAO/WHO (2011)"
    },
    
    # INSECTICIDES - PYRETHROIDS
    "Sipermetrin": {
        "category": "Insektisida",
        "chemical_class": "Piretroid",
        "cas_number": "52315-07-8",
        "mode_of_action": "Sodium channel modulator",
        "moa_detail": "Mengganggu saluran sodium pada membran sel saraf, menyebabkan paralisis",
        "target_pests": "Ulat, wereng, trips, lalat buah, kutu",
        "crops": "Padi, jagung, sayuran, buah, kapas",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "247-4123 mg/kg (tikus, tergantung isomer)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "3-7 hari",
        "environmental_fate": "Sangat toksik untuk ikan dan lebah, persistensi rendah (DT50: 8-16 hari)",
        "safety_precautions": "Jangan aplikasi dekat perairan, hindari saat lebah aktif",
        "resistance_risk": "Tinggi - sudah banyak kasus resistensi",
        "references": "WHO (2018), Nauen (2007)"
    },
    
    "Deltametrin": {
        "category": "Insektisida",
        "chemical_class": "Piretroid",
        "cas_number": "52918-63-5",
        "mode_of_action": "Sodium channel modulator",
        "moa_detail": "Modulator saluran sodium, mengganggu transmisi impuls saraf",
        "target_pests": "Ulat, wereng, trips, kutu daun, lalat buah",
        "crops": "Padi, jagung, sayuran, buah, kapas",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "135 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "3-7 hari",
        "environmental_fate": "Sangat toksik untuk ikan dan organisme akuatik, persistensi rendah",
        "safety_precautions": "Hindari aplikasi dekat sumber air, gunakan APD",
        "resistance_risk": "Tinggi",
        "references": "WHO (2019)"
    },
    
    # INSECTICIDES - NEONICOTINOIDS
    "Imidakloprid": {
        "category": "Insektisida",
        "chemical_class": "Neonikotinoid",
        "cas_number": "138261-41-3",
        "mode_of_action": "Nicotinic acetylcholine receptor agonist",
        "moa_detail": "Berikatan dengan reseptor nikotinik acetylcholine, menyebabkan overstimulasi dan paralisis",
        "target_pests": "Wereng, kutu daun, trips, penggerek, lalat putih",
        "crops": "Padi, jagung, sayuran, buah, kapas",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "450 mg/kg (tikus)",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "7-14 hari",
        "environmental_fate": "Persistensi tinggi di tanah (DT50: 40-997 hari), toksik untuk lebah",
        "safety_precautions": "Hindari aplikasi saat pembungaan, jangan gunakan dekat sarang lebah",
        "resistance_risk": "Sedang-Tinggi",
        "references": "Jeschke et al. (2011), Simon-Delso et al. (2015)"
    },
    
    "Tiametoksam": {
        "category": "Insektisida",
        "chemical_class": "Neonikotinoid",
        "cas_number": "153719-23-4",
        "mode_of_action": "Nicotinic acetylcholine receptor agonist",
        "moa_detail": "Agonis reseptor nikotinik, mengganggu transmisi saraf serangga",
        "target_pests": "Wereng, kutu daun, trips, lalat putih",
        "crops": "Padi, jagung, sayuran, buah",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "1563 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "7-14 hari",
        "environmental_fate": "Persistensi sedang-tinggi, toksik untuk lebah dan organisme akuatik",
        "safety_precautions": "Hindari aplikasi saat pembungaan, rotasi dengan bahan aktif lain",
        "resistance_risk": "Sedang-Tinggi",
        "references": "Maienfisch et al. (2001)"
    },
    
    # FUNGICIDES - TRIAZOLES
    "Propikonazol": {
        "category": "Fungisida",
        "chemical_class": "Triazol",
        "cas_number": "60207-90-1",
        "mode_of_action": "DMI (Demethylation Inhibitor) - Sterol biosynthesis inhibitor",
        "moa_detail": "Menghambat enzim C14-demethylase dalam biosintesis ergosterol, merusak membran sel jamur",
        "target_pests": "Blast, bercak daun, karat, embun tepung, antraknosa",
        "crops": "Padi, jagung, sayuran, buah, kedelai",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "1517 mg/kg (tikus)",
        "ld50_dermal": ">4000 mg/kg",
        "phi": "14-21 hari",
        "environmental_fate": "Persistensi sedang (DT50: 30-110 hari), mobilitas rendah di tanah",
        "safety_precautions": "Gunakan APD, hindari kontaminasi air",
        "resistance_risk": "Tinggi - rotasi dengan fungisida berbeda kelas wajib",
        "references": "FRAC (2021), Hewitt (1998)"
    },
    
    "Tebukonazol": {
        "category": "Fungisida",
        "chemical_class": "Triazol",
        "cas_number": "107534-96-3",
        "mode_of_action": "DMI - Sterol biosynthesis inhibitor",
        "moa_detail": "Inhibitor biosintesis ergosterol, mengganggu integritas membran sel jamur",
        "target_pests": "Blast, bercak daun, karat, embun tepung",
        "crops": "Padi, jagung, gandum, sayuran",
        "toxicity_class": "WHO Class II (Moderately Hazardous)",
        "ld50_oral": "1700 mg/kg (tikus)",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "14-21 hari",
        "environmental_fate": "Persistensi sedang-tinggi (DT50: 50-365 hari)",
        "safety_precautions": "Gunakan APD lengkap, rotasi dengan fungisida lain",
        "resistance_risk": "Tinggi",
        "references": "FRAC (2021)"
    },
    
    # FUNGICIDES - STROBILURINS
    "Azoksistrobin": {
        "category": "Fungisida",
        "chemical_class": "Strobilurin",
        "cas_number": "131860-33-8",
        "mode_of_action": "QoI (Quinone outside Inhibitor) - Respiration inhibitor",
        "moa_detail": "Menghambat respirasi mitokondria pada kompleks III, menghentikan produksi energi jamur",
        "target_pests": "Blast, bercak daun, embun tepung, antraknosa, karat",
        "crops": "Padi, jagung, sayuran, buah, kedelai",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "7-14 hari",
        "environmental_fate": "Persistensi sedang (DT50: 14-79 hari), toksik untuk ikan",
        "safety_precautions": "Hindari aplikasi dekat perairan, maksimal 2-3 aplikasi per musim",
        "resistance_risk": "Sangat Tinggi - gunakan hanya dalam program rotasi",
        "references": "Bartlett et al. (2002), FRAC (2021)"
    },
    
    # HERBICIDES - GLYPHOSATE
    "Glifosat": {
        "category": "Herbisida",
        "chemical_class": "Glisin tersubstitusi",
        "cas_number": "1071-83-6",
        "mode_of_action": "EPSP synthase inhibitor",
        "moa_detail": "Menghambat enzim EPSP synthase dalam jalur shikimat, menghentikan sintesis asam amino aromatik",
        "target_pests": "Gulma berdaun lebar dan sempit (non-selektif)",
        "crops": "Perkebunan, lahan bera, pra-tanam",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg (tikus)",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "N/A (aplikasi pra-tanam atau non-crop)",
        "environmental_fate": "Persistensi rendah-sedang (DT50: 2-197 hari), terikat kuat di tanah",
        "safety_precautions": "Hindari drift ke tanaman budidaya, gunakan pelindung mata",
        "resistance_risk": "Tinggi - banyak gulma resisten, rotasi mode of action penting",
        "references": "Duke & Powles (2008), Heap (2021)"
    },
    
    # HERBICIDES - ALS INHIBITORS
    "Bispiribak-sodium": {
        "category": "Herbisida",
        "chemical_class": "Pyrimidinyl carboxy",
        "cas_number": "125401-92-5",
        "mode_of_action": "ALS inhibitor (Acetolactate synthase)",
        "moa_detail": "Menghambat enzim ALS, menghentikan sintesis asam amino rantai cabang (valine, leucine, isoleucine)",
        "target_pests": "Gulma berdaun lebar dan teki pada padi",
        "crops": "Padi sawah",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "60 hari",
        "environmental_fate": "Persistensi rendah (DT50: 1-10 hari di air)",
        "safety_precautions": "Aplikasi hanya pada padi, hindari drift ke tanaman sensitif",
        "resistance_risk": "Tinggi - rotasi dengan herbisida berbeda mode of action",
        "references": "Heap (2021), Senseman (2007)"
    },
    
    # BIOLOGICAL PESTICIDES
    "Bacillus thuringiensis (Bt)": {
        "category": "Bioinsektisida",
        "chemical_class": "Mikroba (Bakteri)",
        "cas_number": "N/A",
        "mode_of_action": "Midgut membrane disruption",
        "moa_detail": "Protein kristal Cry toxin mengikat reseptor di usus serangga, membentuk pori dan menyebabkan lisis sel",
        "target_pests": "Ulat (Lepidoptera), larva nyamuk (strain tertentu)",
        "crops": "Sayuran, jagung, padi, buah",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "0 hari (dapat dipanen segera)",
        "environmental_fate": "Degradasi cepat oleh UV dan mikroba, tidak persisten",
        "safety_precautions": "Aman untuk manusia dan lingkungan, aplikasi sore hari lebih efektif",
        "resistance_risk": "Sedang - rotasi strain Bt dianjurkan",
        "references": "Bravo et al. (2011), Sanahuja et al. (2011)"
    },
    
    "Beauveria bassiana": {
        "category": "Biofungisida/Bioinsektisida",
        "chemical_class": "Mikroba (Jamur Entomopatogen)",
        "cas_number": "N/A",
        "mode_of_action": "Contact infection and colonization",
        "moa_detail": "Spora menempel pada kutikula serangga, berkecambah, penetrasi, dan mengkolonisasi hemolimf",
        "target_pests": "Trips, kutu daun, lalat putih, penggerek, wereng",
        "crops": "Sayuran, buah, tanaman hias",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": ">5000 mg/kg",
        "ld50_dermal": ">5000 mg/kg",
        "phi": "0 hari",
        "environmental_fate": "Aman untuk lingkungan, dapat bertahan di tanah sebagai saprofit",
        "safety_precautions": "Aman, hindari inhalasi spora dalam jumlah besar",
        "resistance_risk": "Rendah",
        "references": "Faria & Wraight (2007)"
    },
    
    # PLANT GROWTH REGULATORS
    "Paklobutrazol": {
        "category": "Plant Growth Regulator",
        "chemical_class": "Triazol",
        "cas_number": "76738-62-0",
        "mode_of_action": "Gibberellin biosynthesis inhibitor",
        "moa_detail": "Menghambat biosintesis gibberellin, mengurangi pemanjangan sel dan pertumbuhan vegetatif",
        "target_pests": "N/A (bukan pestisida, pengatur pertumbuhan)",
        "crops": "Mangga, buah, tanaman hias",
        "toxicity_class": "WHO Class U (Unlikely to present acute hazard)",
        "ld50_oral": "1300 mg/kg (tikus)",
        "ld50_dermal": ">2000 mg/kg",
        "phi": "Tergantung komoditas",
        "environmental_fate": "Persistensi tinggi di tanah (DT50: 1-3 tahun)",
        "safety_precautions": "Gunakan dosis tepat, overdosis dapat merusak tanaman",
        "resistance_risk": "N/A",
        "references": "Rademacher (2000)"
    }
}

# ========== HELPER FUNCTIONS ==========

def get_categories():
    return sorted(list(set([v["category"] for v in ACTIVE_INGREDIENTS.values()])))

def get_chemical_classes():
    return sorted(list(set([v["chemical_class"] for v in ACTIVE_INGREDIENTS.values()])))

def get_toxicity_classes():
    return sorted(list(set([v["toxicity_class"] for v in ACTIVE_INGREDIENTS.values()])))

def filter_ingredients(category=None, chemical_class=None, toxicity=None, search_term=None):
    filtered = {}
    for name, data in ACTIVE_INGREDIENTS.items():
        if category and category != "Semua" and data["category"] != category:
            continue
        if chemical_class and chemical_class != "Semua" and data["chemical_class"] != chemical_class:
            continue
        if toxicity and toxicity != "Semua" and data["toxicity_class"] != toxicity:
            continue
        if search_term:
            search_lower = search_term.lower()
            if not (search_lower in name.lower() or 
                   search_lower in data["target_pests"].lower() or
                   search_lower in data["moa_detail"].lower()):
                continue
        filtered[name] = data
    return filtered

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #7c3aed;
        text-align: center;
        margin-bottom: 1rem;
    }
    .ingredient-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #7c3aed;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ingredient-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #7c3aed;
        margin-bottom: 0.5rem;
    }
    .cas-number {
        font-size: 0.9rem;
        color: #6b7280;
        font-family: monospace;
    }
    .toxicity-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .tox-class-1 { background: #fee2e2; color: #991b1b; }
    .tox-class-2 { background: #fed7aa; color: #9a3412; }
    .tox-class-3 { background: #fef3c7; color: #92400e; }
    .tox-class-u { background: #d1fae5; color: #065f46; }
    .botanical-badge { background: #dcfce7; color: #166534; border: 1px solid #166534; }
    .moa-box {
        background: #f3e8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #7c3aed;
        margin: 1rem 0;
    }
    .safety-warning {
        background: #fef3c7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #f59e0b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<h1 class="main-header">🔬 Direktori Bahan Aktif Pestisida</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Panduan lengkap bahan aktif pestisida (Kimia & Nabati) berdasarkan WHO, FAO, EPA, dan jurnal ilmiah terpercaya</p>', unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 🔍 Filter Pencarian")
    
    search_term = st.text_input("🔎 Cari Bahan Aktif", placeholder="Nama, hama, atau mode of action...")
    
    categories = ["Semua"] + get_categories()
    selected_category = st.selectbox("Kategori", categories)
    
    chemical_classes = ["Semua"] + get_chemical_classes()
    selected_class = st.selectbox("Kelas Kimia", chemical_classes)
    
    toxicity_classes = ["Semua"] + get_toxicity_classes()
    selected_toxicity = st.selectbox("Kelas Toksisitas WHO", toxicity_classes)
    
    st.markdown("---")
    st.markdown("### 📊 Statistik")
    st.metric("Total Bahan Aktif", len(ACTIVE_INGREDIENTS))
    
    st.markdown("---")
    st.markdown("### ℹ️ Kelas Toksisitas WHO")
    st.markdown("""
    - **Class Ia**: Extremely Hazardous
    - **Class Ib**: Highly Hazardous
    - **Class II**: Moderately Hazardous
    - **Class III**: Slightly Hazardous
    - **Class U**: Unlikely to present acute hazard
    """)

# ========== MAIN CONTENT ==========

filtered = filter_ingredients(
    category=selected_category if selected_category != "Semua" else None,
    chemical_class=selected_class if selected_class != "Semua" else None,
    toxicity=selected_toxicity if selected_toxicity != "Semua" else None,
    search_term=search_term if search_term else None
)

st.markdown(f"### Menampilkan {len(filtered)} bahan aktif")

if len(filtered) == 0:
    st.warning("Tidak ada bahan aktif yang sesuai dengan filter Anda.")
else:
    tabs = st.tabs(["📖 Direktori", "📊 Analisis", "🛡️ Keamanan", "📚 Referensi"])
    
    # TAB 1: DIRECTORY
    with tabs[0]:
        for name, data in filtered.items():
            
            # Custom styling for card
            st.markdown(f"""
            <div class="ingredient-card">
                <div class="ingredient-name">{name} {"🌿" if data['category'] == "Botanical" else "🧪"}</div>
                <div class="cas-number">CAS: {data['cas_number']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Kategori:** {data['category']}")
                st.markdown(f"**Kelas Kimia:** {data['chemical_class']}")
                
                st.markdown('<div class="moa-box">', unsafe_allow_html=True)
                st.markdown(f"**Mode of Action:** {data['mode_of_action']}")
                st.markdown(f"*{data['moa_detail']}*")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f"**Target Hama/Penyakit:** {data['target_pests']}")
                st.markdown(f"**Tanaman:** {data['crops']}")
                
            with col2:
                # Toxicity badge
                tox_class = data['toxicity_class']
                if "Class II" in tox_class:
                    badge_class = "tox-class-2"
                elif "Class U" in tox_class:
                    badge_class = "tox-class-u"
                elif "Class III" in tox_class:
                    badge_class = "tox-class-3"
                else:
                    badge_class = "tox-class-1"
                
                st.markdown(f'<span class="toxicity-badge {badge_class}">{tox_class}</span>', unsafe_allow_html=True)
                
                st.markdown(f"**LD50 Oral:** {data['ld50_oral']}")
                st.markdown(f"**LD50 Dermal:** {data['ld50_dermal']}")
                st.markdown(f"**PHI:** {data['phi']}")
                st.markdown(f"**Risiko Resistensi:** {data['resistance_risk']}")
            
            with st.expander("🛡️ Keamanan & Lingkungan"):
                st.markdown('<div class="safety-warning">', unsafe_allow_html=True)
                st.markdown(f"**Precautions:** {data['safety_precautions']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f"**Environmental Fate:** {data['environmental_fate']}")
                st.markdown(f"**Referensi:** {data['references']}")
            
            st.markdown("---")
    
    # TAB 2: ANALYSIS
    with tabs[1]:
        st.markdown("### 📊 Analisis Distribusi")
        
        # Category distribution
        cat_dist = {}
        for data in filtered.values():
            cat = data["category"]
            cat_dist[cat] = cat_dist.get(cat, 0) + 1
        
        fig_cat = px.pie(
            values=list(cat_dist.values()),
            names=list(cat_dist.keys()),
            title="Distribusi Kategori Bahan Aktif"
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
        # Chemical class distribution
        class_dist = {}
        for data in filtered.values():
            cls = data["chemical_class"]
            class_dist[cls] = class_dist.get(cls, 0) + 1
        
        fig_class = px.bar(
            x=list(class_dist.keys()),
            y=list(class_dist.values()),
            title="Distribusi Kelas Kimia",
            labels={"x": "Kelas Kimia", "y": "Jumlah"}
        )
        st.plotly_chart(fig_class, use_container_width=True)
        
        # Toxicity distribution
        tox_dist = {}
        for data in filtered.values():
            tox = data["toxicity_class"]
            tox_dist[tox] = tox_dist.get(tox, 0) + 1
        
        fig_tox = px.bar(
            x=list(tox_dist.keys()),
            y=list(tox_dist.values()),
            title="Distribusi Kelas Toksisitas WHO",
            labels={"x": "Kelas Toksisitas", "y": "Jumlah"},
            color=list(tox_dist.values()),
            color_continuous_scale="RdYlGn_r"
        )
        st.plotly_chart(fig_tox, use_container_width=True)
    
    # TAB 3: SAFETY
    with tabs[2]:
        st.markdown("### 🛡️ Panduan Keamanan Penggunaan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### APD (Alat Pelindung Diri) Wajib
            
            1. **Masker/Respirator**
               - N95 atau P100 untuk formulasi bubuk
               - Cartridge organik untuk formulasi cair
            
            2. **Sarung Tangan**
               - Nitrile atau neoprene
               - Ganti jika robek atau terkontaminasi
            
            3. **Pakaian Pelindung**
               - Coverall tahan kimia
               - Sepatu boot karet
            
            4. **Pelindung Mata**
               - Goggles atau face shield
               - Wajib untuk aplikasi semprot
            
            #### Waktu Aplikasi Aman
            
            - Pagi: 06:00 - 09:00
            - Sore: 15:00 - 18:00
            - Hindari saat angin kencang (>10 km/jam)
            - Hindari saat hujan atau akan hujan
            """)
        
        with col2:
            st.markdown("""
            #### Prosedur Keselamatan
            
            1. **Sebelum Aplikasi**
               - Baca label dengan teliti
               - Periksa APD lengkap
               - Pastikan alat semprot berfungsi baik
               - Jauhkan anak-anak dan hewan
            
            2. **Saat Aplikasi**
               - Jangan makan/minum/merokok
               - Aplikasi searah angin
               - Jaga jarak aman dari sumber air
               - Hindari drift ke tanaman lain
            
            3. **Setelah Aplikasi**
               - Cuci APD terpisah dari pakaian lain
               - Mandi dengan sabun
               - Simpan pestisida di tempat aman
               - Buang kemasan kosong dengan benar
            
            #### Pertolongan Pertama Keracunan
            
            - **Tertelan:** Jangan dimuntahkan, segera ke dokter
            - **Terhirup:** Pindah ke udara segar
            - **Terkena kulit:** Cuci dengan sabun dan air mengalir
            - **Terkena mata:** Bilas dengan air 15 menit
            - **Selalu bawa label ke dokter**
            """)
    
    # TAB 4: REFERENCES
    with tabs[3]:
        st.markdown("### 📚 Referensi Ilmiah")
        
        st.markdown("""
        #### Organisasi Internasional
        
        1. **WHO (World Health Organization)**
           - WHO Recommended Classification of Pesticides by Hazard (2019)
           - WHO Pesticide Specifications
        
        2. **FAO (Food and Agriculture Organization)**
           - FAO/WHO Joint Meeting on Pesticide Specifications (JMPS)
           - International Code of Conduct on Pesticide Management
        
        3. **EPA (Environmental Protection Agency)**
           - Pesticide Product Labels
           - Reregistration Eligibility Decisions (REDs)
        
        4. **FRAC (Fungicide Resistance Action Committee)**
           - FRAC Code List (2021)
           - Fungicide Resistance Management Guidelines
        
        #### Jurnal Ilmiah Utama
        
        1. **Pest Management Science** (Wiley)
        2. **Journal of Agricultural and Food Chemistry** (ACS)
        3. **Pesticide Biochemistry and Physiology** (Elsevier)
        4. **Crop Protection** (Elsevier)
        5. **Journal of Pesticide Science** (Pesticide Science Society of Japan)
        
        #### Database Online
        
        - **PubChem** (NCBI): Chemical structures and properties
        - **PPDB** (Pesticide Properties Database): Environmental fate data
        - **IRAC** (Insecticide Resistance Action Committee): MoA classification
        - **HRAC** (Herbicide Resistance Action Committee): Herbicide classification
        
        #### Buku Referensi
        
        1. **Hayes' Handbook of Pesticide Toxicology** (3rd Ed, 2010)
        2. **The Pesticide Manual** (18th Ed, 2020)
        3. **Crop Protection Compendium** (CABI)
        """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("""
🔬 **Direktori Bahan Aktif Pestisida v1.1** (Updated)

📊 **Sumber Data:** WHO, FAO, EPA, FRAC, IRAC, HRAC, dan jurnal peer-reviewed

⚠️ **Disclaimer:** Informasi ini untuk tujuan edukasi. Selalu ikuti label produk dan konsultasi dengan ahli.
Penggunaan pestisida harus sesuai regulasi setempat dan good agricultural practices (GAP).

🌱 **Prinsip:** Integrated Pest Management (IPM) - gunakan pestisida sebagai pilihan terakhir
""")
