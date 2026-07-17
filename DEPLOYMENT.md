# 🚀 Smart Chili Harvest - Panduan Deployment VPS

Panduan ini menjelaskan cara mendeploy **Backend API (FastAPI + YOLOv8)** ke VPS CloudeHost menggunakan Docker.

---

## 📋 Prasyarat

| Item | Spesifikasi |
|------|------------|
| VPS OS | Ubuntu 22.04 LTS |
| CPU | 2 vCPU |
| RAM | 2 GB |
| Disk | 20 GB |
| Port terbuka | `22` (SSH), `8000` (API) |

---

## ⚡ Cara 1: Otomatis via Cloud-Init (Recommended)

Cara paling mudah — **cukup paste konfigurasi saat membuat VM**.

### Langkah:

1. Saat membuat VM baru di CloudeHost, centang **"Add custom configuration for the virtual machine"**
2. Copy-paste **seluruh isi** file [`cloud-init.yml`](file:///d:/SKRIPSI/Smart-Chili-Harvest/cloud-init.yml) ke dalam text area "Initialization script"
3. Isi **Resource name** (contoh: `smart-chili-harvest`)
4. Klik **Create** dan tunggu ± 5-10 menit

### Verifikasi:

Setelah VM selesai dibuat, SSH ke VM lalu cek:

```bash
# Cek apakah container sudah berjalan
docker ps

# Cek log backend
docker logs smart-chili-backend

# Test API endpoint
curl http://localhost:8000/
# Expected: {"message":"Backend berjalan 🚀"}
```

---

## 🔧 Cara 2: Manual Setup (Step-by-Step)

Jika VM sudah ada atau cloud-init tidak tersedia.

### Step 1: SSH ke VPS

```bash
ssh root@<IP_VPS_KAMU>
```

### Step 2: Update Sistem & Install Dependencies

```bash
apt update && apt upgrade -y
apt install -y git curl ufw
```

### Step 3: Install Docker

```bash
curl -fsSL https://get.docker.com | sh
systemctl enable docker && systemctl start docker
```

### Step 4: Konfigurasi Firewall

```bash
ufw allow OpenSSH
ufw allow 8000/tcp
ufw --force enable
```

### Step 5: Tambah Swap (Penting untuk 2GB RAM!)

YOLOv8 inference membutuhkan RAM cukup besar. Swap mencegah OOM killer:

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Step 6: Clone Repository

```bash
git clone https://github.com/azulfikri/Smart-Chili-Harvest.git /opt/smart-chili-harvest
cd /opt/smart-chili-harvest
```

### Step 7: Setup Environment

```bash
cp .env.example .env
# Edit jika perlu ganti port:
# nano .env
```

### Step 8: Build & Jalankan

```bash
docker compose up -d --build
```

### Step 9: Verifikasi

```bash
# Cek status container
docker ps

# Cek log
docker logs -f smart-chili-backend

# Test endpoint
curl http://localhost:8000/
curl http://localhost:8000/docs
```

---

## 📱 Konfigurasi Frontend (Capacitor Android)

Setelah backend berjalan di VPS, update URL API di frontend agar mengarah ke IP publik VPS:

```
http://<IP_VPS_KAMU>:8000
```

File-file yang perlu diubah (ganti `http://127.0.0.1:8000` → `http://<IP_VPS>:8000`):

- `frontend/src/views/DashboardView.vue`
- `frontend/src/views/DetectionView.vue`
- `frontend/src/views/HistoryView.vue`
- `frontend/src/views/SessionDetailView.vue`

> **💡 Tip:** Sebaiknya buat file konfigurasi API terpusat (contoh: `src/config.ts`) agar URL hanya perlu diganti di satu tempat.

---

## 🔄 Operasi Sehari-hari

### Update ke Versi Terbaru

```bash
cd /opt/smart-chili-harvest
git pull origin main
docker compose up -d --build
```

### Restart Container

```bash
docker compose restart
```

### Lihat Log Realtime

```bash
docker logs -f smart-chili-backend
```

### Stop Semua Service

```bash
docker compose down
```

### Backup Database

```bash
# Cek nama volume
docker volume inspect smart-chili-harvest_backend_db

# Copy database dari volume ke host
docker cp smart-chili-backend:/app/smart_chili.db ./backup_smart_chili.db
```

### Reset Database (Hapus semua data)

```bash
docker compose down
docker volume rm smart-chili-harvest_backend_db
docker compose up -d
```

---

## 🛡️ Keamanan Tambahan (Opsional tapi Disarankan)

### 1. Disable Root Login SSH

```bash
# Buat user baru
adduser deployer
usermod -aG sudo deployer
usermod -aG docker deployer

# Edit SSH config
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
systemctl restart sshd
```

### 2. Setup Reverse Proxy dengan Nginx + SSL (Jika punya domain)

```bash
apt install -y nginx certbot python3-certbot-nginx

# Buat config Nginx
cat > /etc/nginx/sites-available/smart-chili << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }
}
EOF

ln -s /etc/nginx/sites-available/smart-chili /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# Setup SSL (ganti domain)
certbot --nginx -d your-domain.com
```

---

## ⚠️ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Container tidak start | `docker logs smart-chili-backend` untuk cek error |
| Port 8000 tidak bisa diakses | Cek firewall: `ufw status` dan pastikan port 8000 terbuka |
| OOM Killed (kehabisan RAM) | Pastikan swap sudah aktif: `swapon --show` |
| Build gagal (pip timeout) | Jalankan ulang: `docker compose up -d --build` |
| Database kosong setelah restart | Pastikan volume ter-mount: `docker volume ls` |
| Gambar upload tidak tersimpan | Cek volume mount: `docker inspect smart-chili-backend` |

---

## 📐 Arsitektur Deployment

```
┌──────────────────────────────────────────────┐
│              VPS CloudeHost                  │
│          (Ubuntu 22.04, 2C/2G/20G)           │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │          Docker Engine                 │  │
│  │                                        │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │   smart-chili-backend            │  │  │
│  │  │   (FastAPI + YOLOv8)             │  │  │
│  │  │   Port: 8000                     │  │  │
│  │  └──────┬───────────┬───────────────┘  │  │
│  │         │           │                  │  │
│  │    ┌────┴────┐ ┌────┴────┐             │  │
│  │    │ Volume  │ │ Volume  │             │  │
│  │    │uploads/ │ │  data/  │             │  │
│  │    │(images) │ │(sqlite) │             │  │
│  │    └─────────┘ └─────────┘             │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  UFW Firewall: 22(SSH) + 8000(API)           │
└──────────────────────┬───────────────────────┘
                       │ :8000
                       ▼
              ┌─────────────────┐
              │  📱 Android App │
              │  (Capacitor)    │
              │  → HTTP API     │
              └─────────────────┘
```
