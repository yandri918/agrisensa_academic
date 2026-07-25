# 🌾 AgriSensa MLOps Pipeline

> **Tesis S2 — Arsitektur MLOps Skalabel untuk Pertanian Presisi di Pulau Jawa**

[![MLOps CI/CD Pipeline](https://github.com/yandri918/agrisensa_academic/actions/workflows/mlops.yml/badge.svg)](https://github.com/yandri918/agrisensa_academic/actions/workflows/mlops.yml)

---

## 📋 Deskripsi Proyek

AgriSensa adalah sistem berbasis MLOps untuk prediksi hasil panen (*yield*), rekomendasi tanaman (*crop recommendation*), dan prediksi harga komoditas pertanian di Pulau Jawa (cabai, padi, jagung, bawang merah, tomat, sayuran).

Proyek ini mengimplementasikan pipeline MLOps lengkap dengan **Continuous Training (CT)** — setiap kali ada perubahan kode atau parameter, model ML otomatis dilatih ulang melalui GitHub Actions.

---

## 🏗️ Arsitektur MLOps

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│                                                             │
│  git push  →  GitHub Actions (CI/CD)  →  DVC Pipeline      │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │Preprocess│ → │  Train   │ → │ Evaluate │               │
│  └──────────┘   └──────────┘   └──────────┘               │
│       ↑                ↑              ↓                     │
│  DagsHub           MLflow         evaluation.json          │
│  (Remote Storage)  (Tracking)     (Artifacts)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Struktur Direktori

```
agrisensa-thesis-mlops/
│
├── .github/
│   └── workflows/
│       └── mlops.yml          # CI/CD GitHub Actions
│
├── mlops_backend/
│   ├── pipeline/
│   │   ├── .dvc/              # Konfigurasi DVC (remote: DagsHub)
│   │   ├── data/
│   │   │   └── raw/           # Dataset mentah
│   │   │       ├── yield.csv                        # Data hasil panen
│   │   │       ├── Crop_recommendation.csv          # Data rekomendasi tanaman
│   │   │       └── synthetic_crop_prices_java.csv   # Data harga komoditas
│   │   ├── src/               # Script Python pipeline
│   │   │   ├── preprocess.py       # Preproses yield
│   │   │   ├── train.py            # Training yield model
│   │   │   ├── evaluate.py         # Evaluasi yield model
│   │   │   ├── preprocess_crop.py  # Preproses crop
│   │   │   ├── train_crop.py       # Training crop model
│   │   │   ├── evaluate_crop.py    # Evaluasi crop model
│   │   │   ├── preprocess_price.py # Preproses harga
│   │   │   ├── train_price.py      # Training price model
│   │   │   └── evaluate_price.py   # Evaluasi price model
│   │   ├── dvc.yaml           # Definisi DAG pipeline
│   │   └── params.yaml        # Hyperparameter & konfigurasi
│   │
│   ├── routes/                # FastAPI endpoints
│   ├── services/              # Business logic
│   └── requirements.txt       # Dependencies Python
│
├── thesis_frontend/           # Dashboard Streamlit
├── models_registry/           # Penyimpanan model .pkl
└── README.md
```

---

## 🤖 Model Machine Learning

| Model | Algoritma | Target | Metrik |
|-------|-----------|--------|--------|
| **Yield Model** | RandomForestRegressor | Prediksi hasil panen (ton/ha) | MSE, RMSE, R² |
| **Crop Model** | RandomForestClassifier | Rekomendasi jenis tanaman | Accuracy, F1-Score |
| **Price Model** | RandomForestRegressor | Prediksi harga komoditas (Rp) | MAE, RMSE, R² |

### Hyperparameter (dari `params.yaml`)

| Parameter | Yield | Crop | Price |
|-----------|-------|------|-------|
| `n_estimators` | 150 | 100 | 100 |
| `max_depth` | 20 | 15 | 15 |
| `test_size` | 0.2 | 0.2 | 0.2 |
| `random_state` | 42 | 42 | 42 |

---

## ⚙️ Pipeline DVC (DAG)

```
yield.csv ──→ preprocess ──→ train ──→ evaluate
                                            ↓
                                    evaluation.json

Crop_recommendation.csv ──→ preprocess_crop ──→ train_crop ──→ evaluate_crop
                                                                      ↓
                                                           evaluation_crop.json

synthetic_crop_prices_java.csv ──→ preprocess_price ──→ train_price ──→ evaluate_price
                                                                               ↓
                                                                  evaluation_price.json
```

---

## 🚀 Cara Menjalankan

### Prerequisites
```bash
pip install dvc pandas scikit-learn mlflow pyyaml joblib
```

### Jalankan Pipeline Lokal
```bash
cd mlops_backend/pipeline

# Pertama kali — init DVC
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <dagshub_username>
dvc remote modify origin --local password <dagshub_token>

# Jalankan seluruh pipeline
dvc repro
```

### Ubah Hyperparameter & Retrain
```bash
# Edit params.yaml, misalnya:
# train:
#   n_estimators: 200   ← ubah ini

# Lalu jalankan ulang
dvc repro
```

### Lihat Metrik
```bash
dvc metrics show
```

---

## 🔄 CI/CD — Continuous Training

Setiap kali `git push` ke branch `main`:

1. **GitHub Actions** otomatis berjalan
2. **Install dependencies** (scikit-learn, mlflow, dvc, dll.)
3. **Configure DVC** dengan token DagsHub dari GitHub Secrets
4. **`dvc repro --force`** — semua stage dijalankan ulang:
   - Preprocess 3 dataset
   - Train 3 model
   - Evaluate & simpan metrik
5. **Upload Artifacts** — file `evaluation.json` tersimpan 30 hari di GitHub Actions

### Cara Mengakses Hasil Evaluasi
1. Buka tab **Actions** di GitHub repo
2. Klik run terbaru (✅ centang hijau)
3. Scroll ke bagian **Artifacts**
4. Download **`evaluation-metrics`** (berisi 3 file JSON)

---

## 🔐 GitHub Secrets yang Diperlukan

| Secret | Deskripsi |
|--------|-----------|
| `DAGSHUB_USER_TOKEN` | Token akses DagsHub untuk DVC remote storage |

---

## 🔗 Tautan Penting

- **GitHub Repo:** https://github.com/yandri918/agrisensa_academic
- **DagsHub (DVC Remote):** https://dagshub.com/yandri918/agrisensa_academic

---

## 🛠️ Teknologi

| Kategori | Tools |
|----------|-------|
| **Data Versioning** | DVC + DagsHub |
| **Experiment Tracking** | MLflow |
| **CI/CD** | GitHub Actions |
| **ML Framework** | Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **API Backend** | FastAPI |
| **Frontend** | Streamlit |
| **Model Serialization** | Joblib |

---

## 📊 Hasil Evaluasi Terakhir (dari GitHub Actions)

> Lihat artifact **`evaluation-metrics`** di tab Actions untuk hasil terbaru.

| Model | Metrik Utama |
|-------|-------------|
| Yield | R² ≈ 0.79 |
| Crop | Accuracy ≈ 99.5% |
| Price | Lihat artifact |

---

*Proyek ini merupakan bagian dari penelitian Tesis S2 mengenai implementasi arsitektur MLOps untuk sistem pertanian presisi.*
