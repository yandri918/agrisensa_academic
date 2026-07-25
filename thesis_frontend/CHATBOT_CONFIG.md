# AgriBot Configuration Guide

## 🔑 Konfigurasi API Key untuk Chatbot

Module 23 (AgriBot AI) memerlukan Google Gemini API Key untuk berfungsi. Berikut cara mengkonfigurasinya:

---

## 📋 Langkah 1: Dapatkan API Key

1. **Kunjungi Google AI Studio:**
   - URL: https://makersuite.google.com/app/apikey
   - Atau: https://aistudio.google.com/app/apikey

2. **Login dengan Google Account**

3. **Create API Key:**
   - Klik "Create API Key"
   - Pilih project atau buat project baru
   - Copy API key yang dihasilkan

**Catatan:** API key Gemini **GRATIS** dengan quota yang cukup besar!

---

## 🚀 Langkah 2: Konfigurasi di Hugging Face Spaces

### Option A: Via Web Interface (Recommended)

1. **Login ke Hugging Face:**
   - https://huggingface.co/

2. **Buka Space Anda:**
   - https://huggingface.co/spaces/YOUR_USERNAME/agrisensa-streamlit

3. **Settings → Repository secrets:**
   - Klik tab "Settings"
   - Scroll ke "Repository secrets"
   - Klik "New secret"

4. **Tambahkan Secret:**
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Paste API key Anda
   - Klik "Add secret"

5. **Restart Space:**
   - Tab "Settings" → "Factory reboot"
   - Atau tunggu auto-restart (1-2 menit)

### Option B: Via `.streamlit/secrets.toml` (Local Testing)

Untuk testing lokal, buat file `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

**PENTING:** File ini sudah ada di `.gitignore`, jangan commit ke repository!

---

## 🧪 Langkah 3: Verifikasi

1. **Buka AgriBot Module:**
   - Klik "🤖 AgriBot AI" di sidebar

2. **Cek Status:**
   - Jika berhasil: Welcome message dari AgriBot muncul
   - Jika gagal: Pesan error "Chatbot tidak tersedia"

3. **Test Chat:**
   - Ketik: "Halo AgriBot"
   - AgriBot harus merespons

---

## 🔍 Troubleshooting

### Error: "Chatbot tidak tersedia"

**Penyebab:**
- API key belum dikonfigurasi
- API key salah
- Package `google-generativeai` belum terinstall

**Solusi:**
1. Pastikan `GEMINI_API_KEY` sudah ditambahkan di Hugging Face secrets
2. Pastikan API key valid (test di Google AI Studio)
3. Restart space setelah menambahkan secret
4. Check logs di tab "Logs" untuk error detail

### Error: "API quota exceeded"

**Penyebab:**
- Quota gratis Gemini habis (jarang terjadi)

**Solusi:**
- Tunggu reset quota (biasanya harian)
- Atau upgrade ke paid tier (jika perlu)

### Error: "Import error: google.generativeai"

**Penyebab:**
- Package belum terinstall

**Solusi:**
- Pastikan `google-generativeai` ada di `requirements.txt` ✅ (sudah ditambahkan)
- Rebuild space

---

## 📊 Quota & Limits (Gemini Free Tier)

- **Requests per minute:** 60
- **Requests per day:** 1,500
- **Tokens per minute:** 32,000

Untuk AgriSensa dengan traffic normal, quota gratis **lebih dari cukup**!

---

## 🔐 Security Best Practices

1. ✅ **Jangan commit API key ke git**
   - Gunakan secrets/environment variables
   - File `.streamlit/secrets.toml` sudah di `.gitignore`

2. ✅ **Gunakan API key restrictions** (optional):
   - Di Google Cloud Console
   - Restrict by HTTP referrer atau IP

3. ✅ **Monitor usage:**
   - Check di Google AI Studio dashboard
   - Set up alerts jika mendekati limit

---

## 🎯 Next Steps

Setelah API key dikonfigurasi:

1. ✅ Test chatbot dengan berbagai pertanyaan
2. ✅ Verifikasi integrasi dengan knowledge base
3. ✅ Monitor response quality
4. ✅ Adjust system prompt jika perlu (di `chatbot_service.py`)

---

## 📝 Notes

- **Chatbot Service:** Menggunakan `ChatbotService` dari Flask app
- **Model:** `gemini-flash-latest` (fast & efficient)
- **System Prompt:** Sudah dikonfigurasi untuk AgriBot persona
- **Knowledge:** Terintegrasi dengan database pestisida nabati, panduan budidaya, dll

**Happy Chatting! 🤖🌱**
