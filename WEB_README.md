# Sistem Manajemen PBO - Web Application

Aplikasi web untuk mengelola Perkiraan Biaya Operasi (PBO) di Rumah Sakit Sumber Hidup.

## 🎯 Fitur Utama

- ✅ **Dashboard Interaktif** - Statistik dan data terbaru
- ✅ **Input Data PBO** - Form lengkap dengan perhitungan otomatis
- ✅ **Pencarian & Filter** - Cari data berdasarkan berbagai kriteria
- ✅ **CRUD Operations** - Create, Read, Update, Delete data PBO
- ✅ **Cetak Form** - Export ke format print-friendly
- ✅ **Responsive Design** - Akses dari desktop, tablet, atau mobile
- ✅ **Real-time Calculation** - Perhitungan biaya otomatis dengan AJAX
- ✅ **Modern UI** - Interface yang user-friendly dengan Bootstrap 5

## 📋 Persyaratan Sistem

- Python 3.7 atau lebih tinggi
- Web Browser modern (Chrome, Firefox, Safari, Edge)
- Minimal 2GB RAM
- 100MB ruang disk kosong

## 🚀 Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies yang akan diinstall:
- Flask (Web Framework)
- Jinja2 (Template Engine)
- WeasyPrint (PDF Generation)
- Werkzeug (WSGI utilities)

### 2. Inisialisasi Database

Database akan otomatis dibuat saat aplikasi pertama kali dijalankan. Jika ingin menambahkan data operasi dari CSV:

```bash
python .vscode/import_data.py
```

### 3. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

## 📱 Cara Menggunakan

### 1. Dashboard

- Akses halaman utama untuk melihat statistik
- Lihat data PBO terbaru
- Akses cepat ke fitur input dan pencarian

### 2. Input Data PBO

**Langkah-langkah:**

1. Klik menu **"Input PBO"** atau tombol **"Input Data PBO Baru"**
2. Isi form dengan data pasien:
   - Nama Pasien (wajib)
   - Diagnosa (wajib)
   - Nama Operasi (wajib)
   - Sifat Operasi (Elektif/CITO/Penyulit)
   - Nama Dokter (wajib)
   - Kelas Perawatan (wajib)
   - Tanggal (wajib)

3. Pilih Tabel Operasi (1-4):
   - Pilih tindakan dari dropdown
   - Pilih persentase (100% atau 50%)
   - Klik **"Hitung Biaya Operasi"** untuk kalkulasi otomatis

4. Isi biaya tambahan (opsional):
   - Konsultasi Pre Tindakan
   - Diagnostic Pre Tindakan
   - Recovery Room Charge
   - Alat, Medical Equipment
   - Obat dan Alkes

5. Klik **"Hitung Total"** untuk menghitung total biaya

6. Klik **"Simpan Data"** untuk menyimpan ke database

### 3. Pencarian Data

**Cara mencari:**

1. Klik menu **"Cari Data"**
2. Pilih kriteria pencarian:
   - Nama Pasien
   - Nama Operasi
   - Tanggal
   - Diagnosa
   - Nama Dokter
3. Masukkan kata kunci (kosongkan untuk tampilkan semua)
4. Klik **"Cari"**

**Aksi pada hasil:**
- 👁️ **Lihat Detail** - Melihat informasi lengkap
- ✏️ **Edit** - Mengubah data
- 🖨️ **Cetak** - Mencetak form PBO
- 🗑️ **Hapus** - Menghapus data (dengan konfirmasi)

### 4. Detail & Edit Data

**Melihat Detail:**
- Klik ikon mata (👁️) pada tabel hasil pencarian
- Atau double-click pada baris data
- Tampilan detail lengkap dengan semua informasi

**Mengedit Data:**
- Klik tombol **"Edit Data"** dari halaman detail
- Atau klik ikon pensil (✏️) dari tabel pencarian
- Form akan terisi dengan data existing
- Ubah data yang diperlukan
- Klik **"Update Data"** untuk menyimpan

### 5. Cetak Form

**Cara mencetak:**
1. Dari halaman detail, klik **"Cetak Form"**
2. Atau dari tabel pencarian, klik ikon printer (🖨️)
3. Halaman print preview akan terbuka di tab baru
4. Klik tombol **"Cetak / Print"** atau gunakan Ctrl+P
5. Pilih printer atau "Save as PDF"

## 💡 Perhitungan Biaya

### Biaya Dokter (Surgeon)
```
Surgeon = (Biaya Dokter × Persentase) × Surcharge
```

### Biaya Anesthesi
```
Anesthesi = (Biaya RS × Persentase) × Surcharge
```

### OT Room Charge
```
OT Room Charge = Surgeon × 30%
```

### Surcharge Rates
- **Elektif / Tentative**: 1.0x (0%)
- **CITO**: 1.25x (25%)
- **Penyulit**: 1.30x (30%)

### Tarif Kamar per Hari
| Kelas | Tarif |
|-------|-------|
| BASIC | Rp 350.000 |
| STANDARD | Rp 650.000 |
| DELUXE | Rp 900.000 |
| VIP | Rp 1.800.000 |
| VVIP | Rp 1.900.000 |
| SUITE | Rp 5.000.000 |
| PRESIDENTIAL SUITE | Rp 7.500.000 |
| ODC | Rp 500.000 |

### Total Biaya
```
Total = Konsultasi + Diagnostic Pre + Surgeon + Anesthesi + 
        OT Room Charge + Recovery Room + Alat + Diagnostic + 
        Medical Equipment + Obat & Alkes + Tarif Kamar
```

## 🗂️ Struktur Proyek

```
app pbo/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models & operations
├── utils.py                    # Business logic & utilities
├── requirements.txt            # Python dependencies
├── WEB_README.md              # Dokumentasi web app
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Dashboard
│   ├── input_pbo.html         # Input form
│   ├── search_pbo.html        # Search page
│   ├── detail_pbo.html        # Detail view
│   ├── edit_pbo.html          # Edit form
│   └── print_pbo.html         # Print template
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Custom CSS
│   └── js/
│       └── main.js            # Custom JavaScript
│
└── data/
    └── pbo_database.db        # SQLite database
```

## 🔧 Konfigurasi

Edit file `config.py` untuk mengubah pengaturan:

```python
# Secret key untuk session
SECRET_KEY = 'your-secret-key-here'

# Database path
DATABASE_PATH = 'data/pbo_database.db'

# Pagination
ITEMS_PER_PAGE = 20

# Room rates, surcharge rates, dll
```

## 🌐 API Endpoints

### Public Routes
- `GET /` - Dashboard
- `GET /input` - Form input PBO
- `POST /input` - Submit data PBO
- `GET /search` - Halaman pencarian
- `POST /search` - Cari data PBO
- `GET /detail/<id>` - Detail PBO
- `GET /edit/<id>` - Form edit PBO
- `POST /edit/<id>` - Update data PBO
- `POST /delete/<id>` - Hapus data PBO
- `GET /print/<id>` - Cetak form PBO

### API Routes (AJAX)
- `POST /api/calculate-surgery-fees` - Hitung biaya operasi
- `POST /api/get-room-rate` - Get tarif kamar
- `POST /api/calculate-total` - Hitung total biaya

## 🚀 Deployment

### Development Server
```bash
python app.py
```

### Production Server (dengan Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Opsional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔒 Keamanan

- ✅ Input validation & sanitization
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection
- ✅ CSRF protection (Flask built-in)
- ✅ Secure session management

## 🐛 Troubleshooting

### Error: "Address already in use"
**Solusi:** Port 5000 sudah digunakan. Ubah port di `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error: "No module named 'flask'"
**Solusi:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Database tidak terbuat
**Solusi:** Pastikan folder `data/` ada dan memiliki permission write:
```bash
mkdir data
chmod 755 data
```

### Perhitungan tidak otomatis
**Solusi:** Pastikan JavaScript enabled di browser dan jQuery loaded

## 📊 Perbandingan Desktop vs Web App

| Fitur | Desktop App | Web App |
|-------|-------------|---------|
| Platform | Windows/Linux/Mac | Any (Browser) |
| Installation | Required | Not Required |
| Multi-user | No | Yes |
| Remote Access | No | Yes |
| Mobile Support | No | Yes |
| Auto Update | Manual | Automatic |
| Database | Local SQLite | Local/Cloud SQLite |

## 🔄 Migrasi dari Desktop App

Data dari aplikasi desktop dapat langsung digunakan:

1. Copy file `data/pbo_database.db` dari aplikasi desktop
2. Paste ke folder `data/` di aplikasi web
3. Jalankan aplikasi web
4. Semua data akan tersedia

## 📝 Changelog

### Version 1.0.0 (2024)
- ✅ Konversi dari PyQt5 desktop app ke Flask web app
- ✅ Implementasi responsive design dengan Bootstrap 5
- ✅ AJAX-based real-time calculations
- ✅ Modern UI/UX improvements
- ✅ Print-friendly form template
- ✅ CRUD operations lengkap
- ✅ Search & filter functionality

## 🤝 Kontribusi

Untuk melaporkan bug atau request fitur:
1. Buat issue di repository
2. Atau hubungi tim IT RS Siloam TB Simatupang

## 📞 Kontak & Support

**RS Siloam TB Simatupang**
- Alamat: Jl. RA Kartini No. 08 Cilandak, Jakarta Selatan 12430
- Telp: (021) 29531900 Ext. 29790
- Email: support@rssumberhidup.com

## 📄 Lisensi

© 2024 RS Siloam TB Simatupang. All rights reserved.

---

**Versi:** 1.0.0  
**Terakhir diupdate:** 2024  
**Developer:** IT Team RS Siloam TB Simatupang
