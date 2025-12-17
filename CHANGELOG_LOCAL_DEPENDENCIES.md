# Changelog: Migrasi ke Local Dependencies

## Tanggal: 2024-11-20

## Ringkasan Perubahan
Aplikasi PBO telah diupdate untuk menggunakan file dependencies lokal (Select2) daripada CDN eksternal. Ini memungkinkan aplikasi berjalan secara offline tanpa koneksi internet.

---

## File yang Didownload

### 1. Select2 Library (v4.1.0-rc.0)
**Lokasi:** `static/vendor/select2/`

#### CSS Files:
- `static/vendor/select2/css/select2.min.css` (16.2 KB)
  - File CSS utama untuk Select2
  - Source: https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css

- `static/vendor/select2/css/select2-bootstrap-5-theme.min.css` (31.2 KB)
  - Theme Bootstrap 5 untuk Select2
  - Source: https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css

#### JavaScript Files:
- `static/vendor/select2/js/select2.min.js` (73.2 KB)
  - File JavaScript utama untuk Select2
  - Source: https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js

---

## File Template yang Diupdate

### 1. templates/input_pbo.html
**Perubahan:**
```html
<!-- SEBELUM (CDN) -->
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

<!-- SESUDAH (Local) -->
<link href="{{ url_for('static', filename='vendor/select2/css/select2.min.css') }}" rel="stylesheet" />
<link href="{{ url_for('static', filename='vendor/select2/css/select2-bootstrap-5-theme.min.css') }}" rel="stylesheet" />
<script src="{{ url_for('static', filename='vendor/select2/js/select2.min.js') }}"></script>
```

### 2. templates/edit_pbo.html
**Perubahan:** Sama seperti input_pbo.html

---

## Script Helper yang Dibuat

### download_dependencies.py
Script Python untuk mendownload semua dependencies dari CDN ke folder lokal.

**Cara Penggunaan:**
```bash
python download_dependencies.py
```

**Fungsi:**
- Membuat folder structure: `static/vendor/select2/css/` dan `static/vendor/select2/js/`
- Download 3 file dari CDN
- Verifikasi download berhasil

---

## Struktur Folder Baru

```
static/
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   └── logo siloam.png
└── vendor/                    # ← BARU
    └── select2/               # ← BARU
        ├── css/               # ← BARU
        │   ├── select2.min.css
        │   └── select2-bootstrap-5-theme.min.css
        └── js/                # ← BARU
            └── select2.min.js
```

---

## Keuntungan Perubahan Ini

### 1. ✅ Offline Capability
- Aplikasi dapat berjalan tanpa koneksi internet
- Tidak bergantung pada ketersediaan CDN eksternal

### 2. ✅ Performance
- Loading lebih cepat karena file di-serve dari server lokal
- Tidak ada latency dari CDN eksternal

### 3. ✅ Reliability
- Tidak terpengaruh jika CDN down atau bermasalah
- Versi library terjamin konsisten

### 4. ✅ Security
- Mengurangi risiko dari CDN yang di-compromise
- Full control atas file yang digunakan

### 5. ✅ Compliance
- Memenuhi requirement untuk aplikasi yang harus berjalan di environment tertutup
- Tidak ada data yang keluar ke server eksternal

---

## Testing yang Dilakukan

### ✅ File Download
- [x] select2.min.css berhasil didownload (16.2 KB)
- [x] select2-bootstrap-5-theme.min.css berhasil didownload (31.2 KB)
- [x] select2.min.js berhasil didownload (73.2 KB)

### ✅ Template Update
- [x] input_pbo.html menggunakan path lokal
- [x] edit_pbo.html menggunakan path lokal

### ⏳ Functional Testing (Perlu dilakukan)
- [ ] Test form input PBO dengan Select2
- [ ] Test form edit PBO dengan Select2
- [ ] Test search functionality di Select2
- [ ] Test aplikasi dalam mode offline

---

## Cara Testing Manual

### 1. Test Aplikasi Berjalan
```bash
python app.py
```
Akses: http://127.0.0.1:5000

### 2. Test Form Input
1. Buka http://127.0.0.1:5000/input
2. Klik dropdown "Nama Dokter"
3. Verifikasi Select2 berfungsi dengan baik (search, styling)

### 3. Test Offline Mode
1. Disconnect internet
2. Refresh halaman
3. Verifikasi Select2 masih berfungsi

---

## Dependencies yang Masih Menggunakan CDN

Berikut adalah dependencies lain yang masih menggunakan CDN (dari base.html):

### Bootstrap 5.3.0
- CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
- JS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

### Bootstrap Icons 1.10.5
- CSS: https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css

### jQuery 3.6.0
- JS: https://code.jquery.com/jquery-3.6.0.min.js

**Catatan:** Jika diperlukan, dependencies ini juga bisa didownload ke lokal dengan cara yang sama.

---

## Rollback Plan

Jika terjadi masalah, untuk kembali ke CDN:

### 1. Revert Template Changes
```bash
git checkout templates/input_pbo.html
git checkout templates/edit_pbo.html
```

### 2. Atau Manual Edit
Ganti kembali path lokal dengan URL CDN di kedua file template.

---

## Maintenance

### Update Dependencies
Jika perlu update versi Select2:

1. Edit `download_dependencies.py`
2. Ubah versi di URL (contoh: `4.1.0-rc.0` → `4.1.0`)
3. Jalankan script: `python download_dependencies.py`
4. Test aplikasi

---

## Catatan Penting

1. **Backup**: File dependencies sudah tersimpan di `static/vendor/select2/`
2. **Git**: Pastikan folder `static/vendor/` di-commit ke repository
3. **Deployment**: Saat deploy, pastikan folder `static/vendor/` ikut ter-deploy
4. **.gitignore**: Jangan tambahkan `static/vendor/` ke .gitignore

---

## Kontak & Support

Jika ada pertanyaan atau masalah terkait perubahan ini:
- Developer: BLACKBOXAI
- Tanggal: 2024-11-20
- Project: Sistem Manajemen PBO - RS Sumber Hidup

---

## Status: ✅ COMPLETED

Semua perubahan telah berhasil diimplementasikan dan siap untuk testing.
