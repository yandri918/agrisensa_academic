# 🛰️ AgriSensa MLOps API

Backend engine berbasis **FastAPI** dan **Docker** yang didedikasikan untuk melayani seluruh model Machine Learning (ML) dan analisis citra daun (BWD) dalam ekosistem **AgriSensa**.

Project ini memisahkan logika komputasi ML berat dari dashboard Streamlit frontend untuk meningkatkan efisiensi penggunaan RAM, kecepatan startup, isolasi kegagalan, dan mempermudah integrasi dengan platform eksternal lainnya.

---

## 🚀 Fitur Utama

1. **Rekomendasi Tanaman (`/api/ml/recommend-crop`)**: Memprediksi komoditas paling cocok berdasarkan input NPK tanah, suhu, kelembaban, pH, dan curah hujan.
2. **Estimasi Hasil Panen (`/api/ml/predict-yield` & `/predict-yield-advanced`)**: Memprediksi tonase panen per hektar (kg/ha ke ton/ha) menggunakan model Random Forest/LightGBM lengkap dengan interpretasi kontribusi fitur menggunakan **SHAP**.
3. **Yield Plan Generator (`/api/ml/generate-yield-plan`)**: Menyusun rencana budidaya detail untuk mencapai target hasil tertentu (NPK, varietas benih, kalkulasi biaya, dan timeline pertumbuhan).
4. **Bags Calculator (`/api/ml/calculate-fertilizer-bags`)**: Menghitung kebutuhan karung pupuk (Urea, SP-36, KCl) untuk menutupi defisit unsur hara tanah.
5. **Success Predictor (`/api/ml/predict-success`)**: Menilai probabilitas kesuksesan budidaya.
6. **Analisis Citra Daun BWD (`/api/analysis/bwd`)**: Menerima unggahan gambar daun, memproses histogram warna hijau menggunakan **OpenCV Headless** untuk menilai kebutuhan Nitrogen, serta mendeteksi bercak coklat/putih untuk indikasi penyakit/hama.
7. **Analisis NPK Tanah (`/api/analysis/npk`)**: Mengklasifikasikan kesuburan tanah berdasarkan standard Balitbang Indonesia.

---

## 🛠️ Tech Stack & Dependencies

* **Language**: Python 3.11+
* **Framework**: FastAPI (Async & OpenAPI/Swagger automatic docs)
* **ML Engines**: Scikit-Learn, LightGBM, Joblib, SHAP
* **Image Processing**: OpenCV-python-headless (dioptimalkan untuk server tanpa GUI)
* **Data Processing**: Pandas, NumPy
* **Deployment**: Docker (Multi-stage/slim build), Uvicorn

---

## ⚙️ Cara Menjalankan Lokal

### 1. Inisiasi Virtual Environment & Dependensi
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment (Windows)
venv\Scripts\activate

# Install dependensi
pip install -r requirements.txt
```

### 2. Jalankan Server FastAPI
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Buka browser dan buka `http://localhost:8000/docs` untuk membuka Swagger UI.

### 3. Jalankan Pengujian Otomatis
```bash
python -m pytest tests/
```

---

## 📦 Docker Containerization

Membangun image Docker secara lokal:
```bash
docker build -t agrisensa-mlops-api .
```

Menjalankan container Docker:
```bash
docker run -p 8000:8000 agrisensa-mlops-api
```
Untuk deployment di platform cloud (Hugging Face Spaces, Railway, Render, AWS, GCP, Azure), port akan disesuaikan otomatis menggunakan environment variable `PORT` yang telah terintegrasi di dalam Dockerfile.
