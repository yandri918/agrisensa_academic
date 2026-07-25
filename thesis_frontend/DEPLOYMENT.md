# Deployment Guide: Hugging Face Spaces

## 🚀 Quick Deploy to Hugging Face Spaces (GRATIS!)

### Langkah 1: Persiapan Akun

1. **Buat akun Hugging Face** (jika belum punya)
   - Kunjungi: https://huggingface.co/join
   - Sign up dengan email atau GitHub
   - Verifikasi email

2. **Create New Space**
   - Kunjungi: https://huggingface.co/new-space
   - Space name: `agrisensa-streamlit`
   - License: MIT
   - SDK: **Streamlit**
   - Visibility: Public (gratis) atau Private (berbayar)

### Langkah 2: Upload Files

**Option A: Via Web Interface (Paling Mudah)**

1. Setelah create space, klik "Files and versions"
2. Klik "Add file" → "Upload files"
3. Upload semua file dari folder `agrisensa_streamlit/`:
   ```
   ✅ Home.py
   ✅ requirements.txt
   ✅ README.md
   ✅ pages/1_🌾_Database_Panen.py
   ✅ pages/2_🗺️_Peta_Data_Tanah.py
   ✅ pages/3_🧮_Kalkulator_Pupuk.py
   ✅ pages/4_📊_Analisis_NPK.py
   ✅ pages/5_🔄_Konversi_Pupuk.py
   ```
4. Klik "Commit changes to main"
5. **DONE!** App akan auto-deploy dalam 1-2 menit

**Option B: Via Git (Advanced)**

```bash
# 1. Clone space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/agrisensa-streamlit
cd agrisensa-streamlit

# 2. Copy files
cp -r ../agrisensa_streamlit/* .

# 3. Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Langkah 3: Verifikasi Deployment

1. Tunggu 1-2 menit untuk build
2. Klik tab "App" di Hugging Face Space
3. App akan running di: `https://YOUR_USERNAME-agrisensa-streamlit.hf.space`

### Langkah 4: (Opsional) Custom Domain

Jika ingin custom domain:
1. Upgrade ke Hugging Face Pro ($9/month)
2. Setup custom domain di Space settings
3. Point DNS ke Hugging Face

---

## 🔧 Troubleshooting

### Error: "Application startup failed"

**Solusi:**
1. Check logs di tab "Logs"
2. Pastikan `requirements.txt` benar
3. Pastikan `Home.py` ada di root folder

### Error: "Module not found"

**Solusi:**
1. Tambahkan missing module ke `requirements.txt`
2. Commit changes
3. Wait for rebuild

### Data tidak tersimpan setelah restart

**Ini normal!** Hugging Face Spaces tidak persistent.

**Solusi:**
- Gunakan Hugging Face Datasets untuk storage
- Atau integrate dengan external database (Supabase, Firebase)

---

## 💰 Biaya

| Tier | Cost | Features |
|------|------|----------|
| **Community** | **GRATIS** | 2 CPU, 16GB RAM, Public only |
| Pro | $9/month | 2 CPU, 16GB RAM, Private spaces |
| Enterprise | Custom | Custom resources |

**Untuk AgriSensa:** Community tier sudah cukup! ✅

---

## 📊 Monitoring

1. **View Logs:**
   - Tab "Logs" di Hugging Face Space
   - Real-time application logs

2. **Analytics:**
   - Tab "Analytics" (jika public)
   - View visitor stats

3. **Restart App:**
   - Tab "Settings" → "Factory reboot"
   - Restart jika app hang

---

## 🔄 Update App

**Via Web:**
1. Tab "Files and versions"
2. Edit file atau upload new version
3. Commit → Auto redeploy

**Via Git:**
```bash
git pull
# Make changes
git add .
git commit -m "Update features"
git push
```

---

## 🌟 Tips Optimasi

1. **Caching:**
   ```python
   @st.cache_data
   def load_data():
       # Expensive operation
       return data
   ```

2. **Lazy Loading:**
   - Load data only when needed
   - Use `st.spinner()` for feedback

3. **Optimize Images:**
   - Compress images before upload
   - Use WebP format

---

## 🔗 Useful Links

- **Your Space:** https://huggingface.co/spaces/YOUR_USERNAME/agrisensa-streamlit
- **Docs:** https://huggingface.co/docs/hub/spaces-sdks-streamlit
- **Community:** https://discuss.huggingface.co/

---

## ✅ Checklist Deployment

- [ ] Akun Hugging Face created
- [ ] New Space created (Streamlit SDK)
- [ ] Files uploaded (Home.py + pages + requirements.txt)
- [ ] App running successfully
- [ ] Test all modules
- [ ] Share link dengan tim/users

**Selamat! App Anda sudah online dan gratis! 🎉**
