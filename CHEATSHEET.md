# Smart Chili Harvest - Command Cheatsheet

Dokumen ini berisi daftar perintah penting yang sering digunakan selama pengembangan proyek **Smart Chili Harvest**.

## 🔙 Backend (Python / FastAPI)

Pastikan kamu berada di dalam direktori `backend`:

```powershell
cd backend
```

### 1. Mengaktifkan Virtual Environment (Windows)

Setiap kali membuka terminal baru untuk menjalankan backend, aktifkan _virtual environment_:

```powershell
source venv\Scripts\activate
```

### 2. Menginstal Dependencies

Jika ada penambahan library baru atau baru pertama kali setup:

```powershell
pip install -r requirements.txt
```

### 3. Menjalankan Server Backend (FastAPI)

Untuk menjalankan server (dengan fitur auto-reload bila ada file yang diubah):

```powershell
uvicorn app.main:app --reload
```

- API Server akan berjalan di: `http://127.0.0.1:8000`
- Swagger UI (Dokumentasi API) bisa dibuka di: `http://127.0.0.1:8000/docs`

### 4. Setup / Reset Database

Untuk menjalankan script inisialisasi database (membuat file sqlite dan tabel-tabel):

```powershell
python -m app.database.init_db
```

---

## 🎨 Frontend

Pastikan kamu berada di direktori `frontend` sebelum menjalankan perintah ini:

```powershell
cd frontend
```

### 1. Menginstal Dependencies (Pertama kali clone / setup)

```powershell
npm install
```

### 2. Menjalankan Server Development Frontend

```powershell
npm run dev
```

---

## 💡 Tips Tambahan

- **Buka 2 Terminal**: Saat mengembangkan aplikasi secara keseluruhan, buka dua instance terminal di VSCode. Terminal 1 untuk menjalankan Backend (`uvicorn`), Terminal 2 untuk menjalankan Frontend (`npm run dev`).
- **Ganti Port**: Jika port default (8000) sedang digunakan aplikasi lain, kamu bisa menjalankan backend di port berbeda:
  ```powershell
  uvicorn app.main:app --reload --port 8080
  ```
