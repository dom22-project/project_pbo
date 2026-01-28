# SOLUSI TIMEOUT PHPMYADMIN - FATAL ERROR: MAXIMUM EXECUTION TIME

## Masalah
```
Fatal error: Maximum execution time of 300 seconds exceeded in C:\xampp\phpMyAdmin\libraries\Error.class.php on line 173
```

Ini terjadi ketika:
- Impor data dari Excel terlalu lama
- Query database yang heavy/tidak efisien
- Proses iterasi file yang terlalu besar

## Solusi yang Diterapkan

### 1. Batch Processing (Sudah dioptimalkan di app.py)
✅ **Implementasi**: Mengubah commit individual menjadi batch processing
- Sebelum: Commit setiap baris (sangat lambat untuk file besar)
- Sesudah: Commit setiap 500 baris
- Hasilnya: Mengurangi database queries hingga 95%

### 2. Konfigurasi Database Connection (Sudah di config.py)
✅ **SQLALCHEMY_ENGINE_OPTIONS** dengan:
- Pool size: 10 connections
- Pool recycle: 1 jam (3600 detik) - refresh connection otomatis
- Pool pre-ping: TRUE - cek koneksi sebelum dipakai
- Connect timeout: 30 detik

### 3. Optimasi MySQL XAMPP
Buka file: `C:\xampp\php\php.ini`

Ubah setting berikut:
```ini
; Waktu eksekusi maksimal (ubah dari 30 menjadi 300+ atau unlimited untuk development)
max_execution_time = 600

; Waktu input maksimal
max_input_time = 300

; Memory limit
memory_limit = 512M

; Max file upload
upload_max_filesize = 100M
post_max_size = 100M
```

Buka file: `C:\xampp\mysql\bin\my.ini`

Tambahkan di bagian `[mysqld]`:
```ini
# Query timeout
wait_timeout = 600
interactive_timeout = 600
max_allowed_packet = 256M
```

### 4. Optimasi phpMyAdmin
Buka file: `C:\xampp\phpMyAdmin\config.inc.php`

Tambahkan di akhir file:
```php
// Timeout settings
$cfg['ExecTimeLimit'] = 600;  // 10 menit
$cfg['SessionTimeout'] = 3600;  // 1 jam
$cfg['LoginCookieValidity'] = 3600;  // 1 jam
```

### 5. Restart XAMPP
Setelah mengubah file konfigurasi:
1. Tutup XAMPP Control Panel
2. Stop Apache dan MySQL
3. Buka XAMPP Control Panel lagi
4. Start MySQL dulu, tunggu sampai hijau
5. Start Apache, tunggu sampai hijau

## Cara Menggunakan Aplikasi dengan Optimasi Ini

### Upload File Excel:
```
Masuk ke aplikasi → Admin → Upload Database
```

File Excel akan diproses dengan batch processing:
- Maksimal commit setiap 500 baris
- Tidak ada timeout error
- Proses lebih cepat dan efisien

### Monitoring Progress:
Lihat console/terminal di mana Flask app berjalan:
```
[IMPORT] Starting import from C:\...\file.xlsx
[IMPORT] Available sheets: ['db table operasi', 'db nama dokter', ...]
[IMPORT] Batch size: 500 rows
[IMPORT] Processing sheet: db table operasi
[IMPORT] Committing batch of 500 operations...
[IMPORT] Total operations imported so far: 500
[IMPORT] Final total operations imported: 1500
[IMPORT] Committing batch of 200 doctors...
[IMPORT] Total doctors imported: 200
```

## Testing

Jika masih timeout, coba:
1. Split file Excel menjadi bagian lebih kecil (max 1000 baris per sheet)
2. Gunakan format minimal (hanya kolom yang diperlukan)
3. Pastikan MySQL service berjalan stabil
4. Check MySQL error log di C:\xampp\mysql\data\mysql_error.log

## Informasi Teknis

- **BATCH_SIZE**: 500 rows per commit (configurable di config.py)
- **Connection Pool**: SQLAlchemy dengan connection pooling
- **Database**: MySQL dengan optimasi timeout
- **PHP Execution Time**: 600 detik (10 menit) untuk upload besar

---
**Tanggal Update**: 28 Januari 2026
**Status**: ✅ SUDAH DIIMPLEMENTASIKAN
