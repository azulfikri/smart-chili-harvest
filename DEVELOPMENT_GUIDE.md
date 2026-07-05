# Smart Chili Harvest - Development Blueprint

## 🏛️ 1. Blueprint Arsitektur & Layer Aplikasi

Aplikasi dibangun menggunakan arsitektur Client-Server yang clean dan modular:

### A. Frontend Mobile Layer (Vue.js 3 + Capacitor)

- `/src/components`: Komponen UI reusable (Bottom Navigation, Bounding Box Overlay, Score Gauge, Photo Cards).
- `/src/views`: Halaman utama penampung state (Dashboard.vue, CameraView.vue, HistoryView.vue).
- `/src/services/api.js`: Handler request HTTP (Axios/Fetch) untuk berkomunikasi dengan Backend FastAPI.

### B. Backend Server Layer (FastAPI + SQLite SQLAlchemy)

- `/app/database`: Pengaturan koneksi database (`database.py` & `init_db.py`).
- `/app/models`: Skema tabel SQLAlchemy (`session.py` & `detection.py`).
- `/app/routers`: Endpoint API untuk melayani request dari frontend mobile.
- `/app/services`: Logika bisnis (Inference YOLOv8 dan kalkulasi formula matematika HRS).

---

## 🗄️ 2. Skema Database SQLite Backend (SQLAlchemy Synced)

Database dikelola di sisi backend menggunakan SQLAlchemy. Atribut berikut wajib dijaga konsistensinya:

### Tabel 1: sessions (Model: ObservationSession)

- id (Integer, Primary Key, Index)
- session_name (String, Nullable=False)
- status (String, Default="IN_PROGRESS") -> Sesi aktif atau selesai (COMPLETED)
- sample_quality (String, Nullable=True)
- hrs (Float, Nullable=True) -> Nilai akhir kesiapan panen agregat
- harvest_status (String, Nullable=True) -> Kategori: Siap Panen / Hampir Siap / Belum Siap
- estimated_shelf_life (Integer, Nullable=True) -> Estimasi daya simpan dalam jumlah hari
- created_at (DateTime, Default=UTCnow)
- completed_at (DateTime, Nullable=True)

### Tabel 2: detections (Model: Detection)

- id (Integer, Primary Key, Index)
- session_id (Integer, ForeignKey("sessions.id"))
- original_image (String) -> Path/URL penyimpanan file foto asli petani
- processed_image (String) -> Path/URL file foto hasil gambaran bounding box YOLOv8
- semi_ripe_count (Integer) -> Jumlah cabai semi-ripe per foto
- nearly_ripe_count (Integer) -> Jumlah cabai nearly-ripe per foto
- ripe_count (Integer) -> Jumlah cabai ripe per foto
- average_confidence (Float) -> Rata-rata confidence score deteksi di foto tersebut
- created_at (DateTime, Default=UTCnow)

---

## 🔄 3. Alur Kerja Aplikasi & State Management (MVP Workflow)

Logika urutan aplikasi wajib mengikuti aturan main di bawah ini demi keamanan sidang skripsi:

1. MULAI SESI: Petani membuka Dashboard (`/dashboard`) dan klik "Mulai Sesi Baru". Frontend menembak API backend untuk membuat record baru di tabel `sessions` dengan status="IN_PROGRESS". Backend mengembalikan data ID Sesi yang baru dibuat.
2. AMBIL FOTO (Progres 1 s.d 6): Petani mengambil foto di halaman kamera (`/camera`). Gambar dikirim via API ke FastAPI. Backend menjalankan mock inference, menghitung jumlah cabai per kelas, dan mengembalikan koordinat box beserta statistiknya.
3. FEEDBACK INSTAN & BACKUP LOKAL: Frontend langsung menampilkan overlay bounding box di layar HP petani sebagai feedback instan. Ketika petani klik "Simpan & Lanjut", data objek foto tersebut langsung di-insert ke tabel `detections` di backend dengan status sesi tetap "IN_PROGRESS". Angka counter foto di HP bertambah +1.
4. VALIDASI AGREGAT (Foto ke-7): Selama counter foto < 7, tombol "Hitung Estimasi Kesiapan Panen (HRS)" di aplikasi akan di-disabled. Begitu counter mencapai atau lebih dari 7, tombol menjadi aktif.
5. FINALIASI & PERHITUNGAN HRS: Ketika petani klik "Hitung HRS", frontend mengirim sinyal finalisasi ke backend. Backend akan menarik semua data kumulatif dari tabel `detections` yang terikat pada `session_id` tersebut, mengeksekusi rumus weighted scoring HRS, mengonversi skor ke dalam kategori & daya simpan literatur, mengubah status sesi menjadi "COMPLETED", lalu mengembalikan hasil akhir ke layar HP petani.
6. FILTER RIWAYAT: Halaman Riwayat (`HistoryView.vue`) hanya diperbolehkan menarik dan menampilkan daftar sesi dari database yang statusnya sudah "COMPLETED". Sesi yang tidak tuntas (IN_PROGRESS) tidak akan dimunculkan di riwayat utama.
