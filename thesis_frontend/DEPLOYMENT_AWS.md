# AWS Deployment Guide: AgriSensa Streamlit

Panduan ini berisi langkah-langkah detail untuk men-deploy aplikasi Streamlit **AgriSensa** ke Amazon Web Services (AWS). Kami merekomendasikan **AWS App Runner** sebagai metode utama karena sangat mudah, otomatis mengelola SSL (HTTPS), dan dapat terhubung langsung dengan GitHub. Alternatif lainnya adalah menggunakan **AWS EC2** jika Anda ingin kendali penuh dan masuk dalam Free Tier.

---

## 🚀 Opsi 1: AWS App Runner (Sangat Direkomendasikan ⭐)

AWS App Runner adalah layanan managed container yang secara otomatis membangun dan men-deploy aplikasi web dari repository GitHub atau container registry (ECR).

### Kelebihan:
- Auto-scaling terkelola.
- SSL (HTTPS) gratis dan terintegrasi secara otomatis.
- Terhubung langsung ke Git (otomatis deploy ulang saat Anda melakukan `git push`).
- Tidak perlu mengelola server (patching, OS updates, dll.).

### Langkah-langkah:

1. **Push Proyek Streamlit ke GitHub**
   Pastikan folder `agrisensa_streamlit` Anda sudah di-push ke repository GitHub Anda (baik public maupun private). Pastikan [Dockerfile](file:///c:/Users/yandr/OneDrive/Desktop/agrisensa-api/agrisensa_streamlit/Dockerfile) yang telah kita buat berada di dalam repositori tersebut.

2. **Buka AWS Console & Cari App Runner**
   - Masuk ke AWS Management Console Anda.
   - Cari **App Runner** pada kolom pencarian dan klik **Create an App Runner service**.

3. **Konfigurasi Source dan Trigger**
   - **Repository type**: Pilih **Source code repository**.
   - **Connection**: Klik **Add new** untuk menghubungkan AWS dengan akun GitHub Anda (instal AWS Connector for GitHub).
   - **Repository**: Pilih repository AgriSensa Anda.
   - **Branch**: Pilih branch utama Anda (misalnya: `main` atau `master`).
   - **Deployment settings**: Pilih **Automatic** (untuk auto-deploy setiap kali Anda push kode) atau **Manual**.

4. **Konfigurasi Build**
   - **Configuration file**: Pilih **Configure all settings here**.
   - **Runtime**: Pilih **Python 3** ATAU pilih **Docker** (Direkomendasikan).
     - *Jika memilih **Docker**: AWS akan langsung membaca [Dockerfile](file:///c:/Users/yandr/OneDrive/Desktop/agrisensa-api/agrisensa_streamlit/Dockerfile) kita secara otomatis.*
     - *Jika memilih **Python 3**: masukkan build command (`pip install -r requirements.txt`) dan run command (`streamlit run Home.py --server.port 8080 --server.address 0.0.0.0`).*
     - **Rekomendasi**: Pilih **Docker** agar environment konsisten dan minim konfigurasi tambahan di AWS console.

5. **Konfigurasi Service**
   - **Service name**: `agrisensa-streamlit`
   - **Port**: Isi dengan `8501` (sesuai port yang kita expose di Dockerfile).
   - **Environment variables** (opsional): Masukkan environment variables jika diperlukan (misalnya: API Key untuk Gemini `GEMINI_API_KEY`).
   - **CPU & Memory**: Pilih `1 vCPU & 2 GB Memory` (sudah sangat cukup untuk aplikasi ini).

6. **Review & Create**
   - Klik **Next**, periksa kembali seluruh konfigurasi, lalu klik **Create & Deploy**.
   - AWS App Runner akan melakukan build container image dan men-deploy-nya. Proses ini memakan waktu sekitar 3–5 menit.
   - Setelah selesai, Anda akan diberikan **Default domain** berformat HTTPS (misal: `https://xxxxxx.us-east-1.awsapprunner.com`) yang bisa langsung diakses secara aman.

---

## 🖥️ Opsi 2: AWS EC2 (Kendali Penuh & Ekonomis 💰)

Jika Anda ingin meng-host aplikasi di VM Linux biasa dan memanfaatkan AWS Free Tier (`t2.micro` / `t3.micro`), ikuti panduan ini.

### Langkah-langkah:

1. **Luncurkan Instance EC2**
   - Masuk ke AWS Console, buka layanan **EC2**, lalu klik **Launch Instance**.
   - **Name**: `agrisensa-streamlit-server`
   - **OS**: Pilih **Ubuntu Server 22.04 LTS**.
   - **Instance Type**: Pilih **t2.micro** (masuk dalam Free Tier).
   - **Key pair**: Buat key pair baru atau gunakan yang sudah ada (simpan file `.pem` Anda dengan aman untuk SSH).

2. **Konfigurasi Security Group (Penting!)**
   Secara default, AWS memblokir semua trafik masuk. Kita harus membukanya:
   - Centang **Allow SSH traffic from** (pilih `My IP` demi keamanan, atau `Anywhere` jika mendesak).
   - Centang **Allow HTTP traffic from the internet** (Port 80).
   - Centang **Allow HTTPS traffic from the internet** (Port 443).
   - Tambahkan **Custom TCP Rule**:
     - **Port Range**: `8501` (Port default Streamlit).
     - **Source**: `Anywhere-IPv4` (`0.0.0.0/0`).
     - *Catatan: Jika nanti Anda ingin menggunakan Nginx reverse proxy, Anda tidak perlu membuka port 8501 ke publik.*

3. **Koneksi ke EC2 via SSH**
   Buka terminal di komputer Anda, lalu SSH ke server EC2:
   ```bash
   ssh -i "key-anda.pem" ubuntu@IP_PUBLIC_EC2
   ```

4. **Persiapan Environment di EC2**
   Setelah masuk ke server Ubuntu, jalankan pembaruan sistem dan install Git serta Python venv:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install git python3-pip python3-venv -y
   ```

5. **Clone Repository dan Setup Virtual Environment**
   ```bash
   git clone https://github.com/USERNAME/REPOSITORY_NAME.git agrisensa
   cd agrisensa/agrisensa_streamlit
   
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **Jalankan Streamlit di Background**
   Gunakan alat seperti `nohup` atau `tmux` agar aplikasi tetap berjalan saat Anda keluar dari sesi SSH:
   ```bash
   # Opsi dengan nohup (output log ke nohup.out)
   nohup streamlit run Home.py --server.port 8501 --server.address 0.0.0.0 &
   ```
   Aplikasi Anda kini dapat diakses melalui URL: `http://IP_PUBLIC_EC2:8501`.

7. **(Opsional & Direkomendasikan) Hubungkan dengan Nginx Reverse Proxy**
   Agar pengguna tidak perlu mengetikkan `:8501` di akhir URL dan bisa menggunakan HTTPS standar:
   - Install Nginx: `sudo apt install nginx -y`
   - Konfigurasi file Nginx block (`/etc/nginx/sites-available/default`):
     ```nginx
     server {
         listen 80;
         server_name IP_PUBLIC_EC2_ATAU_DOMAIN;

         location / {
             proxy_pass http://127.0.0.1:8501;
             proxy_http_version 1.1;
             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection "upgrade";
             proxy_set_header Host $host;
             proxy_cache_bypass $http_upgrade;
         }
     }
     ```
   - Restart Nginx: `sudo systemctl restart nginx`
   - Kini aplikasi dapat diakses langsung di port `80` (HTTP biasa tanpa port `:8501`).
   - Gunakan **Certbot (Let's Encrypt)** untuk mendapatkan SSL gratis (HTTPS):
     ```bash
     sudo apt install certbot python3-certbot-nginx -y
     sudo certbot --nginx
     ```

---

## 📋 Ringkasan Perbandingan

| Fitur | AWS App Runner | AWS EC2 (t2.micro) |
|-------|----------------|---------------------|
| **Tingkat Kesulitan** | Sangat Mudah (No-Ops) | Sedang (Membutuhkan Linux Command) |
| **SSL / HTTPS** | Otomatis & Terkelola 🔐 | Manual (Menggunakan Nginx + Certbot) |
| **Auto-Deploy** | Otomatis dari GitHub | Manual (Harus SSH & `git pull`) |
| **Skalabilitas** | Otomatis (Auto-scaling) | Manual (Harus upgrade instance) |
| **Estimasi Biaya** | Berdasarkan pemakaian (~$5–$15/bulan) | Gratis selama 1 tahun (Free Tier) |

Kami merekomendasikan **AWS App Runner** jika Anda mengutamakan kenyamanan pengembangan yang cepat dan otomatisasi deployment tanpa ribet mengelola server OS.
