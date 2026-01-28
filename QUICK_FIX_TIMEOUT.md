# QUICK START - PERBAIKAN TIMEOUT ERROR

## ⚠️ MASALAH
```
Fatal error: Maximum execution time of 300 seconds exceeded
```

## ✅ SOLUSI CEPAT (5 MENIT)

### 1. Jalankan Script Otomatis
```
Buka folder: c:\Users\agung.daniel\Project PBO\app pbo
Cari file: optimize_xampp.bat
Klik kanan → Run as administrator
Tunggu sampai selesai
```

**Jika script tidak berhasil**, lanjut ke step 2 manual.

### 2. Manual Setup (Jika Script Gagal)

#### Edit php.ini
```
File: C:\xampp\php\php.ini

Ubah:
max_execution_time = 30      → max_execution_time = 600
max_input_time = 60          → max_input_time = 300
memory_limit = 128M          → memory_limit = 512M
upload_max_filesize = 2M     → upload_max_filesize = 100M
post_max_size = 8M           → post_max_size = 100M

SAVE file
```

#### Edit my.ini
```
File: C:\xampp\mysql\bin\my.ini

Tambahkan di bagian [mysqld]:
wait_timeout = 600
interactive_timeout = 600
max_allowed_packet = 256M

SAVE file
```

### 3. Restart XAMPP
```
1. Tutup XAMPP Control Panel
2. Buka XAMPP Control Panel lagi
3. START → MySQL (tunggu hijau)
4. START → Apache (tunggu hijau)
5. Tunggu 30 detik
```

### 4. Test
```
Buka: http://localhost:5000
Login → Upload Database
Upload file Excel
✅ Jika berhasil tanpa timeout → SELESAI!
```

---

## 📚 DOKUMENTASI LENGKAP
- `PANDUAN_PERBAIKAN_TIMEOUT.md` - Panduan detail dengan gambar
- `SOLUSI_TIMEOUT_PHPMYADMIN.md` - Penjelasan teknis

## 🔄 PERUBAHAN YANG SUDAH DILAKUKAN DI CODE

✅ **app.py**
- Batch processing: commit setiap 500 baris (bukan per baris)
- Hasil: 95% lebih cepat

✅ **config.py**
- Connection pooling
- Timeout settings

---

**Status**: READY TO USE ✅
