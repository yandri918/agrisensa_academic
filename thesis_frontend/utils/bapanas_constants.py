
# Constants for Bapanas API Integration

import os
import streamlit as st

# Mapping Commodity Names to Bapanas IDs (level_harga_id=1 for retail?)
# Note: These IDs need to be verified against the actual API response
# but we can infer some from standard ordering or use searching
COMMODITY_MAPPING = {
    "Beras Premium": 2,
    "Beras Medium": 3,
    "Bawang Merah": 12,
    "Bawang Putih": 13, # Bonggol
    "Cabai Merah Keriting": 9,
    "Cabai Rawit Merah": 11,
    "Daging Sapi Murni": 16,
    "Daging Ayam Ras": 18,
    "Telur Ayam Ras": 19,
    "Gula Pasir": 7, # Konsumsi
    "Minyak Goreng Kemasan": 23, # Sederhana
    "Tepung Terigu": 5, # Curah
    "Kedelai": 6, # Biji Kering Impir
    "Jagung": 28 # Pipilan Kering
}

# Mapping Province Names to IDs
PROVINCE_MAPPING = {
    "Nasional": 0, # Usually 0 or just params omitted implies national average
    "Aceh": 1,
    "Sumatera Utara": 2,
    "Sumatera Barat": 3,
    "Riau": 4,
    "Jambi": 5,
    "Sumatera Selatan": 6,
    "Bengkulu": 7,
    "Lampung": 8,
    "Kepulauan Bangka Belitung": 9,
    "Kepulauan Riau": 10,
    "DKI Jakarta": 11,
    "Jawa Barat": 12,
    "Jawa Tengah": 13,
    "DI Yogyakarta": 14,
    "Jawa Timur": 15,
    "Banten": 16,
    "Bali": 17,
    "Nusa Tenggara Barat": 18,
    "Nusa Tenggara Timur": 19,
    "Kalimantan Barat": 20,
    "Kalimantan Tengah": 21,
    "Kalimantan Selatan": 22,
    "Kalimantan Timur": 23,
    "Kalimantan Utara": 24,
    "Sulawesi Utara": 25,
    "Sulawesi Tengah": 26,
    "Sulawesi Selatan": 27,
    "Sulawesi Tenggara": 28,
    "Gorontalo": 29,
    "Sulawesi Barat": 30,
    "Maluku": 31,
    "Maluku Utara": 32,
    "Papua Barat": 33,
    "Papua": 34
}

# Add reverse mapping for easy lookup
ID_TO_COMMODITY = {v: k for k, v in COMMODITY_MAPPING.items()}
ID_TO_PROVINCE = {v: k for k, v in PROVINCE_MAPPING.items()}

# Secure API Key Loading
def get_bapanas_key():
    # Priority 1: Streamlit Secrets (Cloud/Local)
    try:
        return st.secrets["BAPANAS_API_KEY"]
    except:
        pass
    
    # Priority 2: OS Environment Variable
    if "BAPANAS_API_KEY" in os.environ:
        return os.environ["BAPANAS_API_KEY"]
        
    # Priority 3: Fallback (Empty/Warning)
    # DO NOT COMMIT REAL KEYS HERE
    return ""

API_CONFIG = {
    "BASE_URL": "https://api-panelhargav2.badanpangan.go.id/api/front",
    "HEADERS": {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Connection": "keep-alive",
        "Host": "api-panelhargav2.badanpangan.go.id",
        "Origin": "https://panelharga.badanpangan.go.id",
        "Referer": "https://panelharga.badanpangan.go.id/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-API-KEY": get_bapanas_key()
    }
}
