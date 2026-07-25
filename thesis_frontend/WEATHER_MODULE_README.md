# 🌤️ Modul Cuaca Pertanian (Open-Meteo Version)

Modul cuaca pertanian yang **gratis**, **powerful**, dan **cerdas** menggunakan data **Open-Meteo**. Dilengkapi dengan deteksi musim otomatis untuk mendukung pengguna di seluruh dunia.

## ✨ Fitur Baru (v2.1 - Seasonal Update)

### 1. 🌍 Deteksi Musim & Iklim Otomatis
- Otomatis mendeteksi **Zona Iklim**:
  - Tropis (Indonesia, dll)
  - Sub-Tropis / 4 Musim (Jepang, Eropa, USA)
- Otomatis mendeteksi **Musim Saat Ini**:
  - 🌸 Spring (Semi)
  - ☀️ Summer (Panas)
  - 🍂 Autumn (Gugur)
  - ❄️ Winter (Dingin)
  - 🌧️ Musim Hujan / Kemarau (Tropis)

### 2. 🌾 Insight Pertanian Musiman
Memberikan rekomendasi spesifik berdasarkan musim, contoh:
- **Winter:** Peringatan Frost (beku), saran greenhouse, perlindungan akar.
- **Spring:** Waktu tanam optimal, persiapan tanah.
- **Summer:** Manajemen stress panas, irigasi.
- **Autumn:** Panen raya, planting cover crops.

### 3. ⛰️ Altimeter & Elevasi
- Otomatis mendeteksi ketinggian lahan (mdpl)
- Menentukan kesesuaian tanaman (misal: Kopi Arabika > 1000 mdpl)

### 4. 🌱 Data Tanah & Hujan
- **Suhu & Kelembaban Tanah:** Indikator irigasi presisi.
- **Curah Hujan:** Real-time & forecast harian.

## 🔧 Setup
Tidak butuh API key! 

```bash
pip install streamlit pandas plotly folium streamlit-folium requests
streamlit run pages/27_🌤️_Cuaca_Pertanian.py
```

## 🎯 Cara Penggunaan untuk User di Jepang (4 Musim)

1. **Pilih Lokasi:**
   - Gunakan Preset: Klik tombol **"📍 Set Lokasi: Tokyo, Jepang"**.
   - Atau pilih lokasi manual di peta.
2. **Lihat Insight Musim:**
   - Dashboard akan menampilkan icon musim (misal: ❄️ Winter).
   - Baca bagian "Rekomendasi Agronomi" untuk tips spesifik musim tersebut.

---
**AgriSensa** - Smart Farming Solutions 🌾
